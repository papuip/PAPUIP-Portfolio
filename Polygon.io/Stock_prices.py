import pandas as pd
import requests

api_key='KPPRWTibl2UuEGQEALJCOPSCT73Ah_DM'
ticker='AAPL'
time_range=1
time_horizont='day'

api_url=f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time_range}/{time_horizont}/2020-06-01/2020-06-17?apiKey={api_key}'

data=requests.get(api_url).json()
df=pd.DataFrame(data['results'])
#df.to_excel("Stock_prices.xlsx",index=False)
statment=df.T
print(statment.head(10))
#print(df)
