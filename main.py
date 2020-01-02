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


for i in range(len(spy['Adj Close']) - 1):
    fdate = (spy["Date"][i + 1]).split("-")
    sdate = (spy["Date"][i]).split("-")
    diff = (datetime.datetime(int(fdate[0]), int(fdate[1]), int(fdate[2])) - datetime.datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]))).days
    
    #print(diff)
    #print(i)
    deltas.append((spy['Adj Close'][i + 1] - spy['Adj Close'][i]) / float(diff))
    deltaMax[spy['Adj Close'][i + 1] - spy['Adj Close'][i]] = spy['Date'][i]


originalDeltas = deltas.copy()
deltas.sort()

highDelt = []
lowDelt = []
highDate = []
lowDate = []
highD = []
lowD = []

ax = close.plot(title='SPY 500')

ax.set_xlabel('Date')
ax.set_ylabel('Close Price')
ax.grid()
months_fmt = mdates.DateFormatter('%M')

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month

for i in range(0, 5):
    lowDelt.append(deltas[i])
    
for i in range(246, 251):
    highDelt.append(deltas[i])

#print(deltaMax[28515.449219])
#print(deltaMax)
    
for x in lowDelt:
    print("LOWDELT")
    d = originalDeltas.index(x)
    print(d)
    print(str(spy["Date"][d]))
    lowD.append(d)
    lowDate.append(spy["Date"][d])
    lowDate.append(spy["Date"][d + 1])
    #highDate.append(deltas[x])
    
for x in highDelt:
    print("HIGHDELT")
    #print(x)
    d = originalDeltas.index(x)
    print(d)
    print(spy["Date"][d])
    print(type(spy["Date"][d]))
    highD.append(d)
    highDate.append(spy["Date"][d])
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

index = 0
for date in dft["created_at"]:
    date_time_obj = datetime.datetime.strptime(date, '%m-%d-%Y %H:%M:%S')
    
    if str(date_time_obj.date()) in highDate:
        if dft["text"][index][0] != "R" and dft["text"][index][1] != "T":
            hightweets.append(dft["text"][index])
        
    
    if str(date_time_obj.date()) in lowDate:
        if dft["text"][index][0] != "R" and dft["text"][index][1] != "T":
            lowtweets.append(dft["text"][index])

    index = index + 1
    #tweetdates.append()
print("HIGHTWEETS")
print(len(hightweets))
print(hightweets)

print("LOWTWEETS")
print(len(lowtweets))
print(lowtweets)


#date_time_obj = datetime.datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S.%f')





#print(deltas)



#print(deltaMax)
#print(deltaMax)



#print(len(spy['Date']))

#plt.plot_date(x=days, y=impressions, fmt="r-")


