# 拔苗助长 · 成语立体互动书（剪纸版 v2.3）

单页网页，不需要构建。

## 文件
- `index.html`：整本书（画面、玩法、音效、背景音乐都在里面）
- `lines.json`：书里所有要朗读的句子（26 句，旁白 + 农夫）
- `make_audio.py`：用微软神经网络语音（Edge TTS）生成配音

## 生成配音（建议做）
```bash
pip install edge-tts
python make_audio.py
```
运行后会出现 `audio/` 文件夹（26 个 mp3 + lines.json）。旁白是晓晓（zh-CN-XiaoxiaoNeural），农夫是云健（zh-CN-YunjianNeural），声音和语速可以在脚本顶部的 `VOICES` 里改。改完以后删掉 `audio/` 重新跑。

## 部署
把 `index.html` 和 `audio/` 放在同一目录，部署到任意静态托管（GitHub Pages / Vercel / Netlify 等）。

- 有 `audio/`：所有设备都用微软配音，听起来一致。
- 没有 `audio/`：退回浏览器自带语音（用 Edge 打开时会自动选微软晓晓）。

注意：需要通过 http(s) 打开。直接双击打开本地文件时，浏览器不允许读取 `audio/lines.json`，只会用浏览器自带语音。

## 改了故事文字以后
句子和配音靠文字内容对应（文件名是文字的哈希）。改了 `index.html` 里任何会被朗读的句子，要同步更新 `lines.json` 并重新生成配音，否则那一句会退回浏览器语音。
