# 我的小火箭配置

上游是 [LingJingMaster/Shadowrocket-Rules](https://github.com/LingJingMaster/Shadowrocket-Rules)。规则名单（`AI.list`、国内、谷歌等）仍用上游地址，每天由小火箭自己拉。这个仓库只发布改过的总配置。

和上游的差别：

- AI 规则直接走 `PROXY`，也就是首页选中的节点，不走「美国节点」分组。
- DNS 只问 `https://cloudflare-dns.com/dns-query#proxy`。
- 直连域名不使用系统 DNS。
- DNS 劫持是 `*:53`。

GitHub Actions 每天拉取上游并重新套上这些改动。小火箭的更新地址用本仓库的 Raw 链接，不要用上游链接。
