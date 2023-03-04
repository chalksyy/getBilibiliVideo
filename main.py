import json
import subprocess
import requests
from bs4 import BeautifulSoup

def getVideo(url, headers):
    # 获取页面信息
    htmlValue = requests.get(url, headers=headers)
    # 把页面信息存储到htmlValue.html，分析代码构成，找到视频连接在哪个位置，可不做
    with open('htmlValue.html', 'w', encoding='utf-8') as f:
        f.write(htmlValue.text)

    # 使用beautifulsoup提取视频连接所在的script标签内容
    htmlValueBs = BeautifulSoup(htmlValue.text, features="lxml")
    script = htmlValueBs.find_all('script')[2].contents[0]
    # 去掉script前面的“window.__playinfo__=”，然后保存到htmlValue.txt文件中
    script = script.replace('window.__playinfo__=', '')
    with open('htmlValue.txt', 'w', encoding='utf-8') as f:
        f.write(script)

    # 将json字符串转换为字典
    urlDic = ''
    with open('htmlValue.txt', 'r', encoding='utf-8') as f:
        count = 0
        jsonStr = ''
        for line in f:
            line.strip()
            for s in line:
                if s == '{':
                    count += 1
                elif s == '}':
                    count -= 1
                jsonStr += s
                if count == 0:
                    urlDic = json.loads(jsonStr)
                    break
            break
    # 提取字典中视频和音频链接
    videoUrl = urlDic['data']['dash']['video'][0]['baseUrl']
    audioUrl = urlDic['data']['dash']['audio'][0]['baseUrl']

    # 下载视频
    videoValue = requests.get(videoUrl, headers=headers)
    with open('un/video.mp4', 'wb') as f:
        f.write(videoValue.content)

    # 下载音频
    audioValue = requests.get(audioUrl, headers=headers)
    with open('un/audio.mp3', 'wb') as f:
        f.write(audioValue.content)

    # 合并音视频
    # 这里记得写自己的ffmpeg地址，记得添加环境变量
    cmd = f'D:\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg -i un/video.mp4 -i un/audio.mp3 -acodec copy -vcodec copy un/movie.mp4'

    subprocess.call(cmd, shell=True)



if __name__ == '__main__':
    # 请求头
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "referer": "https://www.bilibili.com/video/BV1a5411M7AZ/?spm_id_from=333.999.0.0&vd_source=aadf8a8387c848eb5bf832970ee6fa21"
    }
    # 视频页面链接
    url = "https://www.bilibili.com/video/BV1gG4y1X7DJ/?spm_id_from=333.999.0.0&vd_source=aadf8a8387c848eb5bf832970ee6fa21"
    getVideo(url, headers)
