# Imports
import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html, Input, Output
import plotly.express as px
import webbrowser
from jupyter_dash import JupyterDash


def create_HTML_dashboard(df):
    app = JupyterDash(__name__)
    scatter_figure =px.scatter(df, x="song_title", y="views", size="views" , color='channel' ,
                           custom_data=["video_id"], size_max=20, template='plotly_dark', facet_col='channel', facet_col_wrap=3,
                           hover_name='channel', labels= {'channel': 'Top 10 Music Channels', 'views': 'Total Views',  },  
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

    scatter_figure.write_html(f"{pwd}/processed_results/youtube_trending_results_dashboard{datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M')}.html")
  
