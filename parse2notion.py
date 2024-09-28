from notion_client import Client
import json
from tqdm import tqdm

import dotenv
import os

dotenv.load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DATAPATH = "results.json"

notion = Client(auth=NOTION_TOKEN)


with open(DATAPATH, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)


# data preprocessing
for item in data:
    for key, value in item.items():
        if value == "":
            item[key] = None


for item in tqdm(data):
    properties = {
        "이름": {"title": [{"text": {"content": item["이름"]}}]},
        "커리어": {"multi_select": [{"name": career} for career in item["커리어"]]},
        "관심분야": {"multi_select": [{"name": interest} for interest in item["관심분야"]]},
        "회사": {"multi_select": [{"name": company} for company in item["회사"]]},
        "특징": {"multi_select": [{"name": feature} for feature in item["특징"]]},
        "희망 파트너": {"multi_select": [{"name": partner} for partner in item["희망 파트너"]]},
        "경력": {"number": item["경력"]},
    }

    if item.get("링크드인", None):
        properties["링크드인"] = {"url": item["링크드인"]}

    if item.get("연락처", None):
        properties["연락처"] = {"phone_number": item["연락처"]}

    if item.get("이메일", None):
        properties["이메일"] = {"email": item["이메일"]}
        if type(item["이메일"]) == list:
            properties["이메일"] = {"email": item["이메일"][0]}

    if item.get("MBTI", None):
        properties["MBTI"] = {"select": {"name": item["MBTI"]}}

    if item.get("DISC", None):
        properties["DISC"] = {"select": {"name": item["DISC"]}}

    if item.get("취미", None):
        properties["취미"] = {"multi_select": [{"name": major} for major in item["취미"]]}

    if item.get("전공", None):
        properties["전공"] = {"multi_select": [{"name": major} for major in item["전공"]]}

    if item.get("학교", None):
        properties["학교"] = {"multi_select": [{"name": university} for university in item["학교"]]}

    notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties=properties,
    )
