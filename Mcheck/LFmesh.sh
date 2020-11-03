#!/bin/bash
#npy plyfromnpy
#matching 2d→3d LR create

python makeNpy.py
python plyFromNpy.py
python Matching.py
python FP2d_3d.py
python LR.py
python create
