# Imports
import os
import webbrowser
from datetime import date

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


def create_HTML_dashboard(file_path):
    df = pd.read_csv(file_path)
    app = Dash(__name__)
    scatter_figure = px.scatter(
        df,
        x="song_title",
        y="views_count",
        size="views_count",
        color="channel",
        custom_data=["video_url"],
        size_max=50,
        template="plotly_dark",
        hover_name="channel",
        labels={
            "channel": "Music Channel Name",
            "views_count": "Total Views",
            "song_title": "Title of Song",
        },
        title="Trending Musics in India",
    )
    scatter_figure.update_layout(autosize=True, title_x=0.5)
    scatter_figure.update_xaxes(title="Different Songs", showticklabels=False)

    app.layout = html.Div(
        [
            html.Div([dcc.Graph(id="scatterplot", figure=scatter_figure)]),
        ]
    )

    @app.callback(Output("scatterplot", "figure"), Input("scatterplot", "clickData"))
    def open_url(clickData):
        if clickData:
            webbrowser.open(clickData["points"][0]["customdata"][0])

    output_file_name = (
        f"youtube_trending_results_dashboard_{date.today().strftime('%d-%m-%Y')}.html"
    )
    path = os.getcwd()
    scatter_figure.write_html(f"{path}/{output_file_name}")
    return f"{path}/{output_file_name}"


if __name__ == "__main__":
    file_path = "youtube_trending_results_11-05-2024.csv"
    create_HTML_dashboard(file_path)


# if __name__ == "__main__":
#     app.run()
