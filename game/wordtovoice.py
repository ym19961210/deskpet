import requests
import json

API_KEY = "oLFWiwZhHcW83Hqrl2hwapTy"
SECRET_KEY = "1n2yxFPqwt7jCc339HZNKmQDTRumV0Na"

def main():
        
    url = "https://aip.baidubce.com/rpc/2.0/tts/v1/create?access_token=" + get_access_token()
    
    payload = json.dumps({
        "text": "我是一个牛憨笨雕像",
        "format": "mp3-16k",
        "voice": 0,
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
