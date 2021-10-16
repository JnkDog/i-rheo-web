# x=111
# if x>10:
#     print('{} is greater than 10'.format(x))
# else:
#     print('{} is smaller than 10'.format(x))


# y=0
# liiii=[1,6,7,13,52,111,667,83,124]
# for x in liiii:
#     if x>y:
#         y=x
# print(y)


# lalala='tommy girl is a kind of perfume'

# for i in range(0,len(lalala)-1):
#     for j in range(i+1,len(lalala)):
#         if lalala[i]==lalala[j] and lalala[i]!=' ':
#             print('相同的字母为{}'.format(lalala[i]))
#             print('下标分别为{}和{}'.format(i,j))

# def solution(a,b,c):
#     return a+b+c

# if __name__=='__main__':
#     x=solution(1,1,1)
#     print(x)


# while True:
#     try:
        
#         total=int(input())
#         a=(input().strip().split())
        
#         b=max(a)
#         c=min(a)
        
        

#         aa=sorted(a)

        
#         d=aa[int((total-1)/2)]
        
        

#         lll=[0]*total
#         lll[0]=c
#         lll[-1]=d
#         lll[int((total-1)/2)]=b
        
#         # lll=str(lll)
#         lll=[str(i) for i in lll]
#         lll=" ".join(lll)
        
#         print(lll)
#         print(lll[1])
#     except:
#         break

# x={1:'qqq',2:'eeee'}
# z=x.get(3)
# print(z)
# lll=type(z) 
# print(lll)


# while True:
#     try:
#         a=input().strip().split()
#         for i in range(len(a)-1):
            
#             for j in range(i+1,len(a)):
#                 if a[i]==a[j]:
#                     a[j]='remo'
#         del_remo=[]
#         for ii in a:
#             if ii == 'remo':
#                 del_remo.append(ii)

#         for jj in del_remo:
#             a.remove(jj)
        
#         print(a)

    

#     except:
#         break
# import copy

# a=[1,2,3,4,5,['a','b']]
# b=copy.deepcopy(a)
# a.append(9)
# a[5].append('ccc')
# print(b)





# 消除一段字符串的字母和标点符号 并且保留2位小数
# import time
# import string
# # string.punctuation

# import re
# start=time.time()
# text = '''Don't worry, b.....e happy123!''' # 'Don\'t worry, be happy'

# punctuation_string = string.punctuation
# for i in punctuation_string:
#     text = text.replace(i, '')
# print(text)

 
# temp = re.sub('[a-zA-Z]','',text)
# print(temp)

# a=float(temp.strip())
# a=format(a,'.2f')
# print(a)
# end=time.time()

# print('耗时{}秒'.format(end-start))


# lists = [0, 1, 2, 3, 4, 5]
# # 输出 5, 4, 3, 2, 1, 0
# for i in range(len(lists)-1, -1, -1):
#     print(lists[i])
 
# # 输出5, 4, 3
# for i in range(5, 2, -1):
#     print(lists[i])


# 0-2^16的10% 20% 30% 40%
# import random


# def lalala():
#     a=random.randint(0,2**16)
#     b=0
    

#     if a>=0 and a<= (2**16/10):
#         b=1
#     elif a>(2**16/10) and a<=((2**16/10)*3):
#         b=2
#     elif a>((2**16/10)*3) and a<=((2**16/10)*6):
#         b=3
#     elif a>((2**16/10)*6):
#         b=4
#     return b


# if __name__=='__main__':

#     i=0
#     c={1:0,2:0,3:0,4:0}
#     d=[]
#     while i<10000:

#         b=lalala()
#         d.append(b)
#         i+=1
#     a1=d.count(1)
#     a2=d.count(2)
#     a3=d.count(3)
#     a4=d.count(4)
#     print(a1,a2,a3,a4)

# c,d=map(int,input().strip().split())
# while True:
#       try:
#           kind1=[]
#           kind2=[]
#           for i in range(c):
#               a,b=map(int,input().strip().split())
#               kind1.append(a)
#               kind2.append(b)
#           time1=min(a)
#           o1=kind1.count(time1)
#           time2=min(b)
#           o2=kind2.count(time2)
#           if a<=b:
#              x1=time1*d/o1
#              kind1.remove(min(a))
#              for i in range(len(kind1)):
#                  rest1 = 0
#                  rest1=rest1 + x1//kind1[i]
#              rest = d-rest1
#              max1=max(kind1)
#              x2=max1*rest
#              print(x1+x2)
#           else:
#              x1=time2*d/o2
#              kind2.remove(min(b))
#              for i in range(len(kind2)):
#                  rest1 = 0
#                  rest1=rest1 + x1//kind2[i]
#              rest = d-rest1
#              max1=max(kind2)
#              x2=max1*rest
#              print(x1+x2)

#       except:
#             break 
# a=type(c)

# print(a)


# 冒泡排序
# def lalala(array):
#     for i in range(1,len(array)):
#         for j in range(0,len(array)-i):
#             if array[j]>array[j+1]:
#                 array[j],array[j+1]=array[j+1],array[j]
#     return array

# if __name__=='__main__':
#     a=input().strip().split()
#     a=list(map(int,a))
#     b=[]
#     b=lalala(a)
#     print(a)

# 找出0-输入数的奇数和
# a=int(input())
# b=0
# for i in range(0,a):
#     if i%2==1:
#         b+=i
# if a%2==1:
#     b+=a

# print(b)



# a=input()
# b=input()

# c=a[2]
# d=int(a[5])

# e=b[2]
# f=int(b[5])

# aa={c:d}
# bb={e:f}
# aa.update(bb)

# print(aa)


# ''''''''''''''''''''''''''''''''''''''''''''''''''''''



# 动态规划-找出最大递增区间
# import time

# def length(nums):
#     n = len(nums)
#     L = [1]*n
#     for i in reversed(range(0,n)):
#         for j in range(i+1,n):
#             if nums[j]>nums[i]:
#                 L[i] = max(L[i], L[j]+1)
#     return max(L)

# start=time.time()
# nums=[1,5,2,3,4,7]

# b=length(nums)
# print(b)

# end=time.time()
# print(end-start)

# 连续子序列的最大和
# array=list(map(int,input().strip().split()))     

# lists=[]
# res = 0
# temp = 0
# for i in range(len(array)):
#     temp += array[i]
#     lists.append(array[i])
    
#     res = max(res, temp)
    
#     if temp + array[i] < 0:
        
#         lists=[]
    
#         temp = 0 

# print(res)
# print(lists)

    
    

 




# afssadaasgadsgagdggg



# def reverse(n) ->int:
#     a = ""
#     b = ''
#     c=[asd,adfsag,asdgsah,ahhhhh]
#     d=[]
#     for i in range(len(n)):
#         # a = a + n[len(n)-1-i]
#         for j in range(i,len(n)):
#             b+=n[j]
#             c.append(b)

        
#     return a,b


# n = input()
# a = reverse(n)
# if n == a:

# # 斐波那契数列 递归
# def fibonacci(n):
#     if n == 1:
#         return 1
#     elif n == 0:
#         return 0
#     return fibonacci(n-2)+fibonacci(n-1)

# b=[]
# n=0
# while n<=20:
#     b.append(fibonacci(n))
#     n+=1
# print(b)

# c=fibonacci(9)
# print(c)


# import datetime
# a=datetime.datetime.now()
# print(a)

# # 打印自己本身
# with open(r'D:\study\yanyixia\i-rheo\i-rheno-web\algorithm\bulk\study.py','r',encoding='UTF-8') as f:
#     for i in f.readlines():
#         print(i,end='')
#     f.close()





