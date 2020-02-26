
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

if __name__ == "__main__":
    
    t = 1
    
    dict = {}
    S = read("s&t10.0.txt")
    print(S)
    for s1 in S:
        for s2 in s1:
            #print(s2)
            t1 = int(s2[0][2])*600 + int(s2[0][3])*60 + int(s2[0][4])*10 + int(s2[0][5])
            #print("t1:%d"% t1)
            #print(s1.index(s2))
            i = s1.index(s2)
            for s3 in s1[i+1:]:
                print(s3)
                t2 = int(s3[0][2])*600 + int(s3[0][3])*60 + int(s3[0][4])*10 + int(s3[0][5])
                #print("t2:%d"% t2)
                if t2 - t1 <= t:
                    print((s2[0][:2],s3[0][:2]))
                    if (s2[0][:2],s3[0][:2]) in dict:
                        dict[(s2[0][:2],s3[0][:2])] += 1
                    elif (s3[0][:2],s2[0][:2]) in dict:
                        dict[(s3[0][:2],s2[0][:2])] += 1
                    else:
                        dict[(s2[0][:2],s3[0][:2])] = 1
                else:
                    break
    print(dict)  
    
    dict2 = {}
    
    for k,v in dict.items():
        if (k[0][0] in ['X','Y','Z','x','y','z']) or (k[1][0] in ['X','Y','Z','x','y','z']):
            dict2[k] = v;
    print(dict2)    
            #for s3 in s2:
                #print(s3)