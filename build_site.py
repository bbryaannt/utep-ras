"""Build the static chapter site. Update content/chapter.json for verified details."""
from pathlib import Path
import json
import os
import re
from hashlib import sha256
from html import escape as esc
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
settings=json.loads((ROOT/'content/site-settings.json').read_text())
ORIGIN=(os.environ.get('SITE_ORIGIN') or settings['origin']).rstrip('/')
origin_parts=urlparse(ORIGIN)
if origin_parts.scheme!='https' or not origin_parts.netloc or origin_parts.path or origin_parts.query or origin_parts.fragment or origin_parts.username or origin_parts.password:
    raise ValueError('SITE_ORIGIN must be an HTTPS origin, such as https://utepras.org')
page_records=[]
chapter=json.loads((ROOT/'content/chapter.json').read_text())
def e(value): return esc(str(value),quote=True)
def external(url):
    parsed=urlparse(url)
    if parsed.scheme not in ('https','http') or not parsed.netloc: raise ValueError('Expected an absolute http(s) URL')
    return e(url)
def contact_link(address,label):
    if any(c in address for c in '\r\n?') or '@' not in address: raise ValueError('Expected a chapter email address')
    return f'<a class="contact-address" href="mailto:{e(address)}">{e(label or address)} <span>↗</span></a>'
