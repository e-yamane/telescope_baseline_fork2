#!/usr/bin/env python3.8
"""Plot efficinecy

    usage:
        plot_eff.py [-h|--help] -i eff.json -p plotfile.png

    options:
        --help            show this help message and exit
        -i eff.json       Efficinecy data
        -p plotfile.png   Output file
"""
from docopt import docopt                         # command line interface
import numpy as np
import matplotlib.pyplot as plt
from telescope_baseline.dataclass.wl_eff import WlEfic

if __name__ == '__main__':
    args = docopt(__doc__)

input_file = args['-i']

wl_eff = WlEfic.from_json(input_file)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0.8,1.7)
ax.set_ylim(0.0,1)
ax.set_xlabel('Wavelength ($\mu$m)')
ax.set_ylabel('Efficiency')
ax.set_title(wl_eff.title)
ax.text(0.85,0.50,wl_eff.comment,size=7)
ax.plot(wl_eff.wavelength,wl_eff.efficiency,label=wl_eff.title) 
ax.legend()
plt.show()
fig.savefig(args['-p'],transparent=True)
