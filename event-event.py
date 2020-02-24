import time
import sys
PLACE_HOLDER = '_'

def read(filename):
    S = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            elements = line.split(',')      #分隔符
            s = []
            for e in elements:
                s.append(e.split())
            S.append(s)
    return S

  
class SquencePattern:
    def __init__(self, squence, support):
        self.squence = []
        for s in squence:
            self.squence.append(list(s))  #元组换成列表
        self.support = support
    def add(self, p):                           
        self.squence.extend(p.squence)    
        self.support = min(self.support, p.support)

           
def NprefixSpan(pattern, S, threshold):#S为三维数组
    patterns = []
    f_list = get_frequent_items(S, pattern, threshold)
    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support)
        p.add(i)
        patterns.append(p)
        p_S = build_projected_database(S, p) #p_S就是投影数据库
        ###print("p.squence:%s" % p.squence)
        ###print("p_S:%s" % p_S)
        p_patterns = NprefixSpan(p, p_S, threshold)  #将递归得到的频繁模式加进总模式中
        patterns.extend(p_patterns)
    return patterns

def get_frequent_items(S, pattern, threshold):#获得频繁项集
    items = {}
    f_list = []
    if S is None or len(S) == 0:
        return []
        
    for s in S:     #S表示所有行三维数组，s表示单一行二维数组 ##S表示4维数组，s表示单一行三维数组
        break_flag2 = False
        counted = []
        for element in s:
            for item in element:#item:A00210
                '''if item[0] in ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                            'N','O','P','Q','R','S','T','U','V','W']:
                '''
                #if item[0] in ['I','J']:
                #if item[0] in ['D','A','K']:
                if item[0] in ['D']:
                    if item[:2] not in counted:
                        counted.append(item[:2])
                        if item[:2] in items :      
                            items[item[:2]] += 1
                        else:
                            items[item[:2]] = 1
                        ###print("items[%s]= %d" %(item[0],items[item[0]]))
                else:
                    for sequence in pattern.squence:
                        ###print("sequence = %s" %sequence)
                        if item[:2].upper() in sequence:
                            if item[:2] not in counted:
                                counted.append(item[:2])
                                if item[:2] in items : 
                                    items[item[:2]] += 1
                                    ###print("items[%s]= %d" %(item[0],items[item[0]]))
                                    break_flag2 = True
                                else:
                                    items[item[:2]] = 1
                                    ###print("items[%s]= %d" %(item[0],items[item[0]]))
                                    break_flag2 = True
                                if break_flag2 == True:
                                    break
                if break_flag2 == True:
                    break
            if break_flag2 == True:
                break
    f_list.extend([SquencePattern([[k]], v) for k, v in items.items() if v >= threshold])  #进行support比较，此为不带_型
    #print(f_list)
    sorted_list = sorted(f_list, key=lambda x: x.support)    #lambda是虚拟函数,x换成p也没问题，x指f_list，根据support的小大排序f_list
    return sorted_list

def build_projected_database(S, pattern):   ####改变数据库的递归顺序

    # print(S)
    #print(pattern.squence)

    p_S = []
    last_e = pattern.squence[-1]
    last_item = last_e[-1]##不用变
    
    #print("pattern.squence:%s" % pattern.squence)
    #print("last_e:%s" % last_e)
    #print("last_item:%s" % last_item)
    
    for s in S:
        temp_pattern = []
        for element in s:##element = ['_05','C05']
            ###print("element:%s" % element)
            is_prefix = False
            ####
            #for item in element:##item = 'B05'
            
            for item in last_e:####item = 'e' 'a'
                for t2 in element:##t2 = '_05'  'C05'
                    if item == t2[:2]:
                        is_prefix = True
                        break##可有可无？？                   
                break
            ###print("is_prefix:%d" % is_prefix)     
            
            if is_prefix:
                e_index = s.index(element)##该缀在整个序列中的位置
                ###print("e_index:%s" % e_index)
                temp_pattern = s[e_index + 1:]
                
            #
            #
            ###print("temp_pattern:%s" % temp_pattern)
        if len(temp_pattern) != 0:
            p_S.append(temp_pattern)
    return p_S


