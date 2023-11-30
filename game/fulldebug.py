import pyaudio
import time
import threading
import wave
import requests
import json
import pdb
import base64
import urllib
import os
import wget

API_KEY = "oLFWiwZhHcW83Hqrl2hwapTy"
SECRET_KEY = "1n2yxFPqwt7jCc339HZNKmQDTRumV0Na"

def postVoiceToword():
        
    url = "https://vop.baidu.com/pro_api"
    path = "D:\\deskpet\\game\\11.wav"
    # speech 可以通过 get_file_content_as_base64("C:\fakepath\2.wav",False) 方法获取
    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "eK5WZo9zhO1Lci0HQlfiUOhEKc3LxLAd",
        "token": get_access_token(),
        "dev_pid": 80001,
        "speech":get_file_content_as_base64(path, False),
        "len": os.path.getsize(path)
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # print(len(get_file_content_as_base64("D:\\deskpet\\game\\ym.mp3", False)))
    response = requests.request("POST", url, headers=headers, data=payload)
    user_dict = json.loads(response.text)
    reply = user_dict["result"][0]
    return reply
    

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
 
    def start(self):
        threading._start_new_thread(self.__recording, ())
 
    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input_device_index = 1,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
 
        stream.stop_stream()
        stream.close()
        p.terminate()
 
    def stop(self):
        self._running = False
 
    def save(self, filename):
 
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("Saved")

def get_access_token_llm():
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


def llmreply(content):
     
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + get_access_token_llm()
    
    payload = json.dumps({
         "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    # pdb.set_trace()
    # print(response.text)
    user_dict = json.loads(response.text)
    return user_dict['result']

def wordToVoice(text):
        
    url = "https://aip.baidubce.com/rpc/2.0/tts/v1/create?access_token=" + get_access_token()
    
    payload = json.dumps({
        "text": text,
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
 
if __name__ == "__main__":
 
    for i in range(1, 2):
        a = int(input('请输入相应数字开始:'))
        if a == 1:
            rec = Recorder()
            begin = time.time()
            print("Start recording")
            rec.start()
            b = int(input('请输入相应数字停止:'))
            if b == 2:
                print("Stop recording")
                rec.stop()
                fina = time.time()
                t = fina - begin
                print('录音时间为%ds' % t)
                rec.save("1%d.wav" % i)
    reply = postVoiceToword()
    print(reply)
    llmAns = llmreply(reply)
    print(llmAns)
    wordToVoice(llmAns)