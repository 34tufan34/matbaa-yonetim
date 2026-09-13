from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.5-machine-failures' in html:
    raise SystemExit('already patched')

html=html.replace("const DB_VERSION = 2;", "const DB_VERSION = 3;", 1)
html=html.replace("const STORES = ['people','machines','shifts','scrapReasons','downtimeReasons','productionRecords','settings','meta','auditLogs','recycleBin'];", "const STORES = ['people','machines','shifts','scrapReasons','downtimeReasons','productionRecords','machineFailures','settings','meta','auditLogs','recycleBin'];", 1)
html=html.replace("let state = { people:[], machines:[], shifts:[], scrapReasons:[], downtimeReasons:[], productionRecords:[], auditLogs:[], recycleBin:[], settings:{}, meta:{} };", "let state = { people:[], machines:[], shifts:[], scrapReasons:[], downtimeReasons:[], productionRecords:[], machineFailures:[], auditLogs:[], recycleBin:[], settings:{}, meta:{} };", 1)

old='<button class="nav-btn" data-page="records">Üretim Kayıtları</button>\n        <button class="nav-btn" data-page="reports">Rapor Merkezi</button>'
new='<button class="nav-btn" data-page="records">Üretim Kayıtları</button>\n        <button class="nav-btn" data-page="failures">Makine Arızaları</button>\n        <button class="nav-btn" data-page="reports">Rapor Merkezi</button>'
if old not in html: raise SystemExit('nav anchor missing')
html=html.replace(old,new,1)

anchor='      <section id="reports" class="page">'
if anchor not in html: raise SystemExit('reports anchor missing')
page=r'''      <section id="failures" class="page">
        <div class="panel failure-shell">
          <div class="panel-head">
            <div><div class="eyebrow">BAKIM & ARIZA TAKİBİ</div><h2>Makine Arızaları</h2><p>Arızayı kaydet, müdahaleyi takip et ve kapanış süresini makine bazında izle.</p></div>
            <button id="newFailureBtn" class="btn primary" type="button">+ Yeni Arıza</button>
          </div>
          <div id="failureSummary" class="failure-summary-grid"></div>
          <div class="filter-row failure-filters">
            <select id="failureMachineFilter"></select>
            <select id="failureStatusFilter"><option value="all">Tüm durumlar</option><option value="open">Açık</option><option value="working">Müdahalede</option><option value="waiting">Beklemede</option><option value="resolved">Çözüldü</option></select>
            <select id="failureSeverityFilter"><option value="all">Tüm önem seviyeleri</option><option value="low">Düşük</option><option value="medium">Orta</option><option value="high">Yüksek</option><option value="critical">Kritik</option></select>
            <input id="failureSearch" type="search" placeholder="Arıza / sorumlu / açıklama ara" />
            <button id="failureFilterBtn" class="btn ghost" type="button">Filtrele</button>
          </div>
          <div id="failureList" class="failure-list"></div>
        </div>
      </section>

'''
html=html.replace(anchor,page+anchor,1)

