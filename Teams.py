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
club_top = club_top.rename(
    columns={"Vereinsname":"Club Name","Cant_Goal":"Total Goals", "Cant_Player":"Total Players"})
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

club_top_sorted = club_top.sort_values(by="Total Players")


fig = go.Figure(
    data=[
        go.Bar(
            x=club_top_sorted["Club Name"], 
            y=club_top_sorted["Total Goals"],
            customdata=club_top_sorted[["Total Players"]],
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
st.markdown("<hr style='border: 2px solid orange;'>", unsafe_allow_html=True)
# The best player per Team is...     
player_df = players_list.copy()

st.write("Select the team to see the best player score")
left_col_player,  right_col_player = st.columns(2)

clubs_player = ["Best for All"] + sorted(pd.unique(player_df["Vereinsname"]))
club_pl = left_col_player.selectbox("Choose the Club", clubs_player)

max_goals =player_df["Goals"].max()
best_player = player_df[player_df["Goals"] == max_goals]

if club_pl != "Best for All":
    player_df = player_df[player_df["Vereinsname"] == club_pl]
    max_goals =player_df["Goals"].max()
    best_player = player_df[player_df["Goals"] == max_goals]
    
    
right_col_player.write(f"The best scoring Player hat the id-Player: {best_player['Id-Player'].iloc[0]} \
             and has {best_player['Goals'].iloc[0]} goals and plays \
             for the club {best_player['Vereinsname'].iloc[0]} with {best_player['Minutes'].iloc[0]} minutes. ")
    
st.markdown("<hr style='border: 2px solid orange;'>", unsafe_allow_html=True)
# divide width columns in windows
left_col,  right_col = st.columns(2)
# Making the 2 selectbox (popup)
#titles and description

left_col.write("### Players per League")
right_col.write("### Players per Club")
left_col.write("This chart displays how players are distributed across different leagues.")
right_col.write("This chart show the distribution fo registered players across the selected club.")


ligas = ["All"] + sorted(list_Liga)
liga = left_col.selectbox("Choose a League", ligas)

clubs = ["All"] + sorted(pd.unique(players_list["Vereinsname"]))
club = right_col.selectbox("Choose a Club", clubs)

reduced_df = players_list.copy()

if liga != "All":
    reduced_df = reduced_df[reduced_df["Liga"].str.contains(liga, case=False, na=False)]

if club != "All":
    reduced_df = reduced_df[reduced_df["Vereinsname"] == club]

if reduced_df.empty:
    st.warning("There are no filters for this player selection.")
    st.stop()

# aqui busco los players por cada club
players_per_club = (
    reduced_df["Vereinsname"]
    .value_counts()
    .reset_index()
)
players_per_club.columns = ["Club", "Numbers_Players"]

fig_club = px.pie(
    players_per_club,
    names="Club",
    values="Numbers_Players",
    title="Players per Club",
)

# jugadores por liga
players_per_league = (
    reduced_df["Liga"]
    .value_counts()
    .reset_index()
)
players_per_league.columns = ["League", "Numbers_Players"]

fig_league = px.pie(
    players_per_league,
    names="League",
    values="Numbers_Players",
    title="Players per Liga",
)
st.write("\n")
# to show this in the pie grafic
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_club, use_container_width=True)
with col2:
    st.plotly_chart(fig_league, use_container_width=True)









url = "https://docs.google.com/document/d/1uNVnJkBDwP16nCIBTXuiEy7jOdy6IX_XVu9FLK9dn_k/edit?tab=t.0"
st.markdown(f"[Click here for the Project Information](<{url}>)")


