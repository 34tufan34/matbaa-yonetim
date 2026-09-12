from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.6.0-record-entry' in html:
    raise SystemExit('already patched')

# 1) Record modal: machine quick tabs + automatic defaults summary.
old='''      <form id="recordForm" class="form-grid">
        <input type="hidden" id="recordId" />'''
new='''      <div class="record-entry-quick v1.6.0-record-entry">
        <div class="record-entry-label"><span>HIZLI MAKİNE SEÇİMİ</span><small>Makineyi seç; vardiya ve usta otomatik önerilsin.</small></div>
        <div id="recordMachineTabs" class="record-machine-tabs"></div>
        <div id="recordAutoDefaults" class="record-auto-defaults"></div>
      </div>
      <form id="recordForm" class="form-grid">
        <input type="hidden" id="recordId" />'''
if old not in html: raise SystemExit('record form marker not found')
html=html.replace(old,new,1)

# 2) Dedicated production-record work order history modal.
marker='''  <div id="pdfReportModal" class="modal hidden">'''
insert='''  <div id="recordWorkOrderHistoryModal" class="modal hidden">
    <div class="modal-backdrop" data-close-record-workorder></div>
    <div class="modal-card record-workorder-history-card">
      <div class="modal-head"><div><div class="eyebrow">İŞ EMRİ GEÇMİŞİ</div><h2 id="recordWorkOrderHistoryTitle">İş Emri</h2><p id="recordWorkOrderHistorySubtitle">Tüm üretim geçmişi.</p></div><button class="icon-btn" type="button" data-close-record-workorder>×</button></div>
      <div id="recordWorkOrderHistoryBody" class="record-workorder-history-body"></div>
    </div>
  </div>

'''+marker
if marker not in html: raise SystemExit('pdf modal marker not found')
html=html.replace(marker,insert,1)

# 3) PDF button wording: direct PDF generation, no Android print-preview dependency.
html=html.replace('>PDF / Yazdır</button>', '>PDF Rapor</button>', 1)
html=html.replace('id="createSmartPdfBtn" class="btn primary" type="button">Renkli PDF / Yazdır</button>', 'id="createSmartPdfBtn" class="btn primary" type="button">Renkli PDF Oluştur</button>', 1)

# 4) Style additions.
css='''\n/* v1.6.0 quick entry + work-order history */
.record-entry-quick{margin:2px 0 14px;padding:13px;border:1px solid #273445;border-radius:14px;background:linear-gradient(135deg,rgba(46,93,170,.16),rgba(16,21,29,.92))}.record-entry-label{display:flex;justify-content:space-between;gap:12px;align-items:end;margin-bottom:10px}.record-entry-label span{font-size:10px;font-weight:900;letter-spacing:.9px;color:#9ab6e8}.record-entry-label small{font-size:10px;color:#7f8b9b}.record-machine-tabs{display:flex;gap:8px;flex-wrap:wrap}.record-machine-tab{appearance:none;border:1px solid #334156;background:#0d131c;color:#cbd5e3;border-radius:12px;padding:10px 18px;min-width:96px;font-weight:900;cursor:pointer;transition:.16s ease;box-shadow:inset 0 1px 0 rgba(255,255,255,.025)}.record-machine-tab:hover{transform:translateY(-1px);border-color:#5579b9}.record-machine-tab.active{background:linear-gradient(135deg,#315fa9,#477dd7);border-color:#6d98e3;color:#fff;box-shadow:0 8px 24px rgba(49,95,169,.22)}.record-auto-defaults{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.record-default-chip{display:inline-flex;gap:5px;align-items:center;border:1px solid #2a3749;background:#0b1118;border-radius:999px;padding:6px 9px;font-size:10px;color:#95a3b6}.record-default-chip strong{color:#edf3fb}.record-workorder-link{appearance:none;border:0;background:transparent;color:#86b1ff;font-weight:900;padding:0;cursor:pointer;text-decoration:underline;text-decoration-color:rgba(134,177,255,.35);text-underline-offset:3px}.record-workorder-link:hover{color:#b6d0ff}.record-workorder-history-card{width:min(1180px,96vw);max-height:90vh;display:flex;flex-direction:column}.record-workorder-history-body{overflow:auto;max-height:72vh}.wo-history-kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin-bottom:12px}.wo-history-kpi{border:1px solid #27313e;background:#0d131a;border-radius:11px;padding:10px}.wo-history-kpi span{display:block;color:#7f8b9b;font-size:9px;text-transform:uppercase;font-weight:800}.wo-history-kpi strong{display:block;margin-top:5px;font-size:15px}.wo-history-meta{border:1px solid #25303d;background:#0d1218;border-radius:11px;padding:10px 12px;margin-bottom:12px;color:#9aa7b8;font-size:10px;line-height:1.6}.wo-history-meta strong{color:#edf3fb}.wo-history-table-wrap{overflow:auto;border:1px solid #26313e;border-radius:11px}.wo-history-table{width:100%;border-collapse:collapse;min-width:980px}.wo-history-table th,.wo-history-table td{padding:8px 9px;border-bottom:1px solid #222c37;text-align:left;font-size:10px;white-space:nowrap}.wo-history-table th{position:sticky;top:0;background:#151c26;color:#8f9bae;z-index:1}.wo-history-edit{border:1px solid #334257;background:#111823;color:#dce6f5;border-radius:7px;padding:5px 8px;cursor:pointer}@media(max-width:800px){.record-entry-label{display:block}.record-entry-label small{display:block;margin-top:4px}.wo-history-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.record-machine-tab{flex:1;min-width:78px}}\n'''
if '</style>' not in html: raise SystemExit('style end not found')
html=html.replace('</style>',css+'</style>',1)

