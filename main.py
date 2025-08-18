#!/path/to/venv/bin/python
import traceback
from signaler import Signaler
import sys


def exec_command(sig: Signaler):
  
    command = sys.argv[1]
    
    match command:
        case "--base":
            return [sig.base]
        case "--therm":
            return [sig.thermal]
        case "--disks":
            return [sig.disks_mounts]
        case "--space":
            return [sig.disks_spaces]
        case "--all":
             return [sig.base, sig.thermal, sig.disks_mounts, sig.disks_spaces]
        case "--clr":
             return [sig.clear_all]
            


def main():
    try:
        sig = Signaler()
        actions = exec_command(sig)
        for action in actions:
            action()
     
        sys.exit(0)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)

main()
