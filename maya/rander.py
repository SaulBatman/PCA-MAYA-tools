# -*- coding: UTF-8 -*-
# Running in the MAYA env
import maya.cmds as cmds
import pymel.core as pm
import random
import time
import os
from mtoa.cmds.arnoldRender import arnoldRender

st = time.time()
sil_num = 7
min_range = 18.0
max_range = 21.0
cam = pm.PyNode('camera1')
model_path = 'D:/mingxi/myData/obj_dataset/Val'
txt_path = 'D:/mingxi/myData/sil_dataset/Val'
dirs = os.listdir(model_path)
print(len(dirs))
poses = []

def getWSrotate(obj):
    rotate = cmds.xform( obj, q=True, ws=True, ro=True )
    return rotate

number=len(dirs)
for j in range(number):
    a = cmds.file(os.path.join(model_path, dirs[j]), ns="ns", i=True, rnn=True)
    print(a)
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", dirs[j][0]+dirs[j][1]+dirs[j][2]+dirs[j][3], type="string")
    temp = []
    for i in range(sil_num):
        pm.currentTime(i)
        values = [1, -1]
        rand1 = random.uniform(random.choice(values)*min_range, random.choice(values)*max_range)
        rand2 = random.uniform(min_range, max_range)
        rand3 = random.uniform(random.choice(values)*min_range, random.choice(values)*max_range)
        temp.append(rand1)
        temp.append(rand2)
        temp.append(rand3)
        cam.translate.set([0, 0, 0])
        cam.translate.set([rand1, rand2, rand3])
        arnoldRender(224, 224, True, True, 'camera1', ' -layer defaultRenderLayer')

        s = 't' + dirs[j][0]+dirs[j][1]+dirs[j][2]+dirs[j][3] + ' ' + str(temp[0]) + ' ' + str(temp[1]) + ' ' + str(temp[2]) + '\n'
        ss = 'r' + dirs[j][0]+dirs[j][1]+dirs[j][2]+dirs[j][3] + ' '+ str(getWSrotate('camera1')[0]) + ' ' + str(getWSrotate('camera1')[1]) + ' ' + str(getWSrotate('camera1')[2]) + '\n'
        with open(os.path.join(txt_path, 'poses.txt'), 'a') as f:
            f.write(s)
            f.write(ss)
            # f.write('\n')
    # poses.append(temp)
    pm.delete(a)

# for i in range(len(poses)):
#     s = str(poses[i])
#     with open('poses.txt', 'a') as f:
#         f.write(s)
#         f.write('\n')

en = time.time()
mid = en-st
print(mid)