# 5) Replace record quick-entry functions.
start=html.find('function openRecordModal(prefill={}){')
end=html.find('\nfunction updateRecordCalc(){',start)
if start<0 or end<0: raise SystemExit('record function block not found')
new_funcs=r'''function timeInsideShift(hhmm,start,end){
  if(!start||!end)return false;
  const mins=x=>{const [h,m]=String(x).split(':').map(Number);return h*60+(m||0)};
  const n=mins(hhmm),a=mins(start),b=mins(end);return a<=b?(n>=a&&n<b):(n>=a||n<b);
}
function suggestedShiftId(){
  const d=new Date(),now=String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');
  return (state.shifts||[]).find(s=>s.active!==false&&timeInsideShift(now,s.start,s.end))?.id || (state.shifts||[]).find(s=>s.active!==false)?.id || '';
}
function suggestedMasterId(machineId,shiftId){
  const recent=[...(state.productionRecords||[])].filter(r=>r.machineId===machineId&&(!shiftId||r.shiftId===shiftId)&&r.masterId&&getById(state.people,r.masterId)?.active!==false).sort((a,b)=>String(b.updatedAt||b.createdAt||b.date||'').localeCompare(String(a.updatedAt||a.createdAt||a.date||'')))[0];
  if(recent?.masterId)return recent.masterId;
  const machine=getById(state.machines,machineId),ids=(machine?.assignedMasterIds||[]).filter(id=>getById(state.people,id)?.active!==false);return ids[0]||'';
}
function renderRecordMachineTabs(){
  const host=$('recordMachineTabs');if(!host)return;
  const selected=$('recMachine')?.value||'';
  const machines=(state.machines||[]).filter(m=>m.active!==false);
  host.innerHTML=machines.map(m=>`<button type="button" class="record-machine-tab ${m.id===selected?'active':''}" data-record-machine="${m.id}">${esc(m.name)}</button>`).join('');
  qsa('[data-record-machine]',host).forEach(b=>b.onclick=()=>applyRecordMachine(b.dataset.recordMachine));
}
function updateRecordAutoDefaults(){
  const host=$('recordAutoDefaults');if(!host)return;
  const sh=getById(state.shifts,$('recShift')?.value),ma=getById(state.machines,$('recMachine')?.value),me=getById(state.people,$('recMaster')?.value);
  host.innerHTML=`<span class="record-default-chip">Tarih <strong>${esc($('recDate')?.value||'-')}</strong></span><span class="record-default-chip">Makine <strong>${esc(ma?.name||'-')}</strong></span><span class="record-default-chip">Vardiya <strong>${esc(sh?.name||'-')}</strong></span><span class="record-default-chip">Usta <strong>${esc(me?.name||'-')}</strong></span>`;
  renderRecordMachineTabs();
}
function applyRecordMachine(machineId){
  if(!$('recMachine'))return;$('recMachine').value=machineId||'';
  const sh=$('recShift')?.value||suggestedShiftId();if($('recShift')&&!$('recShift').value)$('recShift').value=sh;
  const master=suggestedMasterId(machineId,$('recShift')?.value||sh);if(master&&$('recMaster'))$('recMaster').value=master;
  updateRecordAutoDefaults();
}
function autoSelectMaster(){
  const machineId=$('recMachine')?.value||'';if(!machineId)return updateRecordAutoDefaults();
  const master=suggestedMasterId(machineId,$('recShift')?.value||'');if(master&&$('recMaster'))$('recMaster').value=master;
  updateRecordAutoDefaults();
}
function openRecordModal(prefill={}){
  populateSelects();$('recordForm').reset();$('recordId').value='';$('recordModalTitle').textContent='Yeni Üretim Kaydı';
  const recent=[...(state.productionRecords||[])].sort((a,b)=>String(b.updatedAt||b.createdAt||b.date||'').localeCompare(String(a.updatedAt||a.createdAt||a.date||'')))[0];
  const activeMachines=(state.machines||[]).filter(m=>m.active!==false);
  const recentMachineId=recent?.machineId&&activeMachines.some(m=>m.id===recent.machineId)?recent.machineId:'';
  $('recDate').value=prefill.date||todayISO();$('recShift').value=prefill.shiftId||suggestedShiftId();$('recMachine').value=prefill.machineId||recentMachineId||activeMachines[0]?.id||'';
  $('recGoodQty').value='';$('recPlateQty').value='';$('recScrapQty').value=0;$('recDowntime').value=0;$('recColors').value=4;
  autoSelectMaster();updateRecordCalc();updateRecordAutoDefaults();$('recordModal').classList.remove('hidden');
}
function closeRecordModal(){ $('recordModal').classList.add('hidden'); }
'''
html=html[:start]+new_funcs+html[end:]

