# Importing dependencies
from typing import Text
import streamlit as st
from PIL import Image
import sys
import time
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
from textblob import TextBlob

nltk.download('wordnet')

# authentication of consumer key and secret (i.e API authentication)
auth = tweepy.OAuthHandler(st.secrets["consumer_key"], st.secrets["consumer_secret"])
auth.set_access_token(st.secrets["access_token"], st.secrets["access_token_secret"])
api = tweepy.API(auth, wait_on_rate_limit=True)


# Function to retrieve the tweets                          
def fetch_tweets(user_name, tweet_count):
    tweets_list = []
    img_url = ""
    name = ""

    # fetching the tweets
    try:
        for tweet in api.user_timeline(id=user_name, count=tweet_count, tweet_mode="extended"):
            tweets_dict = {}
            tweets_dict["date_created"] = tweet.created_at
            tweets_dict["tweet_id"] = tweet.id
            tweets_dict["tweet"] = tweet.full_text
            tweets_list.append(tweets_dict)

        img_url = tweet.user.profile_image_url
        name = tweet.user.name
        screen_name = tweet.user.screen_name
        desc = tweet.user.description

    # if unable to fetch then
    except BaseException as e:
        st.exception("Failed to retrieve the Tweets. Please check if the twitter handle is correct.")
        sys.exit(1)
    return tweets_list, img_url, name, screen_name, desc


# defining funtion to clean data (i.e data preprocessing) for Model and Wordclouds
def data_preprocessing(tweet):
    # cleaning the data using Regular Expression (re)
    tweet = re.sub("https?:\/\/\S+", "", tweet) # replacing url with domain name
    tweet = re.sub("#[A-Za-z0–9]+", " ", tweet)  # removing @mentions
    tweet = re.sub("@[A-Za-z0–9]+", "", tweet)  # removing @mentions
    tweet = re.sub("#", " ", tweet)  # removing hash tag
    tweet = re.sub("\n", " ", tweet)  # removing \n (i.e next line)
    tweet = re.sub("RT", "", tweet)  # removing RT
    tweet = re.sub("^[a-zA-Z]{1,2}$", "", tweet) # removing 1-2 char long words
    tweet = re.sub("\w*\d\w*", "", tweet)  # removing words containing digits

    # applying Lemmatization
    lemm = WordNetLemmatizer()
    lemm_str = ""
    for word in tweet.split(" "):
        lemm.lemmatize(word)
        if word not in stopwords.words("english"):
            lemm_str += word + " "
    return lemm_str[:-1]


# defining fuction for plotting wordclouds
def wordcloud(clean_tweet):
    wordcloud_words = " ".join(clean_tweet)
    wordcloud = WordCloud(height=800, width=1200, background_color="black", random_state=300,).generate(wordcloud_words)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("cloud.jpg")
    img = Image.open("cloud.jpg")
    return img


# Function to get the polarity score
def calculate_polarity(tweet):
    sentiment_polarity = TextBlob(tweet).sentiment.polarity
    return sentiment_polarity


# Function to convert the polarity score into sentiment category
def pred_sentiment(polarity_score):
    if polarity_score < 0:
        return "Negative"
    elif polarity_score == 0:
        return "Neutral"
    else:
        return "Positive"


# defining function to plot the bar graph of sentiments
def plot_sent_bar(tweet_df):
    sentiment_df = (
        pd.DataFrame(tweet_df["sentiment"].value_counts())
        .reset_index()
        .rename(columns={"index": "sentiment_name"}))
    fig = px.bar(x=sentiment_df["sentiment_name"], y=sentiment_df["sentiment"], labels={'x': 'Sentiments', 'y': 'Number of Tweets'}, color=sentiment_df["sentiment_name"], color_discrete_sequence=['#23C945', '#2593C9', '#E0401A'])
    return fig


# defining function to plot the pie chart of sentiments
def plot_sent_pie(tweet_df):
    sentiment_df = (
        pd.DataFrame(tweet_df["sentiment"].value_counts())
        .reset_index()
        .rename(columns={"index": "sentiment_name"}))
    fig1 = px.pie(sentiment_df, values="sentiment", names="sentiment_name", color=sentiment_df["sentiment_name"], color_discrete_sequence=["#F5D216", "#003f5c", "#ff6361"])
    return fig1


