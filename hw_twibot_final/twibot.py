import tweepy
import re
from credentials import *
import random

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## Так писать твиты: (не в ответ кому-то)
##tweet = "Привет! Я буду раздражать всех, кто пишет в твиттер про ШЛ."
##api.update_status(tweet)


## Так выводить последний твит
##my_last_tweet = api.user_timeline(count=1)[0]
##print(my_last_tweet.id, my_last_tweet.user.screen_name, my_last_tweet.text)


## Так отвечать на чужие твиты, т.е. в апдейт статус надо добавить ин реплай ту статус айди
##my_last_tweet = api.user_timeline(count=1)[0]
##tweet_reply = "Я буду отвечать на ваши твиты примерно так."
##api.update_status(tweet_reply, in_reply_to_status_id=my_last_tweet.id)


## Непонятно почему не работает поиск: ищет не так, как должен, ШЛ вообще не ищет
##i = 0
##for tweet in tweepy.Cursor(api.search, q='ШЛ').items():
##    print(tweet.user.screen_name, tweet.text, '\n')
##    i += 1
##    if i >= 5:
##        break

class LingSchoolListener(tweepy.StreamListener):

    def on_status(self, status):
        with open ('sayings.txt', 'r', encoding = 'utf-8') as f:
            sayings = f.readlines()
        tweettext = random.choice(sayings)
        if status.user.screen_name != "lingschool_bot":
            
            api.update_status('@{} {} https://twitter.com/{}/status/{}'.format(
                    status.user.screen_name, 
                    tweettext,
                    status.user.screen_name,
                    status.id
                ), 
                              in_reply_to_status_id=status.id)  # постим рандомную фразу в ответ

        
    def on_error(self, status_code):
        if status_code == 420:
            # если окажется, что мы посылаем слишком много запросов, то отсоединяемся
            return False
        # если какая-то другая ошибка, постараемся слушать поток дальше
        return True

def main():
    lingListener = LingSchoolListener()
    myStream = tweepy.Stream(auth = api.auth, listener=lingListener)

    myStream.filter(track=['школа лингвистики', 'школы лингвистики', 'школу лингвистики', 'школе лингвистики', 'школой лингвистики', 'школа ленгвистики', 'школы ленгвистики', 'школу ленгвистики', 'школе ленгвистики', 'школой ленгвистики','ШЛ'])
if __name__ == '__main__':
    main()
