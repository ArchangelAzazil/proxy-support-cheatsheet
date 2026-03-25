<div align="center">

<img src="logo1.png" alt="Insanity Security Logo" width="120"/>

# 🛡️ Proxy Support Engineer Cheatsheet

### *By Anthony Abella — Insanity Security*

[![proxy-cheap](https://img.shields.io/badge/proxy--cheap.com-Reference%20Doc-ff3333?style=for-the-badge&logo=shield&logoColor=white)](https://proxy-cheap.com)
[![Made With](https://img.shields.io/badge/Made%20With-Neovim-57A143?style=for-the-badge&logo=neovim&logoColor=white)](https://neovim.io)
[![Arch Linux](https://img.shields.io/badge/Arch-Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)](https://archlinux.org)
[![License](https://img.shields.io/badge/License-Read%20Only-7c6af7?style=for-the-badge&logo=readthedocs&logoColor=white)](#)

---

> *"The best support engineer isn't the one who knows all the answers —*
> *it's the one who knows exactly where to look."*

</div>

---

## 🔥 What Is This?

This is my **personal T2 Support Engineer reference** for diagnosing, testing, and configuring proxies at [proxy-cheap.com](https://proxy-cheap.com). Everything in here is battle-tested from real support work — no fluff, no filler.

If you're working with proxies, Clash, or just want to stop fumbling around in nano, this is for you.

---

## 📦 What's Inside the PDF

The cheatsheet is a **dark-themed, print-ready PDF** covering the full T2 support workflow from editor to terminal to live diagnostics.

| # | Section | What You'll Find |
|---|---------|-----------------|
| 1 | **Neovim Basics** | Modes, navigation, search/replace, clipboard, splits, recommended `init.vim` |
| 2 | **.conf File Editing** | Navigating sections, proxy edits, commenting blocks, diff, inserting test output |
| 3 | **YAML & Clash Config** | YAML rules, Clash structure, proxy entries, validation commands |
| 4 | **Clash Proxy-Group Types** | `select`, `url-test`, `fallback`, `load-balance`, `relay` — with full config examples |
| 5 | **Clash REST API** | All 19 verified endpoints, copy-paste curl commands, mode switching |
| 6 | **Curl Proxy Testing** | Connectivity, latency, download/upload speed, social media access checks |
| 7 | **Server-Side Diagnostics** | TCP port tests, DNS leak detection, proxy anonymity checks, TLS inspection, CONNECT tunnel tracing |

---

## 🚀 Quick Start

### Download the PDF

Grab the latest release from the [Releases](../../releases) page or directly:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/proxy-support-cheatsheet.git
cd proxy-support-cheatsheet

# Open the PDF
xdg-open proxy-cheap-cheatsheet-v3-final.pdf   # Linux
open proxy-cheap-cheatsheet-v3-final.pdf        # macOS
```

---

## 🧪 Curl Commands — Quick Preview

> Full format: `user:pass@IP:PORT`

### ✅ Basic Connectivity
```bash
# Get your exit IP via HTTP proxy
curl -x http://user:pass@IP:PORT https://api.ipify.org

# SOCKS5
curl --socks5 user:pass@IP:PORT https://api.ipify.org

# SOCKS5h — DNS resolved through proxy
curl --socks5-hostname user:pass@IP:PORT https://api.ipify.org

# Full geo info
curl -x http://user:pass@IP:PORT https://ipapi.co/json/
```

### ⏱️ Latency Breakdown
```bash
curl -x http://user:pass@IP:PORT -o /dev/null -s \
  -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  https://www.google.com
```

### 🕵️ Anonymity Check — Is Your Real IP Leaking?
```bash
# Elite proxy = zero proxy headers returned
curl -s -x http://user:pass@IP:PORT https://httpbin.org/headers \
  | python3 -m json.tool \
  | grep -E "Forwarded|Via|Proxy|X-Real"
# Nothing returned = elite. X-Forwarded-For present = transparent (bad).
```

### 🌍 Batch Social Media Check
```bash
PROXY='http://user:pass@IP:PORT'
for site in facebook.com instagram.com twitter.com tiktok.com youtube.com reddit.com linkedin.com; do
  CODE=$(curl -x $PROXY -o /dev/null -s -w '%{http_code}' https://$site)
  echo "$site -> $CODE"
done
```

### 🔬 CONNECT Tunnel Verification (HTTPS through HTTP proxy)
```bash
curl -v -x http://user:pass@IP:PORT https://www.google.com 2>&1 \
  | grep -i 'CONNECT\|tunnel\|200 Connection'
# Expect: HTTP/1.1 200 Connection established
```

---

## 🌐 Clash REST API — Quick Reference

> Enable with `external-controller: 127.0.0.1:9090` in `config.yaml`

```bash
# List all proxies
curl http://127.0.0.1:9090/proxies | python3 -m json.tool

# Switch active proxy in a group
curl -X PUT http://127.0.0.1:9090/proxies/PROXY \
     -H "Content-Type: application/json" \
     -d '{"name":"pc-us-1"}'

# Kill all connections (force re-route)
curl -X DELETE http://127.0.0.1:9090/connections

# Switch to direct mode instantly (bypass all proxies)
curl -X PATCH http://127.0.0.1:9090/configs \
     -H "Content-Type: application/json" \
     -d '{"mode":"direct"}'

# Stream live logs
curl http://127.0.0.1:9090/logs

# Test latency on a specific proxy
curl "http://127.0.0.1:9090/proxies/pc-us-1/delay?url=http://www.gstatic.com/generate_204&timeout=5000"
```

---

## 🔴 HTTP Status Code Cheat Sheet

| Code | Meaning | What It Tells You |
|------|---------|-------------------|
| `200` | ✅ OK | Proxy working, destination reachable |
| `301/302` | ↪️ Redirect | Use `-L` to follow. Check final URL |
| `403` | 🚫 Forbidden | Proxy works — site is geo-blocking or IP flagged |
| `407` | 🔑 Auth Required | Wrong `user:pass`, expired credentials, or wrong format |
| `429` | 🚦 Rate Limited | Slow down — proxy or site bandwidth cap hit |
| `000` | 💀 No Response | Proxy dead, wrong `IP:PORT`, firewall drop, timeout |
| `502` | ⚠️ Bad Gateway | Proxy got invalid response from upstream |
| `503` | ⚠️ Unavailable | Proxy or destination server overloaded/down |
| `504` | ⏰ Gateway Timeout | Proxy timed out waiting for upstream |
| `ECONNREFUSED` | 🔌 Port Closed | Server reachable but nothing listening on that port |

---

## 🛠️ Tools & Stack

| Tool | Purpose |
|------|---------|
| [Neovim](https://neovim.io) | Primary editor for configs, logs, and docs |
| [Clash](https://en.clash.wiki) | Proxy rule engine and traffic manager |
| `curl` | Primary diagnostic and testing tool |
| [proxy-cheap.com](https://proxy-cheap.com) | Proxy provider |
| `xclip` | System clipboard integration on Arch Linux |
| `python-yaml` | YAML syntax validation |
| Arch Linux | OS of choice |

---

## 📐 Neovim Setup — TL;DR

```bash
# Install on Arch
sudo pacman -S neovim xclip python-yaml

# Jump into the tutor
nvim
:Tutor

# Paste this into ~/.config/nvim/init.vim
set number relativenumber expandtab tabstop=2 shiftwidth=2
set hlsearch ignorecase smartcase nowrap scrolloff=5
set clipboard=unnamedplus
```

---

## 🧩 Clash Proxy-Group Decision Tree

```
Need manual control?          → type: select
Need fastest auto-selection?  → type: url-test   (+ tolerance: 50)
Need automatic failover?      → type: fallback   (order matters)
Need to spread load?          → type: load-balance (strategy: consistent-hashing)
Need multi-hop routing?       → type: relay      (no UDP)

Recommended setup:
  PROXY (select) → AUTO (url-test) → FAILOVER (fallback) → DIRECT
```

---

## ⚠️ Common Gotchas

```
❌ YAML tabs          → Use :set expandtab. Always. Non-negotiable.
❌ Wrong proxy format → Must be user:pass@IP:PORT not IP:PORT:user:pass
❌ 407 on every test  → Check credentials. Regenerate if needed.
❌ 000 on curl        → Test TCP first: nc -zv IP PORT
❌ X-Forwarded-For    → Transparent proxy leaking real IP. Escalate.
❌ Clash group missing from dashboard → Indentation error in YAML
```

---

## 📄 License & Attribution

This document is authored by **Anthony Abella** of **Insanity Security** for internal use at [proxy-cheap.com](https://proxy-cheap.com).

The PDF is **read-only protected** — editing and copying are locked. Attribution stays with the document.

> Feel free to reference and share this repo. If you use something from it, a ⭐ on the repo is appreciated.

---

<div align="center">

<img src="logo1.png" alt="Insanity Security" width="60"/>

**Anthony Abella**
T2 Support Engineer · [proxy-cheap.com](https://proxy-cheap.com)
*Insanity Security*

[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/YOUR_USERNAME)

</div>
