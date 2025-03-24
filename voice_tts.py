import os
import time
import subprocess

from multiprocessing import Queue, Process

from pcm_extraction import extract_pcm
from tts_service import process_text_from_queue
from news_util import news_feeder
from dotenv import load_dotenv


load_dotenv()
PUBLISH_USERNAME = os.getenv('PUBLISH_USERNAME')
PUBLISH_PASSWORD = os.getenv('PUBLISH_PASSWORD')
NEWS_SUPPLIER = os.getenv('NEWS_SUPPLIER')

def main():
    text_queue = Queue(maxsize=2)
    voice_queue = Queue(maxsize=5)
    proc_tts = Process(target=process_text_from_queue, args=(text_queue, voice_queue), daemon=True)
    proc_tts.start()

    proc_news = Process(target=news_feeder, args=(text_queue, NEWS_SUPPLIER), daemon=True)
    proc_news.start()
    time.sleep(2)

    ffmpeg_cmd = [
        "ffmpeg",
        "-re",  # 實時播放
        "-hwaccel", "cuda",
        "-f", "s16le",
        "-ar", "44100",
        "-ac", "1",
        "-i", "pipe:0",  # 從 stdin 讀取
        "-c:a", "libmp3lame",  # 使用 libmp3lame 進行 MP3 編碼
        "-b:a", "128k",  # 設定音訊比特率為 128 kbps
        "-f", "rtsp",
        "-rtsp_transport", "tcp", "rtsp://{}:{}@192.168.1.2:8554/music".format(PUBLISH_USERNAME, PUBLISH_PASSWORD)
    ]

    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    while True:
        time.sleep(0.1)
        if not voice_queue.empty():
            wav_blob = voice_queue.get_nowait()
            process.stdin.write(extract_pcm(wav_blob))
            process.stdin.flush()


if __name__ == '__main__':
    main()
