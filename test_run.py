# %%
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pandas as pd
from tqdm import tqdm
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
DATA_PATH = Path("data/Y-combinator-portfolio.csv")
OUTPUT_PATH = "results/" + DATA_PATH.stem + ".json"
client = OpenAI(api_key=API_KEY)


# %%
def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data.to_dict(orient="records")


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


# data = load_json(DATA_PATH)
data = load_csv(DATA_PATH)


# %%

OUTPUT_FORMAT = """
json
{
"이름": "회사 이름 type: str", 
"현상": "현재 회사에서 풀고있는 문제의 현상 type: list",
"문제": "현재 풀고 있는 회사의 문제 정의 type: list",
"솔루션": "현재 회사에서 제시하는 해결방안 type: str",
"서비스": "현재 회사에서 제공하는 서비스 type: list",
"경쟁사": "현재 회사의 경쟁사 type: list",
"경쟁력": "현재 회사의 경쟁우위로 가지는 서비스 특징 차별점 type: str",
"시장크기": "현재 회사가 목표로 하는 시장의 크기 (단위 1000 달러) type: int",
"한국의 비슷한 서비스": "한국에서 비슷한 서비스를 제공하는 회사들 type: list",
"매출액": "현재 회사 매출액 (단위 1000 달러) type: int",
"시가총액": "현재 회사 시가총액 (단위 1000 달러) type: int",
}
"""

INPUT_PROMPT = f"""
너는 전문 기업 분석가야. 내가 Y-combinator의 포트폴리오 데이터를 입력하면 아래의 OUTPUT FORMAT에 맞는 키워드들을 분석해서 추출해줘.
OUTPUT FORMAT: \n{OUTPUT_FORMAT}
"""

# %%
results = []

for idx, item in enumerate(tqdm(data[1476:])):
    try:
        item_str = json.dumps(item, ensure_ascii=False)
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": INPUT_PROMPT,
                },
                {"role": "user", "content": item_str},
            ],
        )

        message = response.choices[0].message.content
        parsed_message = json.loads(message)
        results.append(parsed_message)

        print(parsed_message)
        # JSON 파일에 새로운 결과를 추가 (실시간으로)
        with open(OUTPUT_PATH, "a", encoding="utf-8") as json_file:
            # 첫 번째 항목이 아니라면 콤마 추가
            if idx > 0:
                json_file.write(",\n")
            json.dump(parsed_message, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)
        continue


# with open(OUTPUT_PATH, "w", encoding="utf-8") as json_file:
#     json.dump(results, json_file, ensure_ascii=False, indent=4)