def header(active):
    links=''.join(f'<a href="{slug}.html"'+(' aria-current="page"' if active==slug or (slug=='index' and not active) else '')+f'>{label}</a>' for slug,label in [('index','Home'),('about','About'),('projects','Projects'),('contact','Contact')])
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="header"><a class="brand" href="index.html" aria-label="UTEP IEEE RAS home"><span class="brand-logo-panel"><img class="brand-logo" src="assets/ieee-ras-logo.webp" alt="IEEE Robotics & Automation Society" width="1275" height="469"></span><span class="brand-chapter">UTEP<span>STUDENT CHAPTER</span></span></a><button class="menu" aria-expanded="false" aria-controls="navigation">Menu <span>＋</span></button><nav id="navigation" aria-label="Main navigation">{links}<a class="nav-join" href="join.html"{' aria-current="page"' if active=='join' else ''}>Join RAS <span>↗</span></a></nav></header>'''
def footer():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    year=datetime.now(ZoneInfo('America/Denver')).year
    links=''.join(f'<li><a href="{slug}.html">{label}</a></li>' for slug,label in [('about','About'),('projects','Projects'),('contact','Contact'),('join','Join RAS')])
    contacts=[]
    if chapter['email']: contacts.append(f'<li><a href="mailto:{e(chapter["email"])}">{e(chapter["email"])}</a></li>')
    for name,url in chapter['socials'].items():
        if url: contacts.append(f'<li><a href="{external(url)}" target="_blank" rel="noopener noreferrer">{e(name)} <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a></li>')
    return f'''<footer class="chapter-footer"><div class="chapter-footer-main"><div class="footer-identity"><a class="footer-mark" href="index.html" aria-label="UTEP IEEE RAS home">UTEP / IEEE RAS</a><p>UTEP Student Chapter<br>The University of Texas at El Paso</p></div><nav class="footer-navigation" aria-label="Footer"><h2>Explore</h2><ul>{links}</ul></nav><div class="footer-contact"><h2>Connect</h2><ul>{''.join(contacts)}</ul></div></div><div class="chapter-footer-bottom"><span>© {year} UTEP IEEE RAS</span><nav class="footer-legal" aria-label="Policies"><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><button type="button" data-privacy-open>Privacy settings</button></nav></div></footer>'''
def responsive_image(match):
    tag=match.group(0)
    src=re.search(r'src="([^"]+)"',tag)
    if not src: return tag
    item=image_manifest.get(src[1])
    if not item: return tag
    variants=item['variants']
    base=min(variants,key=lambda v:abs(v['width']-640))
    is_hero='cutout' in src[1]
    is_gallery='competition-team' in src[1] or 'test-field' in src[1]
    is_poster='loading="lazy"' in tag and not is_gallery
    sizes='(max-width: 600px) 240px, (min-width: 1248px) 344px, 25vw' if is_poster else '(max-width: 760px) calc(100vw - 48px), (min-width: 1248px) 515px, 40vw'
    size_hint=re.search(r'data-image-sizes="([^"]+)"',tag)
    if size_hint:
        sizes=size_hint[1]
        tag=tag.replace(' '+size_hint[0],'')
    if is_hero: sizes='(max-width: 900px) 370px, 422px'
    srcset=', '.join(f"{v['path']} {v['width']}w" for v in variants)
    tag=tag.replace(src[0],f'src="{base["path"]}" srcset="{srcset}" sizes="{sizes}"')
    if 'width=' not in tag:tag=tag.replace('<img ',f'<img width="{item["width"]}" height="{item["height"]}" ',1)
    if 'decoding=' not in tag:tag=tag.replace('<img ','<img decoding="async" ',1)
    if not is_poster and not is_gallery and 'fetchpriority=' not in tag:tag=tag.replace('<img ','<img fetchpriority="high" ',1)
    avif_variants=[v for v in variants if v.get('avif') and v['avif_bytes'] < v['bytes']]
    if len(avif_variants)==len(variants):
        avif_srcset=', '.join(f"{v['avif']} {v['width']}w" for v in avif_variants)
        return f'<picture><source type="image/avif" srcset="{avif_srcset}" sizes="{sizes}">{tag}</picture>'
    return tag
image_manifest=json.loads((ROOT/'content/responsive-images.json').read_text())
def privacy_controls():
    return '''<aside id="privacy-banner" class="privacy-banner" aria-label="Privacy choices" hidden><div><h2>See us on Instagram</h2><p>Allow our Instagram preview now so it’s ready when you visit Contact. Instagram may use cookies. <a href="privacy.html">Privacy policy</a></p></div><div class="privacy-actions"><button type="button" data-privacy-reject>Essential only</button><button type="button" data-privacy-accept>Allow Instagram</button><button type="button" class="privacy-text" data-privacy-open>Choose settings</button></div></aside><dialog id="privacy-dialog" aria-labelledby="privacy-title"><h2 id="privacy-title">Privacy settings</h2><p>Essential hosting and security features remain active.</p><label class="privacy-option"><input id="consent-media" type="checkbox"><span><strong>Instagram preview</strong><span>Allow Instagram to load its profile and posts. Meta may use cookies.</span></span></label><div class="privacy-actions"><button id="privacy-save" type="button">Save choices</button><button type="button" data-privacy-reject>Reject optional</button><button id="privacy-close" type="button" class="privacy-text">Close</button></div></dialog>'''
def page(filename,title,description,body,active=''):
    css_version=sha256((OUT/'style.css').read_bytes()).hexdigest()[:10]
    canonical=ORIGIN+('/' if filename=='index.html' else '/'+filename)
    noindex=not settings['public_indexing'] or filename in ('404.html','thanks.html')
    scripts=['privacy.js','script.js','diagnostics.js']+(['contact.js'] if filename=='contact.html' else [])
    script_html='<script>'+''.join((OUT/name).read_text()+';\n' for name in scripts)+'</script>'
    inline_css=re.sub(r'/\*.*?\*/','',(OUT/'style.css').read_text(),flags=re.S).replace('url(assets/','url(/assets/')
    social=ORIGIN+'/assets/social-preview.png'
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#111e2b"><meta name="description" content="{e(description)}"><meta name="robots" content="{'noindex,nofollow' if noindex else 'index,follow'}"><meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests"><title>{e(title)} — UTEP IEEE RAS</title><link rel="canonical" href="{e(canonical)}"><meta property="og:type" content="website"><meta property="og:site_name" content="UTEP IEEE RAS"><meta property="og:title" content="{e(title)} — UTEP IEEE RAS"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{social}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="UTEP IEEE Robotics and Automation Society — student robotics, projects and competition teams"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)} — UTEP IEEE RAS"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{social}"><meta name="twitter:image:alt" content="UTEP IEEE RAS student robotics chapter"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="preload" href="/assets/fonts/barlow-400-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/barlow-condensed-800-latin.woff2" as="font" type="font/woff2" crossorigin><style>{inline_css}</style></head><body id="top">{header(active)}<main id="main">{body}</main>{footer()}{privacy_controls()}{script_html}</body></html>'''
    html=re.sub(r'<img\b[^>]*>',responsive_image,html)
    html=re.sub(r'(href|src)="(?![a-zA-Z][a-zA-Z0-9+.-]*:|/|#)([^"]+)"',lambda m:f'{m[1]}="/{m[2]}"',html)
    html=re.sub(r'srcset="([^"]+)"',lambda m:'srcset="'+', '.join('/'+item.strip() for item in m[1].split(','))+'"',html)
    arrow='<svg class="arrow-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><path d="M4 20 20 4M5 4h15v15" stroke="currentColor" stroke-width="1.5"/></svg>'
    html=re.sub(r'(?<=>)([^<>]*↗[^<>]*)(?=<)',lambda m:m[0].replace('↗',arrow),html)
    (OUT/filename).write_text(html)
    page_records.append(filename)
