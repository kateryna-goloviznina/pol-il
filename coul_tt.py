import sys
import numpy as np
import math
import argparse
import os

parser = argparse.ArgumentParser( description = 'Automatic coul/tt pair style generator')
parser.add_argument('-d', '--dfile', dest='dfile', default='data-p.lmp', type=str, help='Data file with atomic indexes and labels of polarisable system [default: %(default)s]')
parser.add_argument('-p', '--pfile', dest='pfile', default='pair-p-sc.lmp', type=str, help='Pair file [default: %(default)s]')
parser.add_argument('-a', '--hatoms', dest='hatoms', type=str, nargs='+', help='Atomic indexes of naked charge hydrogen atoms')

args = parser.parse_args()

file = open(args.dfile, 'r')
atoms = list()
line = file.readline()
while line :
    if 'Masses' in line:
        break
    line = file.readline()
line = file.readline()
line = file.readline()
while line :
    if 'Bond Coeffs' in line:
        del atoms[-1]
        break
    atoms.append(line.split())
    line = file.readline()

print('\nTo inlcude to in-p.lmp:')
print('\tpair_style hybrid/overlay ... coul/tt 4 12.0\n')

cores = list()

for a in atoms:
    if 'DC' in a[-1]:
        cores.append(int(a[0]))
    elif 'DP' in a[-1]:
        dp = int(a[0])
        break

res= []
for h in args.hatoms:
    for c in cores:
        if int(h) < c:
            res.append('pair_coeff {0:4} {1:4} coul/tt 4.5 1.0'.format(int(h), c))
        else:
            res.append('pair_coeff {0:4} {1:4} coul/tt 4.5 1.0'.format(c, int(h)))
    res.append('pair_coeff {0:4} {1:3}* coul/tt 4.5 1.0'.format(int(h), dp))

with open(args.pfile, 'a+') as f:
    for line in res:
        f.write(line+'\n')