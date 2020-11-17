#!/bin/bash
#npy plyfromnpy
#matching 2d→3d LR create

#Matching LR createNewPly rendering
#makeNpy plyFromNpy FP3d_3d
set -e
python ./libs/mymkdir.py
# python makeNpy.py
# python plyFromNpy.py
python plyFromImg.py
python Matching.py
python FP2d_3d.py
python LR.py
python createNewPly.py
python rendering.py
