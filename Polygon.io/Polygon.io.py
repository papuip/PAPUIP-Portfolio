import requests
import pandas as pd
import datetime


API_Key='KPPRWTibl2UuEGQEALJCOPSCT73Ah_DM'
ticker='X:BTCUSD' #currency
# start_day=20
# start_month=4
# start_year=2022
# end_day=24
# end_month=4
# end_year=2022
# start_date=f'{start_year}-{start_month}-{start_day}'
# end_date=f'{end_year}-{end_month}-{end_day}'
# start_date_d=datetime.date(int(start_year),int(start_month),int(start_day))
# end_date_d=datetime.date(int(end_year),int(end_month),int(end_day))

end_date_d=datetime.date.today() #Choose between 2 versions
ddelta=datetime.timedelta(days=7) #Past 7 days from Today
start_date_d=end_date_d-ddelta
timespan="minute" #day, hour
multiplier ='1'
adjustments=True
sort='asc'    #asc/desc
limit=50_000   #Max 50_000
#API_url=f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date}/{end_date}?apiKey={API_Key}'
API_url=f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date_d}/{end_date_d}?adjusted={adjustments}&sort={sort}&limit={limit}&apiKey={API_Key}'
data=requests.get(API_url).json()
df=pd.DataFrame(data['results'])
df.rename(columns={"v":"The trading volume",'vw':'The volume weighted average price','o':'Open Price',"c":"Close Price","h":"Highest Price",'l':"Lowest Price",'t':'The Unix Msec timestamp for the start of the aggregate window','n':'The number of transactions in the aggregate window'}, inplace=True)
#print(df.columns)
# indexes=[]
# for x in range(start_date_d,end_date_d):
#     indexes.append(int(x))
df.to_excel("crypto_princes.xlsx", sheet_name=f'{timespan[0:3].upper()}{start_date_d}.{end_date_d}{ticker[2:5]}',index=False)

# print(indexes)