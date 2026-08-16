const STORAGE_KEY = 'matbaa-os-v1';
const stages = ['Planlama','Malzeme','Baskı','Laminasyon','Kesim','Kalite','Paketleme','Sevkiyat'];
const statusLabels = {active:'Aktif',risk:'Riskli',done:'Tamamlandı',fault:'Arızalı',idle:'Bekliyor',maintenance:'Bakımda'};
const seed = {
  customers:[
    {id:1,company:'Atlas Ambalaj',contact:'Murat Kaya',phone:'0532 555 14 21',email:'satinalma@atlasambalaj.com'},
    {id:2,company:'Nova Kozmetik',contact:'Selin Aksoy',phone:'0544 206 88 12',email:'selin@novakozmetik.com'},
    {id:3,company:'Marmara Gıda',contact:'Burak Demir',phone:'0553 178 44 09',email:'operasyon@marmaragida.com'},
    {id:4,company:'Rota Tekstil',contact:'Elif Çetin',phone:'0506 344 17 63',email:'elif@rotatekstil.com'}
  ],
  orders:[
    {id:'ME-2026-0048',customer:'Atlas Ambalaj',product:'350 gr Bristol Kutu',quantity:50000,stage:'Baskı',deadline:'2026-08-18',status:'risk',progress:48,note:'Pantone özel renk'},
    {id:'ME-2026-0049',customer:'Nova Kozmetik',product:'Parfüm Kutusu',quantity:22000,stage:'Kesim',deadline:'2026-08-20',status:'active',progress:72,note:''},
    {id:'ME-2026-0050',customer:'Marmara Gıda',product:'Dondurma Kılıfı',quantity:80000,stage:'Laminasyon',deadline:'2026-08-22',status:'active',progress:56,note:''},
    {id:'ME-2026-0051',customer:'Rota Tekstil',product:'Ürün Etiketi',quantity:120000,stage:'Planlama',deadline:'2026-08-25',status:'active',progress:14,note:''},
    {id:'ME-2026-0047',customer:'Nova Kozmetik',product:'Kampanya Broşürü',quantity:30000,stage:'Sevkiyat',deadline:'2026-08-16',status:'done',progress:100,note:''}
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
function loadState(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY))||cloneSeed();}catch{return cloneSeed();}}
let state=loadState();
function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state));}
function esc(value=''){return String(value).replace(/[&<>'\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','\"':'&quot;'}[c]));}
function fmt(n){return new Intl.NumberFormat('tr-TR').format(n)}
function dateFmt(s){return new Date(s+'T12:00:00').toLocaleDateString('tr-TR',{day:'2-digit',month:'short'});}
function statusBadge(status){return `<span class="badge ${status}">${statusLabels[status]||status}</span>`}
function renderAll(){renderDashboard();renderCustomers();renderOrders();renderProduction();renderMachines();syncOrderCustomers();}
function renderDashboard(){
  const active=state.orders.filter(o=>o.status==='active').length;
  const risk=state.orders.filter(o=>o.status==='risk').length;
  const working=state.machines.filter(m=>m.status==='active').length;
  const faults=state.machines.filter(m=>m.status==='fault').length;
  const kpis=[['Aktif İşler',active,'Üretimde veya planlamada','▤'],['Termin Riski',risk,'Yakın takip gerekli','!'],['Çalışan Makine',`${working}/${state.machines.length}`,'Anlık makine durumu','⚙'],['Açık Arıza',faults,faults?'Müdahale gerekli':'Kritik arıza yok','⚠']];
  document.getElementById('kpiGrid').innerHTML=kpis.map(k=>`<div class="kpi-card"><div><div class="kpi-label">${k[0]}</div><div class="kpi-value">${k[1]}</div><div class="kpi-note">${k[2]}</div></div><div class="kpi-icon">${k[3]}</div></div>`).join('');
  document.getElementById('dashboardOrders').innerHTML=state.orders.filter(o=>o.status!=='done').slice(0,5).map(o=>`<tr><td><span class="order-id">${esc(o.id)}</span></td><td>${esc(o.customer)}</td><td>${esc(o.product)}</td><td>${esc(o.stage)}</td><td>${dateFmt(o.deadline)}</td><td><div class="progress"><i style="width:${o.progress}%"></i></div><span class="subline">%${o.progress}</span></td></tr>`).join('');
  const alerts=[];
  state.machines.filter(m=>m.status==='fault').forEach(m=>alerts.push(['red',m.name,'Makine arızası açık']));
  state.orders.filter(o=>o.status==='risk').forEach(o=>alerts.push(['yellow',o.id,`${o.customer} · termin riski`]));
  state.machines.filter(m=>m.status==='maintenance').forEach(m=>alerts.push(['purple',m.name,'Planlı bakım devam ediyor']));
  document.getElementById('alertsList').innerHTML=(alerts.length?alerts:[['green','Kritik uyarı yok','Sistem normal çalışıyor']]).map(a=>`<div class="alert-item"><i class="alert-dot" style="background:var(--${a[0]})"></i><div><strong>${esc(a[1])}</strong><span>${esc(a[2])}</span></div></div>`).join('');
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
  document.getElementById('ordersTable').innerHTML=items.map(o=>`<tr><td><span class="order-id">${esc(o.id)}</span></td><td>${esc(o.customer)}</td><td>${esc(o.product)}</td><td>${fmt(o.quantity)}</td><td>${esc(o.stage)}</td><td>${dateFmt(o.deadline)}</td><td>${statusBadge(o.status)}</td><td><div class="progress"><i style="width:${o.progress}%"></i></div><span class="subline">%${o.progress}</span></td></tr>`).join('')||`<tr><td colspan="8" class="muted">Bu filtrede iş emri bulunamadı.</td></tr>`;
}
function renderProduction(){
  document.getElementById('productionBoard').innerHTML=stages.map(stage=>{
    const jobs=state.orders.filter(o=>o.stage===stage&&o.status!=='done');
    return `<section class="stage-column"><div class="stage-head"><strong>${stage}</strong><span class="stage-count">${jobs.length} iş</span></div>${jobs.map(o=>`<article class="job-card"><strong>${esc(o.id)}</strong><h3>${esc(o.product)}</h3><p>${esc(o.customer)}</p><div class="progress"><i style="width:${o.progress}%"></i></div><div class="job-meta"><span>${fmt(o.quantity)} adet</span><span>${dateFmt(o.deadline)}</span></div></article>`).join('')||'<div style="padding:16px;color:#5f7189;font-size:10px">Bekleyen iş yok</div>'}</section>`;
  }).join('');
}
function renderMachines(){
  document.getElementById('machineGrid').innerHTML=state.machines.map(m=>`<article class="machine-card"><div class="machine-card-head"><div><h3>${esc(m.name)}</h3><div class="dept">${esc(m.department)}</div></div>${statusBadge(m.status)}</div><div class="machine-stats"><div class="machine-stat"><span>Operatör</span><b>${esc(m.operator||'-')}</b></div><div class="machine-stat"><span>Kullanım</span><b>%${m.utilization||0}</b></div><div class="machine-stat" style="grid-column:1/-1"><span>Bakım / Durum</span><b>${esc(m.nextMaintenance||'-')}</b></div></div></article>`).join('');
}
function syncOrderCustomers(){const el=document.getElementById('orderCustomer');el.innerHTML='<option value="">Müşteri seçin</option>'+state.customers.map(c=>`<option>${esc(c.company)}</option>`).join('');}
function showPage(page){document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id===`page-${page}`));document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.page===page));const titles={dashboard:'Komuta Merkezi',customers:'Müşteriler',orders:'İş Emirleri',production:'Üretim',machines:'Makineler'};document.getElementById('pageTitle').textContent=titles[page]||'Matbaa OS';document.getElementById('sidebar').classList.remove('open');}
function openModal(id){document.getElementById(id)?.classList.add('open');document.getElementById(id)?.setAttribute('aria-hidden','false')}
function closeModals(){document.querySelectorAll('.modal').forEach(m=>{m.classList.remove('open');m.setAttribute('aria-hidden','true')})}
function toast(msg){const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),2200)}
function nextOrderId(){const nums=state.orders.map(o=>Number(o.id.split('-').pop())||0);return `ME-2026-${String(Math.max(...nums,0)+1).padStart(4,'0')}`;}
window.addEventListener('DOMContentLoaded',()=>{
  renderAll();
  document.querySelectorAll('.nav-item').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.page)));
  document.querySelectorAll('[data-goto]').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.goto)));
  document.querySelectorAll('[data-open]').forEach(b=>b.addEventListener('click',()=>openModal(b.dataset.open)));
  document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',closeModals));
  document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',e=>{if(e.target===m)closeModals()}));
  document.getElementById('menuBtn').addEventListener('click',()=>document.getElementById('sidebar').classList.toggle('open'));
  document.getElementById('customerSearch').addEventListener('input',e=>renderCustomers(e.target.value));
  document.querySelectorAll('[data-order-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-order-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');orderFilter=b.dataset.orderFilter;renderOrders()}));
  document.getElementById('customerForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));state.customers.push({id:Date.now(),...d});save();renderAll();e.target.reset();closeModals();toast('Müşteri kaydedildi');});
  document.getElementById('orderForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));state.orders.unshift({id:nextOrderId(),customer:d.customer,product:d.product,quantity:Number(d.quantity),deadline:d.deadline,stage:d.stage,status:d.priority==='risk'?'risk':'active',progress:d.stage==='Planlama'?5:12,note:d.note});save();renderAll();e.target.reset();closeModals();toast('İş emri oluşturuldu');});
  document.getElementById('machineForm').addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target));state.machines.push({id:Date.now(),...d,utilization:d.status==='active'?50:0,nextMaintenance:'Henüz planlanmadı'});save();renderAll();e.target.reset();closeModals();toast('Makine eklendi');});
  const tick=()=>{const now=new Date();document.getElementById('liveClock').innerHTML=`<strong>${now.toLocaleTimeString('tr-TR',{hour:'2-digit',minute:'2-digit'})}</strong><br>${now.toLocaleDateString('tr-TR',{weekday:'short',day:'2-digit',month:'short'})}`};tick();setInterval(tick,30000);
});
