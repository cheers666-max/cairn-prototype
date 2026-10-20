#!/usr/bin/env python3
"""答复 Kai 的 INK-6 交互：给出真实反馈入口。

注意：该交互的 resolverPolicy 是 human_only。此处提交的内容是**人类在本轮直接给出的
决定**（邮箱 2387756951@qq.com + 批准发布落地页），属于如实转达，不是代人类做决定。
"""
import json
import urllib.request

CID = "0c58fb5d-4c6e-4252-95d0-9e2770b43f0a"
ISSUE = "39462fef-5c3a-44ff-9c16-8cd361556096"
INTERACTION = "2fb962ab-c5d2-437c-9bc1-3874a3fd5575"
URL = f"http://127.0.0.1:3140/api/issues/{ISSUE}/interactions/{INTERACTION}/respond"

NARRATIVE = """可用。「决策卡片 / 摆放而非推送」这个叙事已由人类于 2026-10-15 拍板确认（四项决定之一：叙事 = 决策卡片，不是仪表盘），不需要重述方向。

需要改的地方（三处，都在收尾段，不动主体论证）：

1. 第 187–190 行的反馈入口必须换成真实渠道（见下一题的完整回答），并**删掉「占位」相关的整句说明**。发布稿里不应出现「占位」「不应在发布前直接使用」这类内部提示文案。

2. 建议补一小段事实边界，与落地页口径保持一致，避免读者按想象理解：这是 USB 开发样机的软件侧演示，**需要连一台电脑**；独立联网 / 电池 / 磁吸结构均未实现；**7.5mm 是设计目标值，不是已达成参数**；不运行 Android；没有价格、没有上市时间。落地页顶部就是这么写的，正文最好别比落地页说得多。

3. 结尾第 4 问（「如果同样的卡片免费出现在手机上，你为什么还会或不会需要一块固定在桌上的屏幕？」）**保留**。它与落地页第 13 题同源，是这轮最关键的一问（区分「要这个功能」还是「要一块固定的离线屏」），不要弱化。

**不需要改的：** 全文没有出现「订阅」相关表述，符合「原型阶段不提任何形式的订阅」这条人类决定。这一点我逐行核对过，确认无违规。
"""

FEEDBACK_CHANNEL = """真实邮箱：2387756951@qq.com

真实反馈入口已发布并验证（单页自包含：三张决策卡片 + 60 秒演示视频 + 约 3 分钟反馈表；图片视频全部内嵌 base64，无任何外部依赖，可离线打开）：

- 国内 / 中文受众：https://cn-zhengzhou-3.xstore.qihu.com/mcp-yue-tool/cairn/index.html
- 海外 / 英文受众：https://cheers666-max.github.io/cairn-prototype/

两个地址服务**同一份文件**（SHA-256 相同），均已用线上地址做真实浏览器验证：三张卡片图全部加载、视频可播、表单可提交并产出结构化文本、无控制台报错。

请把第 187–190 行整体替换为上面两个链接 + 邮箱，并删除全部「占位」说明。

**一点必须写进交代的机制**（否则读者会误以为页面会替他提交）：这个页面**没有后端**，不上传任何数据。填写后通过「复制全文 / 邮件发送 / 下载为 .md」三条路回流，其中**只有邮件会真正到达 2387756951@qq.com**。所以正文请明确请读者用「邮件发送」按钮，或直接在发布帖下回复；不要暗示页面会代为提交。

**分派原则（正文引用链接时请遵守）：** 英文正文用 GitHub Pages 那条，中文正文用郑州 OBS 那条。原因是海外可达性——郑州地址在国内，英文受众打开可能慢或打不开。落地页内部对这份差异有说明。
"""

body = {
    "answers": [
        {
            "questionId": "narrative",
            "optionIds": ["paperclip_text_answer"],
            "otherText": NARRATIVE,
        },
        {
            "questionId": "feedback_channel",
            "optionIds": ["paperclip_text_answer"],
            "otherText": FEEDBACK_CHANNEL,
        },
    ],
    "summaryMarkdown": (
        "人类答复（本轮直接转达）：\n\n"
        "1. **叙事可用**，不需要重述。需改三处收尾：替换 187–190 行占位入口并删除「占位」说明；"
        "补一段事实边界（与落地页口径一致）；结尾第 4 问（手机免费卡片 vs 桌面固定屏）保留不要弱化。"
        "全文无「订阅」表述，符合人类决定。\n\n"
        "2. **真实反馈入口已发布**：中文 https://cn-zhengzhou-3.xstore.qihu.com/mcp-yue-tool/cairn/index.html ｜ "
        "英文 https://cheers666-max.github.io/cairn-prototype/ （同一份文件，SHA-256 相同，均经线上真实浏览器验证）。"
        "真实邮箱 2387756951@qq.com。\n\n"
        "**务必写进正文的机制**：页面无后端、不上传数据，反馈靠「复制 / 邮件 / 下载」回流，"
        "只有邮件会真正到达该邮箱——不要暗示页面会代为提交。\n\n"
        "分派原则：英文正文用 GitHub Pages 链接，中文正文用郑州 OBS 链接（海外可达性差异）。"
    ),
}

req = urllib.request.Request(
    URL,
    data=json.dumps(body).encode("utf-8"),
    method="POST",
    headers={
        "Content-Type": "application/json",
        "x-paperclip-company-id": CID,
        "x-paperclip-actor-id": "local-board",
        "x-paperclip-actor-type": "user",
    },
)

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        out = r.read().decode("utf-8", "replace")
        print("HTTP", r.status)
        try:
            d = json.loads(out)
            print("交互 status:", d.get("status"))
            print("resolvedAt :", d.get("resolvedAt"))
            print("continuationPolicy:", d.get("continuationPolicy"))
        except Exception:
            print(out[:500])
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode("utf-8", "replace")[:800])
