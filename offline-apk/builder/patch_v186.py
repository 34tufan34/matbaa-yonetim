from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.6-pdf-width-natural-pages' in html:
    raise SystemExit('already patched')
anchor="function buildReportCenterPdfV180(mode='active'){"
if anchor not in html:
    raise SystemExit('pdf build function not found')
css_func=r'''/* v1.8.6-pdf-width-natural-pages */
function managerPdfV186Css(){return `
.pdf-report-v180{width:100%!important;max-width:none!important;margin:0!important;padding:0!important;font-size:13px!important;line-height:1.38!important}
.pdf-report-v180.pdf-all-v184{width:100%!important;max-width:none!important;margin:0!important}
.pdf-report-v180 h1{font-size:26px!important;line-height:1.15!important}
.pdf-report-v180 h2{font-size:19px!important;line-height:1.2!important}
.pdf-report-v180 h3{font-size:15px!important;line-height:1.25!important}
.pdf-report-v180 p,.pdf-report-v180 small{font-size:10px!important;line-height:1.4!important}
.pdf-report-v180 table{width:100%!important;font-size:10.5px!important;table-layout:auto!important}
.pdf-report-v180 th{font-size:9.5px!important;padding:7px 8px!important;white-space:nowrap!important}
.pdf-report-v180 td{font-size:10.5px!important;padding:7px 8px!important}
.pdf-report-v180 .all-report-section{margin:0 0 20px!important;padding:0!important;break-inside:auto!important;page-break-inside:auto!important}
.pdf-report-v180 .metric,.pdf-report-v180 .kpi-card,.pdf-report-v180 .report-card{min-height:auto!important}
.pdf-report-v180 .visual-bars,.pdf-report-v180 .viz-bars{font-size:10px!important}
.pdf-report-v180 .viz-row{min-height:24px!important}
.pdf-report-v180 .viz-track{height:9px!important}
.pdf-report-v180 .eyebrow{font-size:9px!important;letter-spacing:.6px!important}
`;}
'''
html=html.replace(anchor,css_func+anchor,1)
old='const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183()+managerPdfV184Css();'
new='const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183()+managerPdfV184Css()+managerPdfV186Css();'
if old not in html:
    raise SystemExit('pdf css compose marker missing')
html=html.replace(old,new,1)
p.write_text(html,encoding='utf-8')
print('v1.8.6 PDF width and typography patch applied')
