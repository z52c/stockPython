import time
import baostock as bs


#返回今天的日期，格式 2020-05-21
def getTodayDate():
    return time.strftime("%Y-%m-%d", time.localtime())


def getStockListFromFile():
    with open('stocklist','r') as f:
        tmp = f.read()
        return eval(tmp)


#返回列表所有数据的平均值,用于计算均线数据
def getAverangeOfList(listIn):
    sum_ = 0.0
    count = len(listIn)
    zeroCount = 0
    for i in listIn:
        if i == 0.0:
            zeroCount += 1
        sum_ += i
    return format(sum_ / (count-zeroCount),'.2f')


#从指定日期返回最近一个交易日（如果参数是今天，则返回前一个交易日，今日不算）
def getLatestTradeDay(inDate):
    tmp = inDate.split('-')
    if tmp[1] == '01':
        date1 = str(int(tmp[0])-1) + '-12-' + tmp[2]
    else:
        month = int(tmp[1])-1
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        date1 = tmp[0] + '-' + month + '-' + tmp[2]
    rs = bs.query_trade_dates(start_date=date1, end_date=inDate)
    if rs.error_code != '0':
        print('从指定日期返回最近一个交易日: %s' % rs.error_msg)
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    data_list.pop()
    data_list.reverse()
    for i in data_list:
        if i[1] == '1':
            return i[0]



#从baostock中返回指定日期股票列表，去除停牌的,返回6位数字字符的列表，默认今天
def getStockListFromBaoStock(inDate=getTodayDate()):
    rs = bs.query_all_stock(getLatestTradeDay(inDate))
    if rs.error_code != '0':
        print('获取股票列表失败 : %s' % rs.error_msg)
        return
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    rtnList = []
    for i in data_list:
        if i[1] != '1' or 'sh.00' in i[0] or 'sz.39' in i[0]:
            continue
        rtnList.append(i[0][3:])
    return rtnList




if __name__ == '__main__':
    bs.login()
    print(getLatestTradeDay(getTodayDate()))
    bs.logout()
