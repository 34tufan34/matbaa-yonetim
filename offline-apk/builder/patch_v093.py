from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')

css_anchor=""".field input,.field select,.field textarea,.filter-row input,.filter-row select,.backup-card input[type=file]{width:100%;background:#0b0e13;color:var(--text);border:1px solid #2b3240;border-radius:9px;padding:10px 11px;outline:none}"""
css_extra=r""".field input,.field select,.field textarea,.filter-row input,.filter-row select,.backup-card input[type=file]{width:100%;background:#0b0e13;color:var(--text);border:1px solid #2b3240;border-radius:9px;padding:10px 11px;outline:none}.field select,.filter-row select,.bulk-toolbar select,.report-filter-v2 select,.quality-filter{-webkit-appearance:none;appearance:none;background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23B7BEC9' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E\");background-repeat:no-repeat;background-position:right 12px center;background-size:14px;padding-right:36px}.report-title-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.quality-status-bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.quality-status-btn{border:1px solid #2b3240;background:#11161d;color:#d6dce5;border-radius:999px;padding:8px 12px;font-size:11px;font-weight:750;cursor:pointer}.quality-status-btn.active{background:#1a2330;border-color:#48556a}.quality-status-btn[data-value='critical'].active{background:#341920;color:#ffb5bc;border-color:#6d2b36}.quality-status-btn[data-value='warn'].active{background:#2e2413;color:#f3cf7a;border-color:#6a5422}.quality-status-btn[data-value='ok'].active{background:#14271e;color:#88e1b0;border-color:#2f6c51}.quality-dashboard .quality-card{cursor:pointer}.quality-dashboard .quality-card.active{background:#131a22;box-shadow:inset 0 0 0 1px rgba(255,255,255,.03)}.quality-badge{min-width:88px;justify-content:center;padding:6px 10px;font-size:10px}.report-filter-v2,.filter-row{background:linear-gradient(180deg,#0d1218,#0b0f14);border:1px solid #1c2430;border-radius:14px;padding:12px}.hidden-native-select{display:none!important}"""
if css_anchor in html:
    html=html.replace(css_anchor,css_extra,1)

html=html.replace('<button id="exportReportCsv" class="btn ghost">CSV Dışa Aktar</button>', '<div class="report-title-actions"><button id="printReportBtn" class="btn ghost">PDF / Yazdır</button><button id="exportReportCsv" class="btn ghost">CSV Dışa Aktar</button></div>',1)

old_q='<select id="qualityFilter" class="quality-filter"><option value="all">Tüm kalite durumları</option><option value="critical">Kritik</option><option value="warn">Kontrol edilmeli</option><option value="ok">Normal</option></select>'
new_q='''<div class="quality-status-bar" id="qualityFilterBar"><button type="button" class="quality-status-btn active" data-value="all">Tüm kalite durumları</button><button type="button" class="quality-status-btn" data-value="critical">Kritik</button><button type="button" class="quality-status-btn" data-value="warn">Kontrol</button><button type="button" class="quality-status-btn" data-value="ok">Normal</button></div><select id="qualityFilter" class="quality-filter hidden-native-select"><option value="all">Tüm kalite durumları</option><option value="critical">Kritik</option><option value="warn">Kontrol edilmeli</option><option value="ok">Normal</option></select>'''
html=html.replace(old_q,new_q,1)

html=html.replace('id="restoreFile" accept="application/json,.json"','id="restoreFile" accept="application/json,text/json,.json,.yedek,.txt,*/*"')
html=html.replace('id="externalImportFiles" accept="application/json,.json" multiple','id="externalImportFiles" accept="application/json,text/json,.json,text/csv,.csv,application/vnd.ms-excel,.xls,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,.xlsx,*/*" multiple')
html=html.replace('id="historyImportFile" accept="application/json,.json"','id="historyImportFile" accept="application/json,text/json,.json,text/csv,.csv,application/vnd.ms-excel,.xls,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,.xlsx,*/*"')

