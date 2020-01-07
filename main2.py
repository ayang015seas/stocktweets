# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt; plt.rcdefaults()
from matplotlib import style
import matplotlib.dates as mdates

import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame
from scipy.stats import pearsonr
from numpy import cov
from statistics import mean 
import numpy as np



import pandas
import re


clean = []

dft = pandas.read_csv('tweet2.csv')
spy = pandas.read_csv('spy.csv')
# print(dft["text"])

def cleanall():
    for i in range(0, len(dft["text"]) - 1):
        if dft["text"][i][0] == 'R' and dft["text"][i][1] == 'T':
            dft.drop(dft.index[i])
            continue;
        dft.set_value(i, 'text', re.sub(r'^https?:\/\/.*[\r\n]*', '', dft["text"][i], flags=re.MULTILINE).lower()) 
        #dft["text"][i] = re.sub(r'^https?:\/\/.*[\r\n]*', '', dft["text"][i], flags=re.MULTILINE).lower()
        #print(dft["text"][i])
        #print(dft["text"][i])

chinawords = ["china", "tariff", "trade", "xi", "tariffs", "transactions", "intellectual", "deficit", "deal"]
#chinawords = ["tariff", "intellectual", "tariffs", "trade war", "china", "chinese"]
interestwords = ["rates", "rate", "inflation", "powell", "fed", "feds", "federal", "reserve", "hike", "devaluation", "quantitative", "easing", "cut", "stimulus", "recession"]
#interestwords = ["rates", "rate", "inflation", "powell", "fed", "feds", "federal", "reserve", "hike", "devaluation", "quantitative", "easing", "cut", "stimulus", "recession"]
warwords = ["war", "iran", "military", "conflict", "afghanistan", "defense", "north korea", "wars", "combat", "ceasefire", "battle", "battles", "soldier", "soldiers", "syria", "yemen", "iraq", "isis", "troops", "fighting", "combat", "army", "navy", "deploy", "deployment" "nuclear"]
#warwords = ["war", "strike", "iran"]

def china():
    cnt = 0
    
    for i in range(0, len(dft["text"]) - 1):
        #print(dft["text"][i])
        if any(word in dft["text"][i] for word in chinawords):
            cnt += 1
    print(cnt)
    return cnt


def war():
    cnt = 0
    
    for i in range(0, len(dft["text"]) - 1):
        #print(dft["text"][i])
        if any(word in dft["text"][i] for word in warwords):
            cnt += 1
    print(cnt)
    return cnt

def fed():
    cnt = 0
    
    for i in range(0, len(dft["text"]) - 1):
        #print(dft["text"][i])
        if any(word in dft["text"][i] for word in interestwords):
            cnt += 1
    print(cnt)
    return cnt

#cleanall() >>> df.loc[df.filename == 'test2.dat', 'n'] = df2[df2.filename == 'test2.dat'].loc[0]['n']
cleanall()
#interest()
china()
war()
fed()

print(len(dft))


deltas = []
diffList = []
dateList = []
tweetpairs = {}

for i in range(len(spy['Adj Close']) - 1):
    fdate = (spy["Date"][i + 1]).split("-")
    sdate = (spy["Date"][i]).split("-")
    #diff = 1
    diff = (datetime.datetime(int(fdate[0]), int(fdate[1]), int(fdate[2])) - datetime.datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]))).days
    #print("DIFF")
    #print(diff)
    #print(i)
    cdate = []
    cdate.append(fdate[1])
    cdate.append(fdate[2])
    cdate.append(fdate[0])
    #print(cdate)

    sep = "-"
    deltas.append((spy['Adj Close'][i + 1] - spy['Adj Close'][i]) / float(diff))
    diffList.append(diff)
    dateList.append(sep.join(cdate))

#print(len(dateList))
#print(len(dft["created_at"]))
index = 0
for date in dft["created_at"]:
    date_time_obj = datetime.datetime.strptime(date, '%m-%d-%Y %H:%M:%S')
    if (date[0:10] in dateList):
        #print(date[0:10])        
        if date[0:10] in tweetpairs:
            temp = tweetpairs[date[0:10]]
            temp.append(dft["text"][index])
            tweetpairs[date[0:10]] = temp
        else:
            tweetpairs[date[0:10]] = [dft["text"][index]]

    index = index + 1
    #print(date_time_obj.date())

cncore = []
incore = []
wacore = []
cmbcore = []

print(len(tweetpairs))

