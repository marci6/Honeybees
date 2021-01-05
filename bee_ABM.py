import numpy as np
import matplotlib.pyplot as plt

class bee_class:
  def __init__(self):
    self.s=0 # nest advertised
    self.d=0 # dance duration
    self.oriented=1 # orientation correct
       
def find_nest(hive,apriori_prob,l,beta,k):
  prob=np.zeros(k)
  # for each possible site
  for i in range(1,k):
    f=0
    # count portion of bees dancing for site i
    for bee in hive:
      if bee.s==i and bee.oriented==1:
        f+=1
    f=f/len(hive)
    prob[i]=(1-l)*apriori_prob[i]+l*f
  prob[0]=1-np.sum(prob[1:])
  return prob
        
#def quorum(hive,k):
#  site_votes=np.zeros(k)
#  for bee in hive:
#    if bee.s!=0 and bee.oriented==1:
#      site_votes[bee.s]+=1
#  sort_votes=np.sort(site_votes)
#  if site_votes[0]>0.8*len(hive):
#    return 0,0
#  if sort_votes[-1]>2*sort_votes[-2] and sort_votes[-2]!=0:
#    return 1,np.argmax(site_votes)
#  return 0,0
  
def quorum(hive,k):
  site_votes=np.zeros(k)
  #count votes for each site
  for bee in hive:
    if bee.oriented==1:
      site_votes[bee.s]+=1
  first= np.argsort(site_votes)[-1]
  second= np.argsort(site_votes)[-2]
  if site_votes[first]>2*site_votes[second] and second!=0 and site_votes[0]<0.8*len(hive) and first!=0:
    return 1,first
  return 0,0

def simulate(N,k,q,tmax,apriori_prob,beta,l,sigma):
  # initialize hive
  hive = []
  T_quorum=0
  Dancing=np.zeros(tmax)
  for b in range(N):
    hive.append(bee_class())
    if np.random.rand()>beta:
        hive[-1].oriented=0
  # simulate each time step
  for t in range(tmax):
    # simulate each bee
    for bee in hive:
      prob=find_nest(hive,apriori_prob,l,beta,k) # compute probability of finding each nest
      if bee.s==0: # bee is at the original nest
        bee.s=np.random.choice(np.arange(0,k,1),p=prob)
        bee.d=q[int(bee.s)]*np.exp(np.random.randn()*sigma)
      else:
        if bee.d>1:
          bee.d-=1
        else:
          bee.d=0
          bee.s=0
    for bee in hive:
        if bee.s!=0:
            Dancing[t]+=1
    flag,nest=quorum(hive,k) # check if quorum is reached
    if flag:
        T_quorum=t
        return nest,T_quorum,sum(Dancing)
  return 0,tmax,sum(Dancing)


# Scenario parameters
Test=100
N=200 #number of bees
k=6 # number of sites
q=[0,1,3,4,6,8] #quality of the nests
tmax=300 #number of simulated steps
apriori_prob=np.array([0.5,0.1,0.1,0.1,0.1,0.1])
l=0.2
sigma=0.2
betav=np.arange(0,1.2,0.2)

nest_choice=np.zeros((Test,6)) # each row is a test, each col is a value of beta
time_quorum=np.zeros((Test,6)) # each row is a test, each col is a value of beta
dancing_n=np.zeros((Test,6)) # each row is a test, each col is a value of beta
# Simulate
for i,beta in enumerate(betav):
    print('Beta:',beta)
    for rep in range(Test):
        choice,time,dancing_sum=simulate(N,k,q,tmax,apriori_prob,beta,l,sigma)
        if choice == 5:
            nest_choice[rep,i]=1
        else:
            nest_choice[rep,i]=0
        time_quorum[rep,i]=time
        dancing_n[rep,i]=dancing_sum
 
# Analysis    
avg_time_quorum=np.zeros(6) # Average time to reach quorum for each value of beta
std_time_quorum=np.zeros(6) # Standard deviation time to reach quorum for each value of beta
avg_tot_dancing=np.zeros(6) # Average total number of waggle dance for each value of beta
std_tot_dancing=np.zeros(6) # Average total number of waggle dance for each value of beta
correct=np.zeros(6) # Percentage of correct choices for each value of beta

for i in range(6):
   avg_time_quorum[i]=np.mean(time_quorum[:,i]) 
   std_time_quorum[i]=np.std(time_quorum[:,i]) 
plt.figure()
plt.errorbar(betav,avg_time_quorum,yerr=std_time_quorum,c='black')
plt.grid()
plt.xlabel('Beta value')
plt.ylabel('Time')
plt.title('Average time to reach quorum')

for i in range(6):
   avg_tot_dancing[i]=np.mean(dancing_n[:,i]) 
   std_tot_dancing[i]=np.std(dancing_n[:,i]) 
plt.figure()
plt.errorbar(betav,avg_tot_dancing,yerr=std_tot_dancing,c='black')
plt.grid()
plt.xlabel('Beta value')
plt.title('Average number of dances')

for i in range(6):
   correct[i]=np.sum(nest_choice[:,i])/Test*100 

plt.figure()
plt.plot(betav,correct,c='black')
plt.scatter(betav,correct,c='black',marker='x')
plt.grid()
plt.ylim(0,100)
plt.xlabel('Beta value')
plt.ylabel('Percentage')
plt.title('Percentage of correct choices')
