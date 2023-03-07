import os
import pytchat # crawling realtime comments
import pafy # video information
from dotenv import load_dotenv
import pandas as pd

load_dotenv(verbose=True) # return warning message

# get api key
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
# set up api key on pafy
pafy.set_api_key(YOUTUBE_API_KEY)

# set video id and file path
video_id = 'FJfwehhzIhw'
file_path = './news_ytn_youtube.csv'

# create dataframe
emtpy_frame = pd.DataFrame(columns=['댓글 작성 시간', '댓글 작성자', '댓글 내용'])

# create pychate instance
chat = pytchat.create(video_id=video_id)

while chat.is_alive():
    try:
        for c in chat.get().sync_items():
            print(f"{c.datetime} [{c.author.name}]- {c.message}")
            data = {'댓글 작성 시간': [c.datetime], '댓글 작성자': [c.author.name], '댓글 내용': [c.message]}
            result = pd.DataFrame(data)
            result.to_csv(file_path, mode='a', header=False)
    except KeyboardInterrupt:
        chat.terminate()
        break
