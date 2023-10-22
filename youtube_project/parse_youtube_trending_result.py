from youtube_project.youtube_api  import extract_trending_youtube_music_videos
import pandas as pd
from datetime import datetime, time
import re
import numpy as np
import os

pwd = os.getcwd()

def generate_time_duration(time_string):
    """
    Method for transforming the time raw string 'PT3M36S' into a datetime object
    """
    hour_pattern = re.compile(r'(\d+)H')
    minute_pattern = re.compile(r'(\d+)M')
    second_pattern = re.compile(r'(\d+)S')

    hour_match = hour_pattern.search(time_string)      # hour_pattern.search(time_string).group(1)/re.search(hour_pattern, time_string).group(1)
    minute_match = minute_pattern.search(time_string)  # minute_pattern.search(time_string).group(1) /  re.search(minute_pattern, time_string).group(1)
    second_match = second_pattern.search(time_string)  # second_pattern.search(time_string).group(1) / re.search(second_pattern, time_string).group(1)

    hours = int(hour_match.group(1)) if hour_match else 0
    minutes = int(minute_match.group(1)) if minute_match else 0
    seconds = int(second_match.group(1)) if second_match else 0

    return time(hours, minutes, seconds)

def parse_top_10_youtube_music_trending(youtube_trending_results_raw):

    youtube_trending_result_list = youtube_trending_results_raw['items']

    parsed_result_list = list()

    for result in youtube_trending_result_list:

        parsed_result_dict = {
            'song_title': result['snippet']['title'].strip(),
            'published_date': result['snippet']['publishedAt'],
            'channel': result['snippet']['channelTitle'],
            'duration': generate_time_duration(result['contentDetails']['duration']),
            'views': result['statistics']['viewCount'],
            'video_url': f"https://youtu.be/{result['id']}"
        }
        parsed_result_list.append(parsed_result_dict)


    df = pd.DataFrame(parsed_result_list)
    df.insert(0, 'datetime_retrieved', datetime.strftime(datetime.now(), '%d-%m-%Y_%H:%M'))
    df.index = np.arange(1, len(df)+1)
    df.to_csv(f"{pwd}/processed_results/youtube_trending_results_{datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M')}.csv", index=False)
    #return df.to_json()


if __name__ == "__main__":
    result = parse_top_10_youtube_music_trending(extract_trending_youtube_music_videos())
    print(result)