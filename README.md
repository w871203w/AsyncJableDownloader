# AsyncJableDownloader

### vitual env
```
python -m venv env
source env/bin/activate # MacOS
\env\scripts\activate.bat # Windows
```
### requirements
`pip install -r requirements.txt`

安裝 FFmpeg 透過 FFmpeg 合併影片 不需另外轉檔或解碼 

### 資料夾結構（Windows）
```
jable
│  config.py
│  parse.py
│  jable.py
│  README.md
│  requirements.txt
│  urls.txt
│
└─ ffmpeg
│    └─ bin
│        │ ffmpeg.exe
└─ abp
    │ abp-971.jpg
    | abp-971.mp4
```
### 資料夾結構（MacOS）
```
jable
│  config.py
│  parse.py
│  jable.py
│  README.md
│  requirements.txt
│  urls.txt
│  ffmpeg.unix
└─ abp
    │ abp-971.jpg
    | abp-971.mp4
```

### 開始程式 輸入影片網址 下載進度條
`python jable.py`

`https://jable.tv/videos/abp-971/`    
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/2.PNG)  

### 合併影片
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/3.PNG)

### 完成 出現 總共用時 才代表整個跑完
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/4.PNG)

![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/1.PNG)


### 進階 可改參數
```python
base_dir # 預設是現在的資料夾，可改成自己想要放的資料夾 
# 例如 我想放在 'C:\\users\\username\\video'
limit # 預設 100 可根據自己網路調高或者調低
NewJableCrawler(url, base_dir=base_dir, limit=400)
```

### 新增並行下載
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/6.PNG)

### urls.txt 內容
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/5.PNG)
