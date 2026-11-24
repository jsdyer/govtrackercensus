"""Normalize the homepage scan and preserve meaningful changes in its archive."""
import json

from common import ROOT, save, sha


def normalize_record(record):
    row = dict(record)
    ok = row['status'] == 'ok'
    row['third_party_count'] = len(row.get('third_party_domains', [])) if ok else None
    row['cookie_count'] = len(row.get('cookies', [])) if ok else None
    stable = {key: row.get(key) for key in ('status', 'third_party_domains', 'script_hosts', 'services')}
    stable['cookies'] = sorted(row.get('cookies', []), key=lambda c: (c['domain'], c['name'], c['path']))
    stable['request_signatures'] = sorted({
        (request['host'], request['path'], request['type'])
        for request in row.get('requests', [])
    })
    row['_fingerprint'] = sha(json.dumps(stable, sort_keys=True).encode())
    return row


def main():
    import source
    (ROOT / '.cache').mkdir(exist_ok=True)
    source.main()
    data = json.loads((ROOT / '.cache/gov-scan.json').read_text())
    rows = [normalize_record(row) for row in data['records']]
    save(rows, sources=[
        {'label': 'Curated institution homepages', 'url': 'https://github.com/jsdyer/govtrackercensus/blob/main/config/sites.json'},
        {'label': 'Tracker X-Ray methodology', 'url': 'https://coolcode.ca/trackerxray/'},
    ], coverage=f'{len(rows)} curated public homepages · fresh Chromium contexts · eight-second passive observation window',
        warnings=[data['notice']], extra={key: data[key] for key in
                                        ('browser_version', 'method_version', 'classification_version')})


if __name__ == '__main__':
    main()
