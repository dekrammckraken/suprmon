#!/path/to/venv/bin/python

from signaler import Signaler
import sys

def main():
    try:
        sig = Signaler()
        sig.update()
        sys.exit(0)
    except Exception as e:
        sys.exit(1)

main()
