import matplotlib.pyplot as plt
import numpy as np
import math
from pandas import DataFrame
import pandas as pd
from scipy import stats
import sympy as sp
np.set_printoptions(suppress=True)

def statistic(data,k=None,gc=None,begin=None,color='#1f77b4',label_color='black',label_size=10,label_digits=2,max_digits=10,show=False):
    """ 
    data:   列表，或其他可迭代类型
    k:      组距
    gc:     组数
    begin:  数据分割起始值
    
    """
    #求极差
    max_ = max(data)
    min_ = min(data)
    range_ = max_ - min_
    
    #决定组距与组数
    if k == None and gc == None:
        gc = 8
        if range_/gc >=0.9:
            k = math.ceil(range_ / gc)
        else:
            k = float(format(range_/gc,".2f")) + range_/gc/10*1.1
    elif k == None and gc != None:
        if range_/gc >=0.9:
            k = math.ceil(range_ / gc)
        else:
            k = float(format(range_/gc,".2f")) + range_/gc/10*1.1
    elif k != None and gc == None:
        gc = math.ceil(range_ / k)
    
    #将数据分组
    box = []
    if begin == None:
        begin = min_
    nextbegin = begin
    for i in range(gc):
        box.append([nextbegin,nextbegin+k])
        nextbegin += k
    
    drawer = [0]*gc    
    for i in data:
        if i == box[-1][1]:
            drawer[-1] += 1
        for j in range(gc):
            if i >= box[j][0] and i < box[j][1]:
                drawer[j] += 1
    
    freq = []
    for i in range(gc):
        freq.append(drawer[i]/len(data))
          
    #列频率分布表
    # pd.set_option('display.unicode.ambiguous_as_wide', True)
    try:
        zhongshu = stats.mode(data)[0][0]
    except:
        zhongshu = None

    boxs = []
    for b in box:
        if b != box[-1]:
            boxs.append("[%d,%d)" % (b[0],b[1]))
        else:
            boxs.append("[%d,%d]" % (b[0],b[1]))
    pd.set_option('display.unicode.east_asian_width', True)
    df = DataFrame({'分组':boxs,'频数':drawer,'频率':freq},index=range(1,gc+1))
    df.loc[gc+1] = {'分组':'合计','频数':len(data),'频率':1}
    df2 = DataFrame({ "特征":["组距","最大值","最小值","极差","平均数","中位数","众数","方差","标准差"],
                     "数值":[k,max_,min_,range_,np.mean(data),np.median(data),zhongshu,np.var(data),format(math.sqrt(np.var(data)),'.3f')]},
                   index=range(1,10))
    print(df)
    print("*"*20)
    print(df2)
    print("*"*20)
    #绘图
    fig,ax = plt.subplots()
    ax.set_xticks(np.arange(begin,nextbegin+k,k))
    ax.hist(data,gc,range=(begin,nextbegin),density=1,color=color)
    # plt.xticks(np.arange(begin,nextbegin+k,k))
    sub = 0
    for x,y in zip(box,freq):
        label = format(y/k,'.20f')
        c = 0
        f = False
        for z in range(len(label)):
            if (label[z] != '0' and label[z] != '.') or f:
                c+=1
                f=True
                if c == max_digits - label_digits:
                    f = True
                if c == label_digits+1:
                    sub = max([sub,z])
    for x,y in zip(box,freq):
        label = format(y/k,'.20f')
        label = format(y/k,".%df" % (sub - label.index('.')-1))
        ax.text((x[0]+x[1])/2,y/k,label,ha='center',va='bottom',color=label_color,fontsize=label_size)
        
    if show:
        fig.show()

def mean(data,acc=None):
    """ 
    均值
    """
    if acc != None:
        return (sp.Rational(1,len(data))*sum(data)).evalf(acc)
    else:
        return sp.Rational(1,len(data))*sum(data)
    
def var(data,acc=None):
    """ 
    方差
    """
    data_bar = mean(data)
    if acc != None:
        return (sp.Rational(1,len(data))*sum((i-data_bar)**2 for i in data)).evalf(acc)
    else:
        return sp.Rational(1,len(data))*sum((i-data_bar)**2 for i in data)
    

def std(data,acc=None):
    """ 
    标准差
    """
    if acc !=None:
        return sp.sqrt(var(data)).evalf(acc)
    else:
        return sp.sqrt(var(data))

