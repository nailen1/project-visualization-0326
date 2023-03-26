import streamlit as st
import pandas as pd

st.write('DataFrame')

df = pd.read_csv('./database/auction-items-nonan.csv')
st.write(df)
