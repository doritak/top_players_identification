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
all_players = load_data(path = "data/all_players.csv")

club_top = club_top.rename(
    columns={"Vereinsname":"Club Name","Cant_Goal":"Total Goals", "Cant_Player":"Total Players"})
club_top = deepcopy(club_top)
players_list = deepcopy(players_list)
all_players = deepcopy(all_players)

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

all_Ligas = (all_players["Altersklasse"]
                 .str.split(",")
                 .explode()
                 .str.strip()
                 .dropna()
                 .unique())

st.write("# Teams (Vereins)")
st.write("### Here are the listed the Football Groups.")
st.write(club_top)

club_top_sorted = club_top.sort_values(by="Total Players")

if "scatter_key" not in st.session_state:
    st.session_state.scatter_key = "players_scatter_1"
fig = go.Figure(
    data=[
        go.Bar(
            x=club_top_sorted["Club Name"], 
            y=club_top_sorted["Total Goals"],
            customdata = club_top_sorted[["Club Name", "Total Players"]],
            marker=dict(color="lightblue"), 
            hovertemplate="<b>%{x}</b><br> Goals:%{y}<br> Players:%{customdata[1]}"
        )])
    
fig.update_layout(
    title="Goals per Clubs order by Number of Players",
    xaxis_title="Football Clubs",
    yaxis_title="Goals"
)
#Capturar el click del usuario y dibuja el gráfico
event  = st.plotly_chart(
    fig,
    key=st.session_state.scatter_key,
    on_select="rerun",        # la app se vuelve a ejecutar al seleccionar
    selection_mode="points"   # selección de puntos
    )
    
##########===================################
#Buscar al jugador en el event.selection y mostrar el resumen
if event and event.selection and event.selection["points"]:
    pt = event.selection["points"][0]
      
    club_name = pt["customdata"][0]
    total_players = pt["customdata"][1]
    club_row = club_top_sorted[club_top_sorted["Club Name"] == club_name].iloc[0]

    st.markdown("### Club summary")
    st.markdown(
        f"""
        **Club:** {club_row['Club Name']}  
        **Total Goals:** ⚽{club_row['Total Goals']}  
        **Total Players:** 🧑‍🤝‍🧑{total_players}  
        **Altersklasses:**  {club_row['Altersklasse']}  
        """
    )
    if st.button("Reset selection"):
        st.session_state.scatter_key = f"players_scatter_{pd.Timestamp.now().timestamp()}"
        st.rerun()
# st.plotly_chart(fig)

st.markdown("<hr style='border: 2px solid orange;'>", unsafe_allow_html=True)
# The best player per Team is...     
player_df = players_list.copy()

st.markdown("**Select a team to see the team’s top scorer**")
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
             and has {best_player['Goals'].iloc[0]} goals ⚽ and plays \
             for the club {best_player['Vereinsname'].iloc[0]} with {best_player['Minutes'].iloc[0]} minutes. ")

###############=====================####################
st.markdown("<hr style='border: 2px solid orange;'>", unsafe_allow_html=True)
player_df_min = players_list.copy()
st.markdown("**Select a team to view the player who played the most minutes.**")
left_col_min,  right_col_min = st.columns(2)

clubs_player_min = ["Top Minutes Player"] + sorted(pd.unique(player_df_min["Vereinsname"]))
player_max_min = left_col_min.selectbox("Choose one Club", clubs_player_min)

max_min = player_df_min["Minutes"].max()
max_player = player_df_min[player_df_min["Minutes"] == max_min]

if player_max_min != "Top Minutes Player":
    player_df_min = player_df_min[player_df_min["Vereinsname"] == player_max_min]
    max_min =player_df_min["Minutes"].max()
    max_player = player_df_min[player_df_min["Minutes"] == max_min]
    
right_col_min.write(f"The player with the most minutes played has the Id-Player:\
                    {max_player['Id-Player'].iloc[0]} and has played \
                    {max_player['Minutes'].iloc[0]} minutes⏱️, und \
                    has score {max_player['Goals'].iloc[0]} Goals 🥅.")
    
###############=====================####################    
st.markdown("<hr style='border: 2px solid orange;'>", unsafe_allow_html=True)
# divide width columns in windows
left_col,  right_col = st.columns(2)
# Making the 2 selectbox (popup)
#titles and description

left_col.write("### The Altersklasse in each Club")
right_col.write("### Players per Club")
left_col.write("This chart displays how clubs are distributed across different Altersklasse.")
right_col.write("This chart show the distribution fo registered players across the selected club.")


ligas = ["All"] + sorted(all_Ligas)
liga = left_col.selectbox("Choose a Altersklasse", ligas)

clubs = ["All"] + sorted(pd.unique(all_players["Vereinsname"]))
club = right_col.selectbox("Choose a Club", clubs)

reduced_df = all_players.copy()  # change this for all the players #reduced_df = players_list.copy()

if liga != "All":
    reduced_df = reduced_df[reduced_df["Altersklasse"].str.contains(liga, case=False, na=False)]

if club != "All":
    reduced_df = reduced_df[reduced_df["Vereinsname"] == club]

###############=====================####################
if reduced_df.empty:
    st.warning("There are no filters for this player selection.")
    st.stop()

###############=====================####################
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

fig_club.update_traces(
    hovertemplate="%{label}<br>Players: %{value}<br>Percent: %{percent}"
)

# jugadores por liga
players_per_league = (
    reduced_df["Altersklasse"]
    .value_counts()
    .reset_index()
)
players_per_league.columns = ["Altersklasse", "Numbers_Players"]


fig_league = px.pie(
    players_per_league,
    names="Altersklasse",
    values="Numbers_Players",
    title="Players per Altersklasse",
)
num_items = len(fig_league.data[0].labels)

fig_league.update_traces(
    hovertemplate="%{label}<br>Players: %{value}<br>Percent: %{percent}"
)


if num_items <= 6:
    # Leyenda abajo si hay pocas categorías
    fig_league.update_layout(
        legend=dict(
            orientation="v",
            x=1.1,
            y=1,
            xanchor="left",
            yanchor="top",
            font=dict(size=10)
        ),
        # margin=dict(l=40, r=40, t=60, b=120),
        # height=600
    )
else:
    # Leyenda a la derecha si hay muchas categorías
    fig_league.update_layout(
        legend=dict(
            orientation="h",
            x=0.5,
            y=0,
            xanchor="left",
            yanchor="top",
            font=dict(size=9)
        ),
        # margin=dict(l=40, r=220, t=60, b=40),
        # height=600
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