start=html.index("function optionList(arr, placeholder='Seçiniz', selected=''){")
end=html.index('function metric(',start)
block='''function optionList(arr, placeholder='Seçiniz', selected=''){
  return `<option value="">${placeholder}</option>` + activeItems(arr).map(x=>`<option value="${x.id}" ${x.id===selected?'selected':''}>${esc(x.name)}</option>`).join('');
}
function setSelectOptions(id, markup){ const el=$(id); if(!el)return; const current=el.value; el.innerHTML=markup; if([...el.options].some(o=>o.value===current)) el.value=current; }
function syncQualityFilterUi(){ const v=$('qualityFilter')?.value||'all'; qsa('#qualityFilterBar .quality-status-btn').forEach(b=>b.classList.toggle('active',b.dataset.value===v)); qsa('#qualityDashboard .quality-card').forEach(c=>c.classList.toggle('active',c.dataset.quality===v)); }
function populateSelects(){
  setSelectOptions('dashShift',optionList(state.shifts,'Vardiya seç'));
  setSelectOptions('recordShiftFilter',optionList(state.shifts,'Tüm vardiyalar'));
  setSelectOptions('recordMachineFilter',optionList(state.machines,'Tüm makineler'));
  setSelectOptions('reportShiftFilter',optionList(state.shifts,'Tüm vardiyalar'));
  setSelectOptions('reportMachineFilter',optionList(state.machines,'Tüm makineler'));
  setSelectOptions('reportMasterFilter',optionList(state.people.filter(x=>x.role==='Usta'||x.role==='Operatör'),'Tüm ustalar'));
  setSelectOptions('recShift',optionList(state.shifts,'Vardiya seç'));
  setSelectOptions('recMachine',optionList(state.machines,'Makine seç'));
  setSelectOptions('recMaster',optionList(state.people.filter(x=>x.role==='Usta'||x.role==='Operatör'),'Usta seç'));
  setSelectOptions('recScrapReason',optionList(state.scrapReasons,'Fire nedeni seç'));
  setSelectOptions('recDowntimeReason',optionList(state.downtimeReasons,'Duruş nedeni seç'));
  if($('bulkMaster'))setSelectOptions('bulkMaster',optionList(state.people.filter(x=>x.role==='Usta'||x.role==='Operatör'),'Usta değiştir...'));
  if($('bulkShift'))setSelectOptions('bulkShift',optionList(state.shifts,'Vardiya değiştir...'));
  if($('bulkMachine'))setSelectOptions('bulkMachine',optionList(state.machines,'Makine değiştir...'));
  syncQualityFilterUi();
}

'''
html=html[:start]+block+html[end:]

override='''\nfunction renderQualityDashboardV093(rows){
  if(!$('qualityDashboard'))return; const a=rows.map(r=>assessRecord(r)); const c=a.filter(x=>x.severity==='critical').length,w=a.filter(x=>x.severity==='warn').length,o=a.filter(x=>x.severity==='ok').length,v=$('qualityFilter')?.value||'all';
  $('qualityDashboard').innerHTML=`<div class="quality-card ${v==='all'?'active':''}" data-quality="all"><span>Toplam Kayıt</span><strong>${fmtNum(rows.length)}</strong><small>Seçili filtre</small></div><div class="quality-card critical ${v==='critical'?'active':''}" data-quality="critical"><span>Kritik</span><strong>${fmtNum(c)}</strong><small>Öncelikli kontrol</small></div><div class="quality-card warn ${v==='warn'?'active':''}" data-quality="warn"><span>Kontrol</span><strong>${fmtNum(w)}</strong><small>Şüpheli / eksik</small></div><div class="quality-card good ${v==='ok'?'active':''}" data-quality="ok"><span>Normal</span><strong>${fmtNum(o)}</strong><small>Kontrolden geçti</small></div>`;
  qsa('#qualityDashboard .quality-card').forEach(card=>card.onclick=()=>{$('qualityFilter').value=card.dataset.quality||'all';syncQualityFilterUi();renderRecords();});
}
function printMainReport(){
  const rows=currentReportRows||[]; if(!rows.length){toast('Yazdırılacak rapor verisi yok.');return;} const st=statsOf(rows),range=formatRange($('reportStart').value,$('reportEnd').value);
  const gs=(key,src)=>groupStats(rows,key,src); const table=(title,data)=>`<h2>${title}</h2><table><thead><tr><th>Grup</th><th>Net</th><th>Fire %</th><th>Duruş</th><th>İş</th></tr></thead><tbody>${data.map(x=>`<tr><td>${esc(x.name)}</td><td>${fmtNum(x.good)}</td><td>${fmtPct(x.rate)}</td><td>${fmtNum(x.down)} dk</td><td>${fmtNum(x.jobs)}</td></tr>`).join('')}</tbody></table>`;
  const detail=rows.slice().sort((a,b)=>`${a.date}|${a.workOrder}`.localeCompare(`${b.date}|${b.workOrder}`)).map(r=>`<tr><td>${esc(r.date)}</td><td>${esc(getById(state.shifts,r.shiftId)?.name||'-')}</td><td>${esc(getById(state.machines,r.machineId)?.name||'-')}</td><td>${esc(getById(state.people,r.masterId)?.name||'-')}</td><td>${esc(r.workOrder||'-')}</td><td>${fmtNum(r.goodQty)}</td><td>${fmtNum(r.plateQty)}</td><td>${fmtNum(r.scrapQty)}</td><td>${fmtPct(scrapRate(r))}</td><td>${fmtNum(r.downtimeMin)} dk</td></tr>`).join('');
  const doc=`<!doctype html><html><head><meta charset="utf-8"><style>body{font-family:Arial;color:#15171a;margin:24px}h1{font-size:22px}.k{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}.k div{border:1px solid #ddd;padding:9px}table{width:100%;border-collapse:collapse;font-size:10px;margin:8px 0 18px}th,td{border-bottom:1px solid #ddd;padding:6px;text-align:left}th{background:#f2f3f5}</style></head><body><h1>Üretim Performans Raporu</h1><p>${esc(range)}</p><div class="k"><div>Net<br><b>${fmtNum(st.good)}</b></div><div>Fire<br><b>${fmtNum(st.scrap)}</b></div><div>Fire %<br><b>${fmtPct(st.rate)}</b></div><div>Duruş<br><b>${fmtNum(st.down)} dk</b></div><div>İş<br><b>${fmtNum(st.jobs)}</b></div><div>Kalıp<br><b>${fmtNum(st.plates)}</b></div></div>${table('Makine Performansı',gs('machineId',state.machines))}${table('Vardiya Performansı',gs('shiftId',state.shifts))}${table('Usta Performansı',gs('masterId',state.people))}<h2>Detaylı Kayıtlar</h2><table><thead><tr><th>Tarih</th><th>Vardiya</th><th>Makine</th><th>Usta</th><th>İş Emri</th><th>Net</th><th>Kalıp</th><th>Fire</th><th>Fire %</th><th>Duruş</th></tr></thead><tbody>${detail}</tbody></table></body></html>`;
  if(isAndroidNative()&&typeof window.AndroidApp.printHtml==='function'){window.AndroidApp.printHtml('Uretim Performans Raporu',doc);return;} const w=window.open('','_blank'); if(!w){toast('Yazdırma penceresi engellendi.');return;} w.document.write(doc.replace('</body>','<script>window.onload=()=>window.print()<\\/script></body>')); w.document.close();
}
'''
html=html.replace('function exportCsv(){',override+'\nfunction exportCsv(){',1)

