from speed_slide import main as launch
import sys


args = dict()
for i in range(1, len(sys.argv)):
    arg = sys.argv[i].split('=')[0]
    value = sys.argv[i].split('=')[1] if '=' in sys.argv[i] else ''
    args[arg] = value
launch(**args)
