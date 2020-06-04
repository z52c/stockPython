import sqlite3
import os
from config import *
from generalFunc import getAverangeOfList


def tmpUse(stockCode):
    sqlStr1 = 'DELETE FROM min30 WHERE date > "2020-05-19"'
    sqlStr2 = 'DELETE FROM min60 WHERE date > "2020-05-19"'
    dbFileName = dbDir + stockCode + '.db'
    if not os.path.exists(dbFileName):
        return
    conn = sqlite3.connect(dbFileName)
    c = conn.cursor()
    c.execute(sqlStr1)
    conn.commit()
    c.execute(sqlStr2)
    conn.commit()
    conn.close()



#如果周数据最后一条存在，则删除最后一条，防止不完整的周数据存在
def deleteWeeklyLastData(stockCode):
    lastDate = getLastDateInDB(stockCode,'weekly')
    if lastDate == '':
        return
    dbFileName = dbDir + stockCode + '.db'
    conn = sqlite3.connect(dbFileName)
    c = conn.cursor()
    c.execute('DELETE FROM weekly WHERE date = "%s"' %lastDate)
    conn.commit()
    conn.close()




#表名开头带sh和sz，例如sh600000
def updateAdjustFactorInDB(data):
    stockCode = data[0][0]
    stockCode = stockCode.replace('.','')
    dbFile = dbDir + 'adjustfactor.db'
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    sqlStr = 'CREATE TABLE %s (dividOperateDate TEXT,foreAdjustFactor TEXT,backAdjustFactor TEXT);' % stockCode
    try:
        c.execute(sqlStr)
        conn.commit()
    except:
        pass
    sqlStr = 'select * from %s' % stockCode
    cursor = c.execute(sqlStr)
    dateList = []
    for i in cursor:
        dateList.append(i[0])
    for i in data:
        if i[1] not in dateList:
            sqlStr = 'INSERT INTO %s VALUES ("%s","%s","%s")' % (stockCode, i[1], i[2], i[3])
            c.execute(sqlStr)
    conn.commit()
    conn.close()


#返回所有数据，前复权
def getKLineDataInDB(stockCode,dataType):
    rtnList = []
    dbFileName = dbDir + stockCode + '.db'
    if not os.path.exists(dbFileName):  #如果数据库文件不存在，则创建数据库文件
        createDBFileByStockCode(stockCode)
    if stockCode[0] == '6':
        tmpCode = 'sh' + stockCode
    else:
        tmpCode = 'sz' + stockCode
    conn = sqlite3.connect(dbDir + adjustfactorFile)
    c = conn.cursor()
    try:
        cursor = c.execute("SELECT *  from %s" %tmpCode)
        adjustFactorList = cursor.fetchall()
    except:
        print('%s 复权因子不存在' %stockCode)
        return rtnList

    conn = sqlite3.connect(dbFileName)
    c = conn.cursor()
    cursor = c.execute("SELECT *  from %s" %dataType)
    resultList = cursor.fetchall()
    

    if dataType == 'min1':
        for i in resultList:
            flag = False
            for m in adjustFactorList:
                if i[0] < m[0]:
                    k = float(m[1])
                    flag = True
                    break
            if not flag:
                k = 1.0
            tmpDic = {}
            tmpDic['date'] = i[0]
            tmpDic['open'] = float(i[1]) * k
            tmpDic['close'] = float(i[2]) * k
            tmpDic['high'] = float(i[3]) * k
            tmpDic['low'] = float(i[4]) * k
            tmpDic['volume'] = int(i[5])
            tmpDic['amount'] = float(i[6])
            tmpDic['matoday'] = float(i[7]) * k
            rtnList.append(tmpDic)
        return rtnList
    elif 'min' in dataType:
        for i in resultList:
            flag = False
            for m in adjustFactorList:
                if i[0] < m[0]:
                    k = float(m[1])
                    flag = True
                    break
            if not flag:
                k = 1.0
            tmpDic = {}
            tmpDic['date'] = i[0]
            tmpDic['open'] = float(i[1]) * k
            tmpDic['close'] = float(i[2]) * k
            tmpDic['high'] = float(i[3]) * k
            tmpDic['low'] = float(i[4]) * k
            tmpDic['volume'] = int(i[5])
            tmpDic['amount'] = float(i[6])
            rtnList.append(tmpDic)
        return rtnList
    else:
        for i in resultList:
            flag = False
            for m in adjustFactorList:
                if i[0] < m[0]:
                    k = float(m[1])
                    flag = True
                    break
            if not flag:
                k = 1.0
            tmpDic = {}
            tmpDic['date'] = i[0]
            tmpDic['open'] = float(i[1]) * k
            tmpDic['close'] = float(i[2]) * k
            tmpDic['high'] = float(i[3]) * k
            tmpDic['low'] = float(i[4]) * k
            tmpDic['volume'] = int(i[5])
            tmpDic['amount'] = float(i[6])
            tmpDic['amplitude'] = float(i[7])
            tmpDic['pchg'] = float(i[8])
            tmpDic['chg'] = float(i[9])
            tmpDic['turnover'] = float(i[10])
            rtnList.append(tmpDic)
        return rtnList