html=html.replace("$('qualityFilter').onchange=renderRecords; $('bulkApplyBtn').onclick=bulkApplyCorrection;", "$('qualityFilter').onchange=()=>{syncQualityFilterUi();renderRecords();}; qsa('#qualityFilterBar .quality-status-btn').forEach(b=>b.onclick=()=>{$('qualityFilter').value=b.dataset.value||'all';syncQualityFilterUi();renderRecords();}); $('bulkApplyBtn').onclick=bulkApplyCorrection;")
html=html.replace("$('recordFilterBtn').onclick=renderRecords; $('recordSearch').oninput=()=>{clearTimeout(bindEvents.rs);bindEvents.rs=setTimeout(renderRecords,250)};", "$('recordFilterBtn').onclick=renderRecords; $('recordSearch').oninput=()=>{clearTimeout(bindEvents.rs);bindEvents.rs=setTimeout(renderRecords,250)}; ['recordStart','recordEnd','recordShiftFilter','recordMachineFilter'].forEach(id=>$(id).onchange=renderRecords);")
html=html.replace("['reportShiftFilter','reportMachineFilter','reportMasterFilter'].forEach(id=>$(id).onchange=runReport); $('exportReportCsv').onclick=exportCsv;", "['reportStart','reportEnd','reportShiftFilter','reportMachineFilter','reportMasterFilter'].forEach(id=>$(id).onchange=runReport); $('exportReportCsv').onclick=exportCsv; if($('printReportBtn'))$('printReportBtn').onclick=printMainReport;")
html=html.replace("renderQualityDashboard(allBase); const rows=filteredRecords();", "renderQualityDashboardV093(allBase); const rows=filteredRecords();")
html=html.replace("updateSelectionUi(); renderAuditAndTrash();", "updateSelectionUi(); syncQualityFilterUi(); renderAuditAndTrash();")
html=html.replace("function previewHistoryImport(file){\n  historyImportPayload=null; $('historyImportBtn').disabled=true;", "function previewHistoryImport(file){\n  historyImportPayload=null; $('historyImportBtn').disabled=true; const lower=String(file?.name||'').toLowerCase(); if(lower.endsWith('.xlsx')||lower.endsWith('.xls')){ $('historyImportPreview').textContent='Excel dosyası seçildi. Bu sürüm dosyayı seçebilir; doğrudan XLSX okuma modülü bir sonraki adımda eklenecek.'; return; }")
html=html.replace('</head>','<meta name="upm-build" content="v0.9.3-source-build"></head>',1)
p.write_text(html,encoding='utf-8')
print('patched',len(html))