from common import ROOT,save,sha
import source,json

def main():
 (ROOT/'.cache').mkdir(exist_ok=True);source.main();data=json.loads((ROOT/'.cache/gov-scan.json').read_text());rows=data['records']
 for r in rows:
  ok=r['status']=='ok';r['third_party_count']=len(r.get('third_party_domains',[])) if ok else None;r['cookie_count']=len(r.get('cookies',[])) if ok else None
  stable={k:r.get(k) for k in ['status','third_party_domains','script_hosts','services']};stable['cookies']=sorted(r.get('cookies',[]),key=lambda c:(c['domain'],c['name'],c['path']));stable['request_signatures']=sorted({(q['host'],q['path'],q['type']) for q in r.get('requests',[])};r['_fingerprint']=sha(json.dumps(stable,sort_keys=True).encode())
 save(rows,sources=[{'label':'Curated institution homepages','url':'https://github.com/jsdyer/govtrackercensus/blob/main/config/sites.json'},{'label':'Tracker X-Ray methodology','url':'https://coolcode.ca/trackerxray/'}],coverage='15 curated public homepages · fresh Chromium contexts · eight-second passive observation window',warnings=[data['notice']],extra={'browser_version':data['browser_version'],'method_version':data['method_version'],'classification_version':data['classification_version']})
if __name__=='__main__':main()
