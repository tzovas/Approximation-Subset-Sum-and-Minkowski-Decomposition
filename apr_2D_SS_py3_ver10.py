import math
import operator
import time
import random
import sys
import bisect

from aux_functions import *


hit_sum=0
L_sum=0


## trim
def trim_2D_10(inL, mu):
    """
    inL must have the format:
    column 0, x coord
    column 1, y coord
    column 2, length
    column 3, angle
    column 4, list of indexes
"""
    
    t = time.process_time() 
    #sort according to the vectors length
    sorted_L=inL
    #we suppose the list is already sorted
    N=len(inL)
    N2=N
    R=[]
    
    #count the hits, how many vectors are removed
    max_j=0
    sum_j=0
    hit_cnt=0
    max_win=0
    i=0
    A = []

    #leave out very short vectors that do not create a radius more than 1
    x=sorted_L[0]
    while i<N-1 and x[2]<1/mu:        
        if R==[]:
            R.append(x)
        else:
            #add x only if the other vectors in R are different from x
            r=len(R)-1
            add_x_flag= True
            while r>=0 and R[r][2]==x[2]:
                if R[r][0]==x[0] and R[r][1]==x[1]:
                    add_x_flag = False
                    break
                else:
                    r=r-1

            if add_x_flag==True:
                R.append(x)
        x = sorted_L[i]
        i=i+1
    #^^ while
        
    i=i-1            
    if i<0:
        i=0        
    
    j=i
    r=0

    if R==[]:
        x=sorted_L[i]
        R.append[x]
        i=1
        
    while i<N:
        x=sorted_L[i]     

        r=bin_search_2D(R, int(x[2]/(1+mu)), 2, r)
            
        if len(R)-r>max_win:
            max_win=len(R)-r
        
        #at this point, r indicates the the first vector v (the shortest)
        #in whose zone x belongs

        add_x_flag=True
        #check the vector in R.All these vector have the proper length.
        #If one has also the rigth angle, do not add x.

        #print(r,len(R))
        for j in range(r,len(R)):
            if R[j][3]-mu <x[3]< R[j][3]+mu:
                add_x_flag=False
                break
            
        if add_x_flag==True:
            R.append(x)

        i=i+1
    #^while i<N        
    #hit_percent = round(N2/(len ) ,2)

     
    #print("\nin trim:original size=",N2 ," hits=",N2-len(R), "len(ret)=",len(R))
    #print("percentage of deleted items=",round((N2-len(R))/N2*100,2),"%")
    print("maximum window is:", max_win,"len(L_i)=",len(R))
    elap_t = time.process_time() - t
    print("time elapsed=",elap_t)
    

    #print(R)
    
    return R
        
             
                

#
#---------------------------------------------------------------
#---------------------------------------------------------------
#


## SS_aprox
def D2_SS_approx(               inList,
                                #s=0,      #target value
                                c=0.2       #the error 0<c<1
                                ):
    x_list=[]       #x coordinate
    y_list=[]       #y coordinate
    len_list=[]     #length
    p_list=[]
    max_len=0
    cnt=0


    #points_list: every x in p_list is 5 numbers, its x and y coordinate,
    #               its length,its angle in radians and its index
    index=0
    for i in inList:
        i_len = (i[0]**2+i[1]**2)**(0.5)
        i_angle = angle_2D([i[0],i[1]])
        max_len = max_len+i_len
        #len_list.append( i_len )
        p_list.append([i[0],i[1],i_len,i_angle,cnt])
        cnt=cnt+1

    #print(p_list,'<>')
    #print(y_list,'<>',sum(y_list))
    #print(len_list,'<>',sum(len_list))
    
    N = len(inList)      # number of values
    M = max([max(abs(x[0]),abs(x[1])) for x in inList])
    
    #print("\nin approx_Subset sum: target=",s ,", error=",c,"and number of elements=", N)
    #print("also, sum of input is=" , sum(x_list),'\n%%\t%%\t%%\t%%\n')
    #t=time.process_time()

    p_list_2= sort_by_col(p_list,2)

    max_len_hits=0
    max_len_i=0
    S = [(0,0,0,0, [])]
    for x in p_list_2:
        t = time.process_time() 
        T = []
        len_x=x[2]
        max_boundary = max_len-max_len_i+c*M/N
        
        for Sx, Sy, Sl, Sa, tmp_list in S:
            Tx = x[0]+Sx
            Ty = x[1]+Sy
            Tl = (Tx**2+Ty**2)**(0.5)
            Ta = angle_2D([Tx,Ty])
            if Tl<max_len/2:
                if Tl<max_boundary:
                    T.append( (Tx, Ty, Tl, Ta, sorted(tmp_list + [x[4]])) )
                else:
                    T.append( (Tx, Ty, Tl, Ta, sorted(tmp_list + [x[4]])) )
                    max_len_hits=max_len_hits+1
                    
            else:
                T.append( (Tx, Ty, Tl, Ta, sorted(tmp_list + [x[4]])) )
                max_len_hits=max_len_hits +1

        elap_t = time.process_time() - t

        U = T + S
        
        #print(index,"::")
        index=index+1
        #print("max_len_hits=",max_len_hits)
        #print("\tlen(U) before trimming:\t",len(U))

        max_len_hits=0
             
        U = sort_by_col(U, 2)

        #print("largest length in U",U[len(U)-1][2])
        #print("difference =",max_boundary-U[len(U)-1][2])

        #trim the list U
        S = trim_2D_10(U, c/(float(N)**2))

       
    #position, res[1], it has the numbers that achieve this result as an array
    #res = sort_by_col(S, 2)
    res = S
    i=0;
    for x in res:
        #print(i,":",x)
        i=i+1
        if i>20:
            break
        
    return S

############################################################

