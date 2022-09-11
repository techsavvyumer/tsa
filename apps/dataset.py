#Importing dependencies
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
import string


def app():
    #loading the dataset
    sent_df = pd.read_csv('train.csv')
    sent_df = sent_df.dropna() #dropping the null values


    #information about the dataset and app
    st.header("Sentiment Analysis: Emotion in Text Tweets")
    st.markdown("The purpose of this Sentiment Analysis is to classify emotions from Text Tweets. Dataset is taken from a [Kaggle Competition](https://www.kaggle.com/competitions/tweet-sentiment-extraction/).")


    #plotting the sentiments bar graph
    st.subheader("Comparision of Counts of Sentiments")
    fig = sent_df['sentiment'].value_counts().plot.bar(color=['green', 'blue', 'red'], edgecolor='black')
    plt.xticks(rotation=0, horizontalalignment="center")
    plt.xlabel('Sentiments', color='Black', fontsize='12', horizontalalignment="center")
    plt.subplots_adjust(bottom=0.5, top=1.5)
    figur = fig.figure
    figur.savefig('sent_bar.png')
    st.pyplot(figur)


    # defining text cleaning function
    def clean_text(text):
        text = str(text).lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('http?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text


    # applying text cleaning function
    sent_df['clean_text'] = sent_df['text'].apply(lambda x: clean_text(x))
    sent_df['selected_text'] = sent_df['selected_text'].apply(lambda x: clean_text(x))


    # displaying/plotting WordClouds (i.e Most common words in the texts)
    words = " ".join([text for text in sent_df["clean_text"]])
    wordclouds = WordCloud(width=1200, height=800, random_state=42, max_font_size=120).generate(words)
    plt.figure(figsize=(12, 8))
    plt.imshow(wordclouds, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wordcd.png")
    st.subheader("Wordcloud of Tweets")
    st.image("wordcd.png")


    # Main
    if __name__ == "__main__":
        st.empty()
        app()