#返回数据中最后一个日期
def getLastDateInDB(stockCode,dataType):
    dbFileName = dbDir + stockCode + '.db'
    if not os.path.exists(dbFileName):  #如果数据库文件不存在，则创建数据库文件
        createDBFileByStockCode(stockCode)
    conn = sqlite3.connect(dbFileName)
    c = conn.cursor()
    cursor = c.execute("SELECT date  from %s" %dataType)
    resultList = cursor.fetchall()
    if len(resultList) == 0:
        return ''
    return resultList[-1][0]


#返回带macd的数据
def getKLineDataWithMACDInDB(stockCode,dataType):
    klineList = getKLineDataInDB(stockCode,dataType)
    ema12 = 0.0
    ema26 = 0.0
    dif = 0.0
    dea = 0.0
    macd = 0.0
    rtn = []
    for i in klineList:
        closePrice = float(i['close'])
        ema12 = ema12*11/13 + closePrice*2/13
        ema26 = ema26*25/27 + closePrice*2/27
        dif = ema12 - ema26
        dea = dea*8/10 + dif*2/10
        i['ema12'] = ema12
        i['ema26'] = ema26
        i['dif'] = dif
        i['dea'] = dea
        rtn.append(i)
    return rtn   


#返回带macd和均线的数据
def getKLineDataWithMACDMAInDB(stockCode,dataType):
    klineList = getKLineDataInDB(stockCode,dataType)
    ema12 = 0.0
    ema26 = 0.0
    dif = 0.0
    dea = 0.0
    ma = {}
    ma['ma5'] = 0.0
    ma['ma10'] = 0.0
    ma['ma20'] = 0.0
    ma['ma30'] = 0.0
    ma['ma60'] = 0.0
    ma['ma120'] = 0.0
    ma['ma250'] = 0.0
    listDic = {}
    listDic['ma5'] = [0.0] * 5
    listDic['ma10'] = [0.0] * 10
    listDic['ma20'] = [0.0] * 20
    listDic['ma30'] = [0.0] * 30
    listDic['ma60'] = [0.0] * 60
    listDic['ma120'] = [0.0] * 120
    listDic['ma250'] = [0.0] * 250
    rtn = []
    for i in klineList:
        closePrice = float(i['close'])
        ema12 = ema12*11/13 + closePrice*2/13
        ema26 = ema26*25/27 + closePrice*2/27
        dif = ema12 - ema26
        dea = dea*8/10 + dif*2/10
        i['ema12'] = ema12
        i['ema26'] = ema26
        i['dif'] = dif
        i['dea'] = dea
        for m in listDic:
            del listDic[m][0]
            listDic[m].append(closePrice)
            i[m] = str(getAverangeOfList(listDic[m]))
        rtn.append(i)
    return rtn         
    

#更新k线数据，将所有数据导入数据库，在调用之前处理去重等操作
def updateKLineData(stockCode,data,dataType):
    dbFileName = dbDir + stockCode + '.db'
    if not os.path.exists(dbFileName):  #如果数据库文件不存在，则创建数据库文件
        createDBFileByStockCode(stockCode)
    if dataType == 'min1':
        conn = sqlite3.connect(dbFileName)
        c = conn.cursor()
        for i in data:
            sqlStr = 'INSERT INTO %s VALUES("%s", "%s","%s","%s","%s","%s","%s","%s")' %(dataType,i['date'],i['open'],i['close'],i['high'],i['low'],i['volume'],i['amount'],i['matoday']) 
            c.execute(sqlStr)
        conn.commit()   
        conn.close() 
    elif 'min' in dataType:
        conn = sqlite3.connect(dbFileName)
        c = conn.cursor()
        for i in data:
            sqlStr = 'INSERT INTO %s VALUES("%s", "%s","%s","%s","%s","%s","%s")' %(dataType,i['date'],i['open'],i['close'],i['high'],i['low'],i['volume'],i['amount']) 
            c.execute(sqlStr)
        conn.commit()   
        conn.close() 
    else:
        conn = sqlite3.connect(dbFileName)
        c = conn.cursor()
        for i in data:
            sqlStr = 'INSERT INTO %s VALUES("%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %(dataType,i['date'],i['open'],i['close'],i['high'],i['low'],i['volume'],i['amount'],i['amplitude'],i['pchg'],i['chg'],i['turnover']) 
            c.execute(sqlStr)
        conn.commit()   
        conn.close() 


#创建对应股票的数据库文件，并生成表
def createDBFileByStockCode(stockCode):
    dbFile = dbDir + stockCode + '.db'
    tableMinutesList = ['min5', 'min15', 'min30', 'min60']
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    sqlStr = 'CREATE TABLE daily (' + dbTableFieldDayWeek +');'
    c.execute(sqlStr)
    conn.commit()
    sqlStr = 'CREATE TABLE weekly (' + dbTableFieldDayWeek +');'
    c.execute(sqlStr)
    conn.commit()
    for i in tableMinutesList:
        sqlStr = 'CREATE TABLE ' + i + ' (' + dbTableFieldminutes +');'
        c.execute(sqlStr)
        conn.commit()
    sqlStr = 'CREATE TABLE ' + 'min1' + ' (' + dbTableFieldmin1 +');'
    c.execute(sqlStr)
    conn.commit()    
    print(stockCode + 'db table created!')
    conn.close()






if __name__ == '__main__':
    a = getKLineDataWithMACDInDB('300651','min60')
    print(a.pop())
    print(a.pop())