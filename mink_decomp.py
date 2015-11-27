from aux_functions import *
from apr_2D_SS_py3_ver10 import D2_SS_approx
from scipy.spatial import ConvexHull
#import matplotlib.pyplot as plt

def process_polygon (point_List):
    #for every vertex v_i in List calculate the vector a_i=v_i-v_{i-1}
    N= len(point_List)      #the number of the input vertices
    
    U= [[0 for x in range(2)]for x in range(N)]     #the edge sequence
    E= [[0 for x in range(2)]for x in range(N)]     #primitive sequence
    d= [None]*N             #the gcd of every point in A
    #P is the input 'point_List', rename it P for brevity
    P=point_List
    L1=0  #different L approach
    

    U[0][0]=point_List[N-1][0]-point_List[0][0]
    U[0][1]=point_List[N-1][1]-point_List[0][1]
    
    for i in range(0,N+1):
        U[i%N][0] = point_List[(i+1)%N][0]-point_List[i%N][0]
        U[i%N][1] = point_List[(i+1)%N][1]-point_List[i%N][1]
        
    #U is the sequence of edges for the points of the input
    #for each pair of adjecent vertices v1(x1,y1), v2(x2,y2) the edge
    #between them is U1=(x2-x1, y2-y1) (for all 0<=i<=N)

    #create the primitive sequence
    maxD=0      #the maximum divisor
    maxE=0      #the maximum primitive edge coordinate

    for  i in range(0,N):
        d[i] = abs(gcd(U[i][0],U[i][1]))
        if d[i]==0:
            print(i,U[i][0],U[i][1]) 
        
        if d[i]>maxD:
            maxD=d[i]        

        E[i][0] = U[i][0]/d[i]
        E[i][1] = U[i][1]/d[i]
        
        if abs(E[i][0])>maxE:
            maxE=abs(E[i][0])
        if abs(E[i][1])>maxE:
            maxE=abs(E[i][1])
    #^for
    

    #print ('d =',d,'sum(d)=', sum(d))
    #now E hold the primitive sequence of edges

    #we must also create the array of all possible vectors
    #this is A[i]=k_i,j*E[i] where 0<=i<=N and
    # k_i,j is 1<=k_j<=d[i], all possible multiplicants of the primitive sequence
    A=[]
    
    #N*D time to make array A with each primitive vector d[i] times
    '''
    for i in range(0,N):
        for j in range(1,int(d[i]+1)):
            A.append([E[i][0], E[i][1]])
    '''

    for i in range(0,N):
        if d[i]==1:
            A.append([E[i][0],E[i][1]])
        elif d[i]==2:
            A.append([E[i][0],E[i][1]])
            A.append([E[i][0],E[i][1]])
        elif d[i]==3:
            A.append([E[i][0],E[i][1]])
            A.append([E[i][0]*2,E[i][1]*2])            
        else:
            k=0
            while 2**k<=d[i]/2:
                A.append([E[i][0]*2**k, E[i][1]*2**k])
                k=k+1
            if k-1>0:
                diff = d[i]-2**(k)+1
                if diff >0:
                    A.append([E[i][0]*diff, E[i][1]*diff])
    
    
    #now, A is the vector of all possible edges minus the one we removed at random
    print ('len(A)=',len(A),', A =', A)

    return A

###--------------------------------------------------------------

def mink_dec_SS_approx(polygon, e):

    Ppolygon = process_polygon(polygon)
    
    S= D2_SS_approx(Ppolygon, e)
    #the two first position are trivial solution:
    #one must be the empty vector and the other all vectors
    S.pop(0)
    #S.pop(0)

    starting_point_A=polygon[0]
    starting_point_B=[0,0]

    vector_seq_A=[]
    vector_seq_B=[]

    #print(S[0][4])
    
    for x in S[0][4]:
        vector_seq_A.append(Ppolygon[x])
    #A=S[0][4].reverse()
    S[0][4].reverse()
    for x in S[0][4]:
        Ppolygon.pop(x)
    S[0][4].reverse()
    
    vector_seq_B=Ppolygon   
            
    point_seq_A = get_polygon_points(starting_point_A, vector_seq_A)
    point_seq_B = get_polygon_points(starting_point_B, vector_seq_B)

    print("summandA=",point_seq_A,"\nsummandB=",point_seq_B)
    nA=len(point_seq_A)
    nB=len(point_seq_B)
    gapA=((point_seq_A[0][0]-point_seq_A[nA-1][0])**2 + (point_seq_A[nA-1][1]-point_seq_A[0][1])**2)**(0.5)
    gapB=((point_seq_B[0][0]-point_seq_B[nB-1][0])**2 + (point_seq_B[nB-1][1]-point_seq_B[0][1])**2)**(0.5)
    print("- gap=",gapA)
    
    return point_seq_A, point_seq_B

## -----------------------------------------------------------


P=[ [random.randint(0,50),random.randint(0,70)] for i in range(0,30)]
Ph=ConvexHull(P)
Pp=[]
for x in Ph.vertices:
    Pp.append([Ph.points[x][0], Ph.points[x][1]])
#P=[[24,59],[60,90],[83,67],[88,47],[98,21],[48,7],[30,14]]
print("input polygon=",Pp,", number of vertices=", len(Pp))

#P=[ (2, 0), (1, 1), (0, 3),  (11, 1), (10, 0)]

t = time.process_time() 
A,B= mink_dec_SS_approx(Pp,0.1)

C=[]
for a in A:
    for b in B:
        C.append([a[0]+b[0], a[1]+b[1]])

Ch=ConvexHull(C)
Ch2=[]
for x in Ch.vertices:
    Ch2.append([Ch.points[x][0], Ch.points[x][1]])

print("- points of approx:",Ch2,", #vertices:",len(Ch2))
Pvol=polygon_vol(Pp)
Cvol=polygon_vol(Ch2)
#print("input volume=",Pvol ,"approx volume=", Cvol)
print("- vol(P)/vol(C)=",Pvol/Cvol)
print("- perimeter: input =",perimeter(Pp),"approx=",perimeter(Ch2))
print("- vertices difference=",set_min_dist(Pp, Ch2))

elap_t = time.process_time() - t
print("time elapsed=",elap_t)   
    