def filter_patterns(patterns):
    new_patterns = []
    #############需要什么就在这里加
    for p in patterns:
        '''dict = {'A0':0,'A1':0,'A2':0,'A3':0,'A4':0,'B0':0,'B1':0,'B2':0,'C0':0,'C1':0,'C2':0,'D1':0,'D2':0,'D4':0,'E1':0,'E2':0,'F0':0,'G0':0,'H0':0,'I3':0,'J3':0,'K4':0,'X1':0,'X2':0,
                'X4':0,'Y0':0,'Y1':0,'Y2':0,'Z0':0,'Z1':0,'Z2':0}
                '''
        dict = {'A0':0,'A1':0,'A2':0,'A3':0,'A4':0,'B0':0,'B1':0,'B2':0,'C0':0,'C1':0,'C2':0,'D1':0,'D2':0,'D4':0,'E1':0,'E2':0,'F0':0,'G0':0,'H0':0,'I3':0,'J3':0,'K4':0}        
        for item in p.squence:
            for element in item:
                '''if element in ['A0','A1','A2','A3','A4','B0','B1','B2','C0','C1','C2','D1','D2','D4','E1','E2','F0','G0','H0','I3','J3','K4','X1','X2','X4','Y0','Y1','Y2','Z0','Z1','Z2'
                            ]:'''
                if element in ['A0','A1','A2','A3','A4','B0','B1','B2','C0','C1','C2','D1','D2','D4','E1','E2','F0','G0','H0','I3','J3','K4'
                            ]:            
                    dict[element] += 1
                else:
                    dict[element.upper()] -= 1
            judge = True
            for count in dict.values():
                if count != 0:
                    judge = False
        if judge == True:
            new_patterns.append(p)
            #print("pattern:{0}, support:{1}".format(p.squence, p.support))
    #for i in new_patterns:
        #print("pattern:{0}, support:{1}".format(i.squence, i.support))
        
    ########打印第一遍
    return new_patterns
    
'''
def print_patterns(S, S2, patterns):
    count = 0
    for p in patterns:
        if len(p.squence) == 4:##########################################################长度最小限制###########
            pt = 240##########################关联模式过滤时间
            #pt = 60##########################关联模式过滤时间
            ave_time = get_time(S, S2, p.squence)
            #print()
            #print(ave_time)
            #print()
            t0 = int(ave_time[0][0])*600 + int(ave_time[0][1])*60  + int(ave_time[0][2])*10 + int(ave_time[0][3])
            t1 = int(ave_time[1][0])*600 + int(ave_time[1][1])*60  + int(ave_time[1][2])*10 + int(ave_time[1][3])
            t2 = int(ave_time[2][0])*600 + int(ave_time[2][1])*60  + int(ave_time[2][2])*10 + int(ave_time[2][3])
            t3 = int(ave_time[3][0])*600 + int(ave_time[3][1])*60  + int(ave_time[3][2])*10 + int(ave_time[3][3])
            #print(p.squence[1][0])
            if((p.squence[1][0].isupper()) & (p.squence[1][0].lower() != p.squence[2][0])):  #ABab          
                if(t1-t0<=pt):
                    count += 1
                    print("{0}.模式:{1}{2}, 出现次数:{3}".format(count, p.squence[0], p.squence[1], p.support))
                    S2.write("{0}.模式:{1}{2}, 出现次数:{3}\n".format(count, p.squence[0], p.squence[1], p.support))#####
                    print("时间：{0}, {1}".format(ave_time[0], ave_time[1]))
                if(t2-t1<=pt):
                    count += 1
                    print("{0}.模式:{1}{2}, 出现次数:{3}".format(count, p.squence[1], p.squence[2], p.support))
                    S2.write("{0}.模式:{1}{2}, 出现次数:{3}\n".format(count, p.squence[1], p.squence[2], p.support))#####
                    print("时间：{0}, {1}".format(ave_time[1], ave_time[2]))
                if(t3-t2<=pt):
                    count += 1
                    print("{0}.模式:{1}{2}, 出现次数:{3}".format(count, p.squence[2], p.squence[3], p.support))
                    S2.write("{0}.模式:{1}{2}, 出现次数:{3}\n".format(count, p.squence[2], p.squence[3], p.support))#####
                    print("时间：{0}, {1}".format(ave_time[2], ave_time[3]))
            if(p.squence[1][0].isupper() and p.squence[1][0].lower() == p.squence[2][0]):  #ABba          
                if(t1-t0<=pt):
                    count += 1
                    print("{0}.模式:{1}{2}, 出现次数:{3}".format(count, p.squence[0], p.squence[1], p.support))
                    S2.write("{0}.模式:{1}{2}, 出现次数:{3}\n".format(count, p.squence[0], p.squence[1], p.support))#####
                    print("时间：{0}, {1}".format(ave_time[0], ave_time[1]))
                if(t3-t2<=pt):
                    count += 1
                    print("{0}.模式:{1}{2}, 出现次数:{3}".format(count, p.squence[2], p.squence[3], p.support))
                    S2.write("{0}.模式:{1}{2}, 出现次数:{3}\n".format(count, p.squence[2], p.squence[3], p.support))#####
                    print("时间：{0}, {1}".format(ave_time[2], ave_time[3]))
            elif(p.squence[2][0].isupper()): #AaBb
                if(t2-t1<=pt):
                    count += 1
                    print("{0}.模式:{1}{2}, 出现次数:{3}".format(count, p.squence[1], p.squence[2], p.support))
                    S2.write("{0}.模式:{1}{2}, 出现次数:{3}\n".format(count, p.squence[1], p.squence[2], p.support))#####
                    print("时间：{0}, {1}".format(ave_time[1], ave_time[2]))
            #
    print("模式个数为:%d" % count)        
    S2.write("模式个数为:%d\n" % count)'''

