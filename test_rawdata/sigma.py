
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
df_news = pd.read_table('SingExp6_5.txt',header = None)

y = []
#time=np.linspace(1e-2,1e2,10000)
#print(df_news[1]
i=0
#print(time[120], df_news[1][120] )
'''
for i in range(0, 120):
    x.append(time[i])
    y.append(df_news[1][i])
'''
#plt.plot(x,y)
plt.plot(df_news[0],df_news[1],'-o', lw=3, color='royalblue',label='$G^{II}$')
plt.xscale('log')
plt.xlabel('Time (s)')
plt.ylabel('G(t) (Pa)')
#ax.set_xscale('log')
#plt.xticks
#plt.axis([1e-2,1e2,0,1])
plt.show()



'''
import pylab
def loadData(flieName):
    inFile = open(flieName, 'r')#以只读方式打开某fileName文件
 
    #定义两个空list，用来存放文件中的数据
    X = []
    y = []
 
    for line in inFile:
        trainingSet = line.split(',') #对于每一行，按','把数据分开，这里是分成两部分
        X.append(trainingSet[0]) #第一部分，即文件中的第一列数据逐一添加到list X 中
        y.append(trainingSet[1]) #第二部分，即文件中的第二列数据逐一添加到list y 中
 
    return (X, y)    # X,y组成一个元组，这样可以通过函数一次性返回
def plotData(X, y):
    length = len(y)
            
    pylab.figure(1)
 
    pylab.plot(X, y, 'rx')
    pylab.xlabel('Population of City in 10,000s')
    pylab.ylabel('Profit in $10,000s')
 
    pylab.show()#让绘制的图像在屏幕上显示出来

(X,y) = loadData('SingExp6_5.txt')
 
plotData(X,y)
'''