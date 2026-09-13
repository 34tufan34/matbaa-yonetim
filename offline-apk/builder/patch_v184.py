from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.4-shift-rank-fix' in html:
    raise SystemExit('already patched')

old='<strong><span class="xreport-rank">${i+1}</span>${esc(x.name)}</strong>'
new='<strong>${scope===\'shift\'?\'\':`<span class="xreport-rank">${i+1}</span>`}${esc(x.name)}</strong>'
if old not in html:
    raise SystemExit('group rank marker not found')
html=html.replace(old,new,1)

old_main='<main class="pdf-report-v180">'
new_main='<main class="pdf-report-v180${mode===\'all\'?\' pdf-all-v184\':\'\'}">'
if old_main not in html:
    raise SystemExit('pdf main marker not found')
html=html.replace(old_main,new_main,1)

b=html.find("function buildReportCenterPdfV180(mode='active'){")
if b<0: raise SystemExit('build pdf function not found')
extra="""/* v1.8.4-shift-rank-fix */\nfunction managerPdfV184Css(){return `\n.pdf-report-v180.pdf-all-v184{max-width:none!important}\n`; }\n"""
html=html[:b]+extra+html[b:]
old_css='const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183();'
new_css='const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183()+managerPdfV184Css();'
if old_css not in html: raise SystemExit('pdf css compose marker not found')
html=html.replace(old_css,new_css,1)

p.write_text(html,encoding='utf-8')
print('v1.8.4 shift rank and full PDF marker patch applied')