# 6) Make work order number clickable in production list and bind history.
old_cell='<td>${esc(r.workOrder)}</td><td>${fmtNum(r.goodQty)}</td>'
new_cell='<td><button type="button" class="record-workorder-link" data-record-workorder="${esc(r.workOrder)}" title="İş emri geçmişini aç">${esc(r.workOrder)}</button></td><td>${fmtNum(r.goodQty)}</td>'
if old_cell not in html: raise SystemExit('record work order cell not found')
html=html.replace(old_cell,new_cell,1)
old_bind="qsa('[data-edit-record]').forEach(b=>b.onclick=()=>editRecord(b.dataset.editRecord)); qsa('[data-delete-record]').forEach(b=>b.onclick=()=>deleteRecord(b.dataset.deleteRecord)); qsa('[data-quality-record]').forEach(b=>b.onclick=()=>openQualityModal(b.dataset.qualityRecord));"
new_bind=old_bind+" qsa('[data-record-workorder]').forEach(b=>b.onclick=()=>openRecordWorkOrderHistory(b.dataset.recordWorkorder));"
if old_bind not in html: raise SystemExit('record bind marker not found')
html=html.replace(old_bind,new_bind,1)

# 7) Add work order history functions before report period functions.
marker='''function getPeriodRange(period){'''
wo_funcs=r'''function closeRecordWorkOrderHistory(){const m=$('recordWorkOrderHistoryModal');if(m)m.classList.add('hidden')}
function openRecordWorkOrderHistory(workOrder){
  const key=String(workOrder||'').trim();if(!key)return;
  const rows=[...(state.productionRecords||[])].filter(r=>String(r.workOrder||'').trim()===key).sort((a,b)=>String(b.date||'').localeCompare(String(a.date||''))||String(b.updatedAt||'').localeCompare(String(a.updatedAt||'')));
  if(!rows.length){toast('Bu iş emrine ait geçmiş kayıt bulunamadı.');return}
  const st=statsOf(rows),gross=st.good+st.scrap,dates=rows.map(r=>r.date).filter(Boolean).sort(),machines=[...new Set(rows.map(r=>getById(state.machines,r.machineId)?.name).filter(Boolean))],shifts=[...new Set(rows.map(r=>getById(state.shifts,r.shiftId)?.name).filter(Boolean))],masters=[...new Set(rows.map(r=>getById(state.people,r.masterId)?.name).filter(Boolean))];
  $('recordWorkOrderHistoryTitle').textContent='İş Emri '+key;$('recordWorkOrderHistorySubtitle').textContent=`${fmtNum(rows.length)} kayıt • ${dates[0]||'-'} → ${dates.at(-1)||'-'}`;
  $('recordWorkOrderHistoryBody').innerHTML=`<div class="wo-history-kpis"><div class="wo-history-kpi"><span>Net Baskı</span><strong>${fmtNum(st.good)}</strong></div><div class="wo-history-kpi"><span>Brüt Baskı</span><strong>${fmtNum(gross)}</strong></div><div class="wo-history-kpi"><span>Fire</span><strong>${fmtNum(st.scrap)} / ${fmtPct(st.rate)}</strong></div><div class="wo-history-kpi"><span>Duruş</span><strong>${fmtNum(st.down)} dk</strong></div><div class="wo-history-kpi"><span>Kalıp</span><strong>${fmtNum(st.plates)}</strong></div><div class="wo-history-kpi"><span>Kayıt</span><strong>${fmtNum(rows.length)}</strong></div></div><div class="wo-history-meta"><strong>Makine:</strong> ${esc(machines.join(', ')||'-')} &nbsp; • &nbsp; <strong>Vardiya:</strong> ${esc(shifts.join(', ')||'-')} &nbsp; • &nbsp; <strong>Usta:</strong> ${esc(masters.join(', ')||'-')}</div><div class="wo-history-table-wrap"><table class="wo-history-table"><thead><tr><th>Tarih</th><th>Vardiya</th><th>Makine</th><th>Usta</th><th>Net</th><th>Kalıp</th><th>Fire</th><th>Fire %</th><th>Duruş</th><th>Renk</th><th>Lak/UV</th><th></th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.date||'-')}</td><td>${esc(getById(state.shifts,r.shiftId)?.name||'-')}</td><td>${esc(getById(state.machines,r.machineId)?.name||'-')}</td><td>${esc(getById(state.people,r.masterId)?.name||'-')}</td><td>${fmtNum(r.goodQty)}</td><td>${fmtNum(r.plateQty)}</td><td>${fmtNum(r.scrapQty)}</td><td>${fmtPct(scrapRate(r))}</td><td>${fmtNum(r.downtimeMin)} dk</td><td>${r.colors??'-'}</td><td>${r.uvLak===true?'UV':r.lak===true?'Lak':r.lak===false&&r.uvLak===false?'Yok':'-'}</td><td><button type="button" class="wo-history-edit" data-history-edit="${r.id}">Düzenle</button></td></tr>`).join('')}</tbody></table></div>`;
  qsa('[data-history-edit]',$('recordWorkOrderHistoryBody')).forEach(b=>b.onclick=()=>{const id=b.dataset.historyEdit;closeRecordWorkOrderHistory();editRecord(id)});$('recordWorkOrderHistoryModal').classList.remove('hidden');
}

'''+marker
if marker not in html: raise SystemExit('period marker not found')
html=html.replace(marker,wo_funcs,1)

