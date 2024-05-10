import os
import re
import json
from datetime import date, datetime, time

import pandas as pd
from pydantic import BaseModel, Field, computed_field, field_validator

from youtube_api import extract_trending_youtube_videos


def generate_time_duration(time_string: str) -> time:
    """
    Method for transforming the time raw string 'PT3M36S' into a datetime object
    Result: 00:03:36
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

    return time(hours, minutes, seconds)


class VideoMetaData(BaseModel):
    song_title: str = Field(alias="title")
    published_date: datetime = Field(alias="publishedAt")
    channel: str = Field(alias="channelTitle")


class VideoContentDetails(BaseModel):
    duration: time = Field(alias="duration")

    @field_validator("duration", mode="before")
    @classmethod
    def get_video_duration(cls, duration: str) -> time:
        """
        Method for parsing the duration field
        """
        return generate_time_duration(duration)


class VideoStatistics(BaseModel):
    views: int = Field(alias="viewCount")


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
    df.to_csv(
        f"{dag_path}/processed_data/youtube_trending_results_{date.today().strftime('%d-%m-%Y')}.csv",
        index=False,
    )
    return df


if __name__ == "__main__":
    parse_top_10_youtube_music_trending(extract_trending_youtube_videos())
