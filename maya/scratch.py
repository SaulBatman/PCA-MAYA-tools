# -*- coding: UTF-8 -*-
# Running in the MAYA env
# For generate models for PCA
# Each three joins will rotate and each scale will randomly changes
# No need to save parameters
import maya.cmds as cmds
import pymel.core as pm
import random
import time

st = time.time()
model_num = 150
sigma1 = 20
sigma2 = 10
for i in range(model_num):
    a1 = pm.PyNode('joint11')
    a2 = pm.PyNode('joint12')
    a3 = pm.PyNode('joint13')

    rand11 = random.gauss(0, sigma1)
    rand12 = random.gauss(0, sigma1)
    rand13 = random.gauss(0, sigma2)

    rand21 = random.gauss(0, sigma1)
    rand22 = random.gauss(0, sigma1)
    rand23 = random.gauss(0, sigma2)

    rand31 = random.gauss(0, sigma1)
    rand32 = random.gauss(0, sigma1)
    rand33 = random.gauss(0, sigma2)

    pm.rotate(a1, [0, 0, 0])
    pm.rotate(a2, [0, 0, 0])
    pm.rotate(a3, [0, 0, 0])

    pm.rotate(a1, [rand11, rand12, rand13])
    pm.rotate(a2, [rand21, rand22, rand23])
    pm.rotate(a3, [rand31, rand32, rand33])

    cmds.file('F:/Apps/MAYA/Maya2020/bin/myData/models/c'+str(i).zfill(4)+'.obj', pr=1, ea=1, force=1, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", type="OBJexport")

    if i % 10 == 0:
        print('have done', i, ' models')

en = time.time()
mid = en-st
print(mid)

# pm.rotate(a1, [rand11, rand12, rand13], a=False, ws=False, pgp=True)
