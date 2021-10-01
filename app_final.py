import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
from dash_table import DataTable
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Dataset Processing

#importing data
data = pd.read_csv('archive/artists_21.csv')

#data cleaning
nonusefulcolumns = ['sofifa_id','player_url','long_name','league_rank']
#nonusefulattributes = data.loc[:,'player_traits':]

df = data.copy()
df=df[0:20000]

df1 = df.drop_duplicates(subset=['artists','old_school'])

df2 = df.drop_duplicates(subset=['artists','old_school'])


# variables for the analysis
skill_player = ['danceability', 'energy', 'mode', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence']
info_player = ['artists','Followers(Mn.)','artist_popularity','Active Years']
labels_table = ['artists','Followers(Mn.)','artist_popularity','Active Years']
player1 = 'Queen'
player2 = 'Taylor Swift'


###################################################   Interactive Components   #########################################
# choice of the players
players_options_over_25 = []
players_options_under_25= []

for i in df1.index:
    players_options_over_25.append({'label': df1['artists'][i], 'value':  df1['artists'][i]})

for i in df2.index:
    players_options_under_25.append({'label': df2['artists'][i], 'value':  df2['artists'][i]})


dropdown_player_over_25 = dcc.Dropdown(
        id='player1',
        options=players_options_over_25,
        value='Queen'
    )

dropdown_player_under_25 = dcc.Dropdown(
        id='player2',
        options=players_options_under_25,
        value='Taylor Swift'
    )

dashtable_1 = dash_table.DataTable(
        id='table1',
        columns=[{"name": col, "id": info_player[idx]} for (idx, col) in enumerate(labels_table)],
        data=df[df['artists'] == player1].to_dict('records'),
        style_cell={'textAlign': 'left',
                    'font_size': '14px'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )


dashtable_2 = dash_table.DataTable(
        id='table2',
        # columns=[{"name": i, "id": i} for i in info_player[::-1]],
        columns=[{"name": col, "id": info_player[::-1][idx]} for (idx, col) in enumerate(labels_table[::-1])],
        data=df[df['artists'] == player2].to_dict('records'),
        style_cell={'textAlign': 'right',
            'font_size': '14px'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )



#data.drop(nonusefulcolumns, axis=1, inplace=True)
#data.drop(nonusefulattributes, axis=1, inplace=True)

########Dash App Layout##########################

app = dash.Dash(__name__,    external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server



controls_player_1 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label('Choose an old-school Artist:'),
                html.Br(),
                dropdown_player_over_25,
            ]
        ),
    ],
    body=True,
    className="controls_players",
)

controls_player_2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label('Choose a new generation Artist:'),
                html.Br(),
                dropdown_player_under_25,
            ]
        ),
    ],
    body=True,
    className="controls_players",
)



def comparison():
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody([

                        html.H1('Artists Comparison'),
                        html.Hr(),

                        dbc.Row([
                            dbc.Col([
                                dbc.Row(controls_player_1),
                                dbc.Row(id='frame1')
                            ],sm=3),
                            dbc.Col(dcc.Graph(id='graph_example'), sm=5, align = 'center'),
                            dbc.Col([
                                dbc.Row(controls_player_2),
                                dbc.Row(id='frame2')
                            ],sm=3),
                        ],justify="between"),
                        dbc.Row([
                            dbc.Col(
                                [dashtable_1,
                                html.Br()],sm=6),
                            dbc.Col(
                                [dashtable_2,
                                html.Br()],sm=6),
                        ]),
                         html.Div([dbc.Row(id="race_chart",style={"border":"1px black solid"})],
            className="pretty_container" ,style={'width': '48%', 'display': 'inline-block'} ),
    html.Div([dbc.Row(id='tracks_artist',style={"border":"1px black solid"})],
            className="pretty_container" ,style={'width': '48%', 'display': 'inline-block'} ),
                    dbc.Row(id="hof"),
                    html.Div([dbc.Row(id="genres",style={"border":"1px black solid"})],
            className="pretty_container" ,style={'width': '98%', 'display': 'inline-block'} ),
                     dbc.Row(id="network"),
                    html.H1('Recommender system for artists using customer streaming'),
                    html.H3('Play with the portal below(Search,Zoom,Neighbors,TSNE etc)',style={'color': 'brown', 'fontSize': 30}),
                    dcc.Link('My blog post on word2vec based recommendations(Movies)', href='https://pub.towardsai.net/build-floating-movie-recommendations-using-deep-learning-diy-in-10-mins-26f585821697',style={'color': 'blue', 'fontSize': 26}),
                    dbc.Row(id="reccos"),html.H1('Conceptually how reccomendations work for spotify'),
                    
                    dbc.Row(id="gif"),
                    
                    
                    ]
                )
            )
        ]
    )
 
#tab2_content =html.Iframe(src="http://thebridge.aka.corp.amazon.com:9053/", width="99%",height="1000" )
#tab3_content =html.Iframe(src="http://thebridge.aka.corp.amazon.com:8402/", width="99%",height="1000" )

app.title= 'Spotify Catalog Data'

