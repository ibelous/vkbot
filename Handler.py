import vk_api
import praw
import os.path
import re
import random


class BotHandler:

    def __init__(self, token):
        login, password = token.split()[0], token.split()[1]
        self.vk_session = vk_api.VkApi(login, password)

        try:
            self.vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        try:
            rinfo = open("redditinfo.txt", 'r').read().split()
            reddit_id = rinfo[0]
            reddit_secret = rinfo[1]
            reddit_agent = rinfo[2]
        except Exception:
            print("Create valid file with reddit info.")
        self.reddit = praw.Reddit(client_id=reddit_id,
                                  client_secret=reddit_secret,
                                  user_agent=reddit_agent)
        if os.path.exists("memesdata.txt"):
            memesdata = open("memesdata.txt", 'r')
            self.memes_exists = True
            self.d = {}
            for line in memesdata:
                if re.match(r'http', line):
                    self.d[tmp].append(line.strip())
                else:
                    line = line.rstrip()
                    self.d.setdefault(line, [])
                    tmp = line
            memesdata.close()

    def r(self, last_chat_text):
        if last_chat_text == '':
            subreddit = 'dankmemes'
            subs = [k for k in self.reddit.subreddit(subreddit).hot()]
        else:
            text = last_chat_text.split()
            try:
                subreddit = text[0]
                if len(text) > 1:
                    if text[1] == 'hot':
                        subs = [k for k in self.reddit.subreddit(subreddit).hot()]
                    elif text[1] == 'rising':
                        subs = [k for k in self.reddit.subreddit(subreddit).rising()]
                    elif text[1] == 'new':
                        subs = [k for k in self.reddit.subreddit(subreddit).new()]
                    elif text[1] == 'gilded':
                        subs = [k for k in self.reddit.subreddit(subreddit).gilded()]
                    else:
                        subs = [k for k in self.reddit.subreddit(subreddit).top()]
                else:
                    subs = [k for k in self.reddit.subreddit(subreddit).top()]
            except Exception:
                subreddit = 'dankmemes'
                subs = [k for k in self.reddit.subreddit(subreddit).top()]
        nums = [i for i in range(len(subs))]
        while True:
            i = random.choice(nums)
            try:
                subs[i].preview
                break
            except Exception:
                nums.remove(i)
        s = subs[i]
        return s.preview['images'][0]['source']['url']

    def send_message(self, event, message):
        vk = self.vk_session.get_api()
        if event.from_user:
            vk.messages.send(
                user_id=event.user_id,
                message=message
            )
        else:
            vk.messages.send(
                chat_id=event.chat_id,
                message=message
            )

    def send_photo(self, event, attachments):
        vk = self.vk_session.get_api()
        if event.from_user:
            vk.messages.send(
                user_id=event.user_id,
                attachment=','.join(attachments),
                message=''
            )
        else:
            vk.messages.send(
                chat_id=event.chat_id,
                attachment=','.join(attachments),
                message=''
            )
