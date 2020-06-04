
dbDir = 'E://stockdb/'
adjustfactorFile = 'adjustfactor.db'

#dbTableField = 'date char(16) PRIMARY KEY,open REAL,close REAL,high REAL,low REAL,volume INTEGER,amount REAL,pchg REAL,chg REAL,turnover REAL,ema12 REAL,ema26 REAL,dif REAL,dea REAL,ma5 REAL,ma10 REAL,ma20 REAL,ma30 REAL,ma60 REAL,ma120 REAL,ma250 REAL'
dbTableFieldDayWeek = 'date char(16) PRIMARY KEY,open TEXT,close TEXT,high TEXT,low TEXT,volume TEXT,amount TEXT,amplitude TEXT,pchg TEXT,chg TEXT,turnover TEXT'
dbTableFieldmin1 = 'date char(16) PRIMARY KEY,open TEXT,close TEXT,high TEXT,low TEXT,volume TEXT,amount TEXT,matoday TEXT'
dbTableFieldminutes = 'date char(16) PRIMARY KEY,open TEXT,close TEXT,high TEXT,low TEXT,volume TEXT,amount TEXT'
