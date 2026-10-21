#!/usr/bin/env python3
"""生成小红书图文笔记用的竖版图（1080x1440，3:4）。
视觉沿用落地页：纸色底、等宽字体、细线、墨绿点缀。
布局用 top / main(垂直居中) / bot 三段，强化工业设计参数感与信息密度。"""
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
     display:flex;flex-direction:column;padding:80px}
.top{font-size:25px;letter-spacing:.14em;color:#6b6862;text-transform:uppercase;flex:none;
     display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #dedbd4;padding-bottom:24px}
.top b{color:#1f4d3a}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:42px}
.bot{flex:none;font-size:27px;line-height:1.7;color:#6b6862;border-top:2px solid #dedbd4;padding-top:24px}
.bot b{color:#141414}
h1{font-size:86px;line-height:1.28;font-weight:800;letter-spacing:-.02em}
h1.sm{font-size:74px;line-height:1.3}
h1 em{font-style:normal;color:#1f4d3a;border-bottom:9px solid #1f4d3a;padding-bottom:2px}
.mid{font-size:36px;line-height:1.78;color:#38362f}
.mid b{color:#141414}
.rule{border:0;border-top:2px solid #141414}
.quote{font-size:48px;line-height:1.68;font-weight:700}
.cite{font-size:26px;color:#6b6862;line-height:1.7}
.compare{display:flex;flex-direction:column;gap:20px;background:#efede8;padding:30px 34px;border-radius:8px;border-left:6px solid #1f4d3a}
.compare-item{font-size:29px;line-height:1.6;color:#38362f}
.compare-item b{color:#141414}
.compare-item .bad{color:#8c3a2b;font-weight:700}
.compare-item .good{color:#1f4d3a;font-weight:700}
.lit-list{display:flex;flex-direction:column;gap:24px;background:#efede8;padding:32px 36px;border-radius:8px;border:1px solid #dedbd4}
.lit-item{font-size:29px;line-height:1.65;color:#38362f}
.lit-item b{color:#141414}
.cards{display:flex;flex-direction:column;gap:24px}
.cards figure{background:#fff;border:2px solid #dedbd4;border-radius:6px;overflow:hidden}
.cards img{width:100%;height:290px;object-fit:cover;object-position:top center;display:block}
.cards figcaption{font-size:25px;color:#4a4740;padding:14px 20px;border-top:1px solid #dedbd4;display:flex;justify-content:space-between}
.cards figcaption b{color:#141414}
.cards figcaption span.tag{color:#1f4d3a;font-weight:700}
"""

PAGES = {}

PAGES["01-cover"] = (
  '<div class="top"><span>CAIRN · <b>CALM TECH PROTOTYPE</b></span><span>01 / 04</span></div>',
  """
  <div class="main">
    <h1>别让 AI 的进度条<br>绑架你的<br><em>「中心视线」</em></h1>
    <div class="mid">后台同时挂着 Agent 干活之后，<br>
    我们在桌角放了一块<b style="color:#1f4d3a">只给余光看</b>的墨水屏。</div>
  </div>
  """,
  '<div class="bot"><b>800×480 1-BIT E-INK</b> · 固定物理坐标 · 0 弹窗 · 0 提示音</div>'
)

PAGES["02-cards"] = (
  '<div class="top"><span>DECISION HANDOFF · <b>只做三张卡</b></span><span>02 / 04</span></div>',
  """
  <div class="main">
    <div class="cards">
      <figure><img src="%s"><figcaption><span><b>① 跑完了</b> — 结论就绪，随时验收</span><span class="tag">DONE</span></figcaption></figure>
      <figure><img src="%s"><figcaption><span><b>② 卡住了</b> — 缺一个上下文，等你拍板</span><span class="tag">BLOCKED</span></figcaption></figure>
      <figure><img src="%s"><figcaption><span><b>③ 要你批准</b> — 高危操作，人工确认</span><span class="tag">APPROVAL</span></figcaption></figure>
    </div>
  </div>
  """ % (b64(ASSETS/'task-finished-zh.png'), b64(ASSETS/'task-blocked-zh.png'),
         b64(ASSETS/'approval-request-zh.png')),
  '<div class="bot">设计约束：<b>余光扫一眼 ≤ 8 秒必须看懂状态</b>，不滚屏、不看长日志</div>'
)

PAGES["03-quote"] = (
  '<div class="top"><span>WHY PERIPHERY · <b>1995 年的解法</b></span><span>03 / 04</span></div>',
  """
  <div class="main">
    <div class="quote">“平静的技术，会在注意力的<b>外围</b>与<b>中心</b>之间<span style="color:#1f4d3a">轻松来回移动</span>。”</div>
    <div class="cite">— Mark Weiser &amp; John Seely Brown · Xerox PARC, 1995</div>
    <div class="compare">
      <div class="compare-item"><span class="bad">× 手机与桌面通知栏：</span><br>不分轻重，每一条弹窗都在强行索要<b>「注意力中心」</b></div>
      <div class="compare-item"><span class="good">✓ 墙上的挂钟 / Cairn：</span><br>安静待在<b>「注意力外围」</b>，看与不看，主动权在你</div>
    </div>
  </div>
  """,
  '<div class="bot">真正让人筋疲力尽的<b>不是通知太多，而是位置不对。</b></div>'
)

PAGES["04-honest"] = (
  '<div class="top"><span>LITERATURE REVIEW · <b>说点对我们不利的</b></span><span>04 / 04</span></div>',
  """
  <div class="main">
    <h1 class="sm">墨水屏 ≠ 专注<br>不拿「护眼」当噱头</h1>
    <div class="lit-list">
      <div class="lit-item">· <b>Siegenthaler (2012)</b>：决定视觉疲劳的核心是对比度与图像质量，<b>而非显示技术本身</b>。</div>
      <div class="lit-item">· <b>Benedetto (2013)</b>：墨水屏优势仅在连续长文阅读，<b>没有任何研究支撑「全天工作流」</b>。</div>
    </div>
  </div>
  """,
  '<div class="bot">如果一块屏不能减少认知打断，<b>它就不该多占你桌面一寸地方。</b></div>'
)

for name, (top, main, bot) in PAGES.items():
    (OUT / f"{name}.html").write_text(
        f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{top}{main}{bot}")
print("generated", len(PAGES), "pages")
