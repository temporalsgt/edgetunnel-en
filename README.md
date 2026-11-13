# 🚀 edgetunnel 2.1 — English Panel Fork

[![Stars](https://img.shields.io/github/stars/temporalsgt/edgetunnel-en?style=flat-square&logo=github)](https://github.com/temporalsgt/edgetunnel-en/stargazers)
[![Forks](https://img.shields.io/github/forks/temporalsgt/edgetunnel-en?style=flat-square&logo=github)](https://github.com/temporalsgt/edgetunnel-en/network/members)
[![License](https://img.shields.io/github/license/temporalsgt/edgetunnel-en?style=flat-square)](https://github.com/temporalsgt/edgetunnel-en/blob/main/LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Group-blue?style=flat-square&logo=telegram)](https://t.me/CMLiussss)
[![YouTube](https://img.shields.io/badge/YouTube-Channel-red?style=flat-square&logo=youtube)](https://www.youtube.com/watch?v=LeT4jQUh8ok)

---

## 📖 Introduction

**edgetunnel** is an edge-computing tunneling solution built on the Cloudflare Workers/Pages platform. It handles network traffic efficiently and provides a powerful admin panel with flexible node configuration.

> **This repository is an English-panel fork of [cmliu/edgetunnel](https://github.com/cmliu/edgetunnel).**
> The tunnel and protocol logic is unchanged. The login page, admin dashboard, dialogs, buttons, tooltips, and error pages are translated into English. Internal configuration keys keep their original names so the worker and existing KV data remain compatible.

### 🍴 About this fork

- English UI for `/login`, `/admin`, `/noADMIN`, and `/noKV`.
- The worker supports an optional `PAGES_URL` environment variable. When it is set, panel pages are proxied from that origin. When it is unset, this fork uses its default English panel.
- No changes to VLESS/Trojan/Shadowsocks handling, subscription generation, KV keys, or API routes.
- This fork's deployment:
  - Worker / main site: <https://edgetunnel-en-b1g.pages.dev>
  - Admin login: <https://edgetunnel-en-b1g.pages.dev/login>
  - Admin panel: <https://edgetunnel-en-b1g.pages.dev/admin>
  - Static panel project: <https://edgetunnel-en-panel.pages.dev>

### ✨ Core features

- 🛡️ **Protocol support**: VLESS, Trojan, Shadowsocks, and other mainstream protocols with deep integration of encrypted transport.
- 📊 **Admin panel**: a built-in visual dashboard for live configuration changes, operation logs, and traffic statistics.
- 🛠️ **Flexible deployment**: fully supports Cloudflare Workers and Cloudflare Pages (GitHub integration or direct upload).
- 🔄 **Subscription system**: automatic subscription generation and obfuscation conversion, compatible with popular clients such as Clash, Sing-box, and Surge.
- ⚡ **Performance acceleration**: custom ProxyIP, SOCKS5/HTTP chain proxies, and preferred-IP APIs to reduce network latency.
- 🌐 **Cross-platform**: works with Windows, Android, iOS, macOS, and common router firmware.

---

## 💡 Quick deployment

> [!TIP]
> 📖 Detailed illustrated guide (upstream, Chinese): [edgetunnel deployment guide](https://cmliussss.com/p/edt2/)

> [!WARNING]
> ⚠️ **Error 1101**: [video walkthrough](https://www.youtube.com/watch?v=r4uVTEJptdE)

### ⚙️ Workers deployment

<details>
<summary><code><strong>Workers deployment — text guide</strong></code></summary>

1. Deploy a Cloudflare Worker:
   - Create a new Worker in the Cloudflare dashboard.
   - Paste the contents of [_worker.js](https://github.com/temporalsgt/edgetunnel-en/blob/main/_worker.js) into the Worker editor.
   - Open `Settings` → `Variables` → `Add variable`.
     Set the variable name to **ADMIN** and the value to your admin password, then click `Save`.

2. Bind a KV namespace:
   - Open `Bindings` → `Add binding` → `KV namespace`, then select an existing namespace or create a new one.
   - Set the variable name to **KV**, then click `Add binding`.

3. Attach a custom domain to the Worker:
   - Open the Worker's `Triggers` tab and click `Add custom domain`.
   - Enter a subdomain that is already managed by Cloudflare, for example `vless.example.com`, then click `Add custom domain` and wait for the certificate to become active.

4. Open the admin panel:
   - Visit `https://vless.example.com/admin` and enter your admin password.

</details>

### 🛠️ Pages upload deployment **Recommended** — [guide](https://cmliussss.com/p/edt2/)

<details>
<summary><code><strong>Pages file-upload deployment — text guide</strong></code></summary>

1. Deploy Cloudflare Pages:
   - Download [main.zip](https://github.com/temporalsgt/edgetunnel-en/archive/refs/heads/main.zip) and give the repository a Star.
   - In the Cloudflare Pages dashboard, choose `Upload assets`, enter a project name, and click `Create project`. Upload the downloaded [main.zip](https://github.com/temporalsgt/edgetunnel-en/archive/refs/heads/main.zip), then click `Deploy site`.
   - After deployment, click `Continue to project`, then open `Settings` → `Environment variables` → **Production** → `Add variable`.
     Set the variable name to **ADMIN** and the value to your admin password, then click `Save`.
   - Return to the `Deployments` tab, click `Create new deployment` in the lower-right corner, upload [main.zip](https://github.com/temporalsgt/edgetunnel-en/archive/refs/heads/main.zip) again, then click `Save and deploy`.

2. Bind a KV namespace:
   - Open `Settings` → `Bindings` → `+ Add` → `KV namespace`, then select an existing namespace or create a new one.
   - Set the variable name to **KV**, click `Save`, then retry the deployment.

3. Attach a custom domain to Pages: [video guide](https://www.youtube.com/watch?v=LeT4jQUh8ok&t=851s)
   - Open the Pages project's `Custom domains` tab and click `Set up a custom domain`.
   - Enter a subdomain, not your root domain. For example, if your assigned domain is `example.com`, use `panel.example.com`.
   - At your DNS provider, add the CNAME record requested by Cloudflare, using the `pages.dev` target shown in your Pages project (for example `your-project.pages.dev`). Then click `Activate domain`.

4. Open the admin panel:
   - Visit `https://panel.example.com/admin` and enter your admin password.

</details>

### 🛠️ Pages + GitHub deployment

<details>
<summary><code><strong>Pages + GitHub deployment — text guide</strong></code></summary>

1. Deploy Cloudflare Pages:
   - Fork this repository on GitHub and give it a Star.
   - In the Cloudflare Pages dashboard, choose `Connect to Git`, select the `edgetunnel-en` project, and click `Begin setup`.
   - On the `Set up builds and deployments` page, open `Environment variables (advanced)` and click `Add variable`.
     Set the variable name to **ADMIN** and the value to your admin password, then click `Save and deploy`.

2. Bind a KV namespace:
   - Open `Settings` → `Bindings` → `+ Add` → `KV namespace`, then select an existing namespace or create a new one.
   - Set the variable name to **KV**, click `Save`, then retry the deployment.

3. Attach a custom domain to Pages: [video guide](https://www.youtube.com/watch?v=LeT4jQUh8ok&t=851s)
   - Open the Pages project's `Custom domains` tab and click `Set up a custom domain`.
   - Enter a subdomain, not your root domain. For example, if your assigned domain is `example.com`, use `panel.example.com`.
   - At your DNS provider, add the CNAME record requested by Cloudflare, using the `pages.dev` target shown in your Pages project. Then click `Activate domain`.

4. Open the admin panel:
   - Visit `https://panel.example.com/admin` and enter your admin password.

</details>

### ⚡ Deploy with Wrangler

Panel (static site):

```bash
cd panel
wrangler pages project create edgetunnel-en-panel --production-branch main --force
wrangler pages deploy --branch main
```

Worker (Cloudflare Pages, direct upload):

```bash
# Create the Pages project once
wrangler pages project create edgetunnel-en --production-branch main --force

# Set the admin password once
wrangler pages secret put ADMIN --project-name edgetunnel-en

# Deploy the worker with its KV binding and panel origin
KV_ID=<kv-namespace-id> \
PAGES_URL=https://edgetunnel-en-panel.pages.dev \
./scripts/deploy-pages-worker.sh edgetunnel-en
```

Then open `https://<your-worker>.pages.dev/admin`.

---

## 🔑 Environment variables

| Variable | Required | Example | Description |
| :--- | :---: | :--- | :--- |
| **ADMIN** | ✅ | `123456` | Admin panel login password. |
| **KEY** | ❌ | `CMLiussss` | Quick subscription path key. Visit `/CMLiussss` to get nodes quickly. |
| **UUID** | ❌ | `90cd4a77-141a-43c9-991b-08263cfe9c10` | Force a fixed UUID. Only **UUIDv4** is supported. |
| **PROXYIP** | ❌ | `proxyip.cmliussss.net:443` | Global custom reverse-proxy IP. |
| **URL** | ❌ | `https://cloudflare-error-page-3th.pages.dev` | Default camouflage page URL (a web URL or `1101`). |
| **GO2SOCKS5** | ❌ | `blog.cmliussss.com`,`*.ip111.cn`,`*google.com` | List of destinations forced through SOCKS5 (`*` means global; separate domains with commas). |
| **DEBUG** | ❌ | `1` or `true` | **Developer mode**. Debug logging (`console.log`) is **off** by default; set to `1` or `true` to enable it. |
| **OFF_LOG** | ❌ | `1` or `true` | KV log recording is **on** by default; set to `1` or `true` to disable it. |
| **BEST_SUB** | ❌ | `1` or `true` | Preferred-subscription-generator mode is **off** by default; set to `1` or `true` to enable it. |
| **PRELOAD_RACE_DIAL** | ❌ | `1` or `true` | Preload race dialing is **off** by default; set to `1` or `true` to enable it. |
| **TCP_CONCURRENT_DIAL** | ❌ | `2` | Number of concurrent TCP dials. Default: `2`. When set, it no longer automatically drops to a single route on China Mobile networks. |
| **PROXY_CONCURRENT_DIAL** | ❌ | `1` | Number of concurrent proxy dials. Default: `1`. Higher values connect faster but switch IPs more often. |
| **PAGES_URL** | ❌ | `https://edgetunnel-en-panel.pages.dev` | Origin of the English panel static site. When omitted, this fork uses its default English panel. |

---

## 🔧 Advanced tips

To change the **TOKEN in the subscription URL** and the **UUID used for node validation**, modify the variables below:

1. Change the value of `ADMIN` or `KEY` to randomize both the subscription TOKEN and the node-validation UUID.
2. Set the `UUID` variable to force a fixed subscription TOKEN and node-validation UUID. It must be a valid **UUIDv4**, otherwise nodes will not work.

This tool can switch the underlying proxy mode dynamically through the request path:

- Specify `PROXYIP`:

  ```url
  /proxyip=proxyip.cmliussss.net
  /?proxyip=proxyip.cmliussss.net
  ```

- Specify `SOCKS5`:

  ```url
  /socks5=user:password@127.0.0.1:1080
  /?socks5=user:password@127.0.0.1:1080
  /socks://dXNlcjpwYXNzd29yZA==@127.0.0.1:1080 (activates global SOCKS5 by default)
  /socks5://user:password@127.0.0.1:1080 (activates global SOCKS5 by default)
  ```

- Specify an `HTTP proxy`:

  ```url
  /http=user:password@127.0.0.1:1080
  /http://user:password@127.0.0.1:8080 (activates global SOCKS5 by default)
  ```

- Specify a `Trojan fallback` (for self-hosted integrations only; Trojan inbound only; the fallback service must use the same password and must not use WebSocket or TLS; UDP is passed through to the fallback with excellent performance and full functionality):

  ```url
  /trojan=1.1.1.1:1234
  ```

---

## 💻 Client compatibility

| Platform | Recommended clients |
| :--- | :--- |
| **Windows** | [v2rayN](https://github.com/2dust/v2rayN/releases), [Hiddify](https://github.com/hiddify/hiddify-app/releases), [FlClash](https://github.com/chen08209/FlClash/releases), [mihomo-party](https://github.com/mihomo-party-org/clash-party/releases), [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), [Clashmi](https://github.com/KaringX/clashmi/releases), [FlyClash](https://github.com/GtxFury/FlyClash/releases), [Karing](https://github.com/KaringX/karing/releases), [Bettbox](https://github.com/appshubcc/Bettbox/releases) |
| **Android** | [v2rayNG](https://github.com/2dust/v2rayNG/releases), [ClashMetaForAndroid](https://github.com/MetaCubeX/ClashMetaForAndroid/releases/), [FlClash](https://github.com/chen08209/FlClash/releases), [Clashmi](https://github.com/KaringX/clashmi/releases), [Hiddify](https://github.com/hiddify/hiddify-app/releases), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases), [FlyClash](https://github.com/GtxFury/FlyClash/releases), [Karing](https://github.com/KaringX/karing/releases), [Bettbox](https://github.com/appshubcc/Bettbox/releases) |
| **iOS** | Surge, Shadowrocket, Stash, [Hiddify](https://github.com/hiddify/hiddify-app/releases), Loon, Egern, [Clashmi](https://clashmi.app/download), [Karing](https://karing.app/), Quantumult X |
| **macOS** | [FlClash](https://github.com/chen08209/FlClash/releases), [mihomo-party](https://github.com/mihomo-party-org/clash-party/releases), [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), Surge, [Clashmi](https://clashmi.app/download), [Karing](https://karing.app/), [FlyClash](https://github.com/GtxFury/FlyClash/releases) |
| **HarmonyOS** | [ClashBox](https://github.com/xiaobaigroup/ClashBox/releases) |

---

## ⭐ Upstream popularity

![Stargazers over time](https://github.com/cmliu/cmliu/blob/main/star/edgetunnel.svg)

---

## 🙏 Acknowledgements

### 💖 Sponsors — providing cloud servers for the [subscription conversion service](https://sub.cmliussss.net/)

- [Yuusei Network](https://yuusei.io/)
- [VMRack](https://www.vmrack.net?ref_code=5Zk7eNhbgL7)

### 🛠 Open-source code references

- [zizifn/edgetunnel](https://github.com/zizifn/edgetunnel)
- [3Kmfi6HP/EDtunnel](https://github.com/6Kmfi6HP/EDtunnel)
- [SHIJS1999/cloudflare-worker-vless-ip](https://github.com/SHIJS1999/cloudflare-worker-vless-ip)
- [Stanley-baby](https://github.com/Stanley-baby)
- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR/tree/master/Clash/config)
- [股神](https://t.me/CF_NAT/38889)
- [Workers/Pages Metrics](https://t.me/zhetengsha/3382)
- [白嫖哥](https://t.me/bestcfipas)
- [Mingyu](https://github.com/ymyuuu/workers-vless)
- [ToiCF/CF-Workers-HTTPS](https://github.com/ToiCF/CF-Workers-HTTPS)
- [ToiCF/CF-Workers-TURN](https://github.com/ToiCF/CF-Workers-TURN)
- [ToiCF/CF-Workers-SoftEther](https://github.com/ToiCF/CF-Workers-SoftEther)
- [eooce](https://github.com/eooce/Cloudflare-proxy)
- [Sukka](https://ip.skk.moe/)
- [zhangtaile](https://github.com/cmliu/edgetunnel/pull/999)
- [1345695](https://github.com/1345695/edcloudwasm)
- [ToiCF/GrainTCP](https://github.com/ToiCF/GrainTCP)
- [xream](https://github.com/cmliu/edgetunnel/pull/1359)

---

## ⚠️ Disclaimer

1. This project ("edgetunnel") is intended **for educational, scientific research, and personal security testing purposes only**.
2. When downloading or using this project's code, you must strictly comply with the laws and regulations of your region.
3. The original author, **cmliu**, assumes no responsibility for any behavior or consequence caused by misuse of this project's code.
4. This project is not responsible for any direct or indirect damages caused by the use of its code.
5. It is recommended to delete any deployment related to this project within 24 hours after testing.

---

**If you find this project useful, please give it a Star 🌟 — it means a lot!**
