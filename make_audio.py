"""
用微软神经网络语音（Edge TTS）为《拔苗助长》立体书生成全部配音。

用法：
    pip install edge-tts
    python make_audio.py

会在当前目录生成 audio/ 文件夹（每句一个 mp3 + lines.json）。
把 index.html 和 audio/ 一起部署，页面会自动改用这些配音；
没有 audio/ 时，页面退回浏览器自带语音。
"""
import asyncio
import json
import os
import shutil

import edge_tts

# 想换声音、语速，改这里即可。可用声音列表：edge-tts --list-voices | grep zh-CN
VOICES = {
    "narr": {"voice": "zh-CN-XiaoxiaoNeural", "rate": "-12%", "pitch": "+0Hz"},  # 旁白：晓晓，放慢一点给小朋友听
    "man":  {"voice": "zh-CN-YunjianNeural",  "rate": "-5%",  "pitch": "-4Hz"},  # 农夫：云健，成年男声
}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")


async def make(line, sem):
    path = os.path.join(OUT, f"{line['key']}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "skip"
    v = VOICES[line["who"]]
    async with sem:
        for attempt in range(3):
            try:
                await edge_tts.Communicate(line["text"], v["voice"], rate=v["rate"], pitch=v["pitch"]).save(path)
                return "ok"
            except Exception as e:  # network hiccup: retry
                if attempt == 2:
                    raise
                await asyncio.sleep(2)


async def main():
    with open(os.path.join(HERE, "lines.json"), encoding="utf-8") as f:
        lines = json.load(f)["lines"]
    os.makedirs(OUT, exist_ok=True)
    sem = asyncio.Semaphore(4)
    results = await asyncio.gather(*(make(l, sem) for l in lines))
    shutil.copy(os.path.join(HERE, "lines.json"), os.path.join(OUT, "lines.json"))
    print(f"完成：新生成 {results.count('ok')} 句，已存在 {results.count('skip')} 句，共 {len(lines)} 句 → {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
