import scratchattach as scratch
from huggingface_hub import InferenceClient
import warnings
import os

warnings.filterwarnings('ignore', category=scratch.LoginDataWarning)
session = scratch.login(os.environ['USERNAME'], os.environ['PASSWORD'])
client = InferenceClient(os.environ['HF_TOKEN')
project = session.connect_project(1195042681)
comment_object = project.comments(limit=1, offset=0)[0]


def generate(content: str):
    return client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
    ).choices[0].message


def start():
    global comment_object, project
    while True:
        if not comment_object.content == project.comments(limit=1, offset=0)[0].content:
            comment_object = project.comments(limit=1, offset=0)[0]
            comment = comment_object.content
            session.connect_user(comment_object.author_name).follow()
            print(comment)
            response = generate(f"Respond to this comment if you were british: {comment}").content
            print(response[0:500])
            project.reply_comment(response[0:500], parent_id=comment_object.id)
        comment_object = project.comments(limit=1, offset=0)[0]


start()
