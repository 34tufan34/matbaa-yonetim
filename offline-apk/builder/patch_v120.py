from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')

css=r'''
/* v1.2.0 instant report + reconciliation + factory reset */
.report-detail-tabs{position:sticky;top:0;z-index:8;background:linear-gradient(180deg,rgba(16,19,25,.98),rgba(16,19,25,.94));padding:10px 0 8px;margin-top:10px;border-top:1px solid #1f2732;border-bottom:1px solid #1f2732;backdrop-filter:blur(8px)}
.report-focus-shell{margin-top:14px;display:grid;gap:14px}.report-focus-head{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:0 2px}.report-focus-head h3{margin:0;font-size:15px}.report-focus-head p{margin:3px 0 0;color:#8b95a4;font-size:11px}.report-focus-host{scroll-margin-top:100px}.report-consistency{background:linear-gradient(180deg,#10161e,#0d1218);border:1px solid #26303e;border-radius:14px;padding:14px}.consistency-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.consistency-head h3{margin:0;font-size:15px}.consistency-head p{margin:4px 0 0;color:#8792a2;font-size:11px}.consistency-state{padding:6px 10px;border-radius:999px;font-size:11px;font-weight:800;white-space:nowrap}.consistency-state.ok{background:#14291e;color:#8de0b3;border:1px solid #2b6549}.consistency-state.bad{background:#36191e;color:#ffafb7;border:1px solid #74303b}.consistency-state.warn{background:#332814;color:#f0cf79;border:1px solid #6a5525}.consistency-table-wrap{overflow:auto;margin-top:12px}.consistency-table{width:100%;border-collapse:collapse;min-width:720px;font-size:11px}.consistency-table th,.consistency-table td{padding:8px 10px;border-bottom:1px solid #222b37;text-align:right}.consistency-table th:first-child,.consistency-table td:first-child{text-align:left}.consistency-table th{color:#8691a0;font-size:10px;text-transform:uppercase;letter-spacing:.35px}.consistency-table .ok{color:#8de0b3}.consistency-table .bad{color:#ff929c;font-weight:800}.consistency-note{margin-top:10px;color:#8c96a4;font-size:11px;line-height:1.5}.consistency-note strong{color:#d9dfe8}.all-report-divider{height:1px;background:#28313d;margin:22px 0}.factory-reset-card{border-color:#5b2930!important;background:linear-gradient(180deg,#1c1114,#120d0f)!important}.factory-reset-card h2{color:#ffd7db}.factory-reset-actions{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:12px}.factory-reset-warning{font-size:11px;color:#cfa5aa;max-width:720px}.btn.factory-danger{background:#7b1f2a;color:#fff;border:1px solid #a33a47}.btn.factory-danger:hover{background:#922834}
'''
html=html.replace('@media(max-width:1250px)', css+'\n@media(max-width:1250px)',1)

old='''            <button data-report-detail="compare">Karşılaştırma</button>\n          </div>\n        </div>\n\n        <div class="report-kpi-grid" id="reportMetrics"></div>'''
new='''            <button data-report-detail="compare">Karşılaştırma</button>\n            <button data-report-detail="all">Her Şeyi Gör</button>\n          </div>\n        </div>\n\n        <div class="report-focus-shell">\n          <div id="reportConsistencyHost" class="report-consistency"></div>\n          <div class="panel report-focus-host">\n            <div class="report-focus-head"><div><div class="eyebrow">ANLIK RAPOR GÖRÜNÜMÜ</div><h3>Seçilen Analiz</h3><p>Üstteki sekmeye dokunduğunda sonuç burada anında değişir.</p></div><span id="reportFocusLabel" class="subtle-chip">Genel</span></div>\n            <div id="reportDetailHost" class="extended-report-host"></div>\n          </div>\n        </div>\n\n        <div class="report-kpi-grid" id="reportMetrics"></div>'''
if old not in html: raise SystemExit('report tab anchor missing')
html=html.replace(old,new,1)
old_host='''        <div id="reportDetailHost" class="extended-report-host"></div>\n      </section>'''
if old_host not in html: raise SystemExit('old report host missing')
html=html.replace(old_host,'      </section>',1)

anchor='''        <div class="panel">\n          <h3>Veri Güvenliği</h3>'''
factory='''        <div class="panel backup-card factory-reset-card">\n          <div class="panel-head"><div><div class="eyebrow">SİSTEM SIFIRLAMA</div><h2>Fabrika Ayarlarına Dön</h2><p>Programdaki tüm tanımlar, üretim kayıtları, ayarlar, geçmiş ve silinen kayıtları sıfırlar. Uygulama ilk kurulum durumuna döner.</p></div></div>\n          <div class="factory-reset-actions"><div class="factory-reset-warning">İşlem geri alınamaz. Önce <strong>Tam Yedek Oluştur</strong> ile JSON yedeği alman önerilir. Fabrika sıfırlaması sonrası uygulamanın gömülü ilk kurulum verileri yeniden yüklenir.</div><button id="factoryResetBtn" class="btn factory-danger" type="button">Fabrika Ayarlarına Döndür</button></div>\n        </div>\n        <div class="panel">\n          <h3>Veri Güvenliği</h3>'''
if anchor not in html: raise SystemExit('settings data security anchor missing')
html=html.replace(anchor,factory,1)

