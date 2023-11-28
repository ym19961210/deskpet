import requests
import json
import pdb
import wget
import time

API_KEY = "oLFWiwZhHcW83Hqrl2hwapTy"
SECRET_KEY = "1n2yxFPqwt7jCc339HZNKmQDTRumV0Na"

def main():
        
    url = "https://aip.baidubce.com/rpc/2.0/tts/v1/create?access_token=" + get_access_token()
    
    payload = json.dumps({
        "text": "你自己说的，你那天突然对我说，老公，我是一个牛憨笨雕像，我说，别这么说自己。你说，不，老公，我就是一个牛憨笨雕像。我说好吧，你就是一个牛憨笨雕像，你说，嘿嘿",
        "format": "mp3-16k",
        "voice": 5003,
        "lang": "zh",
        "speed": 5,
        "pitch": 5,
        "volume": 5,
        "enable_subtitle": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    user_dict = json.loads(response.text)
    tsk_id = user_dict['task_id']



    url = "https://aip.baidubce.com/rpc/2.0/tts/v1/query?access_token=" + get_access_token()
    
    payload = json.dumps({
        "task_ids": [
            tsk_id
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    user_dict = json.loads(response.text)

    status = user_dict["tasks_info"][0]["task_status"]
    if status == "Failure":
        print("Failure")
        return -1
    
    while status == "Running":
        time.sleep(1)
        response = requests.request("POST", url, headers=headers, data=payload)
        user_dict = json.loads(response.text)
        status = user_dict["tasks_info"][0]["task_status"]
    

    for item in user_dict['tasks_info']:
        url = item['task_result']['speech_url']
        print(item['task_result']['speech_url'])
        # response = requests.get(url, stream=True)
        
        filename = wget.download(url, out='ym1.mp3')
    print(response.text)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
