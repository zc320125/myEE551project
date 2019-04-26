import pandas as pd
import math
import numpy as np
from sklearn import linear_model
import csv
import random
#this function is to calculate the elo score:
def elooperator(wteam,lteam):
    wrank=elo(wteam)
    lrank=elo(lteam)
    exp=(wrank-lrank)/400
    expect=1/(1+math.pow(10,exp))
    if wrank<2100:
        k=32
    elif wrank>=2100 and wrank<2400:
        k=24
    else:
        k=16
    new_wrank=wrank+k*(1-expect)
    new_lrank=lrank-k*(0-expect)
    return new_wrank,new_lrank

def dataset(csv):
    vt=csv['Visitor']
    vts=csv['Visitor PTS']
    ht=csv['Home']
    hts=csv['Home PTS']
    #The home team always have more probability to win, so I add 100 to home team's elo score
    for i in range(len(vt)):
        if(vts[i]<hts[i]):
            wteam=ht[i]
            lteam=vt[i]
            welo=elo(wteam)+100
            lelo=elo(lteam)
        else:
            wteam=vt[i]
            lteam=ht[i]
            welo=elo(wteam)
            lelo=elo(lteam)+100
        wteam_factors=[welo]
        lteam_factors=[lelo]
        #this is to get all the statistics of a team from all data tables.
        for key, value in finalstats.loc[wteam].iteritems():
            wteam_factors.append(value)
        for key, value in finalstats.loc[lteam].iteritems():
            lteam_factors.append(value)
        #This is to get the characteristic value. I fixed half of the data set as [win Team, lose Team],
        # and the second half as [lose Team, win Team] to generate data. So the distribution of the two types of data is balanced,
        if i%2==0:
            x.append(wteam_factors + lteam_factors)
            y.append(0)
        else:
            x.append(lteam_factors + wteam_factors)
            y.append(1)
        new_wrank, new_lrank = elooperator(wteam,lteam)
        elos[wteam] = new_wrank
        elos[lteam] = new_lrank
    return x,y

def elo(team):
    try:
        return elos[team]
    except:
        elos[team]=base_elos
        return elos[team]
#Use the Logistic Distribution model to judge the outcome of a new match and return the probability of its victory.
def predict(vteam,hteam,model):
    factors=[]
    factors.append(elo(vteam))
    for key, value in finalstats.loc[vteam].iteritems():
        factors.append(value)
    factors.append(elo(hteam)+100)
    for key, value in finalstats.loc[hteam].iteritems():
        factors.append(value)
    factors=np.nan_to_num(factors)
    return model.predict_proba([factors])

base_elos = 1600
elos = {}
x=[]
y=[]
stats={}
finalstats={}
outcome=[]
num=0
tpgs=pd.read_csv('tpgs.csv')
opgs=pd.read_csv('opgs.csv')
ms=pd.read_csv('Miscellaneous.csv')
result=pd.read_csv('17-18_result.csv')
schedule=pd.read_csv("18-19_schedule.csv")
new_ms=ms.drop(['Rk','Arena','Attend.','Attend./G','Age'],axis=1)
new_opgs=opgs.drop(['Rk', 'G', 'MP'], axis=1)
new_tpgs=tpgs.drop(['Rk', 'G', 'MP'], axis=1)
stats=pd.merge(new_ms,new_opgs,on='Team')
stats=pd.merge(stats,new_tpgs,on='Team')
finalstats=stats.set_index(['Team'], inplace=False, drop=True)
x,y=dataset(result)
#This is to use Logistic Distribution model to analyze data. I checked on the Internet, most model use this method to predict data.
model=linear_model.LogisticRegression(solver='liblinear')
model.fit(x,y)
vteam=schedule['Visitor']
hteam=schedule['Home']
vteampts=schedule['Visitor PTS']
hteampts=schedule['Home PTS']
for i in range(len(vteam)):
    pred=predict(vteam[i],hteam[i],model)
    #Predict_prob returns an N-dimensional array,In the experiment, I took predict_prob[0],
    # so as to test the possibility that the sample belongs to category 1 [win Team, lose Team].
    # So when the return value is greater than 0.5, the team1 wins, and its probability is predict_prob[0]
    prob = pred[0][0]
    if vteampts[i]>hteampts[i]:
        winner=vteam[i]
    else:
        winner=hteam[i]
    if  prob>0.5:
        wteam=vteam[i]
        lteam=hteam[i]
        outcome.append([wteam,lteam,prob])
    else:
        wteam=hteam[i]
        lteam=vteam[i]
        outcome.append([wteam,lteam,1-prob])
    if winner==wteam:
        num+=1
    else:
        num=num
accuracy=num/len(vteam)
print("the predicted accuracy is:")
print(accuracy)

with open('18-19predict_result.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['win_team', 'lose_team', 'probability'])
    writer.writerows(outcome)
    print(pd.read_csv('18-19predict_result.csv',header=0))




