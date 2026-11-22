#!/usr/bin/env python3
"""CI-only proof collector for a fixed public homepage census. Not run locally."""
import collections,datetime,json,urllib.request,urllib.error
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from urllib.robotparser import RobotFileParser
from playwright.sync_api import sync_playwright,TimeoutError as BrowserTimeout
import tldextract
ROOT=Path(__file__).resolve().parents[1]
UA='CoolCodeGovTrackerCensus/1.0 (+https://github.com/jsdyer/govtrackercensus)'
EXTRACT=tldextract.TLDExtract(suffix_list_urls=(),include_psl_private_domains=True)
SERVICE_DOMAINS={
 'google-analytics.com':('Google Analytics','analytics','https://developers.google.com/tag-platform/security/guides/csp#google_analytics'),
 'googletagmanager.com':('Google Tag Manager / Google tag','tag delivery','https://developers.google.com/tag-platform/security/guides/csp'),
 'clarity.ms':('Microsoft Clarity','analytics','https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-csp'),
 'cloudflareinsights.com':('Cloudflare Web Analytics','analytics','https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/'),
 'omtrdc.net':('Adobe data collection','analytics','https://experienceleague.adobe.com/en/docs/core-services/interface/data-collection/collection-domain'),
 '2o7.net':('Adobe data collection','analytics','https://experienceleague.adobe.com/en/docs/core-services/interface/data-collection/collection-domain'),
 'adobedc.net':('Adobe data collection','analytics','https://experienceleague.adobe.com/en/docs/core-services/interface/data-collection/collection-domain'),
 'demdex.net':('Adobe Audience Manager / Identity','identity service','https://experienceleague.adobe.com/en/docs/audience-manager/user-guide/reference/demdex-calls'),
 'adobedtm.com':('Adobe data collection / tag delivery','tag delivery','https://experienceleague.adobe.com/en/docs/core-services/interface/data-collection/domains')
}
def domain(host):
 value=EXTRACT(host or '').top_domain_under_public_suffix
 return value or (host or '').lower().rstrip('.')
def sanitize_url(value):
 p=urlsplit(value)
 return (p.scheme+'://'+p.netloc+p.path)[:2000] if p.scheme in ('https','http') else ''
def classify(host):
 return SERVICE_DOMAINS.get(domain(host))
_ROBOTS={}
def robots(url):
 p=urlsplit(url);origin=p.scheme+'://'+p.netloc
 if origin not in _ROBOTS:
  target=origin+'/robots.txt'
  try:
   with urllib.request.urlopen(urllib.request.Request(target,headers={'User-Agent':UA}),timeout=20) as r:body=r.read(200000).decode('utf-8',errors='replace')
   rp=RobotFileParser();rp.parse(body.splitlines());_ROBOTS[origin]=(rp,'checked')
  except urllib.error.HTTPError as e:
   _ROBOTS[origin]=(None,'absent' if e.code==404 else 'unavailable')
  except Exception:_ROBOTS[origin]=(None,'unavailable')
 rp,state=_ROBOTS[origin]
 return (rp.can_fetch(UA,url) if rp else state=='absent'),state

def crawl(browser,site):
 checked=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
 row={**site,'checked_at':checked,'date':checked[:10],'method':'Chromium fresh context; en-CA; UTC timezone; 1280×900 viewport; identified crawler UA; GitHub-hosted runner; no consent choice; 8 seconds after DOMContentLoaded','status':'unavailable','requests':[],'cookies':[],'services':[]}
 permitted,state=robots(site['url']);row['robots_status']=state
 if not permitted:row['status']='robots-disallowed' if state=='checked' else 'robots-unavailable';return row
 context=browser.new_context(locale='en-CA',timezone_id='UTC',viewport={'width':1280,'height':900},user_agent=UA)
 page=context.new_page();requests={}
 def requested(req):
  p=urlsplit(req.url)
  if p.scheme not in ('http','https') or not p.hostname:return
  # Fresh anonymous context only. Never retain query values, cookie values, bodies or credentials.
  requests[req]={'host':p.hostname.lower(),'domain':domain(p.hostname),'type':req.resource_type,'method':req.method,'path':p.path[:400],'query_names':sorted(parse_qs(p.query,keep_blank_values=True))[:40],'status':None,'failed':False}
 def responded(response):
  row=requests.get(response.request)
  if row is not None:row['status']=response.status
 def failed(req):
  row=requests.get(req)
  if row is not None:row['failed']=True
 page.on('request',requested);page.on('response',responded);page.on('requestfailed',failed)
 try:
  response=page.goto(site['url'],wait_until='domcontentloaded',timeout=45000)
  page.wait_for_timeout(8000)
  row['final_url']=sanitize_url(page.url);row['http_status']=response.status if response else None
  title=page.title().lower()
  if row['http_status'] and row['http_status']>=400:row['status']='http-error'
  elif any(s in title for s in ('access denied','just a moment','verify you are human','captcha')):row['status']='verification-page'
  else:row['status']='ok'
  primary=domain(urlsplit(page.url).hostname)
  row['site_domain']=primary
  for req in requests.values():
   req['third_party']=req['domain']!=primary
   service=classify(req['host'])
   if service:req['service'],req['service_kind'],req['service_documentation']=service
  row['requests']=list(requests.values())
  row['cookies']=[{k:c.get(k) for k in ('name','domain','path','secure','httpOnly','sameSite')} for c in context.cookies()]
  hosts=sorted(set(r['host'] for r in row['requests'] if r['third_party']))
  row['third_party_hosts']=hosts;row['third_party_domains']=sorted(set(r['domain'] for r in row['requests'] if r['third_party']))
  row['script_hosts']=sorted(set(r['host'] for r in row['requests'] if r['type']=='script'))
  row['services']=sorted(set(r['service'] for r in row['requests'] if r.get('service')))
  row['analytics_requests']=sum(r.get('service_kind')=='analytics' for r in row['requests'])
  row['request_count']=len(row['requests']);row['third_party_request_count']=sum(r['third_party'] for r in row['requests'])
 except BrowserTimeout:row['status']='navigation-timeout'
 except Exception as exc:row['status']='scan-error';row['error_type']=type(exc).__name__
 finally:context.close()
 return row

def main():
 sites=json.loads((ROOT/'config/sites.json').read_text());records=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  version=browser.version
  for site in sites:
   row=crawl(browser,site);records.append(row);print(site['id'],row['status'],row.get('request_count','—'),flush=True)
  browser.close()
 result={'schema':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'browser_version':version,'method_version':'1','classification_version':'2026-11-22','records':records,'notice':'Third-party means a different registrable domain, not necessarily a different owner. A documented analytics service match is evidence of contact, not proof of personal-data collection, consent compliance or tracking behaviour. Missing/blocked scans are unavailable, never zero.'}
 (ROOT/'.cache/gov-scan.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
 if not any(r['status']=='ok' for r in records):raise RuntimeError('No successful homepage scans; keep previous published dataset')
if __name__=='__main__':main()