# main
def app():
    tweet_count = st.empty() #defining the tweet_count variable
    user_name = st.empty() #defining the user_name variable

    st.sidebar.subheader("Enter the Details Here!!") #sidebar header

    user_name = st.sidebar.text_area("Enter the Twitter Handle without @") #user_name input area

    tweet_count = st.sidebar.slider("Select the number of Latest Tweets to Analyze (Note: There is a limitation of 200 tweets imposed by the Twitter API.)", 0, 200, 0, 5) # tweet_count slider

    st.sidebar.markdown("**Press Ctrl+Enter or Use the Slider to initiate the analysis.**") #instructions

    st.image("https://i.ibb.co/K0NLxPw/Twitter-Sentiment-Analysis1.gif", width=700) #gif on main page

    st.write("This app analyzes the Twitter tweets and returns the most commonly used words, associated sentiments.")
    st.markdown('''
                **Notes:**
                - **Private account / Protected Tweets will not be accessible through this app.**
                - **Only English language is supported for now.**''')
    st.write(":bird: All results are based on the number of Latest Tweets selected on the Sidebar. :point_left:")

    # app main logic
    if user_name != "" and tweet_count > 0: # if user_name and tweet_count are not empty
        with st.spinner("Please Wait!! Analysis is in Progress......:construction:"):
            time.sleep(1)

        tweets_list, img_url, name, screen_name, desc = fetch_tweets(
            user_name, tweet_count) # calling fetch_tweets function

        # converting the retrieved tweet data into a dataframe
        tweet_df = pd.DataFrame([tweet for tweet in tweets_list])
        length = len(tweet_df) # length of the total tweets
        st.sidebar.success("Twitter Handle Details:") #user data fetch success message
        # st.sidebar.image(img_url) # displaying the user's profile image
        st.sidebar.markdown("Name: " + name) # displaying the user's name
        st.sidebar.markdown("Screen Name: @" + screen_name) # displaying the user's handle
        st.sidebar.markdown("Description: " + desc) # displaying the user's description

        # creating a new column in the dataframe to store the cleaned tweets
        tweet_df["clean_tweet"] = tweet_df["tweet"].apply(data_preprocessing) # calling data_preprocessing function

        # calling the function to create sentiment scoring
        tweet_df["polarity"] = tweet_df["clean_tweet"].apply(calculate_polarity)
        tweet_df["sentiment"] = tweet_df["polarity"].apply(pred_sentiment)

        # plotting sentiments bar graph
        st.subheader("Sentiment Analysis")
        senti_fig = plot_sent_bar(tweet_df)
        st.success("Sentiment Analysis for Twitter Handle @" + user_name + " based on the last " + str(length) + " tweet(s)!!")
        st.plotly_chart(senti_fig, use_container_width=True)

        # plotting sentiments pie chart
        sent_fig = plot_sent_pie(tweet_df)
        st.success("Tweet Sentiments in Percentage for Twitter Handle @"+ user_name + " based on the last " + str(length)+ " tweet(s)!!")
        st.plotly_chart(sent_fig, use_container_width=True)

        # calling the function to create the word cloud for all tweets
        st.subheader("Word Clouds")
        st.write("Word Clouds display the most prominent or frequent words in a body of text.")
        img = wordcloud(tweet_df["clean_tweet"])
        st.success("Word Cloud for Twitter Handle @" + user_name + " based on the last " + str(length) + " tweet(s)!!")
        st.image(img)

        # displaying the latest tweets
        if st.button("Get Latest Tweets"):
            st.subheader("Latest Tweets!")
            st.markdown("*****************************************************************")
            st.success(str(length) + " Latest Tweets from the Twitter Handle @" + user_name)
            for i in range(length):
                st.write("Tweet Number: " + str(i + 1) + ", Tweet Date: " + str(tweet_df["date_created"][i]))
                st.info(tweet_df["tweet"][i])

        # displaying the positive tweets
        if st.button("Get Positive Tweets"):
            st.subheader("Positive Tweets")
            st.markdown("*****************************************************************")
            for i in range(length):
                if tweet_df["sentiment"][i] == 'Positive':
                    st.write("Tweet Number: " + str(i + 1) + ", Tweet Date: " + str(tweet_df["date_created"][i]))
                    st.info(tweet_df["tweet"][i])

        # displaying the neutral tweets
        if st.button("Get Neutral Tweets"):
            st.subheader("Neutral Tweets")
            st.markdown("*****************************************************************")
            for i in range(length):
                if tweet_df["sentiment"][i] == 'Neutral':
                    st.write("Tweet Number: " + str(i + 1) + ", Tweet Date: " + str(tweet_df["date_created"][i]))
                    st.info(tweet_df["tweet"][i])

        # displaying the negative tweets
        if st.button("Get Negative Tweets"):
            st.subheader("Negative Tweets")
            st.markdown("*****************************************************************")
            for i in range(length):
                if tweet_df["sentiment"][i] == 'Negative':
                    st.write("Tweet Number: " + str(i + 1) + ", Tweet Date: " + str(tweet_df["date_created"][i]))
                    st.info(tweet_df["tweet"][i])
    else:
        st.info(":point_left: Enter the Twitter Handle & Number of Tweets to Analyze on the SideBar :point_left:")


# app execution                                               
if __name__ == "__main__":
    st.empty()
    app()