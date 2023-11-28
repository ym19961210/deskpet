import requests
import json
import pdb
import wget


API_KEY = "oLFWiwZhHcW83Hqrl2hwapTy"
SECRET_KEY = "1n2yxFPqwt7jCc339HZNKmQDTRumV0Na"

def main():
        
    url = "https://aip.baidubce.com/rpc/2.0/tts/v1/query?access_token=" + get_access_token()
    
    payload = json.dumps({
        "task_ids": [
            "6565d5f0ae1afa000153f621"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    user_dict = json.loads(response.text)

    for item in user_dict['tasks_info']:
        url = item['task_result']['speech_url']
        print(item['task_result']['speech_url'])
        # response = requests.get(url, stream=True)
        
        filename = wget.download(url, out='ym.mp3')
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
