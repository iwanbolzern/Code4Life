import shutil
import glob

outfile = 'bin/main.py'
files = [
    'src/data_holder.py',
    'src/utils.py',
    'src/minimax.py',
    'src/simulation.py',
    'src/main.py'
]

excludes = [
    'from data_holder',
    'from utils',
    'from minimax',
    'from simulation'
]

with open(outfile, 'w') as outfile:
    for filename in files:
        if filename == outfile:
            # don't want to copy the output into the output
            continue

        with open(filename, 'r') as readfile:
            outfile.write('####################\n')
            for line in readfile:
                exclude_line = [line.startswith(exclude) for exclude in excludes]
                if any(exclude_line):
                    continue

                outfile.write(line)
            outfile.write('####################\n')
