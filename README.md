# Gov Tracker Census

Who else does a government homepage contact? Compare observed requests, scripts and cookies across a fixed public website sample.

Open https://coolcode.ca/govtrackercensus/

<!-- coolcode:guide -->
Choose a jurisdiction and open an institution row to inspect its request destinations and cookie names. A third-party request is not proof of tracking. Unavailable scans stay visibly unavailable.
<!-- /coolcode:guide -->

## Sources and interpretation

A fixed set of 15 federal, British Columbia and Nova Scotia homepages is visited in a fresh Chromium context, with no consent choices, login or other interaction. Robots restrictions and navigation failures remain explicit. This is a homepage sample, not a census of every government website.

Third-party means a different registrable domain, including private suffixes. It does not establish different ownership. The documented service signatures identify contact with analytics or tag-delivery domains; they do not prove personal-data collection, unlawful tracking or consent compliance.

Cookie values, request bodies and URL query values are not retained. The archive contains destination hosts, paths, parameter names, resource types, response statuses and cookie metadata. Geography, browser version, timing and consent defaults can affect results.

The diary compares subsequent captures. Initial capture is a baseline. A failed scan cannot demonstrate that a technology was removed.

## Collection and archive

Schedule: **Weekly** (`17 9 * * 2`, UTC). GitHub schedules are best effort. Scheduled and manual runs collect, validate, commit dated snapshots and deploy. A first code push also collects if no saved dataset exists. Other code pushes rebuild the saved dataset offline.

`data/current.json` contains the latest normalized source records and metadata. `archive/YYYY-MM/*.json.gz` retains distinct captured versions; `data/history.json` lists them. Identical data checks update the check time without manufacturing a change. An initial capture is labelled baseline. Archive data is tracked in Git and does not expire with Actions artifacts. The site has snapshot selection, filtering, source detail, CSV export and an RSS change feed.

The default build needs no network. Failed source validation does not replace the published dataset. Optional `HEALTHCHECKS_PING_URL` sends start/success/failure pings for collection runs; no accuracy email is implied.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/collect.py
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

## Privacy

Search and filters are local to the browser; no upstream request is made by filtering. Public data collection runs in GitHub Actions. The shared CoolCode counter records aggregate page opens, without searches or filter values. The explorer and collector run without Cloudflare changes. To enable shared visit counts and private issue reports, add `govtrackercensus` to the existing `coolcode-visitor-api` Worker’s `toolList` and deploy it, if not already registered. See the [batch setup notes](https://github.com/jsdyer/jsdyer.github.io/blob/main/docs/tier1-tools.md).

## Software and attribution

Application code is MIT licensed; upstream data retains its original licence and attribution. Follow the source links for original records and terms.
