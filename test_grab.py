import time
import unittest

import torch

from news_util import extract_news_content, extract_news_header_link, news_feeder
from multiprocessing import Process, Queue
from MeloTTS.melo.api import TTS
from bs4 import BeautifulSoup
from curl_cffi import requests


class TestNews(unittest.TestCase):
    def test_yahoo_news_header_list(self):
        for link in extract_news_header_link():
            print(link.text, "https://tw.news.yahoo.com" + link.attrs['href'])

    def test_yahoo_news_body_extraction(self):
        url = "https://tw.news.yahoo.com/%E5%8F%B0%E5%8D%97%E6%B0%B8%E6%A8%82%E5%B8%82%E5%A0%B4%E6%8E%92%E9%9A%8A%E5%B0%8F%E5%90%83%EF%BC%8C%E8%A7%80%E5%85%89%E5%AE%A2%E5%BF%85%E5%90%83%E8%B1%AC%E8%88%8C%E5%8C%85%EF%BC%8C%E7%8D%A8%E9%96%80%E9%A2%A8%E5%91%B3%E8%AE%93%E4%BA%BA%E4%B8%80%E8%A9%A6%E5%B0%B1%E5%96%9C%E6%AD%A1%EF%BC%81-042111123.html"
        print(extract_news_content(url))

    def test_udn_news(self):
        url = "https://udn.com/news/breaknews/1/99#breaknews"
        r = requests.get(url, impersonate="chrome")
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.find_all("div", {'class': 'story-list__news'})
        paragraphs = content.find_all('p')
        all_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        # story-list__news

    def test_news_feeder(self):
        q = Queue(3)
        proc_news_feeder = Process(target=news_feeder, args=(q, ), daemon=True)
        proc_news_feeder.start()

        while True:
            time.sleep(1)
            if q.empty():
                continue
            content = q.get_nowait()
            print(content)

    def test_bert_vits2(self):
        from MeloTTS.melo.api import TTS
        import io
        import wave

        blob = io.BytesIO()
        blob.name = "output.wav"

        speed = 0.9
        device = "cuda"
        text = "[周刊王CTWANT] 國外一名女子是奶油魔人"
        model = TTS(language='ZH', device=device)
        speaker_ids = model.hps.data.spk2id

        model.tts_to_file(text, speaker_ids['ZH'], blob, speed=speed)
        blob.seek(0)  # 檔案指標移回開頭

        with wave.open(blob, "rb") as wav_file:
            num_channels = wav_file.getnchannels()  # 聲道數量
            sample_width = wav_file.getsampwidth()  # 每個取樣點的位元數（bytes）
            frame_rate = wav_file.getframerate()  # 取樣率（Hz）
            num_frames = wav_file.getnframes()  # 總取樣數

            print("Channels:", num_channels)
            print("Sample width (bytes):", sample_width)
            print("Frame rate:", frame_rate)
            print("Number of frames:", num_frames)

    def test_pcm_extraction(self):
        from pcm_extraction import extract_pcm, pcm_info
        import io

        with open('zh.wav', "rb") as f:
            wav_bytes = f.read()

        wav_bytes_io = io.BytesIO(wav_bytes)
        pcm_info(wav_bytes_io)

    def test_tts_speaker(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        speed = 0.9
        model = TTS(language='ZH', device=device)
        print(model.speakers)
