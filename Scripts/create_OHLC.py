#!/usr/bin/env python

import sys
import pandas
import gzip 
import pickle
import time
from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import itertools
import calendar

def main():
    start_time = time.time()

    start_year = 2014
    end_year = 2014 

    weeks = range(1,6)
    months = range(1,13)
    years = range(start_year, end_year+1)

    date_tuple_array = itertools.product(years, months, weeks)

    zipbase = "EUR_USD_Week"
    count = 0
    df = None
    for d in date_tuple_array:
        if d[1] < 10:
            path =  "http://ratedata.gaincapital.com/" + `d[0]` + "/0" + `d[1]` + \
                "%20" + calendar.month_name[d[1]] + "/" + zipbase + `d[2]` + ".zip"
        else:
            path =  "http://ratedata.gaincapital.com/" + `d[0]` + "/" + `d[1]` + \
                "%20" + calendar.month_name[d[1]] + "/" + zipbase + `d[2]` + ".zip"
            
        
        try: 
            url = urlopen(path)
            zipfile = ZipFile(StringIO(url.read()))
            
            foofile = None

            for f in zipfile.namelist():
                print d
                foofile = zipfile.open(f)
                
                try:
                    temp_df = pandas.read_csv(foofile, parse_dates = [3], index_col=3, 
                        names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'], header=1, 
                        date_parser=parse)
                    
                    if temp_df is None: 
                        print "parse returned None"
                        continue

                    del temp_df['Tid']
                    del temp_df['Dealable']
                    del temp_df['Pair']
                   
                    if df is None:
                        df = temp_df
                    else:
                        df = pandas.concat([df,temp_df])
                    
                    print path + "   Success!" 

                except: 
                    print path + "   FAIL!!!!"
           
            #grouped_data.to_pickle(`d[0]` + "_" + calendar.month_name(d[1]) + "_" \
            #                    + `d[2]` + '-OHLC.pkl')
        except:
            print path + "FAILED"
        count += 1
    

    grouped_data = df.resample('24H').ohlc()
    grouped_data.to_pickle('EUR_USD_2015-OHLC.pkl')
    
    print time.time() - start_time                                
    # group every 15 minutes and create OHLC
    #grouped_data = df.resample('24H', 11how='ohlc')

    # save to file

    #print(grouped_data)



    #grouped_data.to_pickle(month + '_' + `week` +'-OHLC.pkl')



def parse(timestamps):
    clean = timestamps.split(".")[0] if '.' in timestamps else timestamps
    return pandas.datetime.strptime(clean,"%Y-%m-%d %H:%M:%S")
    

if __name__ == "__main__":
    
    main()


