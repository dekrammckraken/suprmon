#!/path/to/venv/bin/python
import traceback
from signaler import Signaler
import sys


def exec_command(sig: Signaler):

    if len(sys.argv) == 1:
        command = "--therm"
    else:
        command = sys.argv[1]

    match command:
        case "--cancel":
            return [sig.cancel]
        case "--base":
            return [sig.base]
        case "--therm":
            return [sig.thermals]
        case "--disks":
            return [sig.disks_mounts]
        case "--space":
            return [sig.disks_spaces]
        case "--all":
            return [sig.base, sig.thermals, sig.disks_mounts, sig.disks_spaces]
        case "--clr":
            return [sig.clear_all]
        case "--reboot":
            return [sig.reboot]
        case "--halt":
            return [sig.halt]
        case "--err":
            return [sig.tty_error]
        case "--ok":
            return [sig.tty_success]


def main():
    try:
        sig = Signaler()
        actions = exec_command(sig)
        for action in actions:
            #print(action)
            action()

        sys.exit(0)
    except Exception as e:
        print(f"Invalid command, use --command. {e}")
        sys.exit(1)


main()
