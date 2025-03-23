import io
import time
from MeloTTS.melo.api import TTS
from multiprocessing import Queue
import re

import torch


def process_text_from_queue(text_queue: Queue, voice_queue: Queue):
    # 生成語音
    device = "cuda" if torch.cuda.is_available() else "cpu"
    speed = 0.85
    model = TTS(language='ZH', device=device)
    speaker_ids = model.hps.data.spk2id

    while True:
        while not text_queue.empty():
            content = text_queue.get()
            #sentences = re.split(r'(?<=[，、。！？!?])', content)
            sentences = re.split(r'(?<=[。！？!?])', content)
            sentences = [s.strip() for s in sentences if s.strip()]
            for s in sentences:
                try:
                    blob = io.BytesIO()
                    blob.name = "output.wav"
                    model.tts_to_file(s, speaker_ids['ZH'], blob, speed=speed)
                    blob.seek(0)
                    voice_queue.put(blob, timeout=60*3)
                except:
                    continue
            time.sleep(0.1)
        time.sleep(0.5)
