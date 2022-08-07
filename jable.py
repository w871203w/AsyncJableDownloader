import re
import os
import platform
import asyncio

import aiohttp
from aiohttp import client_exceptions
from tqdm import tqdm

from config import headers, jable_headers


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class NewJableCrawler():

    def __init__(self, url='', base_dir=os.getcwd(), limit=100):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.base_dir = base_dir
        self.video_name = self.get_video_name()
        self.video_dir_name = self.get_video_dir_name()
        self.video_dir_path = self.get_video_dir_path()
        self.video_html_text = self.get_html_data(self.url, 'text')
        self.image_path = self.get_image_path()
        self.m3u8_url = self.get_m3u8_url()
        self.m3u8_data = self.get_html_data(self.m3u8_url, 'text')
        self.base_url = self.get_base_url()
        self.ts_list = self.get_ts_list()
        self.ci = self.get_ci()
        self.limit = limit

    def run(self):
        if os.path.isfile(os.path.join(self.video_dir_path, self.video_name + '.mp4')):
            print("已下载该影片，跳过")
            return
        self.start_async_download_ts()
        self.merge_ts_to_mp4()
        self.delete_ts()

    def get_video_name(self) -> str:
        return self.url.split('/')[-2]

    def get_video_dir_name(self) -> str:
        return self.video_name.split('-')[0]

    def get_video_dir_path(self) -> str:
        if not os.path.exists(self.video_dir_name):
            os.mkdir(self.video_dir_name)
        return os.path.join(self.base_dir, self.video_dir_name)

    def get_image_path(self):
        image_url = re.search('https://.+jpg', self.video_html_text)[0]
        image_path = os.path.join(self.video_dir_path, self.video_name + '.jpg')
        image = self.get_html_data(image_url, 'content')
        with open(image_path, 'wb') as f:
            f.write(image)
        return image_path

    def get_m3u8_url(self):
        return re.search('https://.+m3u8', self.video_html_text)[0]

    def get_base_url(self):
        m3u8_url_split = self.m3u8_url.split('/')
        m3u8_url_split.pop(-1)
        return ('/'.join(m3u8_url_split)) + '/'

    def get_ts_list(self):
        ts_list = re.findall('[0-9].+ts', self.m3u8_data)
        ts_list.pop(0)
        return ts_list

    def get_ci(self):
        from Crypto.Cipher import AES
        uri = re.search('[a-z0-9]+.ts', self.m3u8_data)[0]
        iv = re.search('0x+[a-z0-9]+', self.m3u8_data)[0]
        vt = iv.replace('0x', '')[:16].encode()
        m3u8_key = self.get_html_data(self.base_url + uri, 'content')
        return AES.new(m3u8_key, AES.MODE_CBC, vt)

    def get_html_data(self, url, type):
        return self.loop.run_until_complete(self.html_crawler(url, type))

    async def html_crawler(self, url, type):
        async with aiohttp.ClientSession() as client:
            headerss = headers
            async with client.get(url, headers=headerss, ssl=False, allow_redirects=True) as resp:
                if type == 'text':
                    return await resp.text()
                elif type == 'content':
                    return await resp.read()

    def start_async_download_ts(self):
        self.loop.run_until_complete(self.build_async_client())
        self.loop.close()

    async def build_async_client(self):
        async with aiohttp.ClientSession(headers=jable_headers,
                                         connector=aiohttp.TCPConnector(limit=self.limit, ssl=False)) as client:
            ts_list, base_url, ci, video_dir_path = self.ts_list, self.base_url, self.ci, self.video_dir_path
            tasks = [asyncio.create_task(self.download_ts(client, ts, base_url, ci, video_dir_path)) for ts in ts_list]
            [await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))]

    async def download_ts(self, client, ts, base_url, ci, video_dir_path):
        ts_url = base_url + ts
        save_ts_path = os.path.join(video_dir_path, ts)
        if os.path.isfile(save_ts_path):
            return
        try:
            async with client.get(ts_url, timeout=5) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    if len(content) == 0:
                        return await self.download_ts(client, ts, base_url, ci, video_dir_path)
                    with open(save_ts_path, 'wb') as f:
                        f.write(ci.decrypt(content))
                        return
                else:
                    await asyncio.sleep(5)
                    return await self.download_ts(client, ts, base_url, ci, video_dir_path)
        except asyncio.TimeoutError:
            await asyncio.sleep(5)
            return await self.download_ts(client, ts, base_url, ci, video_dir_path)
        except aiohttp.client_exceptions.ClientError:
            await asyncio.sleep(5)
            return await self.download_ts(client, ts, base_url, ci, video_dir_path)

    def merge_ts_to_mp4(self):
        video_dir_path = self.video_dir_path
        video_name = self.video_name
        txt_path = os.path.join(video_dir_path, video_name + '.txt')
        with open(txt_path, 'w+') as f:
            ts_list = self.ts_list
            for ts in ts_list:
                ts_path = os.path.join(video_dir_path, ts)
                f.write("file '{}'\n".format(ts_path))
        ffmpeg_path = 'ffmpeg'
        if os.name == 'nt':
            ffmpeg_path = os.path.join(self.base_dir, 'ffmpeg\\bin\\ffmpeg')
        elif os.name == 'posix':
            ffmpeg_path = os.path.join(self.base_dir, 'ffmpeg')
        ffmpeg_cmd = '{} -f concat -safe 0 -i {} -c copy {}'.format(
            ffmpeg_path, txt_path, os.path.join(video_dir_path, video_name + '.mp4'))
        os.system(ffmpeg_cmd)
        os.remove(txt_path)

    def delete_ts(self):
        video_dir_path = self.video_dir_path
        video_name = self.video_name
        if os.path.isfile(os.path.join(video_dir_path, video_name + '.mp4')):
            ts_list = self.ts_list
            for ts in ts_list:
                os.remove(os.path.join(video_dir_path, ts))
        else:
            print('還沒合成影片!')


if __name__ == '__main__':
    from parse import args_parse
    from time import time

    args = args_parse()
    urls = []
    url = ""
    if args.txt:
        with open(args.txt, 'r') as f:
            urls = f.read().split(',')
    elif args.url:
        url = args.url
    else:
        url = input('輸入要下載的網址：')
    start = time()
    if urls:
        for url in urls:
            print(f'開始下載 {url} ')
            NewJableCrawler(url).run()
    elif url:
        print(f'開始下載 {url} ')
        NewJableCrawler(url).run()
    print('總共用時 {:d} 分 {:d} 秒'.format(int((time() - start) / 60), int((time() - start) % 60)))
