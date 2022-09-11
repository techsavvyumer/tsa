# import libraries
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def app(): # define the app
    text = ""
    # VADER Sentiment analysis model
    vader = SentimentIntensityAnalyzer() # vader calculate compound score to predict sentiment
    prediction = "" # creating prediction variable
    st.image("home.jpg", use_column_width=True) # image on the homepage
    #introduction text
    st.header("About")
    st.write('This is the homepage of Sentiment Analysis app.') 
    st.write('Kindly select a page from the above selector to get started, or try the demo below.')
    st.header("Sentiment Analysis Demo")
    # getting text input to analyze sentiment
    text = st.text_area("Enter text to find sentiment:")
    # Predicting sentiment
    if text != "": # if text is not empty
        vader_sentiment = vader.polarity_scores(text) # get the sentiment
        if vader_sentiment['compound'] >= 0.05: # if compound score is greater than 0.05
            prediction = "Positive" # predict positive
            st.success(prediction, icon="😊") # show positve prediction message
        elif vader_sentiment['compound'] <= -0.05:
            prediction = "Negative" # predict negative
            st.error(prediction, icon="😠")  # show negative prediction message
        else:
            prediction = "Neutral" # predict neutral
            st.info(prediction, icon="😐") # show neutral prediction message