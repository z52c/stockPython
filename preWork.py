import os
import baostock as bs
import threading
from config import dbDir
from generalFunc import getTodayDate,getStockListFromBaoStock
from dbFunc import updateKLineData,updateAdjustFactorInDB
from emdownload import downloadKLineDataEM
from baoStockDownload import downloadMinustesDataBaoStock,downLoadAdjustFactorByStockCode


threadLock = threading.Lock()
stockList = []


def downloadEMDayWeekData(stockCode):
    '''从东方财富下载日/周数据，直接插入数据库中

    由于是第一次使用，所以下载全部数据，直接插入
    '''
    data = downloadKLineDataEM(stockCode,'daily')
    print('%s daily data downloaded' % stockCode)
    updateKLineData(stockCode,data,'daily')
    data = downloadKLineDataEM(stockCode,'weekly')
    print('%s weekly data downloaded' % stockCode)
    updateKLineData(stockCode,data,'weekly')


def perStockJob(threadName):
    global stockList
    threadLock.acquire()
    while(len(stockList) > 0):
        stockCode = stockList.pop()
        threadLock.release()
        print(stockCode)
        downloadEMDayWeekData(stockCode)
        threadLock.acquire()
    threadLock.release()


class stockThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("开启stock线程： " + self.name)
        perStockJob(self.name)
        print ("结束stock线程： " + self.name)

def preDownloadEMDayWeekData():
    th=[]
    global stockList
    print('准备获取股票列表')
    stockList = getStockListFromBaoStock()
    print('获取股票列表结束')
    for i in range(15):
        t = stockThread(i, "Thread-%d" %i)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    print('结束')


def makeStockListFile():
    stockList = getStockListFromBaoStock()
    with open('stocklist','w') as f:
        f.write(str(stockList))


    


def preDownloadMinutesBaoStock():
    stockList = getStockListFromBaoStock(getTodayDate())
    downloadedList = os.listdir(dbDir)
    for i in stockList:
        if i+'.db' not in downloadedList:
            for m in ['min5','min15','min30','min60']:
                data = downloadMinustesDataBaoStock(i,m)
                updateKLineData(i,data,m)
                print('%s --- %s data finished' %(i,m))


def preDownloadAdjustFactor():
    stockList = getStockListFromBaoStock(getTodayDate())
    for i in stockList:
        data = downLoadAdjustFactorByStockCode(i)
        updateAdjustFactorInDB(data)


def preDownloadWork():
    '''初始使用，下载数据

    先下载baostock中的分钟级别数据，然后使用多线程下载东方财富的日/周数据,最后下载复权因子
    '''
    preDownloadMinutesBaoStock()
    preDownloadEMDayWeekData()
    preDownloadAdjustFactor()


def tmpDownloadNewStock(stockList):
    '''下载新股

    使用过程报告的复权因子不存在的新股，下载数据
    '''
    for i in stockList:
        '''
        for m in ['min5','min15','min30','min60']:
            data = downloadMinustesDataBaoStock(i,m)
            updateKLineData(i,data,m)
            print('%s --- %s data finished' %(i,m))
        data = downloadKLineDataEM(i,'daily')
        print('%s daily data downloaded' % i)
        updateKLineData(i,data,'daily')
        data = downloadKLineDataEM(i,'weekly')
        print('%s weekly data downloaded' % i)
        updateKLineData(i,data,'weekly')  
        '''
        data = downLoadAdjustFactorByStockCode(i)
        updateAdjustFactorInDB(data)
        print('%s 复权因子已更新'%i)





if __name__ == '__main__':
    bs.login()
    #preDownloadEMDayWeekData()

    bs.logout()