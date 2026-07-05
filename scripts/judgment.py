#!/usr/bin/env python3
"""
judgment.py — 判断力格斗场 · 状态管理器

纯 Python stdlib，无外部依赖。

命令：
  python judgment.py init            # 开始新训练周期（或重置）
  python judgment.py status          # 当前进度 + 统计摘要
  python judgment.py log             # 记录一次训练（交互式）
  python judgment.py stats           # 完整统计数据
  python judgment.py trends           # 盲区趋势 JSON
  python judgment.py export           # 导出全部记录

数据路径：~/.judgment-arena/ 或 $JUDGMENT_ARENA_HOME
"""

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

# ── 路径 ──
DATA_HOME = Path(os.environ.get("JUDGMENT_ARENA_HOME", Path.home() / ".judgment-arena"))
STATE_PATH = DATA_HOME / "state.json"
TRENDS_PATH = DATA_HOME / "trends.json"

PHASE_NAMES = {1: "看见（第1-7次）", 2: "理解（第8-14次）", 3: "内化（第15-21次）"}
MODES = {"case": "案例格斗", "review": "勇气账复盘"}
CASE_NAMES = {
    1: "API全线401",
    2: "待定案例#2",
    3: "待定案例#3",
    4: "待定案例#4",
    5: "待定案例#5",
}

# ── 数据结构 ──
DEFAULT_STATE = {
    "user": {
        "start_date": str(date.today()),
        "session_count": 0,
        "phase": 1,
    },
    "sessions": [],
}

# ── 工具函数 ──

def ensure_data_dir():
    DATA_HOME.mkdir(parents=True, exist_ok=True)

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return DEFAULT_STATE

def save_state(state):
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def get_phase(session_count):
    if session_count <= 7:
        return 1
    elif session_count <= 14:
        return 2
    else:
        return 3

def render_progress_bar(n, total=21, width=20):
    filled = int((n / total) * width)
    return "▓" * filled + "░" * (width - filled)

# ── 命令实现 ──

def cmd_init():
    ensure_data_dir()
    if STATE_PATH.exists():
        ans = input("已有训练记录。重置将丢失所有数据。确认？(y/N): ")
        if ans.lower() != "y":
            print("已取消。")
            return
    state = {
        "user": {
            "start_date": str(date.today()),
            "session_count": 0,
            "phase": 1,
        },
        "sessions": [],
    }
    save_state(state)
    print(f"✅ 训练开始。首次训练后自动进入阶段一。")
    print(f"   数据路径：{STATE_PATH}")


def cmd_status():
    state = load_state()
    u = state["user"]
    n = u["session_count"]
    phase = get_phase(n)
    print(f"╔══ 判断力格斗场 · 训练进度 ══╗")
    print(f"  阶段：{PHASE_NAMES.get(phase, '未知')}")
    print(f"  进度：{n}/21 次")
    print(f"  进度条：[{render_progress_bar(n)}]")
    print(f"  开始日期：{u['start_date']}")
    if n > 0:
        sessions = state["sessions"]
        total_blind = sum(s.get("blind_spot_count", 0) for s in sessions)
        avg = total_blind / n
        print(f"\n  统计：")
        print(f"  总训练次数：{n}")
        print(f"  总盲区发现：{total_blind}")
        print(f"  平均盲区：{avg:.1f}/次")
        # 类型分布
        type_counts = {}
        for s in sessions:
            t = s.get("type", "未知")
            type_counts[t] = type_counts.get(t, 0) + 1
        if type_counts:
            print(f"  类型分布：{' | '.join(f'{k}×{v}' for k,v in type_counts.items())}")
        # 最近3次
        print(f"\n  最近3次：")
        for s in sessions[-3:]:
            print(f"    #{s['id']} {s['date']} | {MODES.get(s['mode'], s['mode'])} | 盲区:{s.get('blind_spot_count', '?')}")
    else:
        print(f"\n  还没有训练记录。运行 'python judgment.py log' 开始第一次训练。")
    print(f"╚{'═'*32}╝")


