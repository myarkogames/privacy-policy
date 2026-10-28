# Privacy policy

Public privacy policies of the developer's mobile games, served by GitHub Pages at
`https://myarkogames.github.io/privacy-policy/<slug>/`. That per-app URL goes into Play Console
(App content → Privacy policy) and into the game's own "Privacy policy" button.

## Update

1. Edit `policy.json`: add the app to `apps`, or a new SDK to `sdks` and its key to each app that ships it.
   Change `collected`, `ads`, `purchases`, `permissions` when the game starts collecting data, showing ads,
   selling items or asking for permissions. Set `updated` to today.
2. Run `python3 build.py` and commit `policy.json` together with the generated HTML.
3. Check the page after Pages redeploys (about a minute).

Update the policy whenever a game goes to a store, adds or removes an SDK (ads, analytics, Firebase, IAP),
starts using the network or a new permission, or changes the developer name or contact email.
