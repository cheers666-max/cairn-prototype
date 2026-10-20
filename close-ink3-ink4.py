#!/usr/bin/env python3
"""把 INK-3 / INK-4 从「假 blocked」收掉，让公司进入等待状态。

依据：人类 2026-10-16 选择「两个都关掉，公司安静等你」。
注意：这是**暂缓**，不是「已证伪」——重开条件写进 resolutionNote，避免以后被误读成
「这个方向已经被否掉了」。
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
    return json.load(urllib.request.urlopen(urllib.request.Request(BASE + path, headers=H), timeout=30))


def patch(path, body):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode(), method="PATCH", headers=H
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


NOTES = {
    "INK-3": (
        "关闭（暂缓），非「已证伪」。原前提是「叙事重述待人类确认」——"
        "人类已于 2026-10-15 拍板确认叙事为「决策卡片，不是仪表盘」（四项决定之一），"
        "本 issue 要准备的那个决定已经由人类直接作出，故前提消失。"
        "另：Vega 裁决 3 明确「所有『再调研一轮』的提议本阶段默认否决」。"
        "本 issue 自 2026-10-15 起 blocked 25 小时，且 blockedByIssueIds 为空、"
        "unresolvedBlockerCount=0，属状态未清理的假 blocked，非真正受阻。"
        "重开条件：首批 5 条触达回复回收后，若暴露出定位层面（而非叙事层面）的真实分歧，再开。"
    ),
    "INK-4": (
        "关闭（暂缓），非「已证伪」，也非「方向不存在」。"
        "本 issue 问「除了 agent 监控还有什么购买动机」，其中方向 3（墨水屏阅读 + 摘要）"
        "确实贴着产品定位里写的「电子书阅读」，不是空想方向。"
        "关掉它的理由是**时机**：公司当前 214 KB 文档 vs 0 人触达，唯一付费意愿硬数据是"
        "jorgemf 众筹失败（10 名支持者 / €4 完成度）。在 0/100 触达的情况下继续做桌面前置调研，"
        "是替代性活动——它产出的是文档，不产出用户信号。"
        "本 issue 自 2026-10-15 起 blocked 29 小时，unresolvedBlockerCount=0，属假 blocked。"
        "重开条件：首批 5 条触达有回复后，用真实用户提到的工作流来选方向，而不是靠桌面推演。"
    ),
}

issues = get(f"/api/companies/{CID}/issues")
issues = issues if isinstance(issues, list) else issues.get("items", issues.get("issues", []))
by_id = {i.get("identifier"): i for i in issues}

for ident, note in NOTES.items():
    t = by_id.get(ident)
    if not t:
        print(f"  跳过 {ident}（找不到）")
        continue
    code, resp = patch(f"/api/issues/{t['id']}", {"status": "done", "resolutionNote": note})
    st = resp.get("status") if isinstance(resp, dict) else resp
    print(f"  {ident}: HTTP {code}  → status={st}")

print()
issues = get(f"/api/companies/{CID}/issues")
issues = issues if isinstance(issues, list) else issues.get("items", issues.get("issues", []))
from collections import Counter
print("  看板:", dict(Counter(i.get("status") for i in issues)))
print()
print("  仍在看板上的非 done 条目：")
actionable = 0
for it in sorted(issues, key=lambda x: x.get("issueNumber", 0)):
    if it.get("status") == "done":
        continue
    ba = it.get("blockerAttention") or {}
    idl = f" [{it.get('identifier')}]"
    print(f"    {it.get('identifier'):<8}{it.get('status'):<12}{str(it.get('title'))[:52]}")
    if it.get("status") in ("todo", "in_progress"):
        actionable += 1
print()
print(f"  可自动开工的条目数: {actionable}  {'✅ 公司已进入等待' if actionable == 0 else '⚠ 仍有活会跑'}")