marker='function generalExtended(rows){'
if marker not in html: raise SystemExit('generalExtended missing')
js=r'''
function additiveTotalsFromGroups(groups){return groups.reduce((a,x)=>({good:a.good+Number(x.good||0),scrap:a.scrap+Number(x.scrap||0),down:a.down+Number(x.down||0),plates:a.plates+Number(x.plates||0)}),{good:0,scrap:0,down:0,plates:0})}
function reportReconciliation(rows){
  const base=statsOf(rows),machine=additiveTotalsFromGroups(enhancedGroupStats(rows,'machineId',state.machines)),shift=additiveTotalsFromGroups(enhancedGroupStats(rows,'shiftId',state.shifts)),master=additiveTotalsFromGroups(enhancedGroupStats(rows,'masterId',state.people));
  const metrics=[['Net Baskı','good'],['Fire Adedi','scrap'],['Toplam Duruş','down'],['Kalıp Sayısı','plates']];
  const tolerance=.001;
  const checks=metrics.map(([name,key])=>{const b=Number(base[key]||0),m=Number(machine[key]||0),s=Number(shift[key]||0),u=Number(master[key]||0),maxDiff=Math.max(Math.abs(b-m),Math.abs(b-s),Math.abs(b-u));return{name,key,base:b,machine:m,shift:s,master:u,diff:maxDiff,ok:maxDiff<=tolerance}});
  const missingMachine=rows.filter(r=>!r.machineId).length,missingShift=rows.filter(r=>!r.shiftId).length,missingMaster=rows.filter(r=>!r.masterId).length;
  return{checks,allOk:checks.every(x=>x.ok),missingMachine,missingShift,missingMaster};
}
function renderReportConsistency(rows){
  const host=$('reportConsistencyHost');if(!host)return;const r=reportReconciliation(rows),missing=r.missingMachine+r.missingShift+r.missingMaster;
  const stateClass=!r.allOk?'bad':missing?'warn':'ok',stateText=!r.allOk?'⚠ Toplam farkı bulundu':missing?'✓ Toplamlar eşit • eksik tanım var':'✓ Tüm toplamlar tutarlı';
  const unit=k=>k==='down'?' dk':'';
  host.innerHTML=`<div class="consistency-head"><div><div class="eyebrow">ÇAPRAZ KONTROL</div><h3>Rapor Toplam Tutarlılığı</h3><p>Aynı kayıtların ana toplamı, makine, vardiya ve usta kırılımlarında karşılaştırılır.</p></div><span class="consistency-state ${stateClass}">${stateText}</span></div><div class="consistency-table-wrap"><table class="consistency-table"><thead><tr><th>Gösterge</th><th>Ana Toplam</th><th>Makine Toplamı</th><th>Vardiya Toplamı</th><th>Usta Toplamı</th><th>Durum</th></tr></thead><tbody>${r.checks.map(x=>`<tr><td><strong>${x.name}</strong></td><td>${fmtNum(x.base)}${unit(x.key)}</td><td>${fmtNum(x.machine)}${unit(x.key)}</td><td>${fmtNum(x.shift)}${unit(x.key)}</td><td>${fmtNum(x.master)}${unit(x.key)}</td><td class="${x.ok?'ok':'bad'}">${x.ok?'✓ Eşit':`⚠ Fark ${fmtNum(x.diff)}`}</td></tr>`).join('')}</tbody></table></div><div class="consistency-note">${missing?`Tanımsız kayıt kontrolü: <strong>${r.missingMachine}</strong> makinesiz, <strong>${r.missingShift}</strong> vardiyasız, <strong>${r.missingMaster}</strong> ustasız kayıt. Bunlar toplam hesabına “Tanımsız” grup olarak dahil edilir.`:'Makine, vardiya ve usta kırılımlarında ana toplamdan kayıp kayıt görünmüyor.'} <strong>İş Sayısı, Fire %, Duruş/İş, Tabaka/Saat ve Kapasite % toplanabilir değer değildir;</strong> bu nedenle çapraz toplam kontrolüne dahil edilmez.</div>`;
}
function reportDetailLabel(view){return({general:'Genel',shift:'Vardiya',machine:'Makine',master:'Usta',scrap:'Fire',downtime:'Duruş',workorder:'İş Emri',mix:'Renk / Kalıp / Lak',trend:'Trend',compare:'Karşılaştırma',all:'Her Şeyi Gör'})[view]||'Genel'}
function allExtendedReport(rows){
  const parts=[generalExtended(rows),groupExtended(rows,'shift'),groupExtended(rows,'machine'),groupExtended(rows,'master'),scrapExtended(rows),downtimeExtended(rows),workOrderExtended(rows),mixExtended(rows),trendExtended(rows),comparisonExtended(rows)];
  return parts.map((x,i)=>`${i?'<div class="all-report-divider"></div>':''}${x}`).join('');
}
'''
html=html.replace(marker,js+'\n'+marker,1)

