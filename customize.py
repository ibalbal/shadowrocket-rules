#!/usr/bin/env python3
"""拉取 LingJingMaster 的小火箭总配置，套上本机正在用的个性化设置。"""

import sys
import urllib.request

UPSTREAM = (
    "https://raw.githubusercontent.com/LingJingMaster/"
    "Shadowrocket-Rules/refs/heads/main/Shadowrocket.conf"
)
DNS = "https://cloudflare-dns.com/dns-query#proxy"


def customize(text: str, raw_url: str) -> str:
    out = []
    for line in text.splitlines():
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
