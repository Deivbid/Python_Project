import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly


df_20 = pd.read_csv('Data_Players/players_20.csv')

#Scatter
fig = go.Figure(
    data = go.Scatter(
        x = df_20['overall'],
        y = df_20['value_eur'],
        mode = 'markers',
        marker = dict(
            size = 10,
            color = df_20['age']
        ),
        text = df_20['short_name']
    )
)

fig.update_layout(
    title = 'Scatter Plot (Colored by age) 2020 - Overall Rating vs Value in Euros',
    xaxis_title = 'Overall Rating',
    yaxis_title = 'Value in Euros'
    )
fig.show()

#Pie Chart
fig = px.pie(df_20, names = 'preferred_foot', title = 'Percentage of players pereffered foot', )
fig.show()

#Histogram
fig = px.histogram(df_20, x = 'age', title = 'Histogram of players Age')
fig.show()

#Scatter Polar Plot 
df_16 = pd.read_csv("Data_Players/players_16.csv", error_bad_lines=False)
df_17 = pd.read_csv("Data_Players/players_17.csv", error_bad_lines=False)
df_18 = pd.read_csv("Data_Players/players_18.csv", error_bad_lines=False)
df_19 = pd.read_csv("Data_Players/players_19.csv", error_bad_lines=False)

skills = ['Pace','Shooting','Passing','Dribbling','Defending','Physic','Overall']

def player_growth(name):
    data20 = df_20[df_20.short_name.str.startswith(name)]
    data19 = df_19[df_19.short_name.str.startswith(name)]
    data18 = df_18[df_18.short_name.str.startswith(name)]
    data17 = df_17[df_17.short_name.str.startswith(name)]
    data16 = df_16[df_16.short_name.str.startswith(name)]

    trace0 = go.Scatterpolar(
        r = [
            data20['pace'].values[0],
            data20['shooting'].values[0],
            data20['passing'].values[0],
            data20['dribbling'].values[0],
            data20['physic'].values[0],
            data20['overall'].values[0],
        ],
        theta = skills,
        fill = 'toself',
        name = '2020',
    )

    trace1 = go.Scatterpolar(
        r = [
            data19['pace'].values[0],
            data19['shooting'].values[0],
            data19['passing'].values[0],
            data19['dribbling'].values[0],
            data19['physic'].values[0],
            data19['overall'].values[0],
        ],
        theta = skills,
        fill = 'toself',
        name = '2019',
    )

    trace2 = go.Scatterpolar(
        r = [
            data18['pace'].values[0],
            data18['shooting'].values[0],
            data18['passing'].values[0],
            data18['dribbling'].values[0],
            data18['physic'].values[0],
            data18['overall'].values[0],
        ],
        theta = skills,
        fill = 'toself',
        name = '2018',
    )    

    trace3 = go.Scatterpolar(
        r = [
            data17['pace'].values[0],
            data17['shooting'].values[0],
            data17['passing'].values[0],
            data17['dribbling'].values[0],
            data17['physic'].values[0],
            data17['overall'].values[0],
        ],
        theta = skills,
        fill = 'toself',
        name = '2017',
    )    

    trace4 = go.Scatterpolar(
        r = [
            data16['pace'].values[0],
            data16['shooting'].values[0],
            data16['passing'].values[0],
            data16['dribbling'].values[0],
            data16['physic'].values[0],
            data16['overall'].values[0],
        ],
        theta = skills,
        fill = 'toself',
        name = '2016',
    )

    data = [trace0, trace1, trace2, trace3, trace4]
    layout = go.Layout(
        polar = dict(
            radialaxis = dict(
                visible = True,
                range = [0, 100],

            )
        ),
        showlegend = True,
        title = 'Stat related to {} from 2016 to 2020'.format(name)
    )

    fig = go.Figure(
        data = data,
        layout = layout,
    )
    fig.show()

player_growth('Neymar')