# 8) Bind quick defaults and work-order history close buttons.
old="$ ('newRecordBtn')"
old="$('newRecordBtn').onclick=()=>openRecordModal(); $('recordForm').onsubmit=saveRecord; qsa('[data-close-modal]').forEach(x=>x.onclick=closeRecordModal); $('recMachine').onchange=autoSelectMaster; ['recGoodQty','recScrapQty'].forEach(id=>$(id).oninput=updateRecordCalc);"
new="$('newRecordBtn').onclick=()=>openRecordModal(); $('recordForm').onsubmit=saveRecord; qsa('[data-close-modal]').forEach(x=>x.onclick=closeRecordModal); $('recMachine').onchange=autoSelectMaster; $('recShift').onchange=autoSelectMaster; $('recMaster').onchange=updateRecordAutoDefaults; $('recDate').onchange=updateRecordAutoDefaults; ['recGoodQty','recScrapQty'].forEach(id=>$(id).oninput=updateRecordCalc); qsa('[data-close-record-workorder]').forEach(x=>x.onclick=closeRecordWorkOrderHistory);"
if old not in html: raise SystemExit('bind record marker not found')
html=html.replace(old,new,1)

# 9) Native PDF callback text. Android now creates the PDF file directly and opens Save As.
old_cb="function nativePrintStarted(){toast('Android yazdırma penceresi açıldı.');}\nfunction nativePrintFailed(message){alert('Android yazdırma servisi açılamadı.\\n\\n'+String(message||'Bilinmeyen hata'));}"
new_cb="function nativePrintPreparing(){toast('Renkli PDF oluşturuluyor...');}\nfunction nativePrintStarted(){toast('PDF hazırlandı. Kaydedilecek konumu seç.');}\nfunction nativePdfSaved(name){toast('PDF kaydedildi: '+String(name||'rapor.pdf'));}\nfunction nativePdfSaveCancelled(){toast('PDF kaydetme iptal edildi.');}\nfunction nativePrintFailed(message){alert('PDF oluşturulamadı.\\n\\n'+String(message||'Bilinmeyen hata'));}"
html=html.replace("function nativePrintPreparing(){toast('Yazdırma penceresi hazırlanıyor...');}\n",'')
if old_cb not in html: raise SystemExit('native print callbacks marker not found')
html=html.replace(old_cb,new_cb,1)

p.write_text(html,encoding='utf-8')
print('patched-v160',len(html))
