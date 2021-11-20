import os
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np


# PCA



# ------load obj fils

def pointArray(directory_name):
    nameList = []
    for item in os.listdir(directory_name):
        if item.endswith('obj'):
            nameList.append(item)
    print('Number of object files: ', len(nameList))
    # print(nameList)
    wholePoints = []
    for i in range(0, len(nameList)):
        objFilePath = directory_name + '/' + nameList[i]
        with open(objFilePath) as file:
            points = []
            while 1:
                line = file.readline()
                if not line:
                    break
                strs = line.split(' ')
                if strs[0] == 'f':
                    break
                if strs[0] == 'v':
                    points.append(float(strs[1]))
                    points.append(float(strs[2]))
                    points.append(float(strs[3]))
            # print(points)
            wholePoints.append(points)
        if i % 10 == 0:
            print(i, '/', len(nameList))
    print('Length of wholePoints: ', len(wholePoints))

    return wholePoints


PATH = '/home/uic3dlab/mingxi/PCA_w/uniformModel'
wholePoints = pointArray(PATH)
print(int(len(wholePoints[0]) / 3))

# calculate average model
# x = np.array(wholePoints)
# average = np.sum(x, axis=0) / len(wholePoints)
# print('average shape', np.shape(average))

# # write a average.txt file
# filename = os.listdir('./PCAData')
# if 'average.txt' not in filename:
#     for i in range(len(wholePoints)):
#         s = 'v ' + str(average[3 * i]) + ' ' + str(average[3 * i + 1]) + ' ' + str(average[3 * i + 2])
#         with open('./myData/average.txt', 'a', encoding="utf-8") as f:
#             f.write(s)
#             f.write('\n')
#     print('average.txt is saved')
#     average = pd.DataFrame(average)
#     average.to_csv("./PCAData/average.csv",index=False)
#     print('average.csv is saved')

# else:
#     print('Warning: There is a already a average.txt in the folder. Please delete or move it if you want a new one')



# Principal components analysis
pca_num=10
pca = PCA(n_components = pca_num)
X_new = pca.fit_transform(wholePoints)
eigenVector = pd.DataFrame(pca.components_)
eigenVector.to_csv("/home/uic3dlab/mingxi/ModelsforPCA/uniformModel/eigenVector.csv",index=False)
print('eigenVector.csv is saved')

if __name__ == '__main__':
    print("?")
    eigenVector = np.array(pd.read_csv("./PCAData/eigenVector.csv"))
    # average = np.array(pd.read_csv("./PCAData/average.csv"))
    print('eigenVector\'s shape is: ',eigenVector.shape)
    # print('average\'s shape is: ',average.shape)


