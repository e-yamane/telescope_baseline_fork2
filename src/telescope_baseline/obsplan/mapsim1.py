#!/usr/bin/env python3
"""Make mapping svg file

  usage:
    map1.py [-h|--help] -m M -o out.svg


  options:
    --help     show this help message and exit
    -m M       parameter M
    -o out.svg output file
"""
import numpy as np
import math
import svgwrite
from docopt import docopt 

if __name__ == '__main__':
    args = docopt(__doc__)

#M=6320
M = int(args['-m'])

# Drawing parameters
mm = 3.543307
deg = 14*mm # 1 deg = 40mm
paper_width = 297*mm
paper_hight = 210*mm
xcenter=paper_width/2
ycenter=paper_hight/2

# Model parameters
CellPix=13
EFL = M*10/CellPix
pfov = 10e-3/EFL * 180/math.pi
Npix = 1952
ChipSpacingA = 22.4/EFL * 180/math.pi
ChipSpacingB = 22.4/EFL * 180/math.pi

text='EFL={:.3f}'.format(EFL)

# Field parameters
widex=2
widey=2
gc=0.7
gdw=1.5
gdh=0.3

def degxys(x,y):
  return (x*deg*mm,y*deg*mm)

def degxy(x,y):
  return ((x*deg*mm+xcenter,y*deg*mm+ycenter))

# Prepare a container for all elements
dwg = svgwrite.Drawing( args['-o'],size=(297*mm,210*mm) )

# Add an axis group 
axis = dwg.add(dwg.g(id='axis'))
axis.add(dwg.line(start=degxy(-widex,-widey),end=degxy(widex,-widey),stroke='black',stroke_width=2))
axis.add(dwg.line(start=degxy(-widex,     0),end=degxy(widex,     0),stroke='black',stroke_width=1))
axis.add(dwg.line(start=degxy(-widex, widey),end=degxy(widex, widey),stroke='black',stroke_width=2))
axis.add(dwg.line(start=degxy(-widex,-widey),end=degxy(-widex,widey),stroke='black',stroke_width=2))
axis.add(dwg.line(start=degxy(     0,-widey),end=degxy(     0,widey),stroke='black',stroke_width=1))
axis.add(dwg.line(start=degxy( widex,-widey),end=degxy( widex,widey),stroke='black',stroke_width=2))

# Add Text
title = dwg.add(dwg.g(id='axis'))
title.add(dwg.text(text,insert=degxy(-gc,0.8)))


# Add the central region
cent = dwg.add(dwg.g(id='cent'))
cent.add(dwg.rect(insert=degxy(-gc,-gc),size=degxys(2*gc,2*gc)))
cent.fill('green', opacity=0.1)

# Add the disk region
disk = dwg.add(dwg.g(id='disk'))
disk.add(dwg.rect(insert=degxy(-gc,-gdh),size=degxys(gc+gdw,2*gdh)))
disk.fill('blue', opacity=0.1)

# Add a field
def addfield( centerX,centerY,PA,dwg,id ):
  field = dwg.add(dwg.g(id='field{}'.format(id)))
  for i in range(4):
    X = np.empty(4)
    Y = np.empty(4)
    if i==0 or i==1:
      X[0]=-ChipSpacingA/2-Npix*pfov/2
    else:
      X[0]=ChipSpacingA/2-Npix*pfov/2
    if i==0 or i==2:
      Y[0]=-ChipSpacingB/2-Npix*pfov/2
    else:
      Y[0]=ChipSpacingB/2-Npix*pfov/2
    X[1]=X[0]+Npix*pfov
    X[2]=X[1]
    X[3]=X[0]
    Y[1]=Y[0]
    Y[2]=Y[1]+Npix*pfov
    Y[3]=Y[2]
    Xd = X+centerX
    Yd = Y+centerY
    points = (degxy(Xd[0],Yd[0]),degxy(Xd[1],Yd[1]),degxy(Xd[2],Yd[2]),degxy(Xd[3],Yd[3]))
    field.add(dwg.polygon( points=points ) )
    field.fill('red', opacity=0.2)

addfield(-gc+ChipSpacingA/2+Npix*pfov/2,-gc+ChipSpacingB/2+Npix*pfov/2,0,dwg,0)
addfield(-gc+ChipSpacingA/2+Npix*pfov/2,-gc+ChipSpacingB/2*3+Npix*pfov/2,0,dwg,1)
addfield(-gc+ChipSpacingA/2+Npix*pfov/2,-gc+ChipSpacingB/2*7+Npix*pfov/2,0,dwg,1)
addfield(-gc+ChipSpacingA*3/2+Npix*pfov/2,-gc+ChipSpacingB/2*7+Npix*pfov/2,0,dwg,1)

dwg.save()