modal_anchor='  <div id="pdfReportModal" class="modal hidden">'
if modal_anchor not in html: raise SystemExit('modal anchor missing')
modal=r'''  <div id="failureModal" class="modal hidden failure-modal">
    <div class="modal-backdrop" data-close-failure></div>
    <div class="modal-card failure-modal-card">
      <div class="modal-head"><div><div class="eyebrow">MAKİNE ARIZA KAYDI</div><h2 id="failureModalTitle">Yeni Arıza</h2><p>Arızanın başlangıcı, müdahale süreci ve çözüm bilgisini tek kayıtta tut.</p></div><button class="icon-btn" type="button" data-close-failure>×</button></div>
      <form id="failureForm" class="failure-form">
        <input type="hidden" id="failureId" />
        <div class="form-grid three">
          <label><span>Makine *</span><select id="failureMachine" required></select></label>
          <label><span>Tarih *</span><input type="date" id="failureDate" required /></label>
          <label><span>Saat</span><input type="time" id="failureTime" /></label>
          <label><span>Kategori</span><select id="failureCategory"><option>Mekanik</option><option>Elektrik</option><option>Elektronik</option><option>Baskı / Proses</option><option>Pnömatik</option><option>Su / Nemlendirme</option><option>Yazılım / Otomasyon</option><option>Diğer</option></select></label>
          <label><span>Önem</span><select id="failureSeverity"><option value="low">Düşük</option><option value="medium" selected>Orta</option><option value="high">Yüksek</option><option value="critical">Kritik</option></select></label>
          <label><span>Durum</span><select id="failureStatus"><option value="open">Açık</option><option value="working">Müdahalede</option><option value="waiting">Beklemede</option><option value="resolved">Çözüldü</option></select></label>
          <label><span>Sorumlu / Teknik Servis</span><input type="text" id="failureResponsible" placeholder="İsim / servis" /></label>
          <label><span>Duruş Süresi (dk)</span><input type="number" id="failureDowntime" min="0" step="1" value="0" /></label>
          <label><span>Çözüm Tarihi</span><input type="date" id="failureResolvedDate" /></label>
        </div>
        <label class="field-full"><span>Arıza Açıklaması *</span><textarea id="failureDescription" rows="3" required placeholder="Belirti, arıza noktası, ilk gözlem..."></textarea></label>
        <label class="field-full"><span>Yapılan Müdahale / Çözüm</span><textarea id="failureAction" rows="3" placeholder="Değişen parça, yapılan ayar, servis işlemi..."></textarea></label>
        <label class="field-full"><span>Not</span><textarea id="failureNote" rows="2" placeholder="Tekrar kontrol tarihi, parça bekleniyor vb."></textarea></label>
        <div class="modal-actions"><button type="button" class="btn ghost" data-close-failure>Vazgeç</button><button type="submit" class="btn primary">Arıza Kaydını Kaydet</button></div>
      </form>
    </div>
  </div>

'''
html=html.replace(modal_anchor,modal+modal_anchor,1)

css=r'''
/* v1.8.5-machine-failures */
.failure-summary-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:14px 0}.failure-summary-card{border:1px solid var(--line);border-radius:13px;padding:13px;background:linear-gradient(160deg,var(--panel2),var(--panel))}.failure-summary-card span{display:block;color:var(--muted);font-size:8px;font-weight:800;letter-spacing:.7px;text-transform:uppercase}.failure-summary-card strong{display:block;font-size:21px;margin-top:7px}.failure-summary-card small{display:block;color:var(--muted);font-size:8px;margin-top:5px}.failure-summary-card.bad strong{color:var(--bad)}.failure-summary-card.warn strong{color:var(--warn)}.failure-summary-card.good strong{color:var(--good)}
.failure-list{display:grid;gap:9px;margin-top:12px}.failure-card{display:grid;grid-template-columns:150px 1fr auto;gap:14px;align-items:start;border:1px solid var(--line);border-radius:14px;background:linear-gradient(160deg,color-mix(in srgb,var(--panel2) 96%,transparent),var(--panel));padding:13px}.failure-card.critical{border-color:color-mix(in srgb,var(--bad) 55%,var(--line))}.failure-card.high{border-color:color-mix(in srgb,var(--warn) 45%,var(--line))}.failure-machine strong{display:block;font-size:16px}.failure-machine span{display:block;color:var(--muted);font-size:9px;margin-top:4px}.failure-body h4{font-size:12px;margin:0 0 5px}.failure-body p{color:var(--muted);font-size:9px;line-height:1.5;margin:0}.failure-meta{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}.failure-chip{font-size:8px;padding:4px 7px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}.failure-chip.open{color:var(--bad);border-color:color-mix(in srgb,var(--bad) 40%,var(--line))}.failure-chip.working{color:var(--warn);border-color:color-mix(in srgb,var(--warn) 40%,var(--line))}.failure-chip.resolved{color:var(--good);border-color:color-mix(in srgb,var(--good) 40%,var(--line))}.failure-actions{display:flex;flex-direction:column;gap:6px;min-width:112px}.failure-actions button{padding:7px 9px;font-size:8px}.failure-empty{padding:26px;text-align:center;border:1px dashed var(--line);border-radius:14px;color:var(--muted)}.failure-modal-card{width:min(900px,96vw)}.failure-form{display:grid;gap:12px}.failure-form .form-grid.three{grid-template-columns:repeat(3,1fr)}.failure-form label{display:grid;gap:5px}.failure-form label span{font-size:9px;color:var(--muted);font-weight:750}.failure-form input,.failure-form select,.failure-form textarea{width:100%}.field-full{grid-column:1/-1}.modal-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:4px}
@media(max-width:900px){.failure-summary-grid{grid-template-columns:repeat(2,1fr)}.failure-card{grid-template-columns:1fr}.failure-actions{flex-direction:row;flex-wrap:wrap}.failure-form .form-grid.three{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.failure-form .form-grid.three{grid-template-columns:1fr}.failure-summary-grid{grid-template-columns:1fr 1fr}}
'''
html=html.replace('</style>',css+'</style>',1)

