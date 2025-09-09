import scrapetube

playlist_id = "PLn5vww_8o5KvzqXM5UUgR9AjGW-zHxlP_"  # Your playlist ID
videos = scrapetube.get_playlist(playlist_id)

for video in videos:
    print(video['videoId'])
