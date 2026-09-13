from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.2-white-manager-pdf' in html:
    raise SystemExit('already patched')

start=html.find("function buildReportCenterPdfV180(mode='active'){")
end=html.find('function createReportCenterPdfV180(mode){',start)
if start<0 or end<0:
    raise SystemExit('v1.8 PDF builder block not found')

new=r'''/* v1.8.2-white-manager-pdf */
function managerPdfCssV182(){
  return `
@page{size:A4 landscape;margin:9mm 9mm 11mm}
:root,body{
  --bg:#ffffff!important;--panel:#ffffff!important;--panel2:#f6f8fb!important;
  --line:#d7dee8!important;--muted:#667085!important;--text:#1f2937!important;
  --accent:#245d9f!important;--accent2:#16487f!important;--good:#16835f!important;
  --warn:#b7791f!important;--bad:#c43d4d!important
}
*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important;box-sizing:border-box}
html,body{margin:0!important;padding:0!important;background:#fff!important;color:#1f2937!important;height:auto!important;min-height:0!important;font-family:Arial,Helvetica,sans-serif!important}
.pdf-report-v180{width:100%!important;max-width:none!important;margin:0!important;padding:0!important;background:#fff!important;color:#1f2937!important}
.pdf-report-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-end;padding:13px 15px;margin:0 0 12px;border:1px solid #cad5e3!important;border-left:5px solid #245d9f!important;border-radius:8px!important;background:#f7f9fc!important;box-shadow:none!important}
.pdf-report-head h1{font-size:20px!important;line-height:1.15;margin:3px 0 4px!important;color:#172033!important}.pdf-report-head p{margin:0!important;color:#667085!important;font-size:9px!important}.pdf-report-head .pdf-meta{text-align:right;color:#667085!important;font-size:8px!important}.pdf-report-head .pdf-meta strong{display:block;color:#172033!important;font-size:11px!important;margin-bottom:3px}
.pdf-manager-label{font-size:8px;font-weight:800;letter-spacing:.9px;color:#245d9f!important}
.pdf-report-v180 .report-hub-intro,.pdf-report-v180 .all-report-intro,.pdf-report-v180 .xreport-panel,.pdf-report-v180 .xreport-card,.pdf-report-v180 .hub-section,.pdf-report-v180 .attention-panel,.pdf-report-v180 .decision-kpi,.pdf-report-v180 .shift-number-note,.pdf-report-v180 .metric,.pdf-report-v180 .quality-card{background:#fff!important;color:#1f2937!important;border-color:#d7dee8!important;box-shadow:none!important}
.pdf-report-v180 .all-report-intro{background:#eef4fb!important;border-color:#c9d8e9!important;padding:11px 13px!important;border-radius:8px!important}.pdf-report-v180 .all-report-intro h2,.pdf-report-v180 h1,.pdf-report-v180 h2,.pdf-report-v180 h3,.pdf-report-v180 h4,.pdf-report-v180 strong{color:#172033!important}.pdf-report-v180 p,.pdf-report-v180 small,.pdf-report-v180 .muted,.pdf-report-v180 .section-sub{color:#667085!important}
.pdf-report-v180 .all-report-section{display:block!important;height:auto!important;min-height:0!important;max-height:none!important;overflow:visible!important;margin:0!important;padding:0!important;break-inside:auto!important;page-break-inside:auto!important}.pdf-report-v180 .all-report-divider{height:0!important;border-top:1px solid #dfe5ec!important;background:none!important;margin:13px 0!important;break-before:auto!important;page-break-before:auto!important}.pdf-report-v180 .all-report-section-label{margin:0 0 7px!important}.pdf-report-v180 .all-report-section-label span{background:#eaf0f7!important;color:#24476d!important;border:1px solid #cbd7e5!important;border-radius:5px!important;padding:5px 8px!important;font-size:8px!important}
.pdf-report-v180 .report-subtabs,.pdf-report-v180 .workorder-open-panel,.pdf-report-v180 [data-close-pdfreport],.pdf-report-v180 .icon-btn{display:none!important}
.pdf-report-v180 .xreport-table-wrap,.pdf-report-v180 .table-wrap,.pdf-report-v180 .table-scroll{overflow:visible!important;max-height:none!important;height:auto!important;background:#fff!important;border-color:#d7dee8!important}
.pdf-report-v180 table{width:100%!important;border-collapse:collapse!important;background:#fff!important;color:#1f2937!important;font-size:8px!important}.pdf-report-v180 th{background:#edf2f7!important;color:#344054!important;border:1px solid #d7dee8!important;padding:5px 6px!important;font-weight:800!important;text-align:left!important}.pdf-report-v180 td{background:#fff!important;color:#1f2937!important;border:1px solid #e1e6ed!important;padding:5px 6px!important}.pdf-report-v180 tr{break-inside:avoid!important;page-break-inside:avoid!important}
.pdf-report-v180 .decision-kpi,.pdf-report-v180 .xreport-card{border-radius:7px!important}.pdf-report-v180 .decision-kpi-grid,.pdf-report-v180 .xreport-kpi-grid,.pdf-report-v180 .metric-grid{gap:7px!important}.pdf-report-v180 .decision-kpi b,.pdf-report-v180 .xreport-card b{color:#172033!important}
.pdf-report-v180 .viz-track,.pdf-report-v180 .bar-track,.pdf-report-v180 .progress-track{background:#e8edf3!important}.pdf-report-v180 .viz-fill,.pdf-report-v180 .bar-fill,.pdf-report-v180 .progress-fill{print-color-adjust:exact!important}
.pdf-report-v180 .attention-item,.pdf-report-v180 .command-attention-item,.pdf-report-v180 .quality-issue{background:#f8fafc!important;color:#1f2937!important;border-color:#d7dee8!important}
.pdf-report-v180 .badge,.pdf-report-v180 .pill,.pdf-report-v180 .subtle-chip{background:#eef2f6!important;color:#475467!important;border-color:#d0d7e1!important}
.pdf-report-v180 button{pointer-events:none!important;cursor:default!important}
.pdf-report-v180 .report-hub-intro,.pdf-report-v180 .xreport-section-title,.pdf-report-v180 .attention-panel,.pdf-report-v180 .xreport-card,.pdf-report-v180 .decision-kpi{break-inside:avoid!important;page-break-inside:avoid!important}
.pdf-report-v180 .hub-section,.pdf-report-v180 .xreport-panel{break-inside:auto!important;page-break-inside:auto!important;min-height:0!important;height:auto!important;max-height:none!important;overflow:visible!important}
.pdf-report-v180 .all-report-intro,.pdf-report-v180 .report-hub-intro{margin-bottom:10px!important}
.pdf-report-v180 .eyebrow{color:#245d9f!important}.pdf-report-v180 a{color:#245d9f!important;text-decoration:none!important}
.pdf-report-v180 .good,.pdf-report-v180 .ok{color:#16835f!important}.pdf-report-v180 .warn{color:#9a6418!important}.pdf-report-v180 .bad,.pdf-report-v180 .critical{color:#b63848!important}
`;
}
function cleanManagerReportHtmlV182(raw){
  const box=document.createElement('div');box.innerHTML=raw||'';
  box.querySelectorAll('.report-subtabs,.workorder-open-panel').forEach(x=>x.remove());
  box.querySelectorAll('[onclick],[data-xscope],[data-drill-scope],[data-command-target],[data-report-sub]').forEach(x=>{x.removeAttribute('onclick');x.removeAttribute('data-xscope');x.removeAttribute('data-drill-scope');x.removeAttribute('data-command-target');x.removeAttribute('data-report-sub');});
  return box.innerHTML;
}
function buildReportCenterPdfV180(mode='active'){
  const rows=currentReportRows||[];if(!rows.length)throw new Error('PDF için rapor verisi yok.');
  const view=mode==='all'?'all':(currentReportDetail||'general');
  const title=mode==='all'?'Yönetici Üretim Raporu':reportDetailLabel(view);
  const range=formatRange($('reportStart').value,$('reportEnd').value);
  const reportHtml=reportBlockForPdfV180(view,rows);
  const body=cleanManagerReportHtmlV182(reportHtml);
  const css=reportCssV180()+managerPdfCssV182();
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${css}</style></head><body><main class="pdf-report-v180"><header class="pdf-report-head"><div><div class="pdf-manager-label">ÜRETİM PERFORMANS MERKEZİ</div><h1>${esc(title)}</h1><p>Rapor Merkezi verilerinden oluşturulan yönetici raporu</p></div><div class="pdf-meta"><strong>${esc(range)}</strong>${fmtNum(rows.length)} üretim kaydı</div></header>${body}</main></body></html>`;
}
'''
html=html[:start]+new+html[end:]
p.write_text(html,encoding='utf-8')
print('v1.8.2 white manager PDF patch applied')
