# Imports
import os
import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html, Input, Output
import plotly.express as px
import webbrowser
from dash import Dash
from datetime import datetime, time, date



def create_HTML_dashboard(file_path):
    df = pd.read_csv(file_path)
    app = Dash(__name__)
    scatter_figure =px.scatter(df, x="song_title", y="views_count", size="views_count" , color='channel' ,
                           custom_data=["video_url"], size_max=20, template='plotly_dark', facet_col='channel', facet_col_wrap=3,
                           hover_name='channel', labels= {'channel': 'Top 10 Music Channels', 'views_count': 'Total Views',  },  
                           title='Trending Musics in India'
                            )
    scatter_figure.update_layout(width=1200, height=500, title_x=0.5)
    scatter_figure.update_xaxes(title='', showticklabels=False)

    app.layout = html.Div([
    html.Div([dcc.Graph(id='scatterplot', figure=scatter_figure)]),

])

    @app.callback(
    Output('scatterplot', 'figure'),
    Input('scatterplot', 'clickData'))
    def open_url(clickData):
        if clickData:
            webbrowser.open(clickData["points"][0]["customdata"][0])

    output_file_name = f"youtube_trending_results_dashboard_{date.today().strftime('%d-%m-%Y')}.html"
    path = os.getcwd()
    scatter_figure.write_html(f'{path}/{output_file_name}')
    return f'{path}/{output_file_name}'



if __name__ == "__main__":
    create_HTML_dashboard(file_path)
