import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash
import dash
import numpy as np
import dash_html_components as html

import dash_bootstrap_components as dbc
import dash_html_components as html
import random
import dash_trich_components as dtc
import dash_dangerously_set_inner_html
import pandas as pd
from random import randint
import requests
from sklearn.utils import shuffle
from PIL import Image
import random

import urllib
import urllib.parse

basewidth = 200


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,
    'https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css',
    'https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;700&display=swap',
    'https://fonts.googleapis.com/css2?family=Squada+One&display=swap',
    'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])
server = app.server
app.title= 'Related Titles'

sample=pd.read_csv('archive/sample_tracks.csv')
tracks=sample['id track'].unique().tolist()

algorithm_variants=sample['artists'].unique().tolist()

app.layout =html.Div([html.Div(
                        [
                            

                            
                            html.Div(
                    [
                       html.Div(dcc.Dropdown(id="algo2",options=[{'label': i, 'value': i} for i in algorithm_variants],value='Popularity'),style={'width': '24%','display': 'inline-block','marginRight': 5}),
                    html.Div(dcc.Dropdown(id="algo3",options=[{'label': i, 'value': i} for i in algorithm_variants],value='Contextual',placeholder="Carousel 2 algorithm"),style={'width': '24%','display': 'inline-block','marginRight': 5}),
                    html.Div(dcc.Dropdown(id="algo4",options=[{'label': i, 'value': i} for i in algorithm_variants],value='',placeholder="Carousel 3 algorithm"),style={'width': '24%','display': 'inline-block'}),
                    html.Div(dcc.Dropdown(id="algo5",options=[{'label': i, 'value': i} for i in algorithm_variants],value='',placeholder="Carousel 2 algorithm"),style={'width': '24%','display': 'inline-block','marginRight': 5})]),html.Div([html.Br()]),html.Div(id='page-content'),html.Div([html.Br()]), 
])])

@app.callback(dash.dependencies.Output('page-content', 'children'),[
                                                                   dash.dependencies.Input("algo2", "value"),
                                                                   dash.dependencies.Input("algo3", "value"),
                                                                   dash.dependencies.Input("algo4", "value"),
                                                                   dash.dependencies.Input("algo5", "value")])
def display_page(algo2,algo3,algo4,algo5):
   
    combined=[]
    combined.append(algo2)
    combined.append(algo3)
    combined.append(algo4)
    combined.append(algo5)
    
    combined=list(filter(None, combined))
    num_trays=max(0,len(combined))
    
    tray_name='test1'
    new_tray_name = [tray_name+'_' +x for x in combined]
    tray_name_backup=[tray_name for x in range(0,len(combined))]
    
    tray_name_backup=[]
    
    for loop in range(0,len(combined)):
        
        tray='Ranking algorithm:  '+combined[loop]+' | Micro-genre: '+tray_name
        tray_name_backup.append(tray)
    
    selected_title=sample[sample['artists'].isin(combined)]
    def card_con(imdb):
        id_imdb=imdb
        try:
            content=[
                    html.A(html.Div(html.Iframe(src='https://open.spotify.com/embed/track/'+id_imdb, width="100%" ,height="280"))),
                    dbc.Button("Spotify Page",href="https://open.spotify.com/embed/track/"+id_imdb, color="success")
                          ]
                        
                    
            return content
        
        except:
            1

    
    list_card=[]

    for i in range(0,num_trays):
        tray=new_tray_name[i]
        track_id=selected_title['id track'].unique().tolist()
        
        list_sample=[dbc.Col(dbc.Card(card_con(track_id[x])),style={'width': '90%'}) for x in range(0,len(track_id))]
        
        list_card.append(list_sample)
        
    def cards_dynamic(L,tray_name_subset):
        return html.Div(

            [html.Div([html.Br()]),
                html.Div(html.Div(html.H3(children=tray_name_subset)), style={'color': 'black','text-align': 'center'}),

                        html.Div(dtc.Carousel([
                    html.Div(i) for i in L
                ],
                    slides_to_scroll=3,swipe_to_slide=False,

                    autoplay=False,
                            dots=True,
                    speed=1000,
                            center_mode=False,
                             
                    arrows=False),style={'width': '99%'})
            ]
        )
   
    cards=[cards_dynamic(list_card[x],tray_name_backup[x]) for x in range(0,len(new_tray_name))]
    
    return [html.Div(cards)]



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8402,debug=True,dev_tools_ui=False,dev_tools_props_check=False)