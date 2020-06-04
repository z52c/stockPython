from urllib import request
import time


def downloadData(url):
    '''下载并返回内容

    下载东方财富数据时调用，由于某种原因下载过程可能会出现异常，出现异常后等待2秒再调用自身

    Args:
        url: 需要下载的链接内容

    Return: 返回下载的内容
    '''
    try:
        response = request.urlopen(url)
        result = str(response.read())
        return result
    except:
        print('%s 下载报错,等待2秒' % url)
        time.sleep(2)
        return downloadData(url)



def downloadMin1StockKLineDataEM(stockCode,ndays=1):
    '''下载分时数据

    下载指定股票的一分钟数据，默认下载最近一天的数据，如果是在盘中会下载当日开盘到当前时刻的数据
    只用于被downloadKLineData调用

    Args: 
        stockCode: 6位的股票代码，字符串格式
        ndays: 要下载的分时数据天数，默认当天，最大五天

    Returns:
        返回一个列表数据，列表中每一条为字典格式的数据，每一分钟一条，keys ---> ['date','open','close','high','low','volume','amount','matoday']
    '''
    t = time.time()
    if stockCode[0] == '6':
        secid = '1.' + stockCode
    else:
        secid = '0.' + stockCode
    url = 'http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&ndays=1&iscr=0&cb=jQuery112408200867504629754_1589004986222&_=' + str(round(t * 1000)) + '&secid='
    url = url + secid
    result = downloadData(url)
    leftIndex = result.find('[')
    rightIndex = result.find(']')
    strRtn = result[leftIndex:rightIndex+1]
    #tmpList 一个由字符串组成的列表，每条字符串为一个数据
    tmpList = eval(strRtn)
    kLineTitle = ['date','open','close','high','low','volume','amount','matoday']
    rtn = []  
    for i in tmpList:
        tmpDic = {}
        item = i.split(',')
        index = 0
        for m in item:
            tmpDic[kLineTitle[index]] = m
            index += 1
        rtn.append(tmpDic)
    return rtn



def downloadKLineDataEM(stockCode,dataType,lmt=0):
    '''下载指定股票指定类型的数据

    下载股票指定类型的数据，如5分钟数据，其中一分钟数据调用downloadMin1StockKLineData，如lmt参数不设置则下载所有

    Args:
        stockCode: 6位的股票代码，字符串格式
        dataType: 要下载的类型  'min1' 'min5' 'min15' 'min30' 'min60' 'daily' 'weekly'
        lmt: 规定下载的数据数量，不指定则默认下载所有(其中分钟级别数据只能下载最近两月左右,对于一分钟数据本参数无效)

    Returns:
        返回一个列表数据，列表中每一条为字典格式的数据
        一分钟数据 ，keys ---> ['date','open','close','high','low','volume','amount','matoday']
        其他分钟数据 ，keys ---> ['date','open','close','high','low','volume','amount']
        日/周数据 ，keys ---> ['date','open','close','high','low','volume','amount','amplitude','pchg','chg','turnover']
    '''
    if dataType == 'min1':
        return downloadMin1StockKLineDataEM(stockCode,5)
    t = time.time()
    if stockCode[0] == '6':
        secid = '1.' + stockCode
    else:
        secid = '0.' + stockCode
    if lmt == 0:
        lmt = 1000000

    if dataType == 'min5':
        url = 'http://65.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112408200867504629754_1589004986226&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=5&fqt=0&end=20500101&_=' + str(round(t * 1000)) + '&lmt=' + str(lmt) +'&secid='
    elif dataType == 'min15':
        url = 'http://40.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112408200867504629754_1589004986218&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=15&fqt=0&end=20500101&_=' + str(round(t * 1000)) + '&lmt=' + str(lmt) + '&secid='
    elif dataType == 'min30':
        url = 'http://79.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112408200867504629754_1589004986218&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=30&fqt=0&end=20500101&_=' + str(round(t * 1000)) + '&lmt=' + str(lmt) + '&secid='
    elif dataType == 'min60':
        url = 'http://98.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112408200867504629754_1589004986218&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=60&fqt=0&end=20500101&_=' + str(round(t * 1000)) + '&lmt=' + str(lmt) + '&secid='
    elif dataType == 'daily':
        url = 'http://15.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124013061790954540276_1589003050868&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&beg=0&end=20500101&smplmt=20000&_=' + str(round(t * 1000)) + '&lmt=' + str(lmt) + '&secid='
    elif dataType == 'weekly':
        url = 'http://1.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112406625071576325758_1588982718245&&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=102&fqt=0&end=20500101&_=' + str(round(t * 1000)) + '&lmt=' + str(lmt) + '&secid='    
    url = url + secid
    result = downloadData(url)
    leftIndex = result.find('[')
    rightIndex = result.find(']')
    strRtn = result[leftIndex:rightIndex+1]
    #tmpList 一个由字符串组成的列表，每条字符串为一个数据
    tmpList = eval(strRtn)
    kLineTitle = ['date','open','close','high','low','volume','amount','amplitude','pchg','chg','turnover']
    rtn = []  
    for i in tmpList:
        tmpDic = {}
        item = i.split(',')
        index = 0
        for m in item:
            tmpDic[kLineTitle[index]] = m
            index += 1
        if 'min' in dataType:
            del tmpDic['amplitude']
            del tmpDic['pchg']
            del tmpDic['chg']
            del tmpDic['turnover']
        rtn.append(tmpDic)
    return rtn


if __name__ == '__main__':
    pass