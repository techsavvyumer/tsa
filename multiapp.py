# Frameworks for running multiple Streamlit applications as a single app.
import streamlit as st


class MultiApp:

    def __init__(self): # constructor
        self.apps = [] # list of apps

    def add_app(self, title, func): # add apps to the list
        self.apps.append({"title": title, "function": func}) # append the title and function to the list

    def run(self): # run the app
        app = st.header("Sentiment Analysis Multi-Page App") # header
        app = st.write(
            "This multi-page app is using the Streamlit MultiApps framework.") # write
        app = st.selectbox(
            "Select The App You Want To Use",
            self.apps,
            format_func=lambda app: app["title"]) # selectbox
        app["function"]() # run the function