old_titles="const titles={dashboard:['Komuta Paneli','Makine ve vardiya bazlı hızlı üretim girişi'],records:['Üretim Kayıtları','Kayıtları kontrol et ve düzelt'],reports:['Rapor Merkezi','Günlükten tüm zamanlara performans analizi'],masterdata:['Ayarlar • Merkez Tanımlar','Personel, makine, vardiya, neden ve mesai tanımları'],backup:['Ayarlar','Tema, merkez tanımlar, yedekleme ve sistem yönetimi']};"
new_titles="const titles={dashboard:['Komuta Paneli','Makine ve vardiya bazlı hızlı üretim girişi'],records:['Üretim Kayıtları','Kayıtları kontrol et ve düzelt'],failures:['Makine Arızaları','Arıza kaydı, müdahale ve çözüm takibi'],reports:['Rapor Merkezi','Günlükten tüm zamanlara performans analizi'],masterdata:['Ayarlar • Merkez Tanımlar','Personel, makine, vardiya, neden ve mesai tanımları'],backup:['Ayarlar','Tema, merkez tanımlar, yedekleme ve sistem yönetimi']};"
if old_titles not in html: raise SystemExit('titles anchor missing')
html=html.replace(old_titles,new_titles,1)
html=html.replace("  if(page==='records') renderRecords();\n  if(page==='reports') runReport();", "  if(page==='records') renderRecords();\n  if(page==='failures') renderMachineFailures();\n  if(page==='reports') runReport();",1)

pop="  setSelectOptions('recordMachineFilter',optionList(state.machines,'Tüm makineler'));"
if pop not in html: raise SystemExit('populate anchor missing')
html=html.replace(pop,pop+"\n  if($('failureMachineFilter'))setSelectOptions('failureMachineFilter',optionList(state.machines,'Tüm makineler'));\n  if($('failureMachine'))setSelectOptions('failureMachine',optionList(state.machines,'Makine seç'));",1)

