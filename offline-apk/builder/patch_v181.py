from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.1-plate-color-table-fix' in html:
    raise SystemExit('already patched')

anchor='function mixExtended(rows){'
if anchor not in html:
    raise SystemExit('mixExtended anchor missing')

js=r'''
/* v1.8.1-plate-color-table-fix */
function plateColorTable(stats){
  const data=Array.isArray(stats)?stats:[];
  if(!data.length)return '<div class="xreport-empty">Renk / kalıp analizi için veri yok.</div>';
  return `<div class="xreport-table-wrap"><table class="xreport-table"><thead><tr><th>Renk / Kalıp</th><th>İş</th><th>Net</th><th>Fire</th><th>Fire %</th><th>Duruş</th><th>Kalıp</th></tr></thead><tbody>${data.map(x=>`<tr data-xscope="plateColor" data-xvalue="${esc(x.id)}" data-xlabel="${esc(x.name)}"><td><strong>${esc(x.name)}</strong></td><td>${fmtNum(x.jobs)}</td><td>${fmtNum(x.good)}</td><td>${fmtNum(x.scrap)}</td><td>${fmtPct(x.rate)}</td><td>${fmtNum(x.down)} dk</td><td>${fmtNum(x.plates)}</td></tr>`).join('')}</tbody></table></div>`;
}
'''
html=html.replace(anchor,js+'\n'+anchor,1)

# Runtime guard: all-report/PDF should not fail completely if one optional report block has a rendering problem.
old="""function reportBlockForPdfV180(view,rows){
  if(view==='general')return executiveOverviewV170(rows);
  if(view==='performance')return performanceHubV170(rows);
  if(view==='losses')return lossesHubV170(rows);
  if(view==='production')return productionHubV171(rows);
  if(view==='compare')return comparisonExtended(rows);
  return allExtendedReport(rows);
}"""
new="""function reportBlockForPdfV180(view,rows){
  try{
    if(view==='general')return executiveOverviewV170(rows);
    if(view==='performance')return performanceHubV170(rows);
    if(view==='losses')return lossesHubV170(rows);
    if(view==='production')return productionHubV171(rows);
    if(view==='compare')return comparisonExtended(rows);
    return allExtendedReport(rows);
  }catch(err){
    console.error('reportBlockForPdfV180',view,err);
    throw new Error('Rapor Merkezi görünümü hazırlanamadı: '+((err&&err.message)||String(err||'Bilinmeyen hata')));
  }
}"""
if old not in html:
    raise SystemExit('reportBlockForPdfV180 source missing')
html=html.replace(old,new,1)

p.write_text(html,encoding='utf-8')
print('v1.8.1 plateColorTable/PDF all-report fix applied')
