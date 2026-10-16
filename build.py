#!/usr/bin/env python3
"""把 template.html 构建成自包含单文件：图片与视频全部内嵌为 base64。

这样产出的页面可以放任何地方（OBS 单文件上传 / GitHub Pages / 邮件附件），
不依赖相对路径，不会出现「只传了 HTML 没传 assets」的经典事故。
"""
import base64
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / "site" / "template.html"
ASSETS = ROOT / "assets"
OUT = ROOT / "dist" / "index.html"

CARDS = ["task-finished", "task-blocked", "approval-request"]
LANGS = ["zh", "en"]


def data_uri(path: pathlib.Path, mime: str) -> str:
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())


def main() -> int:
    if not TEMPLATE.exists():
        print("缺少模板: %s" % TEMPLATE, file=sys.stderr)
        return 1

    assets = {}
    missing = []
    for lang in LANGS:
        for card in CARDS:
            f = ASSETS / ("%s-%s.png" % (card, lang))
            if not f.exists():
                missing.append(f.name)
                continue
            assets["%s-%s" % (card, lang)] = data_uri(f, "image/png")
            bf = ASSETS / "bitmap" / ("%s-%s.png" % (card, lang))
            if bf.exists():
                assets["bitmap/%s-%s" % (card, lang)] = data_uri(bf, "image/png")
            else:
                missing.append("bitmap/" + bf.name)

    video = ASSETS / "demo.mp4"
    if not video.exists():
        missing.append("demo.mp4")
        video_src = ""
    else:
        video_src = data_uri(video, "video/mp4")

    if missing:
        print("缺少素材: %s" % ", ".join(missing), file=sys.stderr)
        return 1

    html = TEMPLATE.read_text(encoding="utf-8")
    # 海报用中文「要你批准」那张卡，最贴合「人在决定」的语义
    poster = assets.get("approval-request-zh", "")
    html = html.replace("__ASSETS__", json.dumps(assets, ensure_ascii=False))
    html = html.replace("__VIDEO__", video_src)
    html = html.replace("__POSTER__", poster)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print("✅ 构建完成: %s" % OUT)
    print("   单文件大小: %.0f KB" % kb)
    print("   内嵌资源: %d 张卡片图（含位图）+ 视频 %d KB" % (len(assets), video.stat().st_size // 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
