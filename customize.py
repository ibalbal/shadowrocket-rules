#!/usr/bin/env python3
"""拉取 LingJingMaster 的小火箭总配置，套上本机正在用的个性化设置。"""

import sys
import urllib.request

UPSTREAM = (
    "https://raw.githubusercontent.com/LingJingMaster/"
    "Shadowrocket-Rules/refs/heads/main/Shadowrocket.conf"
)
DNS = "https://cloudflare-dns.com/dns-query#proxy"
# 节点名里高于 1 的倍率。1x、1.0x、0.5x 和没写倍率的名字不会被命中。
ABOVE_1X = (
    r"(?:(?:^|[^0-9.])(?:[1-9]\d+(?:\.\d+)?|[2-9](?:\.\d+)?|1\.\d*[1-9]\d*)\s*[xX×ｘＸ倍]"
    r"|(?:^|[^0-9.xX×ｘＸ])[xX×ｘＸ]\s*(?:[1-9]\d+(?:\.\d+)?|[2-9](?:\.\d+)?|1\.\d*[1-9]\d*)"
    r"|(?:^|[^0-9.])倍率\s*[:：=]?\s*(?:[1-9]\d+(?:\.\d+)?|[2-9](?:\.\d+)?|1\.\d*[1-9]\d*))"
)


def limit_auto_select(expr: str) -> str:
    """自动测速只留下倍率不超过 1x 的节点。"""
    if ABOVE_1X in expr:
        return expr
    wrapped = "^(?!.*(?:"
    if expr.startswith("^((?!(") and expr.endswith(")).)*$"):
        inner = expr[len("^((?!(") : -len(")).)*$")]
        return f"{wrapped}{inner}))(?!.*(?:{ABOVE_1X})).*$"
    return f"^(?=.*(?:{expr}))(?!.*(?:{ABOVE_1X})).*$"


def rewrite_rate_limit(line: str) -> str:
    marker = "policy-regex-filter="
    if marker not in line:
        return line
    head, expr = line.split(marker, 1)
    return head + marker + limit_auto_select(expr.strip())


def customize(text: str, raw_url: str) -> str:
    out = []
    for line in text.splitlines():
        line = rewrite_rate_limit(line)
        if line.startswith("update-url "):
            out.append(f"update-url = {raw_url}")
        elif line.startswith("dns-server "):
            out.append(f"dns-server = {DNS}")
        elif line.startswith("fallback-dns-server "):
            out.append(f"fallback-dns-server = {DNS}")
        elif line.startswith("dns-direct-system "):
            out.append("dns-direct-system = false")
        elif line.startswith("hijack-dns "):
            out.append("hijack-dns = *:53")
        elif "AI.list," in line and line.rstrip().endswith("🤖 AI 服务"):
            out.append(line.replace(",🤖 AI 服务", ",PROXY"))
        elif line.startswith("🤖 AI 服务 "):
            out.append(
                line.replace(
                    "policy-select-name=🇺🇸 美国节点",
                    "policy-select-name=PROXY",
                )
            )
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def main() -> None:
    raw_url = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "Shadowrocket.conf"
    with urllib.request.urlopen(UPSTREAM, timeout=60) as resp:
        text = resp.read().decode("utf-8")
    open(out_path, "w", encoding="utf-8").write(customize(text, raw_url))


if __name__ == "__main__":
    main()
