import os
import pandas as pd 
import gzip 

def main():

    ##Path of the directory or folder where Bitmex .gzips are saved
    directory = 'N://Bitmex/October'  

    bitmex_complete = []
    for filename in os.listdir(directory):
        if filename.endswith('.gz'):
            bitmexRaw = gzip.GzipFile(directory +'/'+filename,'rb')
            bitmexDF =pd.read_csv(bitmexRaw)
            ## Change groupby to timestamp,side,size,symbol,price,tickDirection
            ## trdMacthID,grossValue,homeNotional,foreignNotional
            ## Filter and sort as you wish. 
            bitmexGrouped = bitmexDF.groupby('symbol').get_group('XBTUSD')
            bitmexDailySet = bitmexGrouped[['timestamp','price','size','foreignNotional']]
            bitmexDailySet['Date'] = bitmexGrouped['timestamp'].tail(1) 
            bitmexDailySet['price']= bitmexGrouped['price'].tail(10).mean()
            bitmexDailySet['avg size'] = bitmexGrouped['size'].mean() 
            bitmexDailySet['USDNotional'] = bitmexGrouped['foreignNotional'].sum()
            bitmexDailySet = bitmexDailySet.drop(['timestamp','size','foreignNotional'],axis=1)
            bitmexDailySet= bitmexDailySet.dropna() 
            bitmex_complete.append(bitmexDailySet)
            bitmex_TradeRecord = pd.concat(bitmex_complete) 
            ndate = bitmex_TradeRecord['Date'].str.split('D', n=1,expand=True)
            bitmex_TradeRecord['Date']= ndate[0]
            bitmex_TradeRecord['Date'] = pd.to_datetime(bitmex_TradeRecord['Date']) 
            bitmex_TradeRecord = bitmex_TradeRecord.sort_values(by=['Date'])
            bitmex_TradeRecord.to_csv('N://Bitmex/October/trade_record.csv') 
        
               
if __name__=="__main__":
    main()