def intro(title):
    return f'<section class="page-intro quiet-intro"><h1>{title}</h1></section>'
def meeting():
    m=chapter['meeting']
    bits=f'<p class="meeting-name">{e(m["details"].replace(" team meetings.", ""))}</p>' if m['details'] else ''
    if m['time']: bits+=f'<p class="meeting-time">{e(m["time"])}</p>'
    if m['location']: bits+=f'<p>{e(m["location"])}</p>'
    return bits
PROJECTS=[
    {'title':'Region 5 Autonomous Rover','url':'rover.html','image':'assets/rover.jpg','alt':'Our rover in the workshop'},
    {'title':'Garage Occupancy Sensor','url':'garage-occupancy-sensor.html','image':'assets/garage-occupancy-sensor.jpg','alt':'Orange garage occupancy sensor enclosure with its human-presence sensor visible'},
    {'title':'RTX Drone & Rover','url':'rtx-competition.html','image':'assets/rtx-pop-art.png','alt':'Illustrated autonomous vehicle concept in development; not the team’s final design','ongoing':True}
]
def project_card(heading='h2',project=None,compact=False):
    project=project or PROJECTS[0]
    image_sizes='220px' if compact else '(max-width: 600px) 240px, (min-width: 1248px) 344px, 25vw'
    index=f"{PROJECTS.index(project)+1:02d}"
    sensor=project['url']=='garage-occupancy-sensor.html'
    ongoing=project.get('ongoing',False)
    title='RAYTHEON<br>AVC' if ongoing else ('GARAGE<br>OCCUPANCY<br>SENSOR' if sensor else 'REGION 5<br>AUTONOMOUS<br>ROVER')
    category='DRONE + ROVER' if ongoing else ('ESP32 / DISCORD' if sensor else 'STUDENT ROBOTICS')
    date='IN PROGRESS' if ongoing else 'UTEP / EL PASO'
    pin='<span class="progress-pin" aria-label="Current project, in progress"><span>CURRENT<br>PROJECT</span></span>' if ongoing else ''
    variant='rtx-poster' if ongoing else ('sensor-poster' if sensor else 'rover-poster')
    return f'''<article class="quiet-project poster-card {variant}"><a class="project-poster" href="{e(project['url'])}" aria-label="Explore {e(project['title'])}"><img src="{e(project['image'])}" alt="{e(project['alt'])}" loading="lazy" data-image-sizes="{image_sizes}"><div class="poster-grid" aria-hidden="true"></div><div class="poster-topline" aria-hidden="true"><span>UTEP / IEEE RAS</span><span>PROJECT {index}</span></div><{heading} class="poster-title">{title}</{heading}><div class="poster-bottomline"><span>{category}<br>{date}</span><span class="poster-arrow" aria-hidden="true">↗</span></div></a>{pin}</article>'''
def project_list(heading='h2'):
    return '<div class="project-list">'+''.join(project_card(heading,project) for project in PROJECTS)+'</div>'
