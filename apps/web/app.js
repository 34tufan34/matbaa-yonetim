const STORAGE_KEY = 'matbaa-os-v1';
const stages = ['Planlama','Malzeme','Baskı','Laminasyon','Kesim','Kalite','Paketleme','Sevkiyat'];
const stageProgress = {Planlama:8,Malzeme:18,Baskı:38,Laminasyon:55,Kesim:70,Kalite:84,Paketleme:93,Sevkiyat:98};
const statusLabels = {active:'Aktif',risk:'Riskli',done:'Tamamlandı',fault:'Arızalı',idle:'Bekliyor',maintenance:'Bakımda'};
const seed = {
  customers:[
    {id:1,company:'Atlas Ambalaj',contact:'Murat Kaya',phone:'0532 555 14 21',email:'satinalma@atlasambalaj.com'},
    {id:2,company:'Nova Kozmetik',contact:'Selin Aksoy',phone:'0544 206 88 12',email:'selin@novakozmetik.com'},
    {id:3,company:'Marmara Gıda',contact:'Burak Demir',phone:'0553 178 44 09',email:'operasyon@marmaragida.com'},
    {id:4,company:'Rota Tekstil',contact:'Elif Çetin',phone:'0506 344 17 63',email:'elif@rotatekstil.com'}
  ],
  materials:[
    {id:101,code:'KGT-350-BR',name:'350 gr Bristol 70x100',type:'Kağıt/Karton',stock:8400,minStock:3000,unit:'tabaka',supplier:'Marmara Kağıt'},
    {id:102,code:'KGT-300-KR',name:'300 gr Krome Karton 70x100',type:'Kağıt/Karton',stock:1850,minStock:2500,unit:'tabaka',supplier:'Anadolu Kağıt'},
    {id:103,code:'MUR-CMYK-K',name:'Process Black Ofset Mürekkep',type:'Mürekkep',stock:46,minStock:18,unit:'kg',supplier:'PrintChem'},
    {id:104,code:'LAK-UV-01',name:'Parlak UV Lak',type:'Lak',stock:12,minStock:15,unit:'kg',supplier:'Kimya Mat'},
    {id:105,code:'FILM-OPP-20',name:'20 mikron OPP Film',type:'Film',stock:28,minStock:10,unit:'rulo',supplier:'PackFilm'}
  ],
  orders:[
    {id:'ME-2026-0048',customer:'Atlas Ambalaj',product:'350 gr Bristol Kutu',jobType:'Karton Kutu',quantity:50000,stage:'Baskı',deadline:'2026-08-18',status:'risk',progress:48,note:'Pantone özel renk · baskı öncesi numune onayı alınacak',dimensions:'180 × 120 × 45 mm',colors:'4+0 CMYK + Pantone 186 C',materialId:101,materialQty:5200,machineId:1,createdAt:'2026-08-14'},
    {id:'ME-2026-0049',customer:'Nova Kozmetik',product:'Parfüm Kutusu',jobType:'Karton Kutu',quantity:22000,stage:'Kesim',deadline:'2026-08-20',status:'active',progress:72,note:'Kabartma klişe kontrolü',dimensions:'55 × 35 × 110 mm',colors:'4+0 CMYK',materialId:102,materialQty:2100,machineId:3,createdAt:'2026-08-13'},
    {id:'ME-2026-0050',customer:'Marmara Gıda',product:'Dondurma Kılıfı',jobType:'Ambalaj',quantity:80000,stage:'Laminasyon',deadline:'2026-08-22',status:'active',progress:56,note:'Gıda teması için onaylı film kullanılacak',dimensions:'240 × 160 mm',colors:'4+0 CMYK',materialId:105,materialQty:16,machineId:4,createdAt:'2026-08-15'},
    {id:'ME-2026-0051',customer:'Rota Tekstil',product:'Ürün Etiketi',jobType:'Etiket',quantity:120000,stage:'Planlama',deadline:'2026-08-25',status:'active',progress:14,note:'',dimensions:'80 × 45 mm',colors:'2+0',materialId:null,materialQty:0,machineId:null,createdAt:'2026-08-16'},
    {id:'ME-2026-0047',customer:'Nova Kozmetik',product:'Kampanya Broşürü',jobType:'Broşür',quantity:30000,stage:'Sevkiyat',deadline:'2026-08-16',status:'done',progress:100,note:'',dimensions:'A4',colors:'4+4 CMYK',materialId:null,materialQty:0,machineId:2,createdAt:'2026-08-10'}
  ],
  machines:[
    {id:1,name:'Heidelberg XL 106',department:'Baskı',status:'active',operator:'Ahmet Yılmaz',utilization:86,nextMaintenance:'38 saat'},
    {id:2,name:'Komori Lithrone G40',department:'Baskı',status:'active',operator:'Serkan Doğan',utilization:74,nextMaintenance:'92 saat'},
    {id:3,name:'Bobst Expertcut',department:'Kesim',status:'idle',operator:'Mehmet Can',utilization:62,nextMaintenance:'17 saat'},
    {id:4,name:'Lamina 1116',department:'Laminasyon',status:'maintenance',operator:'-',utilization:0,nextMaintenance:'Bakımda'},
    {id:5,name:'Polar 115',department:'Kesim',status:'active',operator:'Ali Öz',utilization:79,nextMaintenance:'54 saat'},
    {id:6,name:'Heidelberg SM 74',department:'Baskı',status:'fault',operator:'-',utilization:0,nextMaintenance:'Arıza kaydı açık'}
  ],
  production:{target:285000,produced:193500}
};
function cloneSeed(){return JSON.parse(JSON.stringify(seed));}
function migrate(raw){
  const base=cloneSeed();
  if(!raw||typeof raw!=='object') return base;
  raw.customers=Array.isArray(raw.customers)?raw.customers:base.customers;
  raw.machines=Array.isArray(raw.machines)?raw.machines:base.machines;
  raw.orders=Array.isArray(raw.orders)?raw.orders:base.orders;
  raw.materials=Array.isArray(raw.materials)?raw.materials:base.materials;
  raw.production=raw.production||base.production;
  raw.orders=raw.orders.map(o=>({jobType:'Diğer',dimensions:'',colors:'',materialId:null,materialQty:0,machineId:null,createdAt:new Date().toISOString().slice(0,10),...o,progress:Number(o.progress??stageProgress[o.stage]??5)}));
  return raw;
}
function loadState(){try{return migrate(JSON.parse(localStorage.getItem(STORAGE_KEY)));}catch{return cloneSeed();}}
let state=loadState();
function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state));}
function esc(value=''){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function fmt(n){return new Intl.NumberFormat('tr-TR',{maximumFractionDigits:2}).format(Number(n)||0)}
function dateFmt(s){if(!s)return '-';return new Date(s+'T12:00:00').toLocaleDateString('tr-TR',{day:'2-digit',month:'short',year:'numeric'});}
function statusBadge(status){return `<span class="badge ${status}">${statusLabels[status]||status}</span>`}
function materialById(id){return state.materials.find(m=>String(m.id)===String(id));}
function machineById(id){return state.machines.find(m=>String(m.id)===String(id));}
function isLow(m){return Number(m.stock)<=Number(m.minStock);}
function materialStatus(m){return isLow(m)?'<span class="badge risk">Kritik</span>':'<span class="badge active">Normal</span>';}
function renderAll(){renderDashboard();renderCustomers();renderOrders();renderProduction();renderInventory();renderMachines();syncOrderSelects();}
function renderDashboard(){
  const active=state.orders.filter(o=>o.status==='active').length;
  const risk=state.orders.filter(o=>o.status==='risk').length;
  const working=state.machines.filter(m=>m.status==='active').length;
  const lowStock=state.materials.filter(isLow).length;
  const kpis=[['Aktif İşler',active,'Üretimde veya planlamada','▤'],['Termin Riski',risk,'Yakın takip gerekli','!'],['Çalışan Makine',`${working}/${state.machines.length}`,'Anlık makine durumu','⚙'],['Kritik Stok',lowStock,lowStock?'Satın alma kontrolü':'Stoklar normal','▦']];
  document.getElementById('kpiGrid').innerHTML=kpis.map(k=>`<div class="kpi-card"><div><div class="kpi-label">${k[0]}</div><div class="kpi-value">${k[1]}</div><div class="kpi-note">${k[2]}</div></div><div class="kpi-icon">${k[3]}</div></div>`).join('');
  document.getElementById('dashboardOrders').innerHTML=state.orders.filter(o=>o.status!=='done').slice(0,5).map(o=>`<tr class="clickable-row" data-order-id="${esc(o.id)}"><td><span class="order-id">${esc(o.id)}</span></td><td>${esc(o.customer)}</td><td>${esc(o.product)}</td><td>${esc(o.stage)}</td><td>${dateFmt(o.deadline)}</td><td><div class="progress"><i style="width:${o.progress}%"></i></div><span class="subline">%${o.progress}</span></td></tr>`).join('');
  const alerts=[];
  state.machines.filter(m=>m.status==='fault').forEach(m=>alerts.push(['red',m.name,'Makine arızası açık']));
  state.orders.filter(o=>o.status==='risk').forEach(o=>alerts.push(['yellow',o.id,`${o.customer} · termin riski`]));
  state.materials.filter(isLow).forEach(m=>alerts.push(['yellow',m.name,`Kritik stok · ${fmt(m.stock)} ${m.unit}`]));
  state.machines.filter(m=>m.status==='maintenance').forEach(m=>alerts.push(['purple',m.name,'Planlı bakım devam ediyor']));
  document.getElementById('alertsList').innerHTML=(alerts.length?alerts:[['green','Kritik uyarı yok','Sistem normal çalışıyor']]).slice(0,6).map(a=>`<div class="alert-item"><i class="alert-dot" style="background:var(--${a[0]})"></i><div><strong>${esc(a[1])}</strong><span>${esc(a[2])}</span></div></div>`).join('');
  document.getElementById('machineStrip').innerHTML=state.machines.slice(0,4).map(m=>`<div class="machine-mini"><div class="machine-mini-top"><strong>${esc(m.name)}</strong><i class="status-light ${m.status}"></i></div><p>${esc(m.department)} · ${statusLabels[m.status]}</p></div>`).join('');
  const pct=Math.min(100,Math.round(state.production.produced/state.production.target*100));
  document.getElementById('targetPercent').textContent=pct+'%';
  document.getElementById('targetBar').style.width=pct+'%';
  document.getElementById('producedCount').textContent=fmt(state.production.produced);
  document.getElementById('targetCount').textContent=fmt(state.production.target);
}
function renderCustomers(query=''){
  const q=query.toLocaleLowerCase('tr');
  document.getElementById('customersTable').innerHTML=state.customers.filter(c=>`${c.company} ${c.contact}`.toLocaleLowerCase('tr').includes(q)).map(c=>{
    const jobs=state.orders.filter(o=>o.customer===c.company&&o.status!=='done').length;
    return `<tr><td><strong>${esc(c.company)}</strong></td><td>${esc(c.contact||'-')}</td><td>${esc(c.phone||'-')}</td><td>${esc(c.email||'-')}</td><td>${jobs}</td></tr>`;
  }).join('')||`<tr><td colspan="5" class="muted">Kayıt bulunamadı.</td></tr>`;
}
let orderFilter='all';
function renderOrders(){
  const items=state.orders.filter(o=>orderFilter==='all'||(orderFilter==='active'?o.status==='active':o.status===orderFilter));
  document.getElementById('ordersTable').innerHTML=items.map(o=>`<tr class="clickable-row" data-order-id="${esc(o.id)}"><td><span class="order-id">${esc(o.id)}</span></td><td>${esc(o.customer)}</td><td>${esc(o.product)}</td><td>${fmt(o.quantity)}</td><td>${esc(o.stage)}</td><td>${dateFmt(o.deadline)}</td><td>${statusBadge(o.status)}</td><td><div class="progress"><i style="width:${o.progress}%"></i></div><span class="subline">%${o.progress}</span></td></tr>`).join('')||`<tr><td colspan="8" class="muted">Bu filtrede iş emri bulunamadı.</td></tr>`;
}
function renderProduction(){
  document.getElementById('productionBoard').innerHTML=stages.map(stage=>{
    const jobs=state.orders.filter(o=>o.stage===stage&&o.status!=='done');
    return `<section class="stage-column"><div class="stage-head"><strong>${stage}</strong><span class="stage-count">${jobs.length} iş</span></div>${jobs.map(o=>`<article class="job-card clickable-card" data-order-id="${esc(o.id)}"><div class="job-card-top"><strong>${esc(o.id)}</strong>${o.status==='risk'?'<span class="mini-risk">RİSK</span>':''}</div><h3>${esc(o.product)}</h3><p>${esc(o.customer)}</p><div class="progress"><i style="width:${o.progress}%"></i></div><div class="job-meta"><span>${fmt(o.quantity)} adet</span><span>${dateFmt(o.deadline)}</span></div></article>`).join('')||'<div class="empty-stage">Bekleyen iş yok</div>'}</section>`;
  }).join('');
}
function renderInventory(query=''){
  const q=query.toLocaleLowerCase('tr');
  const low=state.materials.filter(isLow).length;
  const total=state.materials.length;
  const types=new Set(state.materials.map(m=>m.type)).size;
  document.getElementById('inventoryKpis').innerHTML=`<div class="inventory-kpi"><span>Toplam Kart</span><strong>${total}</strong></div><div class="inventory-kpi"><span>Kritik Stok</span><strong>${low}</strong></div><div class="inventory-kpi"><span>Malzeme Türü</span><strong>${types}</strong></div>`;
  document.getElementById('materialsTable').innerHTML=state.materials.filter(m=>`${m.code} ${m.name} ${m.type}`.toLocaleLowerCase('tr').includes(q)).map(m=>`<tr class="${isLow(m)?'low-row':''}"><td><span class="material-code">${esc(m.code)}</span></td><td><strong>${esc(m.name)}</strong></td><td>${esc(m.type)}</td><td>${fmt(m.stock)}</td><td>${fmt(m.minStock)}</td><td>${esc(m.unit)}</td><td>${esc(m.supplier||'-')}</td><td>${materialStatus(m)}</td></tr>`).join('')||`<tr><td colspan="8" class="muted">Malzeme bulunamadı.</td></tr>`;
}
function renderMachines(){
  document.getElementById('machineGrid').innerHTML=state.machines.map(m=>`<article class="machine-card"><div class="machine-card-head"><div><h3>${esc(m.name)}</h3><div class="dept">${esc(m.department)}</div></div>${statusBadge(m.status)}</div><div class="machine-stats"><div class="machine-stat"><span>Operatör</span><b>${esc(m.operator||'-')}</b></div><div class="machine-stat"><span>Kullanım</span><b>%${m.utilization||0}</b></div><div class="machine-stat" style="grid-column:1/-1"><span>Bakım / Durum</span><b>${esc(m.nextMaintenance||'-')}</b></div></div></article>`).join('');
}
function syncOrderSelects(){
  const customer=document.getElementById('orderCustomer');
  customer.innerHTML='<option value="">Müşteri seçin</option>'+state.customers.map(c=>`<option>${esc(c.company)}</option>`).join('');
  const material=document.getElementById('orderMaterial');
  material.innerHTML='<option value="">Malzeme seçilmedi</option>'+state.materials.map(m=>`<option value="${m.id}">${esc(m.code)} · ${esc(m.name)} (${fmt(m.stock)} ${esc(m.unit)})</option>`).join('');
  const machine=document.getElementById('orderMachine');
  machine.innerHTML='<option value="">Henüz atanmadı</option>'+state.machines.map(m=>`<option value="${m.id}">${esc(m.name)} · ${esc(m.department)}</option>`).join('');
}
function showPage(page){
  document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id===`page-${page}`));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.page===page));
  const titles={dashboard:'Komuta Merkezi',customers:'Müşteriler',orders:'İş Emirleri',production:'Üretim',inventory:'Stok & Malzeme',machines:'Makineler'};
  document.getElementById('pageTitle').textContent=titles[page]||'Matbaa OS';
  document.getElementById('sidebar').classList.remove('open');
}
function openModal(id){document.getElementById(id)?.classList.add('open');document.getElementById(id)?.setAttribute('aria-hidden','false')}
function closeModals(){document.querySelectorAll('.modal').forEach(m=>{m.classList.remove('open');m.setAttribute('aria-hidden','true')})}
function toast(msg){const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),2200)}
function nextOrderId(){const year=new Date().getFullYear();const nums=state.orders.map(o=>Number(o.id.split('-').pop())||0);return `ME-${year}-${String(Math.max(...nums,0)+1).padStart(4,'0')}`;}
function openJobDetail(id){
  const o=state.orders.find(x=>x.id===id); if(!o)return;
  const material=materialById(o.materialId); const machine=machineById(o.machineId);
  const materialEnough=!material||!o.materialQty||Number(material.stock)>=Number(o.materialQty);
  document.getElementById('detailTitle').textContent=o.id;
  document.getElementById('detailSubtitle').textContent=`${o.customer} · ${o.product}`;
  const timeline=stages.map((s,i)=>{const current=stages.indexOf(o.stage);const cls=o.status==='done'||i<current?'done':i===current?'current':'';return `<div class="timeline-step ${cls}"><i>${o.status==='done'||i<current?'✓':i+1}</i><span>${s}</span></div>`}).join('');
  document.getElementById('jobDetailBody').innerHTML=`
    <div class="detail-wrap">
      <div class="detail-status-row">${statusBadge(o.status)}<span class="detail-progress">İlerleme <b>%${o.progress}</b></span></div>
      <div class="job-timeline">${timeline}</div>
      <div class="detail-grid">
        <section class="detail-panel"><h3>İş Bilgileri</h3><dl><div><dt>İş Türü</dt><dd>${esc(o.jobType||'-')}</dd></div><div><dt>Miktar</dt><dd>${fmt(o.quantity)} adet</dd></div><div><dt>Ebat</dt><dd>${esc(o.dimensions||'-')}</dd></div><div><dt>Renk</dt><dd>${esc(o.colors||'-')}</dd></div><div><dt>Termin</dt><dd>${dateFmt(o.deadline)}</dd></div><div><dt>Makine</dt><dd>${esc(machine?.name||'Atanmadı')}</dd></div></dl></section>
        <section class="detail-panel"><h3>Malzeme Kontrolü</h3>${material?`<div class="material-check ${materialEnough?'enough':'short'}"><div><span>${esc(material.code)}</span><strong>${esc(material.name)}</strong></div><b>${materialEnough?'YETERLİ':'EKSİK'}</b></div><dl><div><dt>Gerekli</dt><dd>${fmt(o.materialQty)} ${esc(material.unit)}</dd></div><div><dt>Stok</dt><dd>${fmt(material.stock)} ${esc(material.unit)}</dd></div><div><dt>Minimum</dt><dd>${fmt(material.minStock)} ${esc(material.unit)}</dd></div></dl>`:'<div class="empty-info">Bu iş için ana malzeme henüz seçilmedi.</div>'}</section>
        <section class="detail-panel full-detail"><h3>Üretim / Kalite Talimatı</h3><p class="detail-note">${esc(o.note||'Özel talimat bulunmuyor.')}</p></section>
      </div>
      <div class="detail-actions"><button class="secondary-btn" data-detail-close>Kapat</button>${o.status!=='done'?`<button class="secondary-btn" data-toggle-risk="${esc(o.id)}">${o.status==='risk'?'Riski Kaldır':'Riskli İşaretle'}</button><button class="primary-btn" data-advance-order="${esc(o.id)}">${o.stage==='Sevkiyat'?'İşi Tamamla':'Sonraki Aşamaya Geç →'}</button>`:''}</div>
    </div>`;
  openModal('jobDetailModal');
}
function advanceOrder(id){
  const o=state.orders.find(x=>x.id===id); if(!o)return;
  const idx=stages.indexOf(o.stage);
  if(idx===stages.length-1){o.status='done';o.progress=100;toast(`${o.id} tamamlandı`);}else{o.stage=stages[idx+1];o.progress=stageProgress[o.stage]||o.progress;toast(`${o.id} → ${o.stage}`);}
  save();renderAll();openJobDetail(id);
}
function toggleRisk(id){const o=state.orders.find(x=>x.id===id);if(!o||o.status==='done')return;o.status=o.status==='risk'?'active':'risk';save();renderAll();openJobDetail(id);}
window.addEventListener('DOMContentLoaded',()=>{
  save();renderAll();
  document.querySelectorAll('.nav-item').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.page)));
  document.querySelectorAll('[data-goto]').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.goto)));
  document.querySelectorAll('[data-open]').forEach(b=>b.addEventListener('click',()=>openModal(b.dataset.open)));
  document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',closeModals));
  document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',e=>{if(e.target===m)closeModals()}));
  document.getElementById('menuBtn').addEventListener('click',()=>document.getElementById('sidebar').classList.toggle('open'));
  document.getElementById('customerSearch').addEventListener('input',e=>renderCustomers(e.target.value));
  document.getElementById('materialSearch').addEventListener('input',e=>renderInventory(e.target.value));
  document.querySelectorAll('[data-order-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-order-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');orderFilter=b.dataset.orderFilter;renderOrders()}));
  document.addEventListener('click',e=>{
    const orderTarget=e.target.closest('[data-order-id]'); if(orderTarget)openJobDetail(orderTarget.dataset.orderId);
    const advance=e.target.closest('[data-advance-order]'); if(advance){e.stopPropagation();advanceOrder(advance.dataset.advanceOrder);}
    const risk=e.target.closest('[data-toggle-risk]'); if(risk){e.stopPropagation();toggleRisk(risk.dataset.toggleRisk);}
    if(e.target.closest('[data-detail-close]'))closeModals();
  });
  document.getElementById('customerForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));state.customers.push({id:Date.now(),...d});save();renderAll();e.target.reset();closeModals();toast('Müşteri kaydedildi');});
  document.getElementById('materialForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));state.materials.push({id:Date.now(),code:d.code.trim().toUpperCase(),name:d.name,type:d.type,stock:Number(d.stock),minStock:Number(d.minStock),unit:d.unit,supplier:d.supplier});save();renderAll();e.target.reset();closeModals();toast('Malzeme kartı kaydedildi');});
  document.getElementById('orderForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));const stage=d.stage||'Planlama';state.orders.unshift({id:nextOrderId(),customer:d.customer,product:d.product,jobType:d.jobType,quantity:Number(d.quantity),dimensions:d.dimensions,colors:d.colors,deadline:d.deadline,stage,status:d.priority==='risk'?'risk':'active',progress:stageProgress[stage]||5,note:d.note,materialId:d.materialId?Number(d.materialId):null,materialQty:Number(d.materialQty)||0,machineId:d.machineId?Number(d.machineId):null,createdAt:new Date().toISOString().slice(0,10)});save();renderAll();e.target.reset();closeModals();toast('İş emri oluşturuldu');});
  document.getElementById('machineForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));state.machines.push({id:Date.now(),...d,utilization:d.status==='active'?50:0,nextMaintenance:'Henüz planlanmadı'});save();renderAll();e.target.reset();closeModals();toast('Makine eklendi');});
  const tick=()=>{const now=new Date();document.getElementById('liveClock').innerHTML=`<strong>${now.toLocaleTimeString('tr-TR',{hour:'2-digit',minute:'2-digit'})}</strong><br>${now.toLocaleDateString('tr-TR',{weekday:'short',day:'2-digit',month:'short'})}`};tick();setInterval(tick,30000);
});
