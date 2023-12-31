import googleapiclient.discovery


def extract_trending_youtube_music_videos():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "xxxxxxxxxxxxxxxxxxxxxxx"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.videos().list(
        part="contentDetails,id,snippet,statistics",
        chart="mostPopular",
        maxResults=10,
        regionCode="IN",
        videoCategoryId="10"
    )
    response = request.execute()

    return response


if __name__ == "__main__":
    extract_trending_youtube_music_videos()
