# 我的小火箭配置

上游是 [LingJingMaster/Shadowrocket-Rules](https://github.com/LingJingMaster/Shadowrocket-Rules)。规则名单（`AI.list`、国内、谷歌等）仍用上游地址，每天由小火箭自己拉。这个仓库只发布改过的总配置。

和上游的差别：

- AI 规则直接走 `PROXY`，也就是首页选中的节点，不走「美国节点」分组。
- DNS 覆写只问 `https://cloudflare-dns.com/dns-query#proxy`。
- 国内直连域名用 `223.5.5.5` 解析，不走节点，避免节点上的 DNS 失败时手机全部断网。
- 直连域名不使用系统 DNS。
- DNS 劫持不使用 `*:53`，只拦住常见的国内外 DNS 地址，并且不拦 `223.5.5.5`。

GitHub Actions 每天拉取上游并重新套上这些改动。小火箭的更新地址用本仓库的 Raw 链接，不要用上游链接。
