import math
import operator
import time
import random
import sys
import bisect
import numpy as np



hit_sum=0
L_sum=0

##----------------------------------------------------------------------------            
#given a starting point and a sequence of vector the functions returns an
#array with the actula points of the polygon
#the point and the vectors are in 2 dimensions
#starting_point=[x0,y0] , vector_seq=[[z0_x,z0_y],[z1_x,z1_y], ... ,[zn_x,zx_y]]
def get_polygon_points(starting_point, vector_seq):
    """returns the actual coordinates of the points from the starting point
        and according to the vector sequence
    """
        
    #print("in auxiliary\\VP2_to_plain... \n...start timer...")
    #t=time.process_time()
    
    res=[[]]
    res[0] = starting_point
    curr_point = starting_point
    #print("in GET_POLYGON 1:",vector_seq,"len=",len(vector_seq))
    #vector_seq_2.append(vector_seq[0])
    #for i in range(1, len(vector_seq)):
    i=1
    #l= len(vector
    while i<len(vector_seq):
        #print('-->',i)
        #if vector_seq[i]==vector_seq[i-1]:
        if are_parallel(vector_seq[i],vector_seq[i-1]):
            tmp = vector_seq[i]
            vector_seq[i-1][0]=vector_seq[i-1][0]+ tmp[0]
            vector_seq[i-1][1]=vector_seq[i-1][1]+ tmp[1]
            vector_seq.pop(i)
        else:
            i=i+1
        #print('<< ', len(vector_seq))
            
    #print("in GET_POLYGON 2:",vector_seq,"len=",len(vector_seq))
        
    for x in vector_seq:
        x_coord = curr_point[0]+x[0]
        y_coord = curr_point[1]+x[1]
        curr_point=[x_coord, y_coord]
        res.append(curr_point)

    #print(res)
        
    #elapsed_time = time.process_time()-t
    #print("leaving get_polygon_points... time passed:",elapsed_time,"\n" )
    return res

#-----------------------------------------------------------------------------

#------------------------------------------------------------

def vector_seq(polygon):
    """returns the vector sequence of a polygon
    """
    vec_seq=[]
    P= polygon
    N = len(polygon)
    for i in range(0,N-1):
        vec_seq.append([P[i+1][0]-P[i][0], P[i+1][1]-P[i][1]])
    vec_seq.append([P[0][0]-P[N-1][0], P[0][1]-P[N-1][1]])

    #print(vec_seq)
    return vec_seq
#-----------------------------------------------------

def are_parallel(vec1, vec2):
    if angle_between(vec1, vec2)==0:
        return True
    else:
        return False

#-------------------------------------------------------------


##--------------- GCD
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return abs(x)
#-------------------------------------------------------------
#------------min with index
#return [a,b]: a is the min and b the index where the min is found
def index_min(values):
    """ return the minimun and the index where it is found
    """
    return min(values), min(range(len(values)),key=values.__getitem__)

#------------------------------------------------------------------

def sort_by_col(table, col=0):
    '''
    http://www.saltycrane.com/blog/2007/12/how-to-sort-table-by-columns-in-python/
    '''
    return sorted(table, key=operator.itemgetter(col))

#---------------------------------------------------------------

def dist_2D(v1, v2):
    """Distance between two vectors
    """
    return ((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 )**(0.5)

#---------------------------------------------------------------
def v_len(v):
    return dist_2D([0,0],v)

#---------------------------------------------------------------
def angle_2D(v):
    """The angle of a vector.
    """
    len_v=(v[0]**2+v[1]**2)**(0.5)
    if len_v==0:
        return 0
    ret = math.acos(v[0]/len_v)
    if v[1]<0:
        ret=6.283185307179586-ret
    return ret

#-------------------------------------------
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between_2(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793

        !!! Because of numerical malfunctions the detection is not
        always correct, that way the round() inside arccos()
            >>> np.dot(unit_vector([1,501]), unit_vector([1,501]))
            0.99999999999999989
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(round(np.dot(v1_u, v2_u),7 ))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

#-----------------------------------------------------

def angle_between(v1, v2):
    return abs(angle_2D(v1)-angle_2D(v2))
               
#---------------------------------------------------------------
def bin_search(A,x, low=0, hi=None):
    """A binary search. If x is not found, returns -1
    """
    hi = hi if hi is not None else len(A)
    pos = bisect.bisect_left(A,x,low,hi)
    return (pos if pos != hi and A[pos]==x else -1)

#---------------------------------------------------------------
def bin_search2(A,x, low=0, hi=None):
    """A binary search that always returns a position,
    even if x is not found
    """
    hi = hi if hi is not None else len(A)
    pos = bisect.bisect_left(A,x,low,hi)
    return pos

#--------------------------------------------------------------
def bin_search_2D(A, x, col, bot=0, top=None):
    """Searches for x in A[][col]. A must be sorted in an increasing order
       in the according col. If x is not in A, the position of an element
       smaller than x will be returned ( A[pos][col] <x< A[pos+1][col] )
    """
    
    top = top if top is not None else len(A)

    pos = round((bot+top)/2)
    #print(bot, pos , top)
    while bot<top-1:
        if A[pos][col]==x:
            return pos
        elif A[pos][col]>x:
            top=pos
        else:
            bot=pos
        #print(bot, pos , top)
        pos=round((bot+top)/2)

    return bot

## ------------------------------------------------------------
def polygon_vol(P):
    """returns the volume of the polygon"""
    area=0
    #first and last points must be the same
    if P==[]:
        return 0
    
    if P[0]!=P[len(P)-1]:
        P.append(P[0])

    for i in range(0,len(P)-1):
        area = area + P[i][0]*P[i+1][1]- P[i+1][0]*P[i][1]

    P.pop()
    return 0.5*area

## ------------------------------------------------------------
def set_min_dist(S1, S2):
    """S1 and S2 are sets of two-dimensional points. The functions return
       the minimum distance of each point in S1 from the points in S2.
    """
    ret =[]
    if len(S2)>len(S1):
        tmp = S1
        S1=S2
        S2=tmp
            
    for x in S1:
        min_x=((x[0]-S2[0][0])**2+(x[1]-S2[0][1])**2)**0.5
        for y in S2:
            d = ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
            if d<min_x:
                min_x = d
        ret.append(min_x)

    return ret

#------------------------------------------------------------

def len_func(polygon):
    """Returns the lengths of all the the edges of a polygon
    """
    ret=[]
    N=len(polygon)
    for i in range(1,N):
        l = ((polygon[i][0]-polygon[i-1][0])**2  + (polygon[i][1]-polygon[i-1][1])**2 )**0.5
        ret.append(l)
    l = ((polygon[0][0]-polygon[N-1][0])**2  + (polygon[0][1]-polygon[N-1][1])**2 )**0.5
    ret.append(l)
    return ret

#------------------------------------------------------------
def perimeter(polygon):
    return sum(len_func(polygon))

#------------------------------------------------------------

