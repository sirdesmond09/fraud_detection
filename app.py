import pandas as pd
import matplotlib.pyplot as plt
import dill
import gzip
plt.style.use('seaborn')
from sklearn.preprocessing import LabelEncoder
from send_mail import send_simple_message



def preprocessdata(data):
    data.drop_duplicates(keep="first", inplace=True) #removing duplicate data if any
    #Extracting time and day from the TransactionStartTime column to create new features
    data['TransactionStartTime'] = data['TransactionStartTime'].str.replace('T', ' ')
    data['TransactionStartTime'] = data['TransactionStartTime'].str.replace('Z', '')
    data['TransactionStartTime'] = pd.to_datetime(data['TransactionStartTime'], infer_datetime_format=True)
    data['hour'] = pd.to_datetime(data.TransactionStartTime).dt.hour
    data['minute'] = pd.to_datetime(data.TransactionStartTime).dt.minute
    data['day'] = pd.to_datetime(data.TransactionStartTime).dt.dayofweek
    # dropping the transaction starttime column
    data = data.drop(["TransactionStartTime"], axis=1)
    
    
    
    #encoding the categorical data
    for col in data.columns:
        if data[col].dtype == 'object' and col not in ['TransactionId', 'FraudResult']:
            # print(col)
            lbl = LabelEncoder()
            data[col] = lbl.fit_transform(list(data[col].values.astype('str')))
    #Normalizing Amount and value columns
    data["Value"] = data["Value"].abs()
    data["Amount"] = data["Amount"].abs()
    
    # dropping non-predictor feature columns and the target(train-set only)
    if "FraudResult" in data.columns:
        target = data["FraudResult"]
        data = data.drop(["FraudResult"], axis=1)
        
    else:
        target = None
    if "TransactionId" in data.columns:
        transaction_id = data["TransactionId"]
        data = data.drop(["TransactionId"], axis=1)
        
    return data, target, transaction_id



#load our machine learning model
with gzip.open("fraud_model.dill.gz", 'rb') as f:
    model = dill.load(f)



#trasform individual rows to dataframes (tables)
def format_to_df(**kwargs):
    
    return pd.DataFrame(**kwargs, index=[0])


#validating our payements using the machine learning model
def validate(func):
    def inner(**data):
        formatted_data = format_to_df(data = data)
        df, target, trans_id = preprocessdata(formatted_data)

        predictions = model.predict(df)

        if predictions == 1:
            send_simple_message(**data, status = "Flagged")
            return func(**data, status = "Flagged")
        if predictions == 0:
            return func(**data)
        
        return func(data)
             
    return inner



