from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.3-pdf-light-cleanup' in html:
    raise SystemExit('already patched')

anchor="function cleanManagerReportHtmlV182(raw){"
if anchor not in html:
    raise SystemExit('v1.8.2 manager PDF anchor missing')

extra=r'''/* v1.8.3-pdf-light-cleanup */
function managerPdfLightOverrideV183(){
  return `
/* PDF-only hard reset: prevent any app dark-theme surface from leaking into the executive report. */
body .pdf-report-v180{background:#fff!important;color:#1f2937!important}
body .pdf-report-v180 div:not(.viz-fill):not(.bar-fill):not(.progress-fill):not(.viz-track):not(.bar-track):not(.progress-track),
body .pdf-report-v180 section,body .pdf-report-v180 article,body .pdf-report-v180 aside,
body .pdf-report-v180 header:not(.pdf-report-head),body .pdf-report-v180 footer,
body .pdf-report-v180 ul,body .pdf-report-v180 ol,body .pdf-report-v180 li{
  background:#fff!important;background-image:none!important;color:#1f2937!important;box-shadow:none!important
}
body .pdf-report-v180 span:not(.viz-fill):not(.bar-fill):not(.progress-fill),
body .pdf-report-v180 label,body .pdf-report-v180 em,body .pdf-report-v180 i{
  background-color:transparent!important;background-image:none!important;color:#1f2937!important
}
body .pdf-report-v180 table,body .pdf-report-v180 tbody,body .pdf-report-v180 thead,
body .pdf-report-v180 tfoot,body .pdf-report-v180 tr,body .pdf-report-v180 td{
  background:#fff!important;background-image:none!important;color:#1f2937!important;box-shadow:none!important
}
body .pdf-report-v180 th{background:#edf2f7!important;background-image:none!important;color:#344054!important}
body .pdf-report-v180 button,body .pdf-report-v180 [role="button"]{
  background:#f2f5f8!important;background-image:none!important;color:#344054!important;
  border:1px solid #d4dce6!important;box-shadow:none!important
}
body .pdf-report-v180 input,body .pdf-report-v180 select,body .pdf-report-v180 textarea{
  background:#fff!important;color:#1f2937!important;border-color:#d7dee8!important;box-shadow:none!important
}
/* Cards and list rows that used hard-coded dark surfaces in the application. */
body .pdf-report-v180 .card,body .pdf-report-v180 .panel,body .pdf-report-v180 .kpi,
body .pdf-report-v180 .metric,body .pdf-report-v180 .stat,body .pdf-report-v180 .summary,
body .pdf-report-v180 .row,body .pdf-report-v180 .list-row,body .pdf-report-v180 .data-row,
body .pdf-report-v180 .work-row,body .pdf-report-v180 .risk-row,body .pdf-report-v180 .compare-row,
body .pdf-report-v180 .xreport-card,body .pdf-report-v180 .xreport-panel,
body .pdf-report-v180 .decision-kpi,body .pdf-report-v180 .attention-item,
body .pdf-report-v180 .quality-card,body .pdf-report-v180 .quality-issue{
  background:#fff!important;background-image:none!important;color:#1f2937!important;
  border-color:#d7dee8!important;box-shadow:none!important
}
/* Keep visual charts, but make them print-friendly rather than black. */
body .pdf-report-v180 .viz-track,body .pdf-report-v180 .bar-track,body .pdf-report-v180 .progress-track{
  background:#e8edf3!important;background-image:none!important
}
body .pdf-report-v180 .viz-fill,body .pdf-report-v180 .bar-fill,body .pdf-report-v180 .progress-fill{
  background:#4f83bd!important;background-image:none!important
}
body .pdf-report-v180 .badge,body .pdf-report-v180 .pill,body .pdf-report-v180 .subtle-chip,
body .pdf-report-v180 .chip,body .pdf-report-v180 .tag,body .pdf-report-v180 .status-badge{
  background:#eef2f6!important;background-image:none!important;color:#475467!important;
  border-color:#d0d7e1!important;box-shadow:none!important
}
body .pdf-report-v180 .all-report-section-label span{
  background:#eaf0f7!important;color:#24476d!important;border:1px solid #cbd7e5!important
}
body .pdf-report-v180 .pdf-report-head{
  background:#f7f9fc!important;background-image:none!important;color:#172033!important
}
/* Last-resort cleanup for inline dark backgrounds in report HTML. */
body .pdf-report-v180 [style*="background:#0"],body .pdf-report-v180 [style*="background: #0"],
body .pdf-report-v180 [style*="background:#1"],body .pdf-report-v180 [style*="background: #1"],
body .pdf-report-v180 [style*="background-color:#0"],body .pdf-report-v180 [style*="background-color: #0"],
body .pdf-report-v180 [style*="background-color:#1"],body .pdf-report-v180 [style*="background-color: #1"]{
  background:#fff!important;background-image:none!important;color:#1f2937!important
}
body .pdf-report-v180 .good,body .pdf-report-v180 .ok{color:#16835f!important}
body .pdf-report-v180 .warn{color:#9a6418!important}
body .pdf-report-v180 .bad,body .pdf-report-v180 .critical{color:#b63848!important}
`;
}
'''
html=html.replace(anchor,extra+'\n'+anchor,1)
old="const css=reportCssV180()+managerPdfCssV182();"
new="const css=reportCssV180()+managerPdfCssV182()+managerPdfLightOverrideV183();"
if old not in html:
    raise SystemExit('PDF CSS composition anchor missing')
html=html.replace(old,new,1)
p.write_text(html,encoding='utf-8')
print('v1.8.3 PDF light cleanup applied')
