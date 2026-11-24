"""Static launch checks; never print matched secret values."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
import re,json
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.h1=0;self.images=0;self.meta={};self.canonical=False;self.local=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if 'id'in a:assert a['id'] not in self.ids,a['id'];self.ids.add(a['id'])
  if t=='img':self.images+=1;assert a.get('alt') is not None,'Missing alt'
  if t=='meta':self.meta[a.get('name')or a.get('property')]=a.get('content')
  if t=='link'and a.get('rel')=='canonical':self.canonical=True
  for k in ['href','src']:
   u=urlsplit(a.get(k,''))
   if not u.scheme and u.path:self.local.append((u.path,u.fragment))
  for item in a.get('srcset','').split(','):
   if item.strip():self.local.append((item.strip().split()[0],''))
parsed={}
for path in DIST.glob('*.html'):
 page=Page();page.feed(path.read_text());parsed[path.name]=page
 if path.name=='officers.html':continue
 assert page.h1==1,path
 assert page.canonical,path
 for key in ['description','og:title','og:description','og:image','twitter:card']:assert page.meta.get(key),(path,key)
 for pattern in [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'(?i)(?:sk_live_|sk-proj-|AKIA)[A-Za-z0-9_-]{16,}']:
  assert not re.search(pattern,path.read_text()),'Secret-pattern match: '+str(path)
for path,page in parsed.items():
 for target,fragment in page.local:
  dest=DIST/target.lstrip('/')
  if target=='/':dest=DIST/'index.html'
  assert dest.exists(),(path,target)
  if fragment and dest.suffix=='.html':assert fragment in parsed[dest.name].ids,(path,target,fragment)
for path in DIST.glob('*.js'):
 assert not re.search(r'(?i)(?:sk_live_|sk-proj-|AKIA)[A-Za-z0-9_-]{16,}',path.read_text()),'Secret-pattern match in JS'
assert json.loads((ROOT/'content/site-settings.json').read_text())['analytics_measurement_id'] is None
assert 'Disallow: /'in(DIST/'robots.txt').read_text()
ET.parse(DIST/'sitemap.xml')
assert 'name="_captcha" value="true"'in(DIST/'contact.html').read_text()
assert not re.search(r'fetch\([^)]*formsubmit', (DIST/'contact.js').read_text())
print(f'PASS: {len(parsed)} HTML files; metadata, local links/fragments, srcsets, image alt, IDs, sitemap, indexing policy, secret patterns and server-CAPTCHA route.')
