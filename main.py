# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates

import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame



start_date = datetime.datetime(2018, 1, 1)
end_date = datetime.datetime(2019, 1, 1)

import pandas
dft = pandas.read_csv('tweet2.csv')
spy = pandas.read_csv('spy.csv')

#print(spy)
#print(spy['Volume'])


spy['Adj Close'].plot()

symbol = "SPY"
close = spy['Adj Close']
close = close.rename(columns={'close': symbol})

#plt.show()

deltas = []
deltaMax = {}
originalDeltas = []
diffList = []


for i in range(len(spy['Adj Close']) - 1):
    fdate = (spy["Date"][i + 1]).split("-")
    sdate = (spy["Date"][i]).split("-")
    diff = (datetime.datetime(int(fdate[0]), int(fdate[1]), int(fdate[2])) - datetime.datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]))).days
    print("DIFF")
    print(diff)
    #print(i)
    deltas.append((spy['Adj Close'][i + 1] - spy['Adj Close'][i]) / float(diff))
    deltaMax[(spy['Adj Close'][i + 1] - spy['Adj Close'][i]) / float(diff)] = spy['Date'][i]
    diffList.append(diff)


originalDeltas = deltas.copy()
deltas.sort()

highDelt = []
lowDelt = []
highDate = []
lowDate = []
highD = []
lowD = []

highDiff = []
lowDiff = []

ax = close.plot(title='SPY 500')

ax.set_xlabel('Date')
ax.set_ylabel('Close Price')
ax.grid()
months_fmt = mdates.DateFormatter('%M')

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month

for i in range(0, 5):
    lowDelt.append(deltas[i])
    lowDiff.append(diffList[originalDeltas.index(deltas[i])])
    
for i in range(246, 251):
    highDelt.append(deltas[i])
    highDiff.append(diffList[originalDeltas.index(deltas[i])])

#print(deltaMax[28515.449219])
#print(deltaMax)
    
for x in lowDelt:
    print("LOWDELT")
    d = originalDeltas.index(x)
    print(d)
    print(str(spy["Date"][d + 1]))
    lowD.append(d + 1)
    #lowDate.append(spy["Date"][d])
    lowDate.append(spy["Date"][d + 1])
    #highDate.append(deltas[x])
    
for x in highDelt:
    print("HIGHDELT")
    #print(x)
    d = originalDeltas.index(x)
    print(d)
    print(spy["Date"][d + 1])
    #print(type(spy["Date"][d]))
    highD.append(d + 1)
    #highDate.append(spy["Date"][d])
    highDate.append(spy["Date"][d + 1])

    #highDate.append(deltas[x])


#print(len(deltas))



#ax.xaxis.set_major_locator(months)
#ax.xaxis.set_major_formatter(months_fmt)
#ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')



for date in lowD:
    ax.axvline(date, color='r')
    #ax.axvline(datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2])))

for date in highD:
    ax.axvline(date, color='b')

ax.plot_date(x = spy['Date'], y = spy['Adj Close'], fmt="r-")


#print(dft["created_at"])

hightweets = []
lowtweets = []
highdict = {}
lowdict = {}

index = 0
for date in dft["created_at"]:
    date_time_obj = datetime.datetime.strptime(date, '%m-%d-%Y %H:%M:%S')
    
    if str(date_time_obj.date()) in highDate:
        if dft["text"][index][0] != "R" and dft["text"][index][1] != "T" or dft["text"][index][0] != "h" and dft["text"][index][1] != "t":
            hightweets.append(dft["text"][index])
            
            dstring = dft["created_at"][index][0:10]
            if dstring in highdict:
                templist = highdict.get(dstring)
                templist.append(dft["text"][index])
                highdict[dstring] = templist
            else:
                templist = []
                templist.append(dft["text"][index])
                highdict[dstring] = templist
                
        
    
    if str(date_time_obj.date()) in lowDate:
        if dft["text"][index][0] != "R" and dft["text"][index][1] != "T" or dft["text"][index][0] != "h" and dft["text"][index][1] != "t":
            lowtweets.append(dft["text"][index])
            
            dstring = dft["created_at"][index][0:10]
            if dstring in lowdict:
                templist = lowdict.get(dstring)
                templist.append(dft["text"][index])
                lowdict[dstring] = templist
            else:
                templist = []
                templist.append(dft["text"][index])
                lowdict[dstring] = templist

    index = index + 1
    #tweetdates.append()
print("HIGHTWEETS")
print(len(hightweets))
print(hightweets)

print("LOWTWEETS")
print(len(lowtweets))
print(lowtweets)

#print(highdict)
#print(lowdict)


print(highDelt)
print(highDate)
print(highDiff)

print(lowDelt)
print(lowDate)
print(lowDiff)


print("HIGH")
for key, value in highdict.items() :
    print (key)

print("LOW")
for key, value in lowdict.items() :
    print (key)
#df = pandas.Dataframe({'hightweets': hightweets, 'lowtweets': lowtweets})
#df.to_csv(index=False)
#date_time_obj = datetime.datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S.%f')


import csv
with open('tweetdata.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["TEST ROW"])
    
    writer.writerow(["HIGHDELT"])
    writer.writerow(highDelt)
    writer.writerow(["HIGHDATE"])
    writer.writerow(highDate)
    writer.writerow(["HIGHDIFF"])
    writer.writerow(highDiff)
    
    writer.writerow(["LOWDELT"])
    writer.writerow(lowDelt)
    writer.writerow(["LOWDATE"])
    writer.writerow(lowDate)
    writer.writerow(["LOWDIFF"])
    writer.writerow(lowDiff)
    
    writer.writerow(["HIGHTWEETS"])
    writer.writerow(hightweets)
    writer.writerow(["LOWTWEETS"])
    writer.writerow(lowtweets)


#print(deltas)



#print(deltaMax)
#print(deltaMax)



#print(len(spy['Date']))

#plt.plot_date(x=days, y=impressions, fmt="r-")


