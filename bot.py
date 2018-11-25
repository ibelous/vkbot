import requests
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import re
import Handler
import random

red = re.compile(r'/r')


def main():
    try:
        chat_bot = Handler.BotHandler(open("bottoken.txt", 'r').readline())
    except Exception:
        print("Create file with vk info.")
    upload = VkUpload(chat_bot.vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(chat_bot.vk_session)
    session = requests.Session()
    print("Launched...")
    print(chat_bot.d.keys())
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
            attachments = []
            if red.match(event.text):
                last_chat_text = red.sub('', event.text)
                s = chat_bot.r(last_chat_text)
                image = session.get(s, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                chat_bot.send_photo(event, attachments)
            elif chat_bot.memes_exists:
                text = event.text.strip("!.,?")
                for word in text.split():
                    if word.lower() in chat_bot.d.keys():
                        nums = [i for i in range(len(chat_bot.d.get(word.lower())))]
                        i = random.choice(nums)
                        image = session.get(chat_bot.d.get(word.lower())[i], stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                        chat_bot.send_photo(event, attachments)
                        break
            for word in event.text.split():
                word += '.'
                if word.lower().find('игор') != -1 and (word[0] == 'и' or word[4] != 'ь'):
                    chat_bot.send_message(event, 'Игорь, блять!')
                    break
            print('ok')


if __name__ == '__main__':
    main()
