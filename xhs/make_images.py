#!/usr/bin/env python3
"""生成小红书图文笔记用的竖版图（1080x1440，3:4）。
视觉沿用落地页：纸色底、等宽字体、细线、墨绿点缀。
布局用 top / main(垂直居中) / bot 三段，避免 space-between 把内容摊散。"""
import base64, pathlib

HERE = pathlib.Path(__file__).parent
ASSETS = HERE.parent / "assets"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

def b64(p):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1440px;background:#f7f6f3;color:#141414;
     font-family:ui-monospace,SFMono-Regular,Menlo,"PingFang SC","Noto Sans CJK SC",monospace;
     display:flex;flex-direction:column;padding:84px}
.top{font-size:26px;letter-spacing:.16em;color:#6b6862;text-transform:uppercase;flex:none}
.top b{color:#1f4d3a}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:44px}
.bot{flex:none;font-size:29px;line-height:1.75;color:#6b6862}
.bot b{color:#141414}
h1{font-size:94px;line-height:1.3;font-weight:800;letter-spacing:-.02em}
h1.sm{font-size:78px}
h1 em{font-style:normal;color:#1f4d3a;border-bottom:10px solid #1f4d3a;padding-bottom:2px}
.mid{font-size:37px;line-height:1.78;color:#38362f}
.mid b{color:#141414}
.rule{border:0;border-top:2px solid #141414}
.quote{font-size:50px;line-height:1.72;font-weight:700}
.cite{font-size:26px;color:#6b6862;line-height:1.7}
.cards{display:flex;flex-direction:column;gap:26px}
.cards figure{background:#fff;border:2px solid #dedbd4;border-radius:6px;overflow:hidden}
.cards img{width:100%;height:300px;object-fit:cover;object-position:top center;display:block}
.cards figcaption{font-size:25px;color:#4a4740;padding:13px 18px;border-top:1px solid #dedbd4}
"""

TOP = '<div class="top">Cairn · <b>原型求反馈</b></div>'

PAGES = {}

PAGES["01-cover"] = (TOP, """
  <div class="main">
    <h1>我们想验证的<br>不是墨水屏<br>是<em>「余光」</em></h1>
    <div class="mid">手机把每件事都推到注意力的<b>中心</b>。<br>
    能不能把 agent 的决定放回<b style="color:#1f4d3a">余光</b>？</div>
  </div>
""", '<div class="bot">卡片待在固定位置 · <b>不亮 · 不响 · 不弹窗</b></div>')

PAGES["02-cards"] = ('<div class="top">它只做三件事</div>', """
  <div class="main">
    <div class="cards">
      <figure><img src="%s"><figcaption>① 跑完了 — agent 干完活了</figcaption></figure>
      <figure><img src="%s"><figcaption>② 卡住了 — 它缺一个信息走不下去</figcaption></figure>
      <figure><img src="%s"><figcaption>③ 要你批准 — 这一步只有你能决定</figcaption></figure>
    </div>
  </div>
""" % (b64(ASSETS/'task-finished-zh.png'), b64(ASSETS/'task-blocked-zh.png'),
       b64(ASSETS/'approval-request-zh.png')),
  '<div class="bot">三张卡，<b>8 秒之内能看懂</b>——这也是设计目标之一</div>')

PAGES["03-quote"] = ('<div class="top">这个想法不是我们发明的</div>', """
  <div class="main">
    <div class="quote">“平静的技术会在注意力的外围<br>
    和中心之间<span style="color:#1f4d3a">轻松来回移动</span>。”</div>
    <hr class="rule">
    <div class="cite">— Mark Weiser &amp; John Seely Brown<br>Xerox PARC，1995</div>
  </div>
""", '<div class="bot">外围 = 我们<b>被调谐到、但不明确注视</b>的东西。<br>读一遍，你就知道手机为什么让人累。</div>')

PAGES["04-honest"] = ('<div class="top">说点<b>对我们不利</b>的</div>', """
  <div class="main">
    <h1 class="sm">墨水屏<br>并不等于专注</h1>
    <div class="mid">我们查了那批文献：<br>
    显示技术不是关键，<b>图像质量</b>才是；<br>
    也没有任何研究接近「全天工作」。</div>
  </div>
""", '<div class="bot">所以「墨水屏护眼」<b>我们不拿来当论据</b>。<br>'
     '如果大家根本不需要第二块屏，<b>这东西就不该存在。</b></div>')

for name, (top, main, bot) in PAGES.items():
    (OUT / f"{name}.html").write_text(
        f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{top}{main}{bot}")
print("generated", len(PAGES), "pages")
