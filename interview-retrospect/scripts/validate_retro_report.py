#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


REQUIRED_HEADINGS = [
    "## 一、基本信息",
    "## 二、面试总结",
    "## 三、综合评分",
    "## 四、逐题复盘",
    "## 五、面试反问环节",
    "## 六、表现亮点",
    "## 七、P0 / P1 / P2 调整项",
    "## 八、下一轮准备计划",
    "## 九、面试官画像",
]

REQUIRED_SNIPPETS = [
    "| 项目 | 内容 |",
    "| 维度 | 得分 | 支持证据 | 限制得分的证据 |",
    "| 序号 | 类型 | 面试官问题 | 我的回答摘要 | 原话证据 | 反思 | 理想回答框架 |",
    "| 优先级 | 问题 | 我当时怎么回答 | 证据 | 根本原因 | 改进方案 | 理想回答 |",
    "### 准备优先级",
    "### 可迁移训练",
    "### 面试官特征",
    "### 下一轮方向预测",
]

TITLE_PATTERN = re.compile(
    r"^# 面试复盘 \| (?:\d{4}-\d{2}-\d{2}|日期未知) .+\s+.+\s+.+\s*$",
    re.MULTILINE,
)

PLACEHOLDERS = ["YYYY-MM-DD", "X/10", "X/40", "✅／🟡／🔴"]
NO_REVERSE_QA_MARKERS = ["没有反问", "无反问", "未记录", "没有相关记录"]
REVERSE_QA_FIELDS = [
    "**我的原始问题**",
    "**面试官的完整回答**",
    "**关键原话**",
    "**透露的业务、团队或岗位信息**",
    "**对我求职判断的影响**",
    "**后续值得验证的问题**",
]


def section(text: str, heading: str, next_heading: Optional[str] = None) -> str:
    body = text.split(heading, 1)[1]
    if next_heading and next_heading in body:
        body = body.split(next_heading, 1)[0]
    return body


def validate(text: str) -> list[str]:
    errors: list[str] = []

    if not TITLE_PATTERN.search(text):
        errors.append(
            "标题不符合「面试复盘 | YYYY-MM-DD 公司 岗位 轮次」格式；日期未知时使用“日期未知”。"
        )

    positions = []
    for heading in REQUIRED_HEADINGS:
        position = text.find(heading)
        if position < 0:
            errors.append(f"缺少必需章节：{heading}")
        positions.append(position)
    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        errors.append("九个必需章节的顺序不正确。")

    for snippet in REQUIRED_SNIPPETS:
        if snippet not in text:
            errors.append(f"缺少必需结构：{snippet}")

    for placeholder in PLACEHOLDERS:
        if placeholder in text:
            errors.append(f"仍含未替换的模板占位符：{placeholder}")

    if all(heading in text for heading in [REQUIRED_HEADINGS[3], REQUIRED_HEADINGS[4]]):
        question_section = section(text, REQUIRED_HEADINGS[3], REQUIRED_HEADINGS[4])
        if not any(marker in question_section for marker in ["✅", "🟡", "🔴"]):
            errors.append("逐题复盘中未看到 ✅、🟡 或 🔴 状态标记。")

    if all(heading in text for heading in [REQUIRED_HEADINGS[4], REQUIRED_HEADINGS[5]]):
        reverse_section = section(text, REQUIRED_HEADINGS[4], REQUIRED_HEADINGS[5])
        no_reverse_qa = any(marker in reverse_section for marker in NO_REVERSE_QA_MARKERS)
        if not no_reverse_qa:
            for field in REVERSE_QA_FIELDS:
                if field not in reverse_section:
                    errors.append(f"反问环节缺少字段：{field}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="验证面试复盘 Markdown 的结构完整性。")
    parser.add_argument("report_path", help="待验证的 Markdown 报告路径；使用 - 从标准输入读取。")
    args = parser.parse_args()

    if args.report_path == "-":
        report_text = sys.stdin.read()
    else:
        report_path = Path(args.report_path)
        if not report_path.is_file():
            print(f"报告文件不存在：{report_path}", file=sys.stderr)
            raise SystemExit(1)
        report_text = report_path.read_text(encoding="utf-8")

    errors = validate(report_text)
    if errors:
        print("验证失败：")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("验证通过。")


if __name__ == "__main__":
    main()
