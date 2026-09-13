from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.7-print-adapter-layout' in html:
    raise SystemExit('already patched')
anchor="function buildReportCenterPdfV180(mode='active'){"
if anchor not in html:
    raise SystemExit('pdf build function not found')
css_func=r'''/* v1.8.7-print-adapter-layout */
function managerPdfV187Css(){return `
@page{size:A4 landscape;margin:9mm}
html,body{width:auto!important;min-width:0!important;max-width:none!important;margin:0!important;padding:0!important;background:#fff!important}
.pdf-report-v180,.pdf-report-v180.pdf-all-v184{box-sizing:border-box!important;width:100%!important;max-width:none!important;margin:0!important;padding:0!important}
.pdf-report-v180 .all-report-section{margin-bottom:16px!important;page-break-inside:auto!important;break-inside:auto!important}
.pdf-report-v180 table{width:100%!important;max-width:100%!important}
`;}
'''
html=html.replace(anchor,css_func+anchor,1)
old='const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183()+managerPdfV184Css()+managerPdfV186Css();'
new='const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183()+managerPdfV184Css()+managerPdfV186Css()+managerPdfV187Css();'
if old not in html:
    raise SystemExit('pdf css compose marker missing')
html=html.replace(old,new,1)
p.write_text(html,encoding='utf-8')
print('v1.8.7 PDF print-adapter layout patch applied')
