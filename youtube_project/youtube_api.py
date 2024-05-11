import googleapiclient.discovery


def extract_trending_youtube_videos():
    """
    Method for extracting the Youtube Trending data
    for the region India (IN) and
    music category (10)
    """
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = 'xxx'

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.videos().list(
        part="contentDetails,id,snippet,statistics",
        chart="mostPopular",
        maxResults=30,
        regionCode="IN",
        videoCategoryId="10"
    )
    response = request.execute()

    return response


if __name__ == "__main__":
    extract_trending_youtube_videos()
