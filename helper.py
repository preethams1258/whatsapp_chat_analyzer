from urlextract import URLExtract
import pandas as pd
import wordcloud
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import string
from collections import Counter
import unicodedata
import emoji
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


extractor = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user] 

    #1.fetching total number of messages
    total_messages = len(df)

    #2.fetching total number of words
    words = []
    for message in df["message"]:
        words.extend(message.split())

    total_words = len(words)
    media_keywords = [
        'image omitted',
        'video omitted',
        'GIF omitted',
        'sticker omitted',
        'audio omitted',
        'document omitted',
        'Contact card omitted'
    ]

    media_shared = df['message'].str.contains(
        '|'.join(media_keywords),
        case=False,
        na=False
    ).sum()

    url =[]

    for message in df['message']:
        url.extend(extractor.find_urls(message))
    
    total_url = len(url)

    

    return total_messages,total_words,media_shared,total_url


def most_busy_users(df):
    x=df['users'].value_counts().head()
    percent_x=x/len(df)*100
    percent_pd = pd.DataFrame({'users':percent_x.index,'percentage':percent_x.values})

    return x,percent_pd



def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    stop_words = set(stopwords.words('english'))


    media_keywords = [
        'image omitted',
        'video omitted',
        'GIF omitted',
        'sticker omitted',
        'audio omitted',
        'document omitted',
        'Contact card omitted'
    ]

    df = df[~df['message'].str.contains(
        ("|").join(media_keywords),case =False,na=False
    )]

    words=[]

    for message in df['message']:
        words.extend(message.split())

    words = [word.lower() for word in words if word.lower() not in stop_words]
    words = [word.strip(string.punctuation) for word in words]
    words = [word for word in words if word]
   
    counter = Counter(words).most_common(10)
    most_common = pd.DataFrame(counter,columns=["word","count"])

    text = " ".join(words)
    word_cloud = WordCloud(width=500,height=400,background_color='white')





    return most_common,word_cloud.generate(text)

def emojis(selected_user,df):
    if selected_user !="Overall":
        df=df[df['user']==selected_user]

    emo=[]
    for sentences in df['message']:
        for ch in sentences:
            if emoji.is_emoji(ch):
                emo.append(ch)

    return pd.DataFrame(Counter(emo).most_common(),columns=['emojis','count'])    


def timeline(selected_user,df):

    if selected_user != "Overall":
        df =df[df['users']==selected_user]

    new_df =df.groupby(['year','month','month_name']).count()['message'].reset_index()
    new_df['month_year']=new_df['month_name'] + "-" +new_df['year'].astype(str)
    return new_df

def daily_active(selected_user,df):
    if selected_user != "Overall":
        df =df[df['users']==selected_user]

    new=df['day_name'].value_counts().reset_index()
    return new

def monthly_active(selected_user,df):
    if selected_user != "Overall":
        df =df[df['users']==selected_user]

    new=df['month_name'].value_counts().reset_index()
    return new

def heat_map(selected_user,df):
    if selected_user != "Overall":
        df =df[df['users']==selected_user]

    df =df.sort_values(by='hour')
    act_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return act_heatmap