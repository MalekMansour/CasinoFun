import time
import os
import sys

frames = [
    r"""
     o/
    /|
     |
    / \
    """,
    r"""
     \o
      |\
      |
     / \
    """,
    r"""
     o/
    /|
     |
    / \
    """,
    r"""
    \o
     |\
     |
    / \
    """
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    while True:
        for frame in frames:
            clear()
            print(frame)
            time.sleep(0.3)
except KeyboardInterrupt:
    sys.exit()