#Running in the env with sklearn, not in MAYA
#For PCA and generating new model for training
import os
import numpy as np
from sklearn.decomposition import PCA
import random
import time
import pandas as pd
import re


class myPCA():
    def __init__(self, component_num=10, model_PATH='D:/mingxi/myData/allmodels',
                 ori_PATH='D:/mingxi/myData/originalModels/original_30k.obj'):
        print('PCA component_num is: ', component_num,'\n')
        print('model_PATH: ', model_PATH,'\n')
        print('original_PATH: ', ori_PATH,'\n')
        # extract vertices in obj files
        self.com_num=component_num
        nameList = []
        for item in os.listdir(model_PATH):
            if item.endswith('obj'):
                nameList.append(item)
        print('Number of object files: ', len(nameList))
        # print(nameList)
        with open(ori_PATH) as file:
            self.faces = []
            while 1:
                line = file.readline()
                if not line:
                    break
                strs = line.split(' ')
#                 print(strs)
                #print(strs)
                if strs[0] == 'f':
#                     search1 = re.search(r'(.*)//(.*)', strs[1], re.M | re.I)
# #                     print('search1: ', search1.group(1))
#                     search2 = re.search(r'(.*)//(.*)', strs[2], re.M | re.I)
# #                     print('search2: ', search2.group(1))
#                     search3 = re.search(r'(.*)//(.*)', strs[3], re.M | re.I)
# #                     print('search3: ', search3.group(1))
#                     search4 = re.search(r'(.*)//(.*)', strs[4], re.M | re.I)
#                     haha ='f '+ search1.group(1)+ '// '+ search2.group(1)+ '// '+ search3.group(1)+ '// '+ search4.group(1)+ '//\n' 
#                     self.faces.append(haha)
                    #print(strs)
                    self.faces.append(strs)
    
        self.wholePoints = []
        for i in range(0, len(nameList)):
            objFilePath = os.path.join(model_PATH, nameList[i])
            with open(objFilePath) as file:
                points = []
                while 1:
                    line = file.readline()
                    if not line:
                        break
                    strs = line.split(' ')
                    if strs[0] == 'v':
                        points.append(float(strs[1]))
                        points.append(float(strs[2]))
                        points.append(float(strs[3]))
                # print(points)
                self.wholePoints.append(points)
                if i>0 and i%10 == 0:
                    print(i,'/',len(nameList))
        print('Length of wholePoints: ', len(self.wholePoints))
        print('Each model has ',int(len(self.wholePoints[0]) / 3), ' vertices')

        self.pca = PCA(n_components=component_num)
        X2D = self.pca.fit_transform(self.wholePoints)
        self.eigenVec = self.pca.components_

        x = np.array(self.wholePoints)
        self.average = np.sum(x, axis=0) / len(self.wholePoints)

        self.eigenVector = self.pca.components_

        
        self.faces_num = len(self.faces)
        print('faces length: ', self.faces_num)
        print('model number is : ', len(self.wholePoints))
        self.vertex_num = int(len(self.average)/3)
        print('vertex_num is : ', self.vertex_num)

    def singularValue(self):
        return self.pca.singular_values_

    def explain(self):
        return self.pca.explained_variance_ratio_


# class generater(myPCA):
#     def __init__(self):
#         super(new_mbv2, self).__init__()
        
        
    def generate_average_obj(self, file_name =  'average.obj'):
        print(self.average)
        for j in range(self.vertex_num):
            s = 'v ' + str(self.average[3 * j]) + ' ' + str(self.average[3 * j + 1]) + ' ' + str(self.average[3 * j + 2])
            with open(file_name, 'a', encoding="utf-8") as f:
                f.write(s)
                f.write('\n')
        for p in range(self.faces_num):
            m = self.faces[p][0] + ' ' + self.faces[p][1] + ' ' + self.faces[p][2] + ' ' + self.faces[p][3]
            with open(file_name, 'a', encoding="utf-8") as ff:
                ff.write(m)
                
        df = pd.DataFrame(self.average)
        df.to_csv('average.csv', index=False)
        df = pd.read_csv('average.csv')
        print(np.array(df).shape)

                
    def generated_points(self, wj):
        wj = np.array(wj)
        cusvector = np.dot(wj, self.eigenVector)
        new = self.average + cusvector
        return new

    def generate_one_obj(self, wj, file_name):
        wj = np.array(wj)
