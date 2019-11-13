from ae_api_client import ActiveEnergyAPIClient
import pandas as pd
import json
import os.path
from pathlib import Path

def make_client():
    return ActiveEnergyAPIClient('https', 'cylonaem.com', 443, 'ucd-api', 'xolg-cpgo-ugzc-itve-zbdj-sjgp-tdtn-ydad')


def print_node_ids(client):
    tree_query = {
        'tree_id': 3, # UCD
    }

    response = client.query_trees(tree_query)
    for node in response['results']:
        print('%i: %s' % (node['node_id'], node['name']))


def make_datalog_query(client,node):
    import datetime;
    now = datetime.datetime.now();
    tom = now- datetime.timedelta(days=365);
    preone = now - datetime.timedelta(days=1);
    D = preone.strftime("%Y-%m-%d")

    datalog_query = [{
        'request_id': 'Request ID',
        'node_id': node, # 87Engineering + Material Science Electricity
        'request_type': 'usage',
        'from_date': tom.strftime("%Y-%m-%d"),
        'to_date': now.strftime("%Y-%m-%d"),
        'group': 'raw',
        'timezone': 'UTC',
        'date_format': 'iso',
        'ignore_today': False,
    }]

    response = client.query_datalogs(datalog_query)
    p=[]
    for datapoint in response['results'][0]['datapoints']:
        c = datapoint['timestamp'], datapoint['value']
        p.append(c)

    Data_DF = pd.DataFrame(p, columns=['date', 'value'])
    Data_DF.to_csv('data.csv',index = False)
    df = pd.read_csv('data.csv', parse_dates=['date'], index_col='date')
    df.reset_index(inplace=True)
    df['year'] = [d.year for d in df.date]
    df['month'] = [d.strftime('%b') for d in df.date]
    df['mon_no'] = [d.month for d in df.date]
    df['date_only'] = [d.strftime("%Y-%m-%d") for d in df.date]
    #print(df)
    jan = monthly_data(now,'Jan',df)
    #print(jan)
    feb = monthly_data(now, 'Feb', df)
    #print(feb)
    mar = monthly_data(now, 'Mar', df)
    apr = monthly_data(now, 'Apr', df)
    may = monthly_data(now, 'May', df)
    jun = monthly_data(now, 'Jun', df)
    jul = monthly_data(now, 'Jul', df)
    aug = monthly_data(now, 'Aug', df)
    sep = monthly_data(now, 'Sep', df)
    oct = monthly_data(now, 'Oct', df)
    nov = monthly_data(now, 'Nov', df)
    dec = monthly_data(now, 'Dec', df)
    #all_mon = {**jan,**feb,**mar,**apr,**may,**jun,**jul,**aug,**sep,**oct,**nov,**dec}
    all_mon = []
    all_mon.append(jan),all_mon.append(feb),all_mon.append(mar),all_mon.append(apr),all_mon.append(may),all_mon.append(jun)
    all_mon.append(jul), all_mon.append(aug), all_mon.append(sep),all_mon.append(oct),all_mon.append(nov),all_mon.append(dec)
    print(all_mon)

    root = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(root, r'solarDj/YearlyResult'+str(node)+'.json'), 'w') as fp:
         json.dump(all_mon,fp)
    w = days_data(D, df)
    print(w)
    with open(os.path.join(root, r'solarDj/DailyMonthResult'+str(node)+'.json'), 'w') as fp:
        json.dump(w, fp)

def monthly_data(p,r,df):
    l = {}
    sum1 = 0
    for index, row in df.iterrows():
        if row["year"] == (p.year) and row["month"] == r:
            sum1 = sum1 + row["value"]
            #print(row["date"],sum1)
    if sum1 == 0:
        pass
    elif sum1>0:
        #l.update({r+" "+str(p.year):sum1})
        l.update({'Month': r + " " + str(p.year)})
        l.update({'Rating':sum1})

       # print(l)
    return l

'''def days_data(p,df):
    l = {}
    w = []
    sum1 = 0
    for index, row in df.iterrows():
        if row["year"] == (p.year)  and row["mon_no"] == (p.month):
            l={}
            sum1 = sum1 + row["value"]
            #l.update({str(row["date"]):sum1})
            l.update({'Date':str(row["date"])})
            l.update({'Rating':sum1})
            w.append(l)
    return w
'''

def days_data(D,df):
    l = {}
    w = []
    sum1 = 0
    for index, row in df.iterrows():
        if (row["date_only"] == D):
            l={}
            sum1 = sum1 + row["value"]
            l.update({'Timestamp':str(row["date"])})
            l.update({'Rating':sum1})
            w.append(l)
    return w



def main():
    import time
    var = 1
    while (var==1):
        client = make_client()
        #print_node_ids(client)
        make_datalog_query(client,87)
        make_datalog_query(client,790)
        var=0


if __name__ == '__main__':
    main()
