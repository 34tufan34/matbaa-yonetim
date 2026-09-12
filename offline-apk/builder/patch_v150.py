from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')

css=r'''
/* v1.5.0 professional settings, command center and themes */
body[data-app-theme="graphite"]{--bg:#090c11;--panel:#11161d;--panel2:#151b24;--line:#252e3a;--muted:#8d98a8;--text:#f2f5f8;--accent:#eb4650;--accent2:#c72d3a;--good:#38cf92;--warn:#d7a83f;--bad:#ef5d68}
body[data-app-theme="aurora"]{--bg:#071014;--panel:#0d1b20;--panel2:#10232a;--line:#1f3941;--muted:#8aa8ae;--text:#eefcff;--accent:#18b7a7;--accent2:#10897f;--good:#56d7a7;--warn:#f2b84b;--bad:#ff6d7b}
body[data-app-theme="ocean"]{--bg:#08101d;--panel:#0e192b;--panel2:#122138;--line:#243754;--muted:#91a5c1;--text:#f2f7ff;--accent:#4c8dff;--accent2:#2c67ce;--good:#39d19d;--warn:#eeb04b;--bad:#ff6173}
body[data-app-theme="copper"]{--bg:#100b08;--panel:#1a120e;--panel2:#221711;--line:#3b2b21;--muted:#b5a091;--text:#fff8f1;--accent:#d87939;--accent2:#a84e24;--good:#6bc896;--warn:#e0aa4a;--bad:#e95f63}
body[data-app-theme="violet"]{--bg:#0c0913;--panel:#171120;--panel2:#1f172c;--line:#38294b;--muted:#a79ab9;--text:#faf5ff;--accent:#9b6cff;--accent2:#7045d2;--good:#52d3a5;--warn:#e2b252;--bad:#f3697e}
body[data-app-theme="forest"]{--bg:#07100c;--panel:#0e1914;--panel2:#13221b;--line:#263b31;--muted:#92a99d;--text:#f0faf5;--accent:#46b879;--accent2:#2d8b59;--good:#65d49a;--warn:#d7aa4a;--bad:#ed6670}
body{background:radial-gradient(circle at 75% -10%,color-mix(in srgb,var(--accent) 10%,transparent),transparent 32%),var(--bg)}
.sidebar{background:linear-gradient(180deg,color-mix(in srgb,var(--panel) 92%,#000),color-mix(in srgb,var(--bg) 95%,#000))}.panel{background:linear-gradient(180deg,color-mix(in srgb,var(--panel) 97%,#fff 1%),var(--panel));box-shadow:0 16px 40px rgba(0,0,0,.12)}
.command-hero{position:relative;overflow:hidden;display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;padding:22px 24px;margin-bottom:14px;border:1px solid color-mix(in srgb,var(--accent) 22%,var(--line));border-radius:18px;background:linear-gradient(130deg,color-mix(in srgb,var(--accent) 10%,var(--panel)),var(--panel) 55%,color-mix(in srgb,var(--panel2) 92%,#000));box-shadow:0 22px 50px rgba(0,0,0,.18)}
.command-hero:after{content:"";position:absolute;width:260px;height:260px;border-radius:50%;right:-90px;top:-145px;background:color-mix(in srgb,var(--accent) 14%,transparent);filter:blur(2px)}.command-hero h2{font-size:24px;margin:3px 0 7px}.command-hero p{margin:0;color:var(--muted);max-width:760px}.command-chip-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.command-chip{font-size:11px;padding:7px 10px;border-radius:999px;border:1px solid var(--line);background:color-mix(in srgb,var(--panel2) 88%,transparent);color:#dce3eb}.command-chip.good{border-color:color-mix(in srgb,var(--good) 48%,var(--line));color:var(--good)}.command-hero-actions{position:relative;z-index:2;display:grid;gap:8px;min-width:170px}.command-hero-actions .btn{width:100%}.dashboard-period-shell,.filter-panel{border-radius:14px!important}.metric-grid .metric{position:relative;overflow:hidden}.metric-grid .metric:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--accent);opacity:.75}.dashboard-summary-panel{background:linear-gradient(180deg,color-mix(in srgb,var(--panel2) 92%,transparent),color-mix(in srgb,var(--panel) 96%,transparent));border:1px solid var(--line);border-radius:16px!important;padding:16px!important}
.settings-shell{display:grid;gap:16px}.settings-hero{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 24px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 9%,var(--panel)),var(--panel));box-shadow:0 18px 44px rgba(0,0,0,.14)}.settings-hero h2{font-size:23px;margin:3px 0 6px}.settings-hero p{margin:0;color:var(--muted)}.settings-nav-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.settings-nav-card{border:1px solid var(--line);border-radius:15px;background:linear-gradient(180deg,var(--panel2),var(--panel));padding:15px;text-align:left;color:var(--text);cursor:pointer}.settings-nav-card:hover{border-color:color-mix(in srgb,var(--accent) 45%,var(--line));transform:translateY(-1px)}.settings-nav-card strong{display:block;font-size:13px}.settings-nav-card span{display:block;color:var(--muted);font-size:11px;margin-top:5px;line-height:1.45}.theme-panel{padding:18px 20px}.theme-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px}.theme-card{position:relative;border:1px solid var(--line);border-radius:14px;background:var(--panel2);padding:12px;cursor:pointer;color:var(--text);text-align:left}.theme-card.active{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 16%,transparent)}.theme-preview{height:58px;border-radius:10px;margin-bottom:10px;display:grid;grid-template-columns:26% 1fr;overflow:hidden;border:1px solid rgba(255,255,255,.08)}.theme-preview i:first-child{background:#0d1117}.theme-preview i:last-child{background:linear-gradient(145deg,var(--t1),var(--t2))}.theme-card strong{font-size:12px}.theme-card span{display:block;font-size:10px;color:var(--muted);margin-top:3px}.settings-breadcrumb{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:11px;margin-bottom:12px}.settings-breadcrumb button{border:0;background:transparent;color:var(--accent);cursor:pointer;padding:0}.settings-section-label{font-size:10px;letter-spacing:1px;color:var(--muted);font-weight:800}.master-tabs{border-radius:14px;background:color-mix(in srgb,var(--panel2) 85%,transparent);padding:7px}.master-tabs button{border-radius:9px}
@media(max-width:980px){.command-hero{grid-template-columns:1fr}.command-hero-actions{display:flex;min-width:0}.settings-nav-grid,.theme-grid{grid-template-columns:1fr 1fr}}
@media(max-width:620px){.settings-nav-grid,.theme-grid{grid-template-columns:1fr}.settings-hero{align-items:flex-start;flex-direction:column}.command-hero-actions{display:grid;width:100%}}
'''
html=html.replace('@media(max-width:1250px)',css+'\n@media(max-width:1250px)',1)
html=html.replace('        <button class="nav-btn" data-page="masterdata">Merkez Tanımlar</button>\n','',1)
html=html.replace('<button class="nav-btn" data-page="backup">Ayarlar & Yedekleme</button>','<button class="nav-btn" data-page="backup">Ayarlar</button>',1)
anchor='''      <section id="dashboard" class="page active">\n        <div class="panel filter-panel">'''
hero='''      <section id="dashboard" class="page active">\n        <div class="command-hero">\n          <div><div class="eyebrow">OPERASYON KOMUTA MERKEZİ</div><h2>Üretimin Nabzı Tek Ekranda</h2><p id="commandHeroText">Seçili dönem için üretim, fire, duruş ve vardiya hareketlerini hızlıca izle.</p><div class="command-chip-row"><span id="commandStatusChip" class="command-chip good">● Sistem Hazır</span><span id="commandPeriodChip" class="command-chip">Günlük</span><span class="command-chip">Tamamen Offline</span></div></div>\n          <div class="command-hero-actions"><button id="commandReportsBtn" class="btn primary" type="button">Detaylı Rapor Merkezi</button><button id="commandNewRecordBtn" class="btn ghost" type="button">+ Üretim Kaydı</button></div>\n        </div>\n        <div class="panel filter-panel">'''
if anchor not in html: raise SystemExit('dashboard anchor missing')
html=html.replace(anchor,hero,1)
backup_anchor='''      <section id="backup" class="page">\n        <div class="grid-2">'''
settings='''      <section id="backup" class="page">\n        <div class="settings-shell">\n          <div class="settings-hero"><div><div class="eyebrow">SİSTEM YÖNETİMİ</div><h2>Profesyonel Ayarlar Merkezi</h2><p>Görünüm, merkez tanımlar, veri güvenliği ve sistem yönetimini tek yerden kontrol et.</p></div><span class="pill">v1.5.0 • Production</span></div>\n          <div class="settings-nav-grid"><button class="settings-nav-card" type="button" data-settings-definitions><strong>Merkez Tanımlar</strong><span>Personeller, makineler, vardiyalar, fire/duruş nedenleri ve çalışma & mesai.</span></button><button class="settings-nav-card" type="button" data-settings-backup><strong>Veri & Yedekleme</strong><span>Tam yedek, geri yükleme ve eski sistemlerden veri aktarımı.</span></button><button class="settings-nav-card" type="button" data-settings-security><strong>Güvenlik & Sıfırlama</strong><span>Yerel veri durumu, fabrika ayarları ve güvenli kullanım işlemleri.</span></button></div>\n          <div class="panel theme-panel"><div class="panel-head"><div><div class="settings-section-label">GÖRÜNÜM</div><h2>Modern Temalar</h2><p>Sıradan açık/koyu tema yerine operasyon ekranına özel karakterli arayüzler.</p></div></div><div id="themeGrid" class="theme-grid"></div></div>\n        </div>\n        <div id="settingsDataAnchor" class="grid-2">'''
if backup_anchor not in html: raise SystemExit('backup anchor missing')
html=html.replace(backup_anchor,settings,1)
master_anchor='''      <section id="masterdata" class="page">\n        <div class="panel">'''
master_new='''      <section id="masterdata" class="page">\n        <div class="settings-breadcrumb"><button id="backToSettingsBtn" type="button">← Ayarlar</button><span>/</span><strong>Merkez Tanımlar</strong></div>\n        <div class="panel">'''
if master_anchor not in html: raise SystemExit('master anchor missing')
html=html.replace(master_anchor,master_new,1)
nav_marker='function navTo(page){'
theme_js=r'''
const APP_THEMES=[{id:'graphite',name:'Graphite Command',desc:'Koyu, nötr ve yüksek okunabilirlik.',a:'#eb4650',b:'#11161d'},{id:'aurora',name:'Aurora Ops',desc:'Petrol yeşili ve modern operasyon görünümü.',a:'#18b7a7',b:'#0d1b20'},{id:'ocean',name:'Deep Ocean',desc:'Lacivert ve elektrik mavisi yönetim teması.',a:'#4c8dff',b:'#0e192b'},{id:'copper',name:'Copper Press',desc:'Bakır ve koyu kahve endüstriyel tema.',a:'#d87939',b:'#1a120e'},{id:'violet',name:'Violet Intelligence',desc:'Mor vurgulu analitik kontrol teması.',a:'#9b6cff',b:'#171120'},{id:'forest',name:'Forest Control',desc:'Yeşil ve mat koyu tonlarda sakin görünüm.',a:'#46b879',b:'#0e1914'}];
function currentTheme(){return state.settings?.theme||'graphite'}
function applyTheme(theme){const id=APP_THEMES.some(x=>x.id===theme)?theme:'graphite';document.body.dataset.appTheme=id;const meta=document.querySelector('meta[name="theme-color"]');if(meta){const t=APP_THEMES.find(x=>x.id===id);meta.setAttribute('content',t?.b||'#0b0d12')}}
function renderThemePicker(){const host=$('themeGrid');if(!host)return;const active=currentTheme();host.innerHTML=APP_THEMES.map(t=>`<button type="button" class="theme-card ${t.id===active?'active':''}" data-theme-choice="${t.id}"><div class="theme-preview" style="--t1:${t.b};--t2:${t.a}"><i></i><i></i></div><strong>${t.name}</strong><span>${t.desc}</span></button>`).join('');qsa('[data-theme-choice]').forEach(b=>b.onclick=()=>saveTheme(b.dataset.themeChoice));}
async function saveTheme(theme){const next={...defaultSettings(),...(state.settings||{}),id:'settings',theme};await dbPut('settings',next);state.settings=next;applyTheme(theme);renderThemePicker();toast('Tema uygulandı: '+(APP_THEMES.find(x=>x.id===theme)?.name||theme));}
function openSettingsDefinitions(){navTo('masterdata')}
function scrollSettingsTo(target){navTo('backup');setTimeout(()=>document.querySelector(target)?.scrollIntoView({behavior:'smooth',block:'start'}),80)}
'''
if nav_marker not in html: raise SystemExit('navTo missing')
html=html.replace(nav_marker,theme_js+'\n'+nav_marker,1)
html=html.replace("  document.querySelector(`.nav-btn[data-page=\"${page}\"]`).classList.add('active');", "  const sidebarPage=page==='masterdata'?'backup':page; const navBtn=document.querySelector(`.nav-btn[data-page=\"${sidebarPage}\"]`); if(navBtn)navBtn.classList.add('active');",1)
html=html.replace("masterdata:['Merkez Tanımlar','Sistemin beslendiği ana kayıtlar'],backup:['Ayarlar & Yedekleme','Tek cihaz, güvenli veri taşıma']", "masterdata:['Ayarlar • Merkez Tanımlar','Personel, makine, vardiya, neden ve mesai tanımları'],backup:['Ayarlar','Tema, merkez tanımlar, yedekleme ve sistem yönetimi']",1)
needle="  if($('dashSummaryNote')) $('dashSummaryNote').innerHTML=`<strong>${dashboardPeriodName(dashboardPeriod)} genel bakış:</strong>"
idx=html.find(needle)
if idx<0: raise SystemExit('dashboard summary needle missing')
insert="""  if($('commandHeroText')) $('commandHeroText').innerHTML=`<strong>${fmtNum(good)}</strong> net tabaka • <strong>${fmtPct(fireRate)}</strong> fire • <strong>${fmtNum(down)} dk</strong> duruş${bestMachine?` • Lider makine <strong>${esc(bestMachine.name)}</strong>`:''}`;\n  if($('commandPeriodChip')) $('commandPeriodChip').textContent=`${dashboardPeriodName(dashboardPeriod)} • ${formatRange(startDate,endDate)}`;\n  if($('commandStatusChip')){const risky=fireRate>=5||down>=600;$('commandStatusChip').classList.toggle('good',!risky);$('commandStatusChip').textContent=risky?'● Dikkat Gerekiyor':'● Operasyon Dengeli';}\n"""
html=html[:idx]+insert+html[idx:]
fs=html.index('function printSmartReportV140(){')
fe=html.index('\nfunction printReportFullV130()',fs)
chunk=html[fs:fe]
tail_start=chunk.rfind("  closePdfReportModal();if(isAndroidNative()")
if tail_start<0: raise SystemExit('smart pdf tail missing')
new_tail="""  try{\n    if(isAndroidNative()&&window.AndroidApp){toast('Yazdırma penceresi hazırlanıyor...');window.AndroidApp.printHtml('Uretim Performans Raporu',doc);closePdfReportModal();return;}\n    const w=window.open('','_blank');if(!w){toast('Yazdırma penceresi engellendi.');return}w.document.write(doc.replace('</body>','<script>window.onload=()=>setTimeout(()=>window.print(),250)<\\\\/script></body>'));w.document.close();closePdfReportModal();\n  }catch(err){console.error(err);alert('PDF / Yazdır işlemi başlatılamadı.\\n\\nTeknik ayrıntı: '+((err&&err.message)?err.message:String(err)));}\n}\n"""
chunk=chunk[:tail_start]+new_tail
html=html[:fs]+chunk+html[fe:]
bind='function bindEvents(){'
callbacks=r'''
function nativePrintStarted(){toast('Android yazdırma penceresi açıldı.');}
function nativePrintFailed(message){alert('Android yazdırma servisi açılamadı.\n\n'+String(message||'Bilinmeyen hata'));}
'''
html=html.replace(bind,callbacks+'\n'+bind,1)
bind_start="  qsa('.nav-btn').forEach(b=>b.onclick=()=>navTo(b.dataset.page));"
bind_new=bind_start+" if($('commandReportsBtn'))$('commandReportsBtn').onclick=()=>navTo('reports'); if($('commandNewRecordBtn'))$('commandNewRecordBtn').onclick=()=>openRecordModal(); if($('backToSettingsBtn'))$('backToSettingsBtn').onclick=()=>navTo('backup'); qsa('[data-settings-definitions]').forEach(b=>b.onclick=openSettingsDefinitions); qsa('[data-settings-backup]').forEach(b=>b.onclick=()=>scrollSettingsTo('#settingsDataAnchor')); qsa('[data-settings-security]').forEach(b=>b.onclick=()=>scrollSettingsTo('.factory-reset-card'));"
html=html.replace(bind_start,bind_new,1)
old_init="    await loadState();\n    const seeded=await applyEmbeddedSeedIfFresh();\n    bindEvents(); populateSelects(); setPeriod('week'); renderDashboard(); renderBackupInfo(); renderStorageMode();"
new_init="    await loadState();\n    applyTheme(currentTheme());\n    const seeded=await applyEmbeddedSeedIfFresh();\n    bindEvents(); populateSelects(); setPeriod('week'); renderDashboard(); renderBackupInfo(); renderStorageMode(); renderThemePicker();"
if old_init not in html: raise SystemExit('init anchor missing')
html=html.replace(old_init,new_init,1)
html=html.replace('v1.4.0 • Android / tamamen offline','v1.5.0 • Android / tamamen offline')
html=html.replace('v1.4.0-focused-report','v1.5.0-professional-ui')
p.write_text(html,encoding='utf-8')
print('patched-v150',len(html))
