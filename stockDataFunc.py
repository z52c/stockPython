import baostock as bs
from generalFunc import getTodayDate,getStockListFromBaoStock
from dbFunc import updateAdjustFactorInDB   


#更新所有复权因子
def updateAllAdjustFactor():
    stockList = getStockListFromBaoStock()
    for i in stockList:
        rs = bs.query_adjust_factor(code=i, start_date="1990-01-01", end_date=getTodayDate())
        if rs.error_code != '0':
            print('下载复权因子失败 :%s  %s' % (i, rs.error_msg))
            return
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        updateAdjustFactorInDB(data_list)
        print('更新复权因子 %s' %i)





