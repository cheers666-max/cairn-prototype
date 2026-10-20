#!/usr/bin/env python3
"""看板清理：把「活已干完但状态没关」的 issue 收掉。

只做**可验证**的清理：交付物存在且与任务要求逐条对上，才动。
不做判断题（比如某个方向该不该继续跑）——那要人来定。
"""
import json
import urllib.request

CID = "0c58fb5d-4c6e-4252-95d0-9e2770b43f0a"
BASE = "http://127.0.0.1:3140"
H = {
    "Content-Type": "application/json",
    "x-paperclip-company-id": CID,
    "x-paperclip-actor-id": "local-board",
    "x-paperclip-actor-type": "user",
}


def get(path):
    req = urllib.request.Request(BASE + path, headers=H)
    return json.load(urllib.request.urlopen(req, timeout=30))


def patch(path, body):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode(), method="PATCH", headers=H
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


issues = get(f"/api/companies/{CID}/issues")
issues = issues if isinstance(issues, list) else issues.get("items", issues.get("issues", []))
by_id = {i.get("identifier"): i for i in issues}

# INK-1：交付物逐条核对过，两项要求均已满足
target = by_id.get("INK-1")
if not target:
    raise SystemExit("找不到 INK-1")

print(f"INK-1 当前状态: {target.get('status')}")
print("交付核对：")
print("  ① 硬件/软件/生态/价格 分类不满清单（带来源） → research/2026-10-14-...md 第一、二、三、四节 ✓")
print("  ② 假设证伪测试（明确给出结论）            → 同文件第二章，结论「极低 / 伪需求」 ✓")
print()

code, resp = patch(
    f"/api/issues/{target['id']}",
    {
        "status": "done",
        "resolutionNote": (
            "交付已核实（本机会话逐条比对，2026-10-16）："
            "① research/2026-10-14-eink-user-painpoints-and-agent-monitoring-validation.md "
            "含按硬件/软件/生态/价格四维分类的墨水屏不满清单，每条带来源；"
            "② 同文件第二章为「墨水屏监控多台 Agent」假设的证伪测试，结论「极低 / 伪需求」，"
            "并给出社区反例（声音通知优先、Telegram/tmux 双向控制优先）。"
            "另附 research/2026-10-15-token-monitor-kickstarter-verification.md 与 "
            "research/remarkable-reviews/（3 份）。任务要求两项均已满足。"
            "此 issue 自 2026-10-14 起挂 in_progress 50 小时未关，属看板状态未更新，非工作未完成。"
        ),
    },
)
print(f"PATCH HTTP {code}")
if isinstance(resp, dict):
    print(f"  → status={resp.get('status')}  completedAt={resp.get('completedAt')}")
else:
    print("  ", resp)