app.layout = dbc.Container([
  

        dbc.Tabs(
            [
                dbc.Tab(comparison(), label="Music meets Data"),
                #dbc.Tab(tab2_content, label="ML Model Track popularity prediction"),
                #dbc.Tab(tab3_content, label="Recommendation Engine")
            ], 
        ),
    ],
    fluid=True,
)

#----------------Callbacks for 1st tab, clubs analysis----------------#

@app.callback(
    [   
        Output('graph_example', 'figure'),
        
        Output('table1', 'data'),
        
        Output('table2', 'data'),
        Output('frame1', 'children'),
        Output('frame2', 'children'),
        Output('race_chart', 'children'),
        Output('tracks_artist','children'),
        Output('hof','children'),
        Output('genres','children'),
        Output('network','children'),
        Output('reccos','children'),
        Output('gif','children')
    ],
    [
        Input('player1', 'value'),
        Input('player2', 'value')
    ]
)

###############################################   radar plot   #####################################################

def tab_1_function(player1, player2):

    # scatterpolar
    df1_for_plot = pd.DataFrame(df1[df1['artists'] == player1][skill_player].iloc[0])
    df1_for_plot.columns = ['score']
    df2_for_plot = pd.DataFrame(df2[df2['artists'] == player2][skill_player].iloc[0])
    df2_for_plot.columns = ['score']
    list_scores = [df1_for_plot.index[i].capitalize() +' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    text_scores_1 = player1
    for i in list_scores:
        text_scores_1 += '<br>' + i

    list_scores = [df2_for_plot.index[i].capitalize() +' = ' + str(df2_for_plot['score'][i]) for i in range(len(df2_for_plot))]
    text_scores_2 = player2

    for i in list_scores:
        text_scores_2 += '<br>' + i

    fig = go.Figure(data=go.Scatterpolar(
        r=df1_for_plot['score'],
        theta=df1_for_plot.index,
        fill='toself', 
        marker_color = 'rgb(45,0,198)',   
        opacity =1, 
        hoverinfo = "text" ,
        name = text_scores_1,
        text  = [df1_for_plot.index[i] +' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    ))


    fig.add_trace(go.Scatterpolar(
        r=df2_for_plot['score'],
        theta=df2_for_plot.index,
        fill='toself',
        marker_color = 'rgb(255,171,0)',
        hoverinfo = "text" ,
        name= text_scores_2,
        text  = [df2_for_plot.index[i] +' = ' + str(df2_for_plot['score'][i]) for i in range(len(df2_for_plot))]
        ))

    print(fig)
    fig.update_layout(
        polar=dict(
            hole=0.1,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type='linear',
                range=[0, 1],
                angle=90,
                showline=False,
                showticklabels=False, ticks='',
                gridcolor='black'),
                ),
        width = 550,
        height = 550,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="black",
        font_size= 15
    )

    
    table_updated1 = df[df['artists'] == player1].to_dict('records')


    table_updated2 = df[df['artists'] == player2].to_dict('records')


    
    artist_id1=df1[df1['artists']==player1]['artist_id'].unique().tolist()[0]
    artist_id2=df1[df1['artists']==player2]['artist_id'].unique().tolist()[0]

    frame1=html.Iframe(src='https://open.spotify.com/embed/artist/'+artist_id1, width="100%" ,height="280")

    frame2=html.Iframe(src='https://open.spotify.com/embed/artist/'+artist_id2, width="100%" ,height="280")
    race_chart=html.Iframe(src="https://flo.uri.sh/visualisation/7055448/embed", width="98%",height="600" )
    
    hof=html.Iframe(src="https://flo.uri.sh/visualisation/7062766/embed", width="98%",height="700" )
   
    tracks_artist=html.Iframe(src="https://flo.uri.sh/visualisation/7055989/embed", width="100%",height="600" )
    
    genres=html.Iframe(src="https://flo.uri.sh/visualisation/7062896/embed", width="90%",height="500" )
    catalogue=html.Iframe(src="https://flo.uri.sh/visualisation/7063126/embed", width="90%",height="500" )
    genres=html.Iframe(src="https://public.tableau.com/views/Spotify_Analysis_16296762745890/dash_board_final?:linktarget=_blank&:iframeSizedToWindow=true&:embed=y&:toolbar=no&:showAppBanner=false&:display_count=no&:showVizHome=no&:device=desktop", width="99%",height="2000" )
    
    network=html.Iframe(src="https://flo.uri.sh/visualisation/7104615/embed", width="95%",height="600")
    reccos=html.Iframe(src="https://projector.tensorflow.org/?config=https://gist.githubusercontent.com/ravi07bec/220f8c079f2992e2d30bcc0e74b47a70/raw/22b7aa15783c17ebea485d9501b452ed221cb6a8/music_vector.json", width="95%",height="650"  )
    gif=html.Iframe(src="https://miro.medium.com/max/1260/1*xbNM_CnEIWQtGbsLmZtE-A.gif", width="95%",height="750")
    


    return fig, table_updated1, table_updated2,frame1,frame2,race_chart,tracks_artist,hof,genres,network,reccos,gif



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8401,debug=True,dev_tools_ui=False,dev_tools_props_check=False)

