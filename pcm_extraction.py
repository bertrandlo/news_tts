import io
import wave
import numpy as np


def pcm_info(blob):
    # 取得 WAV 檔案的基本參數
    with wave.open(blob) as wav_file:
        num_channels = wav_file.getnchannels()  # 聲道數量
        sample_width = wav_file.getsampwidth()  # 每個取樣點的位元數 (bytes)
        frame_rate = wav_file.getframerate()  # 取樣率（Hz）
        num_frames = wav_file.getnframes()  # 總取樣數
        print("Channels:", num_channels)
        print("Sample width (bytes):", sample_width)
        print("Frame rate:", frame_rate)
        print("Number of frames:", num_frames)


def extract_pcm(blob: io.BytesIO):
    # 開啟 WAV 檔案（請將 "example.wav" 替換成你的檔案路徑）
    with wave.open(blob) as wav_file:
        sample_width = wav_file.getsampwidth()  # 每個取樣點的位元數 (bytes)
        num_frames = wav_file.getnframes()  # 總取樣數
        # 讀取所有音訊資料（raw PCM 資料）
        frames = wav_file.readframes(num_frames)
        num_channels = wav_file.getnchannels()  # 聲道數量
    # 根據 sample_width 設定對應的 NumPy 資料型態
    if sample_width == 1:
        dtype = np.uint8   # 8-bit PCM 通常為無符號整數
    elif sample_width == 2:
        dtype = np.int16   # 16-bit PCM 通常為有符號整數
    elif sample_width == 4:
        dtype = np.int32   # 32-bit PCM
    else:
        raise ValueError("不支援的 sample width: {}".format(sample_width))

    # 將 bytes 轉換為 NumPy 陣列，這就是原始的 PCM 數據
    pcm_data = np.frombuffer(frames, dtype=dtype)

    # 如果是多聲道，根據聲道數量進行重塑
    if num_channels > 1:
        pcm_data = pcm_data.reshape(-1, num_channels)

    return pcm_data
