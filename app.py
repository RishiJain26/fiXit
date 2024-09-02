import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yaml
import streamlit_authenticator as stauth

with open('info.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)


name, authentication_status, username = authenticator.login( "main")


if authentication_status:
    st.title("Welcome to Sentiment Analysis on Call Transcripts")

    # Upload Transcript File
    uploaded_file = st.file_uploader("Upload a Transcript", type=["txt"])
    if uploaded_file is not None:
        transcript = uploaded_file.read().decode('utf-8')

        if st.button("Analyze Sentiment"):
            response = requests.post("http://127.0.0.1:5000/",json = {"transcript":transcript})
            print(response)
            if response.status_code == 200:
                sentiment_result = response.json()
                st.write("Sentiment Analysis Result:")
                for res in sentiment_result:
                    st.write(f"**Speaker**: {res['speaker']}")
                    st.write(f"**Text**: {res['text']}")
                    st.write(f"**Sentiment**: {res['score']['label']} (Score: {res['score']['score']:.2f})")
                    st.write("---")
                fig1, ax1 = plt.subplots()

                sentiments = [res['score']['label'] for res in sentiment_result]
                sentiment_counts = pd.Series(sentiments).value_counts()

                ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'red', 'grey'])
                ax1.axis('equal')
                st.write("Sentiment Distribution")
                st.pyplot(fig1)
                
                fig2, ax2 = plt.subplots()
                sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=['green', 'red', 'grey'], ax=ax2)
                ax2.set_xlabel('Sentiment')
                ax2.set_ylabel('Count')
                st.write("Sentiment Counts")
                st.pyplot(fig2)
    else:
        st.write("Error in File")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

