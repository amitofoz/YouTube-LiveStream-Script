YouTube Livestream Filtering Script


Overview:
The Python script filters YouTube livestreams based on the number of subscribers to the channel and the number of concurrent viewers on the livestream.

Features:
Fetch live YouTube videos based on video categories.
Filter channels by the number of subscribers.
Filter livestreams by concurrent viewers.
Uses pagination to evaluate up to 9,500 live streams per run.

Prerequisites:
  Before running the script, ensure the following requirements are met:
  * Python 3.x is installed on your machine.
  * requests library is installed:
      pip install requests
  * A valid YouTube Data API key.

Setup Instructions:
  1) Clone the Repository: Clone the GitHub repository to your local machine:
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository

  2) Obtain a YouTube API Key:
    Go to the Google Cloud Console.
    Create a new project and enable the YouTube Data API v3.
    Generate an API key and copy it.

  3) Configure the Script: Open the Python script and insert your API key where indicated:
     API_KEY = 'YOUR_API_KEY'
     
  4) Run the Script: To run the script, navigate to the directory where it's stored and use the following command:
     python your_script_name.py
     
Script Parameters:
  MAX_RESULTS: The number of results to fetch per API call. Default is 50.
  TOTAL_DESIRED_RESULTS: The total number of results to process. Default is 9500.
  SLEEP_TIME: Time in seconds between API requests to avoid hitting rate limits. Default is 6.
  MIN_SUBSCRIBER_COUNT: The minimum number of subscribers for a channel to be considered. Default is 50.
  MAX_SUBSCRIBER_COUNT: The maximum number of subscribers for a channel to be considered. Default is 5000.
  MIN_CONCURRENT_VIEWERS: The minimum number of concurrent viewers required on a livestream. Default is 5.

License:
  This project is licensed under the MIT License - see the LICENSE file for details.
