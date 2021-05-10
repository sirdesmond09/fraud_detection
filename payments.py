import pandas as pd
from app import validate
import time
import datetime

@validate
def save_payments(**kwargs):
    trans_time = datetime.datetime.strptime(kwargs.get('TransactionStartTime'),"%Y-%m-%dT%H:%M:%SZ")

    print('\n=====================')
    print(f"""Tran-id: {kwargs.get('TransactionId')}
Amount : {kwargs.get('Amount')}
Time : {trans_time}
Status : {kwargs.get('status', 'Success')}""")
    print('=======================\n')  






#geting the data of our payments
data = pd.read_csv("training.csv")
data=data.iloc[12800:12815]


#validating the data
for index, transaction in data.iterrows():
    
    
    save_payments(
                    TransactionId = transaction["TransactionId"],
                    BatchId = transaction["BatchId"],
                    AccountId = transaction["AccountId"],
                    SubscriptionId = transaction["SubscriptionId"],
                    CustomerId = transaction["CustomerId"],
                    CurrencyCode = transaction["CurrencyCode"],
                    CountryCode = transaction["CountryCode"],
                    ProviderId = transaction["ProviderId"],
                    ProductId = transaction["ProductId"],
                    ProductCategory = transaction["ProductCategory"],
                    ChannelId = transaction["ChannelId"],
                    Amount = transaction["Amount"],
                    Value = transaction["Value"],
                    TransactionStartTime = transaction["TransactionStartTime"],
                    PricingStrategy = transaction["PricingStrategy"]
                )
    time.sleep(1)
    



