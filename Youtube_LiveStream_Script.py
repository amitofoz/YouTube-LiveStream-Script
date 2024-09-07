import requests
import time

API_KEY = 'INSERT API KEY HERE' #Replace with Youtube API Key. 
#Note this API key is used in all requests made to the YouTube API (fetch_category_names, fetch_live_broadcasts, fetch_channel_subscribers, and fetch_concurrent_viewers).
MAX_RESULTS = 50 #Limits each API response to 50 live videos per request.
TOTAL_DESIRED_RESULTS = 9500 #Script will stop processing once it has evaluated 9,500 live streams, the max is 10,000.
SLEEP_TIME = 6  #Waits 6 seconds between API calls to avoid hitting rate limits.
MIN_SUBSCRIBER_COUNT = 50 #Filter channels from 50 subscribers.
MAX_SUBSCRIBER_COUNT = 5000 #Filter channels up to 5,000 subscribers.
MIN_CONCURRENT_VIEWERS = 5 #The livestream must have at least 5 concurrent viewers to be considered.

#SEARCH_URL: Used to find live broadcasts.
#CHANNEL_URL: Used to get statistics, specifically subscriber counts, of the channels broadcasting live.
#VIDEO_URL: Used to get details about the live stream, like the number of concurrent viewers.

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=live&videoCategoryId={}&maxResults={}&regionCode=US&key={}"
CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id={}&key={}"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={}&key={}"


#The 'fetch_category_names' function gets a list of video categories available on YouTube, such as "Music," "Gaming," etc, by making a request to the YouTube API. 
#It returns a dictionary mapping of category IDs to category names.
def fetch_category_names():
    url = "https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=US&key=" + API_KEY
    response = requests.get(url).json()
    categories = {}
    for item in response.get('items', []):
        categories[item['id']] = item['snippet']['title']
    return categories

#The 'fetch_live_broadcasts' function fetches a list of live broadcasts for a specific video category.
#It supports pagination through 'next_page_token' to get more results.
def fetch_live_broadcasts(category_id, next_page_token=''):
    url = SEARCH_URL.format(category_id, MAX_RESULTS, API_KEY)
    if next_page_token:
        url += "&pageToken=" + next_page_token
    response = requests.get(url).json()
    return response

#The 'fetch_channel_subscribers' function retrieves the number of subscribers for a given channel using the YouTube Channels API.
def fetch_channel_subscribers(channel_id):
    response = requests.get(CHANNEL_URL.format(channel_id, API_KEY)).json()
    subscribers = int(response['items'][0]['statistics']['subscriberCount'])
    return subscribers

#The 'fetch_concurrent_viewers' function retrieves the number of concurrent viewers for a live stream using the YouTube Videos API.
def fetch_concurrent_viewers(video_id):
    response = requests.get(VIDEO_URL.format(video_id, API_KEY)).json()
    live_details = response['items'][0].get('liveStreamingDetails', {})
    return int(live_details.get('concurrentViewers', 0))




#The script starts by fetching all YouTube video categories (CATEGORY_NAMES) and processes them one by one.

#For each category:
	#It calls fetch_live_broadcasts to get live videos.
	#For each video, it gets the channel's subscriber count.
	#If the channel has between 50 and 5,000 subscribers, it checks how many people are watching the live stream using fetch_concurrent_viewers.
	#If the stream has more than 5 viewers, it prints the channel's URL and its subscriber/viewer counts.

#This process continues until 9,500 live streams have been evaluated (TOTAL_DESIRED_RESULTS), or there are no more streams to evaluate.


CATEGORY_NAMES = fetch_category_names()
# List of categories to process. Ensure these exist in the CATEGORY_NAMES mapping
CATEGORY_IDS = list(CATEGORY_NAMES.keys())

for category_id in CATEGORY_IDS:
    category_name = CATEGORY_NAMES.get(category_id, "Unknown Category")
    print(f"\nProcessing category: {category_name}\n{'=' * 30}")

    next_page_token = ''
    results_fetched = 0

    while results_fetched < TOTAL_DESIRED_RESULTS:
        broadcasts = fetch_live_broadcasts(category_id, next_page_token)

        for item in broadcasts.get('items', []):
            channel_id = item['snippet']['channelId']
            video_id = item['id']['videoId']
            subscriber_count = fetch_channel_subscribers(channel_id)

            if not MIN_SUBSCRIBER_COUNT <= subscriber_count <= MAX_SUBSCRIBER_COUNT:
                continue

            concurrent_viewers = fetch_concurrent_viewers(video_id)

            if concurrent_viewers > MIN_CONCURRENT_VIEWERS:
                print(f"Channel ID: https://www.youtube.com/channel/{channel_id} has {subscriber_count} subscribers and {concurrent_viewers} viewers on their live stream.")

            results_fetched += 1
            if results_fetched >= TOTAL_DESIRED_RESULTS:
                break

            time.sleep(SLEEP_TIME)

        next_page_token = broadcasts.get('nextPageToken')
        if not next_page_token:
            break
