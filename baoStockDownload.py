import baostock as bs
import os
from config import dbDir
from generalFunc import getTodayDate,getStockListFromBaoStock
from dbFunc import updateKLineData,updateAdjustFactorInDB


#下载一个股票的数据(baostock)
def baoStockFirstMinutesDownloadJob(baoStockCode):
    stockCode = baoStockCode[3:]
    for m in ['5','15','30','60']:
        rs = bs.query_history_k_data_plus(baoStockCode,
            "date,time,code,open,high,low,close,volume,amount",
            start_date='2006-01-01', end_date=getTodayDate(),
            frequency=m, adjustflag="3")
        print(stockCode + ' query_history_k_data_plus respond error_code:'+rs.error_code)
        print(stockCode + ' query_history_k_data_plus respond  error_msg:'+rs.error_msg)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            a = rs.get_row_data()
            dicTmp = {}
            dicTmp['date'] = a[1][0:4] + '-' + a[1][4:6] + '-' + a[1][6:8] + ' ' + a[1][8:10] + ':' + a[1][10:12]
            dicTmp['open'] = a[3]
            dicTmp['high'] = a[4]
            dicTmp['low'] = a[5]
            dicTmp['close'] = a[6]
            dicTmp['volume'] = a[7]
            dicTmp['amount'] = a[8]
            data_list.append(dicTmp)
        updateKLineData(stockCode,data_list,'min'+m)
        print('%s --- %s data finished' %(stockCode,m))


def downloadMinustesDataBaoStock(stockCode,dataType,start_date='2006-01-01',end_date=getTodayDate()):
    '''从baosStock下载指定股票的分钟级别数据

    从baoStock下载指定股票的分钟级别数据，baoStock分钟级别数据从2006-01-01开始
    (baoStock中股票代码格式一般为sh.或者sz.开头，本程序中所有股票代码都使用六位数字)

    Args: 
        stockCode: 6位的股票代码，字符串格式
        start_date: 数据开始时间，默认baostock上的第一天
        end_date: 数据结束时间,默认今天

    Returns:
        返回一个列表数据，列表中每一条为字典格式的数据
        分钟数据 ，keys ---> ['date','open','close','high','low','volume','amount']
    '''
    if stockCode[0] == '6':
        baoStockCode = 'sh.' + stockCode
    else:
        baoStockCode = 'sz.' + stockCode
    frequency = dataType[3:]
    rs = bs.query_history_k_data_plus(baoStockCode,
        "date,time,code,open,high,low,close,volume,amount",
        start_date='2006-01-01', end_date=getTodayDate(),
        frequency=frequency, adjustflag="3")
    print(stockCode + ' query_history_k_data_plus respond error_code:'+rs.error_code)
    print(stockCode + ' query_history_k_data_plus respond  error_msg:'+rs.error_msg)
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        a = rs.get_row_data()
        dicTmp = {}
        dicTmp['date'] = a[1][0:4] + '-' + a[1][4:6] + '-' + a[1][6:8] + ' ' + a[1][8:10] + ':' + a[1][10:12]
        dicTmp['open'] = a[3]
        dicTmp['high'] = a[4]
        dicTmp['low'] = a[5]
        dicTmp['close'] = a[6]
        dicTmp['volume'] = a[7]
        dicTmp['amount'] = a[8]
        data_list.append(dicTmp)
    return data_list



def downLoadAdjustFactorByStockCode(stockCode):
    '''下载指定股票的复权因子

    下载指定股票所有的复权因子

    Args: 
        stockCode: 6位的股票代码，字符串格式

    Returns:
        返回复权因子的列表 [['sz.300634', '2018-03-23', '0.996584', '1.000000', '1.000000'], ['sz.300634', '2019-06-03', '1.000000', '1.003428', '1.003428']]
        [股票代码，除权除息日期	，前复权，后复权,最后一个不要]
    '''
    if stockCode[0] == '6':
        baoStockCode = 'sh.' + stockCode
    else:
        baoStockCode = 'sz.' + stockCode
    rs = bs.query_adjust_factor(code=baoStockCode, start_date="1990-01-01", end_date=getTodayDate())
    if rs.error_code != '0':
        print('下载复权因子失败 :%s  %s' % (baoStockCode, rs.error_msg))
        return
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    return data_list


if __name__ == '__main__':
    bs.login()
    downLoadAdjustFactorByStockCode('300634')
    bs.logout()