for key in tweetpairs:
    val = tweetpairs[key]
    #print(val)
    cncnt = 0
    incnt = 0
    wacnt = 0
    cmb = 0

    for i in range(0, len(val)):
        if any(word in val[i] for word in interestwords):
            incnt += 1
            cmb += 1
        if any(word in val[i] for word in chinawords):
            cncnt += 1
            cmb += 1
        if any(word in val[i] for word in warwords):
            wacnt += 1
            cmb += 1
    cncore.append(cncnt)
    incore.append(incnt)
    wacore.append(wacnt)
    cmbcore.append(cmb)

delta1 = []
delta2 = []
delta3 = []

cnf = []
inf = []
waf = []


cnnegdelt = []

innegdelt = []

wanegdelt = []

for i in range(len(cncore) - 1):
    if cncore[i] != 0:
        cnf.append(cncore[i])
        delta1.append(deltas[i])
    else:
        cnnegdelt.append(deltas[i])
    
for i in range(len(cncore) - 1):
    if incore[i] != 0:
        inf.append(incore[i])
        delta2.append(deltas[i])
    else:
        innegdelt.append(deltas[i])

for i in range(len(cncore) - 1):
    if wacore[i] != 0:
        waf.append(wacore[i])
        delta3.append(deltas[i])
    else:
        wanegdelt.append(deltas[i])
    
print(len(cnf))
print(len(delta1))

print(len(inf))
print(len(delta2))

print(len(waf))
print(len(delta3))

matplotlib.style.use('ggplot')

import statistics 
performance = []

plt.title('China Tweets and SPY Deltas')
plt.xlabel('Delta')
plt.ylabel('China Tweets')

plt.scatter(delta1, cnf)
plt.show()
corr1, _ = pearsonr(cnf, delta1)
cov1 = cov(delta1, cnf)
print("Covariance: " + str(cov1))
print('Pearsons correlation: %.3f' % corr1)
print("STDDEV: " + str(statistics.stdev(cnf)))
print("POSDELT: " + str(mean(delta1)))
print("NEGDELT: " + str(mean(cnnegdelt)))

performance.append(mean(delta1))
performance.append(mean(cnnegdelt))

plt.xlabel('Delta')
plt.ylabel('Federal Reserve Tweets')
plt.title('Fed Tweets and SPY Deltas')

plt.scatter(delta2, inf)
plt.show()
corr2, _ = pearsonr(delta2, inf)
cov2 = cov(delta2, inf)
print("Covariance: " + str(cov2))
print('Pearsons correlation: %.3f' % corr2)
print("STDDEV: " + str(statistics.stdev(inf)))
print("POSDELT: " + str(mean(delta2)))
print("NEGDELT: " + str(mean(innegdelt)))

performance.append(mean(delta2))
performance.append(mean(innegdelt))

plt.xlabel('Delta')
plt.ylabel('War Tweets')
plt.title('War Tweets and SPY Deltas')

plt.scatter(delta3, waf)
plt.show()
corr3, _ = pearsonr(delta3, waf)
cov3 = cov(delta3, waf)
print("Covariance: " + str(cov3))
print('Pearsons correlation: %.3f' % corr3)
print("STDDEV: " + str(statistics.stdev(waf)))
print("POSDELT: " + str(mean(delta3)))
print("NEGDELT: " + str(mean(wanegdelt)))


performance.append(mean(delta3))
performance.append(mean(wanegdelt))

datelist = []
for key in tweetpairs:
    date_time_obj = datetime.datetime.strptime(key, '%m-%d-%Y')
    datelist.append(date_time_obj)

datelistmod = mdates.date2num(datelist)

plt.title('China Tweets by Date')
plt.xlabel('Date')
plt.ylabel('China Tweets')
plt.plot_date(datelistmod, cncore, linestyle='-', marker='', color='blue')
plt.show()

plt.title('Fed Tweets by Date')
plt.xlabel('Date')
plt.ylabel('Fed Tweets')
plt.plot_date(datelistmod, incore, linestyle='-', marker='', color='blue')
plt.show()


plt.title('War Tweets by Date')
plt.xlabel('Date')
plt.ylabel('War Tweets')
plt.plot_date(datelistmod, wacore, linestyle='-', marker='', color='blue')
plt.show()


objects = ('China \n Tweets', 'No \n China \n Tweets', 'Fed \n Tweets', 'No \n Fed \n Tweets', 'War \n Tweets', 'No \n War \n Tweets')
y_pos = np.arange(len(objects))

plt.bar(y_pos, performance, align='center', alpha=0.5, color=['red', 'red', 'green', 'green', 'blue', 'blue'])

plt.xticks(y_pos, objects)
plt.ylabel('Average SPY Delta')
plt.title('Average SPY Performance')
plt(figsize=(10, 6))

plt.show()
#When does trump tweet about china 
