#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy
import sys
import os.path

# Check command-line arguments
if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' <file.tsv>\n')
    exit(-1)
elif not os.path.isfile(sys.argv[1]):
    print('File not found: ' + sys.argv[1] + '\n')
    exit(-2)

# Open file
x = numpy.loadtxt(sys.argv[1])

# Plot data
plt.plot(x[:, 0], 'g', x[:, 1], 'm', x[:, 2], 'r')
plt.legend(['Healthy', 'Infected', 'Deaceased'])
plt.grid(True)
plt.show()
