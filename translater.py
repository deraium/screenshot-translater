import requests
import json
import urllib.parse
import time
import re

re_get_qtv = r'var qtv = "(.+?)"'
re_get_qtk = r'var qtk = "(.+?)"'


def read_headers():
    headers = {}
    with open("headers.txt", "r") as f:
        for line in f.readlines():
            line = line.strip().split(":", 1)
            if len(line) == 2:
                headers[line[0].strip()] = line[1].strip()
    return headers


def write_datas(datas_dict):
    results = []
    for k, v in datas_dict.items():
        results.append(f"{k}={v}")
    return "&".join(results)


def get_qt_datas():
    qtv = ""
    qtk = ""
    request = requests.get("https://fanyi.qq.com")
    request.raise_for_status()
    content = request.text
    match_qtv = re.search(re_get_qtv, content)
    if match_qtv:
        qtv = match_qtv.group(1)
    match_qtk = re.search(re_get_qtk, content)
    if match_qtk:
        qtk = match_qtk.group(1)
    return qtv, qtk


url = "https://fanyi.qq.com/api/translate"
url_test = "http://www.httpbin.org/post"
headers = read_headers()
qtv, qtk = get_qt_datas()
datas = {}


def translate(text: str):
    datas["source"] = "auto"
    datas["target"] = "zh"
    datas["sourceText"] = text
    datas["qtv"] = qtv
    datas["qtk"] = qtk
    datas["sessionUuid"] = f"translate_uuid{int(time.time())}"
    headers["Cookie"] = f"qtk={qtk}"
    request = requests.post(
        url, data=urllib.parse.urlencode(datas, encoding="utf-8"), headers=headers
    )
    request.raise_for_status()
    return_datas = json.loads(request.text)
    try:
        results = []
        for result in return_datas["translate"]["records"]:
            result = result["targetText"].strip()
            if len(result) == 0:
                continue
            results.append(result)
        return "\n".join(results)
    except:
        return ""


if __name__ == "__main__":
    print(translate("The cat sat on the mat."))