def r(x,y,acc = None,usenumpy = False):
    """ 
    样本相关系数
    """
    if usenumpy == False:
        x_bar = mean(x)
        y_bar = mean(y)
        # print(x_bar,y_bar,std(x),std(y))
        anwser = sum((i-x_bar)*(j-y_bar) for i,j in zip(x,y))/(len(x)*std(x)*std(y))
        if acc != None:
            return anwser.evalf(acc)
        else:
            return anwser
    else:
        x_bar = np.mean(x)
        y_bar = np.mean(y)
        # print(x_bar,y_bar,std(x),std(y))
        anwser = (sum(i*j for i,j in zip(x,y)) - len(x)*x_bar*y_bar)/(len(x)*np.std(x)*np.std(y))
        return anwser
    
def lse(x,y,acc=None,usenumpy = False):
    """ 
    一元线性回归方程的参数的最小二乘估计
    返回a_hat,b_hat
    """
    if usenumpy == False:
        x_bar = mean(x)
        y_bar = mean(y)
        b_hat = sum((i-x_bar)*(j-y_bar) for i,j in zip(x,y))/(len(x)*var(x))
        a_hat = y_bar - b_hat*x_bar
        if acc != None:
            return a_hat.evalf(acc),b_hat.evalf(acc)
        else:
            return a_hat,b_hat
    else:
        x_bar = np.mean(x)
        y_bar = np.mean(y)
        b_hat = (sum(i*j for i,j in zip(x,y)) - len(x)*x_bar*y_bar)/(len(x)*np.var(x))
        a_hat = y_bar - b_hat*x_bar
        return a_hat,b_hat

    

if __name__ == "__main__":

    data = [9.0 ,13.6,14.9,5.9 ,4.0 ,7.1 ,6.4 ,5.4 ,19.4,2.0 ,
            2.2 ,8.6 ,13.8,5.4 ,10.2,4.9 ,6.8 ,14.0,2.0 ,10.5,
            2.1 ,5.7 ,5.1 ,16.8,6.0 ,11.1,1.3 ,11.2,7.7 ,4.9 ,
            2.3 ,10.0,16.7,12.0,12.4,7.8 ,5.2 ,13.6,2.6 ,22.4,
            3.6 ,7.1 ,8.8 ,25.6,3.2 ,18.3,5.1 ,2.0 ,3.0 ,12.0,
            22.2,10.8,5.5 ,2.0 ,24.3,9.9 ,3.6 ,5.6 ,4.4 ,7.9 ,
            5.1 ,24.5,6.4 ,7.5 ,4.7 ,20.5,5.5 ,15.7,2.6 ,5.7 ,
            5.5 ,6.0 ,16.0,2.4 ,9.5 ,3.7 ,17.0,3.8 ,4.1 ,2.3 ,
            5.3 ,7.8 ,8.1 ,4.3 ,13.3,6.8 ,1.3 ,7.0 ,4.9 ,1.8 ,
            7.1 ,28.0,10.2,13.8,17.9,10.1,5.5 ,4.6 ,3.2 ,21.6]

    data2 = [5678 ,13039,8666 ,9521 ,8722 ,10575,2107 ,4165 ,17073,11205,
            5467 ,11736,9986 ,8592 ,6542 ,12386,13115,5705 ,8358 ,13234,
            20142,9769 ,10426,12802,16722,8587 ,9266 ,8635 ,2455 ,4524 ,
            8260 ,13165,9812 ,9533 ,2377 ,5132 ,8212 ,7968 ,9859 ,3961 ,
            5484 ,11344,8722 ,12944,8597 ,12594,15101,4751 ,11130,11286,
            8897 ,7192 ,7313 ,8790 ,7699 ,10892,9583 ,9207 ,16358,10182,
            3607 ,1789 ,9417 ,4566 ,12347,3228 ,7606 ,8689 ,8755 ,15609,
            8767 ,9226 ,5622 ,11094,8865 ,11246,17417,7995 ,7317 ,6878 ,
            4270 ,11051,5705 ,5442 ,10078,9107 ,8354 ,6483 ,16808,1509 ,
            1301 ,10843,13864,12691,8419 ,14267,9809 ,9858 ,8922 ,12682]

    statistic(data,gc=10,label_size=8,show=True)
    x = [10,20,30,40,50,60,70,80,90,100]
    y = [62,68,75,81,89,95,102,108,115,122]
    lse(x,y)
    print(lse(x,y,acc=10),r(x,y,acc=10))