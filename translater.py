import requests
import json
import html


def read_headers():
    headers = {}
    with open("headers.txt", "r") as f:
        for line in f.readlines():
            line = line.strip().split(":", 1)
            if len(line) == 2:
                headers[line[0].strip()] = line[1].strip()
    return headers


def read_datas():
    datas = {}
    with open("datas.txt", "r") as f:
        lines = f.read().split("&")
        for line in lines:
            line = line.strip().split("=", 1)
            if len(line) == 2:
                datas[line[0].strip()] = line[1].strip()
    return datas


def write_datas(datas_dict):
    result = ""
    for k, v in datas_dict.items():
        result += f"{k}={v}&"
    return result[:-1]


url = "https://fanyi.qq.com/api/translate"
url_test = "http://www.httpbin.org/post"
headers = read_headers()
datas = read_datas()


def translate(text: str):
    lines = text.replace(" ", "+").splitlines()
    text = "%0A".join(lines)
    datas["sourceText"] = html.escape(text)
    request = requests.post(
        url, data=write_datas(datas).encode("utf-8"), headers=headers
    )
    request.raise_for_status()
    return_datas = json.loads(request.text)
    try:
        results = []
        for result in return_datas["translate"]["records"]:
            result = result["targetText"].strip()
            if len(result) == 0:
                continue
            print(result)
            results.append(result)
        return "\n".join(results)
    except Exception as e:
        print(e)
        return ""