hero=(ROOT/'templates/home-hero.html').read_text()
m=chapter['meeting']
meeting_strip=f'''<section class="meeting-strip" aria-labelledby="meeting-invitation"><div class="meeting-welcome"><h2 id="meeting-invitation">Raytheon Autonomous Vehicle Competition</h2><p>All majors are welcome, including CS, EE, and ME. <strong>No experience is needed.</strong></p></div><div class="meeting-schedule"><span class="meeting-label">{e(m["time"].partition("·")[0].strip())}</span><p class="meeting-hour">{e(m["time"].partition("·")[2].strip())}</p></div><div class="meeting-place"><span class="meeting-label">LOCATION</span><p>{e(m['location'])}</p></div></section>'''
home=hero+meeting_strip+'''<section class="section home-updates"><div><h2 class="minor-heading">Projects</h2>'''+project_list('h3')+'''</div></section>'''
(OUT/'site-config.js').write_text('window.RAS_CONFIG = '+json.dumps({'analyticsId':settings['analytics_measurement_id']})+';\n')
page('index.html','Robotics at UTEP','UTEP IEEE Robotics and Automation Society. Student robotics, projects, and team meetings.',home)
page('projects.html','Projects','UTEP IEEE RAS robotics projects.',intro('PROJECTS.')+'<section class="section quiet-projects">'+project_list()+'</section>','projects')
def project_detail(project, number, summary, facts, overview, components, notes, other):
    fact_html=''.join(f'<div'+(' class="project-status"' if label=='Status' else '')+f'><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for label,value in facts)
    related_html=''.join('<div class="related-poster">'+project_card('h3',item,compact=True)+'</div>' for item in PROJECTS if item['url']!=project['url'])
    gallery=''
    if project['url']=='rover.html':
        gallery='<section class="project-gallery" aria-labelledby="trip-heading"><h2 id="trip-heading">The competition trip</h2><div class="project-gallery-grid">'+''.join(f'<figure><a href="assets/{image}" target="_blank" rel="noopener" aria-label="{e(alt)} — open full-size photo"><img src="assets/{image}" alt="{e(alt)}" width="1800" height="1350" loading="lazy"></a><figcaption>{e(caption)}</figcaption></figure>' for image,alt,caption in [('rover-competition-team.jpg','UTEP IEEE RAS competition team together outdoors','The team on the competition trip.'),('rover-test-field.jpg','Rover on a small test field with team members working on laptops','Working with the rover and test field.')])+'</div></section>'
    component_html=''.join(f'<li>{e(item)}</li>' for item in components)
    return f'''<article class="project-detail" data-project="{number}"><header class="project-heading"><a class="back-link" href="projects.html">← All projects</a><p class="project-eyebrow">UTEP IEEE RAS / PROJECT {number}</p><h1>{e(project['title'])}</h1><p class="project-deck">{e(summary)}</p></header><div class="project-feature"><figure><div class="project-image-frame"><img src="{e(project['image'])}" alt="{e(project['alt'])}"></div>{('<span class="progress-pin" aria-label="Current project, in progress"><span>CURRENT<br>PROJECT</span></span><figcaption>Project in progress</figcaption>' if project.get('ongoing') else '')}</figure><div class="project-overview"><p>{e(overview)}</p><dl class="project-facts">{fact_html}</dl><h2 class="project-build-label">Focus</h2><ul class="project-components">{component_html}</ul><div class="project-notes">{notes}</div></div></div>{gallery}<section class="project-next" aria-labelledby="more-projects"><div><h2 id="more-projects">More projects</h2><a class="back-link" href="projects.html">View all projects ↗</a></div><div class="related-projects">{related_html}</div></section></article>'''
rover=project_detail(PROJECTS[0], '01', 'IEEE Region 5 Robotics Competition', [('Status','Competition project'),('Result','7th out of 30 teams')], 'Built by UTEP IEEE RAS for three-minute autonomous matches, the rover brings mechanical, electrical, and software engineering together in one competition system.', ['Mechanical','Electrical','Software'], '<div><h2>Design</h2><p>The competition required robots to operate using onboard sensors and programming, with all processing on the robot and no outside control. Starting size was limited to a 12-inch cube, with a maximum mass of 12 kg.</p></div><div><h2>Development</h2><p>The mechanical team developed the intake, sorting system, drivetrain, frame, arms, and mounts, balancing 3D printing, machining, and outsourcing. Electrical and software teams worked alongside them to integrate the robot into a unified system under competition deadlines.</p></div>', PROJECTS[1])
page('rover.html','Region 5 Autonomous Rover','UTEP IEEE RAS autonomous rover for the IEEE Region 5 Robotics Competition. Mechanical, electrical, and software teamwork; 7th out of 30 teams.',rover,'projects')
sensor=project_detail(PROJECTS[1], '02', 'Real-time garage status, sent to Discord.', [('Status','Built'),('Application','Garage availability')], 'A presence-sensing system that lets members check whether the robotics garage is occupied through Discord notifications.', ['ESP32','Human-presence sensor','SolidWorks','Bambu Lab','Discord'], '<div><h2>Design</h2><p>A human-presence sensor detects occupancy, and an ESP32-based system posts status notifications to Discord so members can check garage availability.</p></div><div><h2>Development</h2><p>The enclosure was designed in SolidWorks and 3D-printed on a Bambu Lab printer to house the ESP32 and presence sensor.</p></div>', PROJECTS[0])
page('garage-occupancy-sensor.html','Garage Occupancy Sensor','An ESP32 garage occupancy sensor with a Bambu Lab 3D-printed enclosure and Discord notifications.',sensor,'projects')
rtx=project_detail(PROJECTS[2], '03', 'Raytheon Autonomous Vehicle Competition · 2026–2027 · Mission Bird Dog', [('Status','In progress'),('Stage','Early development')], 'We’re building a drone paired with a rover for Mission Bird Dog, the 2026–2027 Raytheon Autonomous Vehicle Competition. The project brings aerial and ground robotics together in one autonomous system.', ['Mechanical','Electrical','Software'], '<div><h2>Design</h2><p>The challenge is to follow spoken or written mission instructions, navigate indoors without GPS, identify the correct target, and read its NFC message. Each seven-minute challenge adds complexity, from obstacles to a target change during the mission. Returning the target object earns bonus points.</p></div><div><h2>Development</h2><p>Our drone-and-rover system is in early development. The competition calls for edge processing and coordinated autonomy; hardware choices, vehicle roles, and test results will be shared as the design develops.</p><a class="back-link" href="join.html">Join the team ↗</a></div>', PROJECTS[0])
page('rtx-competition.html','RTX Drone & Rover','UTEP IEEE RAS is developing a drone-and-rover system for Mission Bird Dog at the 2026–2027 Raytheon Autonomous Vehicle Competition.',rtx,'projects')
about_content=json.loads((ROOT/'content/about.json').read_text())
about=f'''<section class="about-masthead"><div class="about-title"><p class="about-eyebrow">ABOUT THE CHAPTER</p><h1>IEEE RAS.<br><span>AT UTEP.</span></h1><p class="about-lead">{e(about_content['intro'])}</p></div><div class="about-emblem"><img src="assets/ieee-ras-logo.webp" alt="IEEE Robotics & Automation Society" width="1275" height="469"><p>The University of Texas at El Paso<br><span>Student Chapter</span></p></div></section><section class="about-welcome"><h2>All majors.<br>All experience levels.</h2><p>{e(about_content['welcome'].replace('All majors and experience levels are welcome. ', ''))}</p><a class="back-link" href="join.html">Come meet us <span aria-hidden="true">↗</span></a></section><section class="about-activities" aria-label="Chapter activities"><article><p class="about-eyebrow">COMPETE</p><h2>Competition teams</h2><p>{e(about_content['sections'][0]['copy'])}</p><a class="back-link" href="projects.html">Explore our projects ↗</a></article><article><p class="about-eyebrow">CONNECT</p><h2>Beyond competitions</h2><p>{e(about_content['sections'][1]['copy'])}</p></article></section><section class="about-history"><div><p class="about-eyebrow">OUR CHAPTER</p><h2>Revived by students.</h2><p>IEEE RAS has a history at UTEP. After a period of inactivity, students revived the organization over the past few years. Since the restart, we’ve returned to competition at IEEE Region 5.</p></div><a class="about-result" href="rover.html" aria-label="Our rover: 7th place out of 30 teams at the IEEE Region 5 Robotics Competition"><span class="about-result-number">7<span>th</span></span><span>OUT OF 30 TEAMS</span><p>IEEE Region 5 Robotics Competition <span aria-hidden="true">↗</span></p></a></section><section class="about-partner"><div><h2>Partners & sponsors</h2><p>{e(about_content['sections'][3]['copy'])}</p></div><a class="button" href="contact.html">Get in touch <span aria-hidden="true">↗</span></a></section>'''
page('about.html','About','About the UTEP IEEE Robotics and Automation Society student chapter.',about,'about')
(OUT/'officers.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=about.html"><title>About — UTEP IEEE RAS</title></head><body><p><a href="about.html">About UTEP IEEE RAS</a></p></body></html>')
email=contact_link(chapter['email'],chapter['email']) if chapter['email'] else ''
socials=''.join(f'<div class="contact-entry"><h2>{e(name)}</h2><a class="contact-address" href="{external(url)}" target="_blank" rel="noopener noreferrer">{e("@utep.ras" if name=="Instagram" and "utep.ras" in url else name)} <span>↗</span><span class="sr-only"> (opens in a new tab)</span></a></div>' for name,url in chapter['socials'].items() if url)
sponsor_note=('<p>For sponsorship and collaboration: '+contact_link(chapter['sponsor_email'],chapter['sponsor_email'])+'</p>') if chapter['sponsor_email'] and chapter['sponsor_email']!=chapter['email'] else '<p>For sponsorship and collaboration, email the chapter.</p>'
contact=intro('CONTACT.')+f'''<section class="section contact-layout"><div class="contact-message"><h2>Send us a message.</h2><p class="contact-intro">Questions about joining, projects, or working with us? Get in touch.</p><form id="contact-form" action="https://formsubmit.co/{e(chapter['email'])}" method="POST"><input type="hidden" name="_subject" value="UTEP IEEE RAS — website inquiry"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="true"><input type="hidden" name="_next" value="{ORIGIN}/thanks.html"><input type="hidden" name="_url" value="{ORIGIN}/contact.html"><div class="form-trap" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="_honey" type="text" tabindex="-1" autocomplete="off"></div><div class="form-pair"><div class="form-field"><label for="contact-name">Name</label><input id="contact-name" name="name" autocomplete="name" required maxlength="100"></div><div class="form-field"><label for="contact-email">Email</label><input id="contact-email" name="email" type="email" autocomplete="email" required maxlength="254"></div></div><div class="form-pair"><div class="form-field"><label for="contact-topic">What’s this about?</label><select id="contact-topic" name="topic"><option>General inquiry</option><option>Joining RAS</option><option>Projects</option><option>Sponsorship or collaboration</option></select></div><div class="form-field"><label for="contact-details">Other contact details <span>(optional)</span></label><input id="contact-details" name="contact_details" maxlength="200" placeholder="Phone or organization"></div></div><div class="form-field"><label for="contact-body">Message</label><textarea id="contact-body" name="message" rows="5" required minlength="10" maxlength="5000"></textarea></div><p class="form-privacy">Submitting continues to spam verification. Read our <a href="privacy.html">Privacy policy</a>. Your details and message are processed by <a href="https://formsubmit.co/privacy.pdf" target="_blank" rel="noopener noreferrer">FormSubmit</a> and emailed to {e(chapter['email'])} so we can reply.</p><div class="form-actions"><button class="button" type="submit">Send message <span aria-hidden="true">↗</span></button><a id="email-draft" class="back-link" href="mailto:{e(chapter['email'])}">Use my email app ↗</a></div><p id="form-status" role="status" aria-live="polite" tabindex="-1"></p><noscript><p>You’ll continue to FormSubmit to complete your submission.</p></noscript></form></div><aside class="contact-social"><div class="contact-direct"><h2>Email us directly</h2>{email}<p>Opens your preferred email app.</p></div><section class="instagram-preview" aria-labelledby="instagram-title"><div class="instagram-heading"><svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg><h2 id="instagram-title">Instagram</h2></div><div id="instagram-consent-placeholder"><p>Allow optional media to show our Instagram profile and posts.</p><button type="button" data-privacy-open>Choose privacy settings</button></div><iframe hidden class="instagram-profile-frame" data-src="https://www.instagram.com/utep.ras/embed/" title="UTEP IEEE RAS on Instagram" loading="eager" referrerpolicy="strict-origin-when-cross-origin" allowtransparency="true"></iframe><a class="back-link instagram-fallback" href="https://www.instagram.com/utep.ras/" target="_blank" rel="noopener noreferrer">@utep.ras on Instagram ↗</a></section></aside></section>'''
page('contact.html','Contact','Send a message to UTEP IEEE RAS, email the chapter directly, or find us on Instagram.',contact,'contact')
join_action=f'<a class="button dark" href="{external(chapter["join_url"])}" target="_blank" rel="noopener noreferrer">Join RAS <span>↗</span><span class="sr-only"> (opens in a new tab)</span></a>' if chapter['join_url'] else email
membership=''.join(f'<div><h2>{label}</h2><p>{e(chapter["membership"][key])}</p></div>' for label,key in [('Membership','eligibility'),('Experience','experience'),('Dues','dues')] if chapter['membership'][key])
join=f'''<section class="join-page"><div class="join-page-intro"><p class="about-eyebrow">UTEP IEEE RAS / MEMBERSHIP</p><h1>JOIN RAS.</h1><h2>Start with a meeting.</h2><p>All majors and experience levels are welcome. Come to a general meeting or a competition team meeting to meet the group and find a project to join.</p><a class="join-page-contact" href="contact.html">Contact us <span aria-hidden="true">↗</span></a></div><section class="join-meeting-card" aria-labelledby="join-meeting-title"><p class="about-eyebrow">COMPETITION TEAM MEETINGS</p><h2 id="join-meeting-title">Raytheon Autonomous<br>Vehicle Competition</h2><dl class="join-meeting-details"><div class="join-meeting-when"><dt>WHEN</dt><dd><span class="join-meeting-days">{e(chapter['meeting']['time'].partition('·')[0].strip())}</span><span class="join-meeting-time">{e(chapter['meeting']['time'].partition('·')[2].strip())}</span></dd></div><div><dt>WHERE</dt><dd class="join-meeting-place">{e(chapter['meeting']['location'])}</dd></div></dl><p class="join-meeting-note">No experience is needed. Just come by.</p></section>{membership}</section>'''
page('join.html','Join RAS','UTEP IEEE RAS competition team meeting schedule and membership contact.',join,'join')
legal=json.loads((ROOT/'content/legal-pages.json').read_text())
for slug,content in legal.items():
    body=intro(e(content['title']).upper())+'<article class="section policy-page"><p class="policy-updated">Updated November 8, 2026</p>'+''.join('<section><h2>'+e(heading)+'</h2><p>'+copy+'</p></section>' for heading,copy in content['sections'])+'</article>'
    page(slug+'.html',content['title'],content['description'],body)
page('thanks.html','Thank you','Your message has been submitted to UTEP IEEE RAS.',intro('THANK YOU.')+'<section class="section utility-page"><p>Your message has been submitted. Thanks for getting in touch.</p><a class="button" href="index.html">Back to Home <span aria-hidden="true">↗</span></a></section>')
page('404.html','Page not found','Find your way back to the UTEP IEEE RAS website.',intro('PAGE NOT FOUND.')+'<section class="section utility-page"><p>This address doesn’t match a page on our site.</p><a class="button" href="index.html">Back to Home <span aria-hidden="true">↗</span></a><a class="back-link" href="projects.html">Explore projects ↗</a></section>')
from xml.sax.saxutils import escape as xml_escape
urls=[ORIGIN+('/' if name=='index.html' else '/'+name) for name in page_records if name not in ('404.html','thanks.html')]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+xml_escape(url)+'</loc></url>' for url in urls)+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\n'+('Allow: /' if settings['public_indexing'] else 'Disallow: /')+'\nSitemap: '+ORIGIN+'/sitemap.xml\n')
print('Built',len(page_records),'pages, sitemap, robots, metadata and consent controls')