###算法1的打印
def print_patterns(S, S2, patterns):
    count = 0
    for p in patterns:
        if len(p.squence) == 6:##########################################################长度最小限制###########
            count += 1
            print("{0}.模式:{1}, 出现次数:{2}".format(count, p.squence, p.support))
            #S2.write("{0}.模式:{1}, 出现次数:{2}\n".format(count, p.squence, p.support))#####
            get_time(S, S2, p.squence)
            
    print("模式个数为:%d" % count)        
    S2.write("模式个数为:%d\n" % count)



def get_time(S, S2, squence):        
    time = {}
    length = len(squence)
    #print("squence:%s" % squence)
    #print("length:%d" % length)
    for i in range(length):
        time[i] = []
    #print("time:%s" % time)
    for s1 in S:
        #print("s1:%s" % s1)
        count = 0
        temp_time = {}
        for s2 in s1:           
            #print("s2:%s" % s2)
            #print("s2[0][0]:%s" % s2[0][0])
            '''if s2[0][0] == squence[count][0]:####s2[0][0]解决原序列中有多个
                temp_time[count]= s2[0][1:]
                count += 1'''
            for s3 in s2:
                #print("s3:%s" % s3)
                #print("squence[count][0]:%s" % squence[count][0])
                if s3[:2] == squence[count][0]:
                    temp_time[count] = s3[2:]
                    count += 1
                    #print("count:%d" % count)  
                    break
            if count == length:    ###全部符合就记录           
                for k,v in temp_time.items():
                    time[k].append(v)
                #print("done")
                #print("time:%s" % time)  
                break             
                #print("temp_time:%s" % temp_time)
    for k,v in time.items():
        time[k].sort()##########排序
    #print("time:%s" % time)
    #S2.write("time:%s\n" % time)

    
    ave_time = {}
    get_ave(time, ave_time)

    #print("ave_time:%s" % ave_time)
    #S2.write("ave_time:%s\n" % ave_time)
    
    recommend_time(time, ave_time)    #np4.5
    
    #return ave_time
