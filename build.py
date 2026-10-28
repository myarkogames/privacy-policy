import html
import json
import pathlib

root = pathlib.Path(__file__).parent
policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
dev = html.escape(policy["developer"])
email = html.escape(policy["email"])
updated = policy["updated"]

style = """
:root{color-scheme:light dark;--fg:#1d1d1f;--muted:#5f6368;--bg:#fff;--line:#e3e3e3;--link:#1a5fd0}
@media (prefers-color-scheme:dark){:root{--fg:#ececec;--muted:#a8a8a8;--bg:#141414;--line:#2c2c2c;--link:#7fb0ff}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:28px;line-height:1.25;margin:0 0 4px}h2{font-size:20px;margin:32px 0 8px;padding-top:16px;border-top:1px solid var(--line)}
.meta{color:var(--muted);margin:0 0 24px}a{color:var(--link)}li{margin:4px 0}
"""


def page(title, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{style}</style>
</head>
<body><main>
{body}
</main></body>
</html>
"""


def items(values, empty):
    if not values:
        return f"<p>{empty}</p>"
    return "<ul>" + "".join(f"<li>{html.escape(v)}</li>" for v in values) + "</ul>"


def app_page(app):
    name = html.escape(app["name"])
    sdks = [policy["sdks"][key] for key in app["sdks"]]
    sdk_list = "".join(
        f'<li><b>{html.escape(s["name"])}</b>: {html.escape(s["purpose"])} '
        f'<a href="{html.escape(s["policy"])}">Privacy policy</a>.</li>'
        for s in sdks)
    collected = items(app["collected"],
                      "We do not collect, store on our servers, sell or share any personal data. "
                      "The app does not ask for your name, email, location, contacts or any account.")
    ads = ("The app shows ads from the providers listed above. They may use your device's advertising ID "
           "to show and measure ads; you can reset or opt out of it in your device settings."
           if app["ads"] else "The app does not show third-party ads and does not use your advertising ID.")
    purchases = ("In-app purchases are processed by the store; we never see your payment details."
                 if app["purchases"] else "The app has no in-app purchases.")
    permissions = items(app["permissions"], "The app does not request any special device permissions.")
    stores = ", ".join(app["stores"])
    return page(f"{app['name']} Privacy Policy", f"""
<h1>{name}: Privacy Policy</h1>
<p class="meta">Developer: {dev} · App ID: {html.escape(app["package"])} · Last updated: {updated}</p>
<p>This policy explains how the mobile game <b>{name}</b> ("the app"), published by {dev} on {html.escape(stores)},
handles your information. By using the app you agree to this policy.</p>
<h2>Information we collect</h2>
{collected}
<h2>Information stored on your device</h2>
<p>{html.escape(app["local"])} This data never leaves your device and is deleted when you uninstall the app.</p>
<h2>Third-party services</h2>
<p>The app relies on these services, which may process data under their own privacy policies:</p>
<ul>{sdk_list}</ul>
<h2>Advertising and purchases</h2>
<p>{ads}</p>
<p>{purchases}</p>
<h2>Permissions</h2>
{permissions}
<h2>Children's privacy</h2>
<p>The app is not directed at children under 13, and we do not knowingly collect personal information from anyone,
including children. If you believe a child has provided us personal information, contact us and we will delete it.</p>
<h2>Your rights and data deletion</h2>
<p>Because we hold no personal data on our servers, there is nothing for us to export or delete. You can remove all
app data at any time by clearing the app's storage or uninstalling it. For data held by the services above, use their
own tools linked in their policies.</p>
<h2>Security</h2>
<p>The app does not transmit your game data over the network, so it stays protected by your device's own security.</p>
<h2>Changes to this policy</h2>
<p>We will update this page when the app's data practices change, for example when a new service is added, and change
the "Last updated" date above.</p>
<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:{email}">{email}</a>.</p>
<p><a href="../">All apps by {dev}</a></p>
""")


apps = policy["apps"]
for app in apps:
    folder = root / app["slug"]
    folder.mkdir(exist_ok=True)
    (folder / "index.html").write_text(app_page(app), encoding="utf-8")

links = "".join(f'<li><a href="{a["slug"]}/">{html.escape(a["name"])}</a> ({html.escape(a["package"])})</li>'
                for a in apps)
(root / "index.html").write_text(page(f"{policy['developer']} Privacy Policies", f"""
<h1>Privacy policies</h1>
<p class="meta">Developer: {dev} · Last updated: {updated}</p>
<p>Each app has its own privacy policy:</p>
<ul>{links}</ul>
<p>Contact: <a href="mailto:{email}">{email}</a>.</p>
"""), encoding="utf-8")
(root / ".nojekyll").write_text("", encoding="utf-8")
