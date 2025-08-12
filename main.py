#!/path/to/venv/bin/python
import traceback
from signaler import Signaler
import sys

def main():
    try:
        sig = Signaler()
        sig.update()
        sys.exit(0)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)

main()
