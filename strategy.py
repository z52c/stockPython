from generalFunc import getStockListFromFile
from dbFunc import getKLineDataWithMACDInDB
import math
import threading

threadLock = threading.Lock()
#stockList = []

#判断当前是否金叉且开口向上
def jinchaAndOpenUp(stockCode,dataType,length=80):
    a = getKLineDataWithMACDInDB(stockCode,dataType)
    if len(a) == 0:
        print('%s 空数据' %stockCode)
    if len(a) < length:
        return False
    z = a.pop()
    y = a.pop()
    zmacd = z['dif'] - z['dea']
    if z['dif'] > z['dea'] and zmacd > y['dif'] - y['dea'] and zmacd > 0.2:
        return True
    else:
        return False


def jijiangJincha(stockCode,dataType):
    a = getKLineDataWithMACDInDB(stockCode,dataType)
    z = a.pop()
    y = a.pop()
    if z['dif'] < z['dea'] and z['dif'] - z['dea'] > y['dif'] - y['dea'] and abs(z['dif'] - z['dea']) < 0.5:
        return True
    else:
        return False



def perStockJob(threadName):
    global stockList
    threadLock.acquire()
    while(len(stockList) > 0):
        stockCode = stockList.pop()
        threadLock.release()
        if jinchaAndOpenUp(stockCode,'weekly') and jijiangJincha(stockCode,'min60'):
            print(stockCode)
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

    



if __name__ == '__main__':
    th=[]
    global stockList
    print('准备获取股票列表')
    stockList = getStockListFromFile()
    print('获取股票列表结束')
    for i in range(15):
        t = stockThread(i, "Thread-%d" %i)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    print('结束')
