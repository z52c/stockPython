from dbFunc import getLastDateInDB,deleteWeeklyLastData,updateKLineData



def storeKlineData(stockCode,dataType,data):
    if dataType == 'weekly':
        deleteWeeklyLastData(stockCode)
    lastDate = getLastDateInDB(stockCode,dataType)
    dataList = []
    for i in data:
        if i['date'] > lastDate:
            dataList.append(i)
    updateKLineData(stockCode,dataList,dataType)
    
