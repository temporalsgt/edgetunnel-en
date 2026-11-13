# edgetunnel-en

An English-panel fork of [cmliu/edgetunnel](https://github.com/cmliu/edgetunnel).

The tunnel/protocol logic is unchanged. The only goal of this fork is to make the
login page, admin dashboard, dialogs, buttons and error pages readable in English.
Internal configuration keys are kept in their original form so that the worker and
existing KV data remain compatible.

## What is different

- English UI in `panel/public/admin`, `panel/public/login`, `panel/public/noADMIN`
  and `panel/public/noKV`.
- The worker reads an optional `PAGES_URL` environment variable. If it is set, the
  worker proxies the panel pages from that origin instead of the upstream Chinese
  panel at `https://edt-pages.github.io`.
- No changes to VLESS/Trojan/Shadowsocks handling, subscription generation, KV
  keys, or API routes.

## Deploy the panel (Cloudflare Pages)

The panel is a static site. From the `panel/` directory:

```bash
cd panel
wrangler pages project create edgetunnel-en-panel --production-branch main --force
wrangler pages deploy --branch main
```

The project name in `panel/wrangler.toml` determines the URL. This repository uses
`https://edgetunnel-en-panel.pages.dev`.

## Deploy the worker (Cloudflare Pages)

1. Create a Pages project, for example `edgetunnel-en`.
2. Add a KV namespace binding named `KV`.
3. Add a secret named `ADMIN` (the admin panel password).
4. Optionally add `PAGES_URL` as a variable if the panel is hosted elsewhere.
5. Deploy `_worker.js` with a Pages configuration whose
   `pages_build_output_dir` contains `_worker.js` at its root.

The helper script does the upload part:

```bash
./scripts/deploy-pages-worker.sh edgetunnel-en
```

Then open:

- Panel: `https://<worker>.pages.dev/admin`
- Login: `https://<worker>.pages.dev/login`

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `ADMIN` | Yes | Admin panel password. |
| `KEY` | No | Quick subscription path key. |
| `UUID` | No | Fixed UUIDv4 for generated nodes. |
| `PROXYIP` | No | Custom proxy IP/host. |
| `URL` | No | Camouflage page URL or `1101`. |
| `PAGES_URL` | No | Origin of the English panel, for example `https://edgetunnel-en-panel.pages.dev`. |
| `DEBUG` | No | Set to `1` or `true` to enable debug logs. |
| `OFF_LOG` | No | Set to `1` or `true` to disable KV log recording. |

## Upstream and license

This project is a derivative of `cmliu/edgetunnel` and keeps the original
`LICENSE` and attribution. The upstream project and its contributors own the
protocol implementation. See `LICENSE` for the full GPL-2.0 terms.

Upstream: https://github.com/cmliu/edgetunnel
