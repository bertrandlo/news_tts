### 透過 MeloTTS 將 Yahoo News 持續讀出

- Python 3.11 + PyTorch
- 透過 curl_cffi 讀取
- 透過兩個子行程擷取與轉換，4070 可以穩定持續轉換不中斷。
- 內部加入 ffmpeg windows binary 靜態執行檔進行串流發送給 RTSP server
- MeloTTS installation into the sub-folder MeloTTS
  - [LINK](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md)
  - 接著透過 unidic 下載
  - 透過 NLTK 下載 英語斷句
    - ``` nltk.download('averaged_perceptron_tagger_eng') ```
- 