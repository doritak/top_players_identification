import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


st.write("# Players")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

st.markdown("""
<style>
input::placeholder {
    color: #b3b3b3;   /* gris suave */
    opacity: 1;       /* asegura que se vea en todos los navegadores */
}
</style>
""", unsafe_allow_html=True)



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

st.write("# Player identification")

x = st.text_input("Select the Player Id-Number", placeholder="enter the id-player number")
if st.button("Click Me"):
    if x.isdigit():
        x = int(x)
        st.write(f"The information for your player es: `{x}`")
        chart_player = players_list[players_list["Id-Player"]==x]
        if not chart_player.empty:
            row = chart_player.iloc[0]

            for key, value in row.items():
                col1, col2 = st.columns([1, 3])
                col1.write(f"**{key}**")
                col2.write(value)
        
        # st.write(chart_player) 

st.write("### Here are only listed players from B and C  Junior League.")

st.write(players_list)
players_list['Efficency']=round(players_list['Goals']/players_list['Minutes'],2)

fig = px.scatter(players_list, x= "Minutes", y="Goals", color="Efficency", 
                 custom_data=players_list[["Vereinsname"]],
                 hover_name="Id-Player")

fig.update_traces(
    hovertemplate=
    "<b>Id Player:</b> %{hovertext}<br>" +
    "<b>Club:</b> %{customdata[0]}<br>" +
    "<b>Minutes:</b> %{x}<br>" +
    "<b>Goals:</b> %{y}<br>" +
    "<extra></extra>"
)
st.plotly_chart(fig)