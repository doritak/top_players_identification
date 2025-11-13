import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df
# st.markdown("""
# <style>
# input::placeholder {
#     color: #b3b3b3;   /* gris suave */
#     opacity: 1;       /* asegura que se vea en todos los navegadores */
# }
# </style>
# """, unsafe_allow_html=True)



club_top = load_data(path = "data/club_top.csv")
players_list = load_data(path = "data/players_list.csv")

club_top = deepcopy(club_top)
players_list = deepcopy(players_list)

list_position = (players_list["Position"]
                 .str.split(",")
                 .explode()
                 .str.strip()
                 .dropna()
                 .unique())
print(list_position)

list_Liga = (players_list["Liga"]
                 .str.split(",")
                 .explode()
                 .str.strip()
                 .dropna()
                 .unique())


st.write("# Teams (Vereins)")
st.write("### Here are the listed the Football Groups.")
st.write(club_top)

club_top_sorted = club_top.sort_values(by="Cant_Player")
fig = go.Figure(
    data=[
        go.Bar(
            x=club_top_sorted["Vereinsname"], 
            y=club_top_sorted["Cant_Goal"],
            customdata=club_top_sorted[["Cant_Player"]],
            marker=dict(color="lightblue"), 
            hovertemplate="<b>%{x}</b><br> Goals:%{y}<br> Players:%{customdata[0]}"
        )])
    
fig.update_layout(
    title="Goals per Clubs order by Number of Players",
    xaxis_title="Football Clubs",
    yaxis_title="Goals"
)
# fig.add_annotation(
    
# )
st.plotly_chart(fig)

url = "https://docs.google.com/document/d/1uNVnJkBDwP16nCIBTXuiEy7jOdy6IX_XVu9FLK9dn_k/edit?tab=t.0"
st.markdown(f"[Click here for the Project Information](<{url}>)")


