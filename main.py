from speed_slide import main as launch
import sys


args = {sys.argv[i].split('=')[0].strip('-'): sys.argv[i].split('=')[1] for i in range(1, len(sys.argv))}
launch(**args)
