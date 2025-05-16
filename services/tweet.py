from .twitter_auth import api, client

def upload_media(image_path):
    # Upload the image
    media = api.media_upload(image_path)
    return media.media_id

def tweet(content, image_path=None):
    if image_path:
        # Upload the image
        media_id = upload_media(image_path)
        # Post a tweet with image
        response = client.create_tweet(text=content, media_ids=[media_id])
    else:
        # Post a tweet without image
        response = client.create_tweet(text=content)

    # Check if the tweet was successful
    if response.data:
        print("Tweet posted successfully!")
        return response.data['id']
    else:
        print("Failed to post tweet.")
        return None