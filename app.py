import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import unicodedata
import seaborn as sns
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide"
)

st.sidebar.title("Whats App Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df, use_container_width=True)

    user_list = df['users'].unique().tolist()

    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox(
        "show analysis with respect to",
        user_list,
    )

    num_messages,num_words,media_shared,total_url = helper.fetch_stats(selected_user,df)
    if st.sidebar.button("show analysis"):
        col1,col2,col3,col4 = st.columns(4,border=True,gap="xlarge")
        with col1:
            st.header("Total messages")
            st.title(num_messages)
            

        with col2:
            st.header("Total words")
            st.title(num_words)
            

        with col3:
            st.header("Media Shared")
            st.title(media_shared)

        with col4:
            st.header("URL Shared")
            st.title(total_url)

        time_line=helper.timeline(selected_user,df)
        st.title("Timeline")
        
        col1, col2 = st.columns([2,1])

        with col1:
            fig,ax=plt.subplots(figsize=(4,3))
            ax.plot(time_line['month_year'],time_line['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user == 'Overall':
            x,per_pd = helper.most_busy_users(df)
            st.title("most buusy users")
            col5, col6 = st.columns([3, 1],border=True)

            
            col5.bar_chart(x,color='red')

            col6.table(per_pd)
        tab,img = helper.most_common_words(selected_user,df)
        st.title("word cloud")
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.imshow(img)
        ax.axis('off')

        st.pyplot(fig)

        st.title("most common words")
        
        col7, col8 = st.columns([1,3])

        with col7:
        
            st.dataframe(tab, width=300, height=500)

        with col8:
            fig,ax = plt.subplots()
            ax.barh(tab['word'],tab['count'])
            st.pyplot(fig)

        st.title("Emoji Count")
        emo_df = helper.emojis(selected_user,df)
        

        col9, col10 = st.columns(2)

        with col9:
        
            st.dataframe(emo_df, width=300, height=500)

        with col10:
            fig,ax = plt.subplots(figsize=(4,4))
            myexplode = [0.2, 0, 0, 0,0]
            ax.pie(emo_df['count'].head(),labels=emo_df['emojis'].head(),autopct='%0.2f',explode=myexplode,shadow=True)
            st.pyplot(fig)

    

        col1,col2 = st.columns(2)

        with col1:
            st.title("Daily active")
            daily_act = helper.daily_active(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(daily_act['day_name'],daily_act['count'])
            st.pyplot(fig)

        with col2:
            st.title("Monthly active")
            month_act=helper.monthly_active(selected_user,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(month_act['month_name'],month_act['count'])
            st.pyplot(fig)
        act_heatmap = helper.heat_map(selected_user,df)
        st.title("Weakly activity map")
        fig,ax = plt.subplots()
        ax = sns.heatmap(act_heatmap)
        st.pyplot(fig)




        

        


