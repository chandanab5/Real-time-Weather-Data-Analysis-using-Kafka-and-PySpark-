import streamlit as st
import pymongo
import pandas as pd

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data():
    db = client.test
    items = db.weather.find()
    items = list(items)  # make hashable for st.experimental_memo
    return items

items = get_data()

# Print results.
for item in items:
    a=item['time']
    b=item['prediction']
    chart_data = pd.DataFrame(b, a)
    st.line_chart(chart_data)



# #import numpy as np

# chart_data = pd.DataFrame(columns=[items[0], items[1]])
# st.line_chart(chart_data)