bind='function bindEvents(){'
if bind not in html: raise SystemExit('bind anchor missing')
js=r'''
function failureStatusLabelV185(v){return ({open:'Açık',working:'Müdahalede',waiting:'Beklemede',resolved:'Çözüldü'})[v]||v||'Açık'}
function failureSeverityLabelV185(v){return ({low:'Düşük',medium:'Orta',high:'Yüksek',critical:'Kritik'})[v]||v||'Orta'}
function failureDateTimeV185(r){return [r.date||'-',r.time||''].filter(Boolean).join(' • ')}
function renderMachineFailures(){populateSelects();const machine=$('failureMachineFilter')?.value||'',status=$('failureStatusFilter')?.value||'all',severity=$('failureSeverityFilter')?.value||'all',q=String($('failureSearch')?.value||'').trim().toLocaleUpperCase('tr-TR');const all=[...(state.machineFailures||[])];const rows=all.filter(r=>(!machine||r.machineId===machine)&&(status==='all'||r.status===status)&&(severity==='all'||r.severity===severity)&&(!q||[r.description,r.responsible,r.action,r.note,getById(state.machines,r.machineId)?.name].some(x=>String(x||'').toLocaleUpperCase('tr-TR').includes(q)))).sort((a,b)=>String(b.date||'').localeCompare(String(a.date||''))||String(b.time||'').localeCompare(String(a.time||'')));const open=all.filter(r=>r.status==='open').length,working=all.filter(r=>r.status==='working'||r.status==='waiting').length,resolved=all.filter(r=>r.status==='resolved').length,down=all.reduce((a,r)=>a+Number(r.downtimeMin||0),0);if($('failureSummary'))$('failureSummary').innerHTML=`<div class="failure-summary-card"><span>Toplam Arıza</span><strong>${fmtNum(all.length)}</strong><small>Tüm kayıtlar</small></div><div class="failure-summary-card bad"><span>Açık</span><strong>${fmtNum(open)}</strong><small>Aksiyon bekliyor</small></div><div class="failure-summary-card warn"><span>Müdahalede / Beklemede</span><strong>${fmtNum(working)}</strong><small>Devam eden kayıt</small></div><div class="failure-summary-card good"><span>Çözüldü</span><strong>${fmtNum(resolved)}</strong><small>Kapanan kayıt</small></div><div class="failure-summary-card"><span>Toplam Arıza Duruşu</span><strong>${fmtNum(down)} dk</strong><small>Kayıtlı süre</small></div>`;if(!$('failureList'))return;if(!rows.length){$('failureList').innerHTML='<div class="failure-empty">Seçili filtrelerde arıza kaydı yok.</div>';return;}$('failureList').innerHTML=rows.map(r=>{const m=getById(state.machines,r.machineId)?.name||'Makine';return `<div class="failure-card ${r.severity||'medium'}"><div class="failure-machine"><strong>${esc(m)}</strong><span>${esc(failureDateTimeV185(r))}</span><div class="failure-meta"><span class="failure-chip ${r.status||'open'}">${failureStatusLabelV185(r.status)}</span><span class="failure-chip">${failureSeverityLabelV185(r.severity)}</span><span class="failure-chip">${esc(r.category||'Diğer')}</span></div></div><div class="failure-body"><h4>${esc(r.description||'Arıza açıklaması')}</h4><p>${r.responsible?`Sorumlu/Servis: ${esc(r.responsible)} • `:''}${Number(r.downtimeMin||0)?`Duruş: ${fmtNum(Number(r.downtimeMin||0))} dk • `:''}${r.action?`Müdahale: ${esc(r.action)}`:'Müdahale bilgisi henüz girilmedi.'}</p>${r.note?`<p style="margin-top:5px">Not: ${esc(r.note)}</p>`:''}</div><div class="failure-actions"><button class="btn ghost" type="button" data-failure-edit="${r.id}">Düzenle</button>${r.status!=='working'&&r.status!=='resolved'?`<button class="btn ghost" type="button" data-failure-working="${r.id}">Müdahalede</button>`:''}${r.status!=='resolved'?`<button class="btn ghost" type="button" data-failure-resolve="${r.id}">Çözüldü</button>`:''}<button class="btn ghost" type="button" data-failure-delete="${r.id}">Sil</button></div></div>`}).join('');qsa('[data-failure-edit]').forEach(b=>b.onclick=()=>openFailureModalV185(b.dataset.failureEdit));qsa('[data-failure-working]').forEach(b=>b.onclick=()=>setFailureStatusV185(b.dataset.failureWorking,'working'));qsa('[data-failure-resolve]').forEach(b=>b.onclick=()=>setFailureStatusV185(b.dataset.failureResolve,'resolved'));qsa('[data-failure-delete]').forEach(b=>b.onclick=()=>deleteFailureV185(b.dataset.failureDelete));}
function openFailureModalV185(id=''){populateSelects();const r=(state.machineFailures||[]).find(x=>x.id===id)||null;$('failureId').value=r?.id||'';$('failureMachine').value=r?.machineId||'';$('failureDate').value=r?.date||todayISO();$('failureTime').value=r?.time||new Date().toTimeString().slice(0,5);$('failureCategory').value=r?.category||'Mekanik';$('failureSeverity').value=r?.severity||'medium';$('failureStatus').value=r?.status||'open';$('failureResponsible').value=r?.responsible||'';$('failureDowntime').value=Number(r?.downtimeMin||0);$('failureResolvedDate').value=r?.resolvedDate||'';$('failureDescription').value=r?.description||'';$('failureAction').value=r?.action||'';$('failureNote').value=r?.note||'';if($('failureModalTitle'))$('failureModalTitle').textContent=r?'Arıza Kaydını Düzenle':'Yeni Arıza';$('failureModal').classList.remove('hidden');}
function closeFailureModalV185(){if($('failureModal'))$('failureModal').classList.add('hidden')}
async function saveFailureV185(e){e?.preventDefault();const id=$('failureId').value||uid(),old=(state.machineFailures||[]).find(x=>x.id===id),status=$('failureStatus').value||'open';const row={...(old||{}),id,machineId:$('failureMachine').value,date:$('failureDate').value,time:$('failureTime').value||'',category:$('failureCategory').value||'Diğer',severity:$('failureSeverity').value||'medium',status,responsible:$('failureResponsible').value.trim(),downtimeMin:Number($('failureDowntime').value||0),resolvedDate:$('failureResolvedDate').value||((status==='resolved')?todayISO():''),description:$('failureDescription').value.trim(),action:$('failureAction').value.trim(),note:$('failureNote').value.trim(),createdAt:old?.createdAt||new Date().toISOString(),updatedAt:new Date().toISOString()};if(!row.machineId||!row.date||!row.description){toast('Makine, tarih ve arıza açıklaması zorunlu.');return}await dbPut('machineFailures',row);state.machineFailures=await dbGetAll('machineFailures');closeFailureModalV185();renderMachineFailures();toast(old?'Arıza kaydı güncellendi.':'Arıza kaydı oluşturuldu.');}
async function setFailureStatusV185(id,status){const r=(state.machineFailures||[]).find(x=>x.id===id);if(!r)return;const next={...r,status,updatedAt:new Date().toISOString()};if(status==='resolved'&&!next.resolvedDate)next.resolvedDate=todayISO();await dbPut('machineFailures',next);state.machineFailures=await dbGetAll('machineFailures');renderMachineFailures();}
async function deleteFailureV185(id){if(!confirm('Bu arıza kaydı silinsin mi?'))return;await dbDelete('machineFailures',id);state.machineFailures=await dbGetAll('machineFailures');renderMachineFailures();toast('Arıza kaydı silindi.');}

'''
html=html.replace(bind,js+bind,1)
line="  qsa('.nav-btn').forEach(b=>b.onclick=()=>navTo(b.dataset.page));"
if line not in html: raise SystemExit('bind nav missing')
extra=" if($('newFailureBtn'))$('newFailureBtn').onclick=()=>openFailureModalV185(); if($('failureForm'))$('failureForm').onsubmit=saveFailureV185; qsa('[data-close-failure]').forEach(x=>x.onclick=closeFailureModalV185); if($('failureFilterBtn'))$('failureFilterBtn').onclick=renderMachineFailures; ['failureMachineFilter','failureStatusFilter','failureSeverityFilter'].forEach(id=>{if($(id))$(id).onchange=renderMachineFailures;}); if($('failureSearch'))$('failureSearch').oninput=()=>{clearTimeout(bindEvents.fs);bindEvents.fs=setTimeout(renderMachineFailures,220)};"
html=html.replace(line,line+extra,1)

p.write_text(html,encoding='utf-8')
print('v1.8.5 machine failures patch applied')