old_start="function renderExtendedReport(view,rows){currentReportDetail=view||currentReportDetail||'general';"
start=html.find(old_start)
if start<0: raise SystemExit('renderExtendedReport start missing')
end=html.find('\n\nfunction drillScopeName',start)
if end<0: raise SystemExit('renderExtendedReport end missing')
new_func=r'''function renderExtendedReport(view,rows){
  currentReportDetail=view||currentReportDetail||'general';
  qsa('#reportDetailTabs button').forEach(b=>b.classList.toggle('active',b.dataset.reportDetail===currentReportDetail));
  if($('reportFocusLabel'))$('reportFocusLabel').textContent=reportDetailLabel(currentReportDetail);
  const host=$('reportDetailHost');if(!host)return;
  if(!rows.length){host.innerHTML='<div class="xreport-panel"><div class="xreport-empty">Seçilen filtrelerde rapor verisi yok.</div></div>';return}
  let out='';
  if(currentReportDetail==='all')out=allExtendedReport(rows);
  else if(currentReportDetail==='general')out=generalExtended(rows);
  else if(['shift','machine','master'].includes(currentReportDetail))out=groupExtended(rows,currentReportDetail);
  else if(currentReportDetail==='scrap')out=scrapExtended(rows);
  else if(currentReportDetail==='downtime')out=downtimeExtended(rows);
  else if(currentReportDetail==='workorder')out=workOrderExtended(rows);
  else if(currentReportDetail==='mix')out=mixExtended(rows);
  else if(currentReportDetail==='trend')out=trendExtended(rows);
  else if(currentReportDetail==='compare')out=comparisonExtended(rows);
  host.innerHTML=out;bindExtendedDrill(host,rows);
}
'''
html=html[:start]+new_func+html[end:]

needle="  drawDailyTrend($('dailyTrendChart'),rows);\n  renderExtendedReport(currentReportDetail,rows);"
repl="  drawDailyTrend($('dailyTrendChart'),rows);\n  renderReportConsistency(rows);\n  renderExtendedReport(currentReportDetail,rows);"
if needle not in html: raise SystemExit('runReport anchor missing')
html=html.replace(needle,repl,1)

bind_marker='function bindEvents(){'
if bind_marker not in html: raise SystemExit('bindEvents missing')
factory_js=r'''
async function factoryResetApp(){
  const ok=confirm('FABRİKA AYARLARI\n\nTüm üretim kayıtları, tanımlar, ayarlar, değişiklik geçmişi ve silinen kayıtlar sıfırlanacak. Bu işlem geri alınamaz. Devam edilsin mi?');
  if(!ok)return;
  const code=prompt('Yanlışlıkla sıfırlamayı önlemek için FABRİKA yaz:','');
  if(String(code||'').trim().toLocaleUpperCase('tr-TR')!=='FABRİKA'){toast('Fabrika sıfırlaması iptal edildi.');return;}
  try{
    for(const name of STORES)await dbClear(name);
    toast('Program fabrika ayarlarına döndürülüyor...');
    setTimeout(()=>location.reload(),500);
  }catch(err){console.error(err);alert('Fabrika ayarlarına dönüş sırasında hata oluştu. Mevcut verileriniz için yedek dosyanızı koruyun.');}
}
'''
html=html.replace(bind_marker,factory_js+'\n'+bind_marker,1)

old="qsa('#reportDetailTabs button').forEach(b=>b.onclick=()=>{currentReportDetail=b.dataset.reportDetail;renderExtendedReport(currentReportDetail,currentReportRows);});"
new="qsa('#reportDetailTabs button').forEach(b=>b.onclick=()=>{currentReportDetail=b.dataset.reportDetail;renderExtendedReport(currentReportDetail,currentReportRows);const focus=$('reportDetailHost');if(focus)focus.scrollIntoView({behavior:'smooth',block:'start'});});"
if old not in html: raise SystemExit('detail tab bind missing')
html=html.replace(old,new,1)
backup_bind="$('historyImportFile').onchange=e=>e.target.files[0]&&previewHistoryImport(e.target.files[0]); $('historyImportBtn').onclick=importHistoryProduction;"
backup_new=backup_bind+" if($('factoryResetBtn'))$('factoryResetBtn').onclick=factoryResetApp;"
if backup_bind not in html: raise SystemExit('backup bind anchor missing')
html=html.replace(backup_bind,backup_new,1)

html=html.replace('v1.1.0-stable-install','v1.2.0-instant-report',1)
html=html.replace('v1.1.0 • Android / tamamen offline','v1.2.0 • Android / tamamen offline')
p.write_text(html,encoding='utf-8')
print('patched-v120',len(html))
