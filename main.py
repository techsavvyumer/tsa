# importing libraries
import streamlit as st
from multiapp import MultiApp
# import your app modules here
from apps import home, dataset, realtime 

app = MultiApp() # Create MultiApp variable

# Add all your application here
app.add_app("Homepage", home.app) # adding homepage
app.add_app("Tweets Dataset Analysis", dataset.app) # adding dataset analysis
app.add_app("Realtime Tweets Analysis", realtime.app) # adding realtime analysis
# The main app
app.run()