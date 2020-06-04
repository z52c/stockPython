import os
import baostock as bs
import threading
from config import dbDir
from generalFunc import getTodayDate,getStockListFromBaoStock,getStockListFromFile
from dbFunc import updateKLineData,getLastDateInDB
from emdownload import downloadKLineDataEM
from storeFunc import storeKlineData


threadLock = threading.Lock()
stockList = []


def updateTodayMin1Data(stockCode):
    data = downloadKLineDataEM(stockCode,'min1')
    storeKlineData(stockCode,'min1',data)



def updateMinutesData(stockCode):
    minutesList = ['min5','min15','min30','min60']
    for i in minutesList:
        data = downloadKLineDataEM(stockCode,i)
        storeKlineData(stockCode,i,data)



def updateDailyData(stockCode):
    data = downloadKLineDataEM(stockCode,'daily')
    storeKlineData(stockCode,'daily',data)


def updateWeeklyData(stockCode):
    data = downloadKLineDataEM(stockCode,'weekly')
    storeKlineData(stockCode,'weekly',data)


#每日更新操作,更新分钟级别数据以及日线数据,周线数据放在周末更新
def dailyUpdateWork(stockCode):
    updateTodayMin1Data(stockCode)
    updateMinutesData(stockCode)
    updateDailyData(stockCode)





#stockThread中调用，默认type=1，日更新，type=2，则为周更新
def perStockJob(threadName,updateType=1):
    global stockList
    threadLock.acquire()
    while(len(stockList) > 0):
        stockCode = stockList.pop()
        threadLock.release()
        print(stockCode)
        if updateType == 1:
            dailyUpdateWork(stockCode)
        else:
            updateWeeklyData(stockCode)
        threadLock.acquire()
    threadLock.release()


class stockThread (threading.Thread):
    def __init__(self, threadID, name,updateType=1):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.updateType = updateType
    def run(self):
        print ("开启stock线程： " + self.name)
        perStockJob(self.name,self.updateType)
        print ("结束stock线程： " + self.name)


#默认type=1，日更新，type=2，则为周更新
def updateData(updateType=1):
    th=[]
    global stockList
    print('准备获取股票列表')
    stockList = getStockListFromBaoStock()
    print('获取股票列表结束')
    for i in range(15):
        t = stockThread(i, "Thread-%d" %i,updateType)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    print('结束')


if __name__ == '__main__':
    bs.login()
    updateData(1)
    bs.logout()