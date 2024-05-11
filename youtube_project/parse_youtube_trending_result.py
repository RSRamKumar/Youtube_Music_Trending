import os
import re
import json
from datetime import date, datetime, time, timedelta

import pandas as pd
from pydantic import BaseModel, Field, computed_field, field_validator

from youtube_api import extract_trending_youtube_videos


def generate_time_duration(time_string: str) -> int:
    """
    Method for transforming the time raw string 'PT3M36S' into a datetime object
    Result: 00:03:36 i.e. 216 seconds
    """
    hour_pattern = re.compile(r"(\d+)H")
    minute_pattern = re.compile(r"(\d+)M")
    second_pattern = re.compile(r"(\d+)S")

    hour_match = hour_pattern.search(
        time_string
    )  # hour_pattern.search(time_string).group(1)/re.search(hour_pattern, time_string).group(1)
    minute_match = minute_pattern.search(
        time_string
    )  # minute_pattern.search(time_string).group(1) /  re.search(minute_pattern, time_string).group(1)
    second_match = second_pattern.search(
        time_string
    )  # second_pattern.search(time_string).group(1) / re.search(second_pattern, time_string).group(1)

    hours = int(hour_match.group(1)) if hour_match else 0
    minutes = int(minute_match.group(1)) if minute_match else 0
    seconds = int(second_match.group(1)) if second_match else 0

    return timedelta(hours=hours,minutes= minutes, seconds=seconds).total_seconds()


class VideoMetaData(BaseModel):
    song_title: str = Field(alias="title")
    published_date: date = Field(alias="publishedAt")
    channel: str = Field(alias="channelTitle")
    language: str = Field(alias="defaultAudioLanguage")

    @field_validator("song_title", mode="before")
    @classmethod
    def get_song_title(cls, song_title: str) -> str:
        """
        Method for stripping the song title field
        """
        return song_title.strip().replace(',','|')
    
    @field_validator("published_date", mode="before")
    @classmethod
    def get_published_date(cls, published_date: str) -> date:
        """
        Method for parsing the date from published_date datetime field
        """
        return  datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").date()


class VideoContentDetails(BaseModel):
    duration_in_seconds: int = Field(alias="duration")

    @field_validator("duration_in_seconds", mode="before")
    @classmethod
    def get_video_duration(cls, duration: str) -> float:
        """
        Method for parsing the duration field
        """
        return generate_time_duration(duration)


class VideoStatistics(BaseModel):
    views_count: int = Field(alias="viewCount")
    likes_count: int = Field(alias="likeCount")


class YoutubeData(BaseModel):
    id: str = Field(repr=False)
    snippet: VideoMetaData
    contentDetails: VideoContentDetails
    statistics: VideoStatistics

    @computed_field(alias="video_url")
    def video_url(self) -> str:
        return f"https://youtu.be/{self.id}"


dag_path = os.getcwd()


def parse_top_10_youtube_music_trending(
    youtube_trending_results_raw: json,
) -> pd.DataFrame:
    """
    Method for parsing the top 10 music from raw json response
    """
    results = [YoutubeData(**item) for item in youtube_trending_results_raw["items"]]

    parsed_result_list = []
    for result in results:
        result_dict = result.model_dump()
        parsed_result_list.append(
            {
                **result_dict["snippet"],
                **result_dict["contentDetails"],
                **result_dict["statistics"],
                **{"video_url": result_dict["video_url"]},
            }
        )

    df = pd.DataFrame(parsed_result_list)
    #df['published_date'] = pd.to_datetime(df['published_date'])
    df.to_csv(
        f"{dag_path}/processed_data/youtube_trending_results_{date.today().strftime('%d-%m-%Y')}.csv",
        index=False,
    )
    return df


if __name__ == "__main__":
    parse_top_10_youtube_music_trending(extract_trending_youtube_videos())