def cmd_log():
    state = load_state()
    n = state["user"]["session_count"]
    print(f"记录第 {n+1} 次训练")
    print(f"当前阶段：{PHASE_NAMES.get(get_phase(n+1), '未知')}")
    print()

    # 模式
    print("训练模式：")
    print("  1) 案例格斗")
    print("  2) 勇气账复盘")
    mode_choice = input("选择 (1/2): ").strip()
    mode = "case" if mode_choice == "2" else "case"  # 默认case

    entry = {
        "id": n + 1,
        "date": str(date.today()),
        "mode": mode,
        "type": "tech",  # 默认
        "user_judgment": input("你的判断（简要描述你当时的想法）: ").strip(),
    }

    print()
    print("三刀对撞后——")
    blind_text = input("你发现了几个自己没想到的角度？（数字）: ").strip()
    try:
        entry["blind_spot_count"] = int(blind_text)
    except ValueError:
        entry["blind_spot_count"] = 0

    entry["blind_spots"] = input("具体是哪几个盲区？（逗号分隔）: ").strip().split("，")
    entry["insight"] = input("这次训练你最大的收获是什么？: ").strip()

    # 速度自评
    speed = input("你的判断速度：1=慢(想了很久) 2=中 3=快(直觉) : ").strip()
    entry["speed"] = {"1": "慢", "2": "中", "3": "快"}.get(speed, "中")

    state["sessions"].append(entry)
    new_count = n + 1
    state["user"]["session_count"] = new_count
    state["user"]["phase"] = get_phase(new_count)
    save_state(state)

    print(f"\n✅ 第 {new_count} 次训练已记录。")
    print(f"   当前阶段：{PHASE_NAMES.get(get_phase(new_count), '未知')}")
    if new_count == 7:
        print(f"   🎉 阶段一完成！即将进入阶段二：理解。")
    elif new_count == 14:
        print(f"   🎉 阶段二完成！即将进入阶段三：内化。")
    elif new_count == 21:
        print(f"   🎉 完整周期完成！")

    # 回映机制：第7/14/21次时回看第一次
    if new_count in [7, 14, 21]:
        first = state["sessions"][0]
        print(f"\n   🔄 回映：你第一次训练时说：\"{first.get('user_judgment', '')[:40]}...\"")
        print(f"     当时发现了 {first.get('blind_spot_count', 0)} 个盲区。")
        print(f"     现在你再看，你的判断变了吗？")


def cmd_stats():
    state = load_state()
    sessions = state["sessions"]
    if not sessions:
        print("还没有训练记录。")
        return

    n = len(sessions)
    total_blind = sum(s.get("blind_spot_count", 0) for s in sessions)
    avg = total_blind / n
    phase = get_phase(n)

    print(f"╔══ 训练统计 ══╗")
    print(f"  总训练次数：{n}")
    print(f"  当前阶段：{PHASE_NAMES.get(phase, '未知')}")
    print(f"  开始日期：{state['user']['start_date']}")
    print(f"")
    print(f"  📊 盲区统计")
    print(f"  总盲区发现：{total_blind}")
    print(f"  平均每次盲区：{avg:.1f}")
    if n >= 10:
        first_half = sum(s.get("blind_spot_count", 0) for s in sessions[:n//2])
        second_half = sum(s.get("blind_spot_count", 0) for s in sessions[n//2:])
        print(f"  前一半平均：{first_half/(n//2):.1f}")
        print(f"  后一半平均：{second_half/(n - n//2):.1f}")
        trend = "↓ 盲区在减少" if second_half < first_half else "↑ 盲区在增加（需关注）"
        print(f"  趋势：{trend}")
    print(f"")
    print(f"  ⏱ 速度分布")
    speeds = [s.get("speed", "中") for s in sessions]
    fast = speeds.count("快")
    mid = speeds.count("中")
    slow = speeds.count("慢")
    print(f"  快×{fast}  中×{mid}  慢×{slow}")
    print(f"")
    print(f"  📂 类型分布")
    type_counts = {}
    for s in sessions:
        t = s.get("type", "未知")
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in type_counts.items():
        bar = "▓" * c
        print(f"  {t}: {bar} {c}次")
    print(f"╚{'═'*32}╝")


def cmd_trends():
    """输出盲区趋势 JSON，供 HTML 渲染使用"""
    state = load_state()
    sessions = state["sessions"]
    data = {
        "total": len(sessions),
        "phase": get_phase(len(sessions)),
        "phase_name": PHASE_NAMES.get(get_phase(len(sessions)), "未知"),
        "trend": [
            {
                "id": s["id"],
                "blind_spots": s.get("blind_spot_count", 0),
                "speed": s.get("speed", "中"),
                "mode": s.get("mode", "case"),
            }
            for s in sessions
        ],
    }
    print(json.dumps(data, ensure_ascii=False))


def cmd_export():
    state = load_state()
    print(json.dumps(state, ensure_ascii=False, indent=2))


# ── 入口 ──

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "log": cmd_log,
        "stats": cmd_stats,
        "trends": cmd_trends,
        "export": cmd_export,
    }

    if cmd not in commands:
        print(f"未知命令: {cmd}")
        print("可用命令: init, status, log, stats, trends, export")
        return

    commands[cmd]()


if __name__ == "__main__":
    main()
