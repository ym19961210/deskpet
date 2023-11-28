
import requests
import json
import pdb

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Cg8aiOTqiB18gTVPegP8HXEI&client_secret=xVWOOdlKmMeOZFmREjcLE4rWjYzoGCKN"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def main():
     
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + get_access_token()
    
    payload = json.dumps({
         "messages": [
            {
                "role": "user",
                "content": "你认识程序员小明兄吗？"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    # pdb.set_trace()
    print(response.text)
    user_dict = json.loads(response.text)
    print(user_dict['result'])

if __name__ == '__main__':
    main()