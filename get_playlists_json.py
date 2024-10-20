import sqlite3
import json
import sys
from pathlib import Path


def main():


    try:
        path = Path(sys.argv[1])
    except IndexError:
        path = Path("./com.plexapp.plugins.library.db")
    if not path.is_file():
        raise FileNotFoundError(f"Tried to open library.db in {path.absolute()} file was not found")


    conn = sqlite3.Connection(path)

    playlists_metadata = conn.execute("SELECT title FROM metadata_items where metadata_type = 15;")
    playlists = sorted([playlist[0] for playlist in playlists_metadata.fetchall()])
    
    all_playlist_data = {
                         "music":{},
                         "video":{}
                         }
    
    for playlist_name in playlists:
        if not playlist_name == "All Music":
            playlist_data = conn.execute("""SELECT file
                FROM media_parts AS mp
                LEFT JOIN media_items AS mi ON mi.id = mp.media_item_id
                LEFT JOIN play_queue_generators AS pqg ON pqg.metadata_item_id = mi.metadata_item_id
                LEFT JOIN metadata_items AS m ON m.id = pqg.playlist_id
                WHERE m.title = ? ORDER BY "order" ASC;""", (playlist_name,))
            playlist_data_retrieved = playlist_data.fetchall()

            num= 1
            current_data = {}
            for data in playlist_data_retrieved:
                current_data[str(num)] = data[0]
                num+=1
            

            test_file = current_data.get("1","").upper()
            playlist_key = playlist_name.upper()
            if test_file.endswith("MP3") or test_file.endswith("FLAC") or test_file.endswith("M4A"):
                current= all_playlist_data["music"].get(playlist_key,{})
                if len(current.keys()) > len(current_data.keys()):          #USE SHORTER OF REPEATS
                    all_playlist_data["music"][playlist_key] = {"tracks":current_data}    
                elif not current:
                    all_playlist_data["music"][playlist_key] = {"tracks":current_data}
            else:
                current= all_playlist_data["video"].get(playlist_key,{})
                if len(current.keys()) > len(current_data.keys()):          #USE SHORTER OF REPEATS
                    all_playlist_data["video"][playlist_key] = {"episodes":current_data}
                elif not current:
                    all_playlist_data["video"][playlist_key] = {"episodes":current_data}

    print(len(all_playlist_data["music"]))
    
    with open("plex_playlists.json","w") as output_file:
        json.dump(all_playlist_data,output_file,indent=2)
    
if __name__ == "__main__":
    main()