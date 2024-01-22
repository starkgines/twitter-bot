import tweepy as tw
import keys

def api_V1():
    """the auth function 

    Returns:
        object: tw auth
    """
    auth = tw.OAuthHandler(keys.api_key,keys.api_secret)
    auth.set_access_token(keys.access_token,keys.access_token_secret)

    return tw.API(auth)


def api_V2() -> tw.Client:
    """Get twitter conn 2.0"""
    client = tw.Client(
        consumer_key=keys.api_key,
        consumer_secret=keys.api_secret,
        access_token=keys.access_token,
        access_token_secret=keys.access_token_secret,
    )

    return client

def tweet(apiV1: tw.API,apiV2: tw.Client, message: str, image_path = None):
    """Post the tweet into the tweeter bot account

    Args:
        api (tw.API): recibe the out put of the function api
        message (str): recibe a string to post into tweeter
        image_path (_type_, optional): optal if you want post your messege with a image. Defaults to None.
    """

    if image_path:
        media = apiV1.media_upload(filename=image_path)
        media_id = media.media_id
        apiV2.create_tweet(text=message, media_ids=[media_id])
    else: 
         apiV2.create_tweet(message)
    
    print('Tweeted successfully')



if __name__ == '__main__':
    apiV1 = api_V1()
    apiV2 = api_V2()
    
    tweet(apiV1,apiV2,'Hello word! Im a bot', 'test_x_post.jpg')


