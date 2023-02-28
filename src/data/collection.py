import csv
import googleapiclient
from googleapiclient.discovery import build

# Set up the YouTube Data API client
api_key = 'AIzaSyBokaV5eqLjEFhwp5rxN37I77BAh95ApZE'
youtube = build('youtube', 'v3', developerKey=api_key)

# Define the search query parameters
query = 'coupon code OR discount code OR promo code OR voucher code OR % off OR use code'
topic_id = '/m/019_rr'
max_results = 50
max_subscribers = 100000
region = "US,CA,UK"
page_token = ''


# Open the CSV file for appending data
with open('youtube.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['datePublished', 'videoId', 'title', 'description', 'channelName']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header if the file is empty
    if csvfile.tell() == 0:
        writer.writeheader()

    # Retrieve multiple pages of search results
    while True:
        # Execute the API request
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=max_results,
            pageToken=page_token,
            # VideoDefinition parameter set to high can ensure videos are of high quality
            videoDefinition="high"
            #channelType='show',
        ).execute()

        # Parse the search results and write to CSV
        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet'
            ).execute()

            for video_result in video_response.get('items', []):
                video_info = {
                    'datePublished': video_result['snippet']['publishedAt'],
                    'videoId': video_id,
                    'title': video_result['snippet']['title'],
                    'description': video_result['snippet']['description'],
                    'channelName': video_result['snippet']['channelTitle']
                }
                writer.writerow(video_info)

        # Check if there are more results to retrieve
        page_token = search_response.get('nextPageToken', None)
        if page_token is None:
            break



# add other labels data labels -> CouponCode,Website,Discount,Expired Date for youtube file
