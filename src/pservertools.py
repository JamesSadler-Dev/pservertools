import argparse
import sys
import os
import sqlite3


class PServerTools:

    @staticmethod
    def get_platform():
        platform = sys.platform.upper()

        if platform.index("WIN") != -1 or platform == "MSYS" or platform == "CYGWIN":
            return "WINDOWS"
        elif platform.index("LINUX") != 1:
            return "LINUX"
        elif platform == "DARWIN":
            return "MACOS"