###########################新时间    
    new_time = {}
    for i in range(len(time)):
        if(len(time[i])>= 2):
            #print((time[i][0]))
            new_time[i] = []
            new_time[i].append(time[i][0])
            if(time[i][-1] != time[i][0]):
                new_time[i].append(time[i][-1])
        elif(len(time[i]) == 1):
            new_time[i] = []
            new_time[i].append(time[i][0][0]+time[i][0][1]+':'+time[i][0][2]+time[i][0][3])
        else:
            new_time[i] = ['无合适时间']
#############################新时间2
    new_time2 = {}
    for i in range(len(new_time)):
        if(len(new_time[i]) == 2):
            new_time2[i] = []
            new_time2[i].append(new_time[i][0][0]+new_time[i][0][1]+':'+new_time[i][0][2]
            +new_time[i][0][3]+'-'+new_time[i][1][0]+new_time[i][1][1]+':'+new_time[i][1][2]
            +new_time[i][1][3]) 
        else:
            new_time2[i] = new_time[i]
            #new_time2[i] = []
            #new_time2[i].append(new_time[i][0][0]+new_time[i][0][1]+':'+new_time[i][0][2]+new_time[i][0][3])
          
    print("推荐时间:%s" % new_time2)
    #S2.write("推荐时间:%s\n" % new_time2)
###################################      
    #print("____________________________________________")
    S2.write("____________________________________________\n")
    
    
def recommend_time(time, ave_time):
    for i in range(len(time)):
        for j in range(len(time[i])):
            #print(time[i][j])
            #print(ave_time[i])
            a = time[i][j]
            b = ave_time[i]
            sum1 = int(a[0])*600 + int(a[1])*60  + int(a[2])*10 + int(a[3])
            sum2 = int(b[0])*600 + int(b[1])*60  + int(b[2])*10 + int(b[3])
            if (abs(sum1 - sum2)>240):###################################时间过滤限制##################################
                time[i][j] = 'null'           #if (b[0]>a[0])or((b[0]==a[0])and(b[1]>a[1]))or((b[0]==a[0])and(b[1]==a[1])and(b[2]>a[2]))or(b[0]==a[0])and((b[1]==a[1])and(b[2]==a[2])and(b[3]>=a[3])):
            #b>a                    
                #print("yes")
                #gap = (b[0]-a[0])*600
            #else:
            #a>b
                #print("no")
    #print(time)
    for i in range(len(time)):
        c = time[i].count('null')
        if c > 0:
            for j in range(c):
                time[i].remove('null')
    #print(time)    
    #new_time = time
    #for k,v in time.items():

def get_ave(time, ave_time):
    for k,v in time.items():
        length2 = len(v)
        sum = 0
        #print("length2:%d" % length2)
        #print("v:%s" % v)
        #v = [int(x) for x in v]
        for a in v:
            sum = sum + int(a[0])*600 + int(a[1])*60  + int(a[2])*10 + int(a[3])
        #print("sum:%d" % sum)
        ave = int(sum/length2)
        n1 = int(ave/600)
        #print("n1:%d" % n1)
        s1 = ave % 600
        #print("s1:%d" % s1)
        n2 = int(s1/60)
        #print("n2:%d" % n2)
        s2 = s1 % 60
        #print("s2:%d" % s2)
        n3 = int(s2/10)
        #print("n3:%d" % n3)
        s3 = s2 % 10
        #print("s3:%d" % s3)
        last = str(n1) + str(n2) + str(n3) + str(s3)
        #print("last:%s" % last)
        ave_time[k] = last    
        
        
if __name__ == "__main__":
    #S = read("s&t4.0.txt")
    S = read("s&t10.0.txt")
    #S2 = read("sequence.txt")
    S2 = open("exam.txt", 'w+') 
    #print(S)
    num_p = 0
    #patterns = NprefixSpan(SquencePattern([], sys.maxsize), S, 2)
    patterns = NprefixSpan(SquencePattern([], sys.maxsize), S, 14)
    new_patterns = filter_patterns(patterns)
    #print_patterns(S, S2, patterns)
    print_patterns(S, S2, new_patterns) ################算法2的打印