#         print('wj:\n',wj, '\n')
        cusvector = np.dot(wj, self.eigenVector)
#         print('cusvector:\n',cusvector, '\n')
        new = self.average + cusvector
#         print(new-self.average)
        print('self.average:\n',self.average, '\n')
        print('new:\n',new, '\n')
        for jj in range(self.vertex_num):
            s = 'v ' + str(new[3 * jj]) + ' ' + str(new[3 * jj + 1]) + ' ' + str(new[3 * jj + 2])
            with open(file_name, 'a', encoding="utf-8") as f:
                f.write(s)
                f.write('\n')
        for p in range(self.faces_num):
#             print(self.faces[p])
            # m = self.faces[p]
            m = self.faces[p][0] + ' ' + self.faces[p][1] + ' ' + self.faces[p][2] + ' ' + self.faces[p][3]
            with open(file_name, 'a', encoding="utf-8") as ff:
                ff.write(m)
                ff.write('\n')

    def generate_random_obj(self, wj_range, number, Path='./', counter=0):
        # random wj[i] plus&minus wj_range
        print('wj_range is: ', wj_range)
        print('model number is: ', number)
        print('Path is: ', Path)
        values = [1, -1]
        weightWhole = []
        for i in range(number):
            rand_w = np.zeros(self.com_num)
            # rand_w = np.ceil(n*np.random.rand(1,5))
            for n in range(self.com_num):
                #rand_w[n] = random.uniform(-wj_range[n], wj_range[n])
                rand_w[n] = random.uniform(-wj_range[n], wj_range[n])
            print('rand_w is: ',rand_w, '\n')
            new_cusvector = np.dot(rand_w, self.eigenVector)
            new = self.average + new_cusvector

            file_name = Path + '/allmodels/'+ str(counter).zfill(4) + '.obj'
            print('file_name is: ',file_name)
            for j in range(self.vertex_num):
                s = 'v ' + str(new[3 * j]) + ' ' + str(new[3 * j + 1]) + ' ' + str(new[3 * j + 2])
                with open(file_name, 'a', encoding="utf-8") as f:
                    f.write(s)
                    f.write('\n')

            for p in range(self.faces_num):
#                 print(self.faces[p])
                ss =  self.faces[p][0] + ' ' + self.faces[p][1] + ' ' + self.faces[p][2] + ' ' + self.faces[p][3] 
                # ss =  self.faces[p]
                with open(file_name, 'a', encoding="utf-8") as ff:
                    ff.write(ss)
                    ff.write('\n')

            pca_file=Path+'/pca_weight.csv'
            weightWhole.append(rand_w)
            
            # sss = str(rand_w)
            # with open(pca_file, 'a', encoding="utf-8") as fff:
            #     fff.write(sss)
            #     fff.write('\n')
                
            print('counter: ', counter,'\n')
            counter = counter + 1
            
            if i % 10 == 0:
                print('have done', i, ' models\n')

        df = pd.DataFrame(np.array(weightWhole))
        df.to_csv(pca_file, index=False)
        # df = pd.read_csv('average.csv')
        # print(np.array(df).shape)
            
# Need a 1xComponent_num weight

data = myPCA(component_num=2,
	    model_PATH='./ModelsforPCA/uniformModel',
            ori_PATH='./originalModels/original_30k.obj')

# data.generate_average_obj(file_name =  '/home/uic3dlab/mingxi/bbbFootNet/myData/average.obj')
df = pd.DataFrame(np.array(data.eigenVec))
df.to_csv('./PCAData/eigenVector.csv', index=False)

start=time.time()
data.generate_random_obj([0, 150], 4000, './PCAData/crazy1')


# data.generate_one_obj([0, 0, 0, 0, 20, 0, 0, 0, 0, 0], './PCAData/test4.obj')
# data.generate_one_obj([0, 0, 0, 0, 0, 20, 0, 0, 0, 0], './PCAData/test5.obj')
# data.generate_one_obj([0, 0, 0, 0, 0, 0, 10, 0, 0, 0], './PCAData/test6.obj')
# data.generate_one_obj([0, 0, 0, 0, 0, 0, 0, 10, 0, 0], './PCAData/test7.obj')

end=time.time()

print('it costs ', end-start, ' seconds.\n')
