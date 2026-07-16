import re
import pandas as pd
import unicodedata

def preprocess(data):
    ## use regex101.com dont use ^ and $
    pattern = r"\[\d{2}/\d{2}/\d{2},\s*\d{1,2}:\d{2}:\d{2}\s*[AP]M\]\s*~?\s*"
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date'] = (df['message_date']
                        .str.replace('\u202f'," ",regex=False)
                        .str.replace(r'[\[\]]','',regex=True)
                        .str.replace('~','',regex=False)
                        .str.strip()
    )
    df['message_date'] = pd.to_datetime(df['message_date'],format='%d/%m/%y, %I:%M:%S %p')
    df.rename(columns={'message_date':'date'},inplace=True)
    users =[]
    messages=[]

    for message in df['user_message']:
        entry = re.split(r"([\w\W]+?):\s",message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            messages.append(entry[0])
            users.append('group_notification')
    df['users'] = users
    df['message'] = messages

    def remove_unicode(sentence):
        return ''.join([ch for ch in sentence if unicodedata.category(ch) != 'Cf'])

    df['message'] =df['message'].apply(remove_unicode)



    df.drop(columns=['user_message'],inplace = True)
    df['year'] = df['date'].dt.year
    df['month']=df['date'].dt.month
    df['month_name']=df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['time'] = df['date'].dt.time
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period=[]
    for hour in df['hour']:
        if hour ==23:
            period.append(str(hour) +"-"+str(00))
        elif hour ==0:
            period.append(str(00)+'-'+str(hour+1))
        else :
            period.append(str(hour)+'-'+str(hour + 1))

    df['period'] = period


    return df



