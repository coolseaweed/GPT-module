from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pandas as pd
from tqdm import tqdm

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
DATA_PATH = "self_introduce_data.csv"

client = OpenAI(api_key=API_KEY)


OUTPUT_FORMAT = """
{
"이름" : `json의 key`, 
"커리어": `경력을 나타낼 수 있는 직업 키워드 예를 들어 PM, PO, 개발자, CEO 등등 type: list`,
"관심분야": `관심분야를 알 수 있는 키워드 type: list`,
"회사": `자기 소개 중 언급된 회사 키워드 type: list`,
"특징": `업무 성향 등을 분석해서 키워드로 나열하기 type: list`,
"희망 파트너": "찾고있는 사람을 키워드로 나열하기 type: list",
"경력": "총 경력을 계산해서 나타내줘 type: int",
"링크드인" : "만약 linkedin 주소를 남겼다면 추가해줘",
"연락처": "만약 연락처에 대한 정보가 있다면 추가해줘",
"이메일": "만약 이메일에 대한 정보가 있다면 추가해줘",
"MBTI": "만약 MBTI에 대한 정보가 있다면 추가해줘",
"DISC": "만약 DISC에 대한 정보가 있다면 추가해줘",
"취미": "만약 취미에 대한 정보가 있다면 추가해줘 type: list",
"전공": "만약 전공에 대한 정보가 있다면 추가해줘 type: list",
"학교": "만약 학교에 대한 정보가 있다면 추가해줘 type: list"
}
"""


def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data.to_dict(orient="records")


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


# data = load_json(DATA_PATH)
data = load_csv(DATA_PATH)


results = []


for item in tqdm(data):
    v = item["introduce"]

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""
                내가 자기소개 데이터를 입력하면 아래의 OUTPUT FORMAT에 맞는 키워드들을 분석해서 추출해줘.
                OUTPUT FORMAT: \n{OUTPUT_FORMAT}
                """,
            },
            {"role": "user", "content": v},
        ],
    )

    message = response.choices[0].message.content
    parsed_message = json.loads(message)
    results.append(parsed_message)

with open("results.json", "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)
