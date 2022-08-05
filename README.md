# AsyncJableDownloader

### vitual env
```
python3 -m venv env
source env/bin/activate. # MacOS
.\env\scripts\activate.bat # Windows
```

### requirements
`pip install -r requirements.txt`

需要安裝 FFmpeg 透過 FFmpeg 合併檔案 影片就不會卡頓 也不需要另外轉檔 \
下載完 FFmpeg 放到同個資料夾 

### 資料夾結構(Windows)
```
jable
|   config.py
|   jable.py
|   README.md
|   requirements.txt
└─── ffmpeg
│   └─── bin
│       └─── ffmpeg.exe
└─── abp
│   │ abp-971.jpg
│   │ abp-971.mp4
```

### 資料夾結構(MacOS)
```
jable
|   config.py
|   jable.py
|   README.md
|   requirements.txt
|   ffmpeg.unix
└─── abp
│   │ abp-971.jpg
│   │ abp-971.mp4
```

### 執行程式 輸入影片網址 開始下載進度條
`python jable.py`
`https://jable.tv/videos/abp-971/`    
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/2.PNG)


### 下載完後 會開始用 FFmpeg 合併成mp4
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/3.PNG)


### 所有程序跑完 會出現總共花費時間
![image](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/4.PNG)

### 資料夾透過番號排序 裡面會包含影片( mp4 )跟封面( jpg ) 同種番號的會在同個資料夾
![image]([https://](https://github.com/w871203w/AsyncJableDownloader/blob/main/image/1.PNG))