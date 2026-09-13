from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.6.1-all-reports-shifts' in html:
    raise SystemExit('already patched')

# 1) Make "Her Şeyi Gör" explicitly render every report section to its left.
old='''function allExtendedReport(rows){
  const parts=[generalExtended(rows),groupExtended(rows,'shift'),overtimeExtended(rows),groupExtended(rows,'machine'),groupExtended(rows,'master'),scrapExtended(rows),downtimeExtended(rows),workOrderExtended(rows),mixExtended(rows),trendExtended(rows),comparisonExtended(rows)];
  return parts.map((x,i)=>`${i?'<div class="all-report-divider"></div>':''}${x}`).join('');
}'''
new='''function allExtendedReport(rows){
  const sections=[
    ['general','Genel',generalExtended(rows)],
    ['shift','Vardiya',groupExtended(rows,'shift')],
    ['overtime','Mesai',overtimeExtended(rows)],
    ['machine','Makine',groupExtended(rows,'machine')],
    ['master','Usta',groupExtended(rows,'master')],
    ['scrap','Fire',scrapExtended(rows)],
    ['downtime','Duruş',downtimeExtended(rows)],
    ['workorder','İş Emri',workOrderExtended(rows)],
    ['mix','Renk / Kalıp / Lak',mixExtended(rows)],
    ['trend','Trend',trendExtended(rows)],
    ['compare','Karşılaştırma',comparisonExtended(rows)]
  ];
  return `<div class="all-report-intro v1.6.1-all-reports-shifts"><div><div class="eyebrow">TÜM RAPORLAR</div><h2>Her Şeyi Gör</h2><p>Soldaki tüm rapor sekmeleri aynı sırayla bu ekranda eksiksiz gösterilir. İş emri ayrıntı listesi önceki tercih doğrultusunda ayrı pencerede açılır.</p></div><span class="subtle-chip">${sections.length} bölüm</span></div>`+
    sections.map(([id,label,body],i)=>`${i?'<div class="all-report-divider"></div>':''}<section class="all-report-section" data-all-section="${id}"><div class="all-report-section-label"><span>${label}</span></div>${body}</section>`).join('');
}'''
if old not in html: raise SystemExit('allExtendedReport block missing')
html=html.replace(old,new,1)

# 2) Styling so all-report mode is visibly separated and easy to scan.
css='''\n/* v1.6.1 all reports + numbered shifts */\n.all-report-intro{display:flex;justify-content:space-between;gap:14px;align-items:end;padding:14px 16px;border:1px solid #2b3746;border-radius:14px;background:linear-gradient(135deg,rgba(58,101,170,.16),rgba(14,19,27,.94));margin-bottom:4px}.all-report-intro h2{margin:2px 0 0;font-size:20px}.all-report-intro p{margin:5px 0 0;color:#8996a8;font-size:10px}.all-report-section{display:grid;gap:12px}.all-report-section-label{display:flex;align-items:center;gap:9px;margin-bottom:-3px}.all-report-section-label span{display:inline-flex;align-items:center;border:1px solid #34445a;background:#121b27;color:#b9c9df;border-radius:999px;padding:6px 10px;font-size:9px;font-weight:900;letter-spacing:.5px;text-transform:uppercase}.all-report-divider{height:1px;background:linear-gradient(90deg,transparent,#344152 18%,#344152 82%,transparent);margin:24px 0}.shift-number-note{border:1px solid #2b3746;background:#0e151e;border-radius:10px;padding:9px 11px;color:#8e9bad;font-size:10px;margin-top:8px}\n'''
if '</style>' not in html: raise SystemExit('style close missing')
html=html.replace('</style>',css+'</style>',1)

# 3) Standardize existing Gündüz/Gece master definitions to 1. / 2. Vardiya without changing IDs.
marker='''function defaultSettings(){'''
migration=r'''async function migrateShiftNamesV161(){
  const rows=state.shifts||[];let changed=false;
  for(const sh of rows){
    const raw=String(sh.name||'').trim();
    const up=raw.toLocaleUpperCase('tr-TR');
    let target='';
    if(up==='GÜNDÜZ'||up==='GUNDUZ'||up.startsWith('1. VARDİYA')||up==='1 VARDİYA') target='1. Vardiya';
    else if(up==='GECE'||up.startsWith('2. VARDİYA')||up==='2 VARDİYA') target='2. Vardiya';
    if(target&&raw!==target){sh.name=target;await dbPut('shifts',sh);changed=true;}
  }
  if(changed) state.shifts=await dbGetAll('shifts');
  return changed;
}

'''
if marker not in html: raise SystemExit('defaultSettings marker missing')
html=html.replace(marker,migration+marker,1)

# 4) Migrate after first-run seed as well as existing installs.
old_init='''    const seeded=await applyEmbeddedSeedIfFresh();
    bindEvents(); populateSelects(); setPeriod('week'); renderDashboard(); renderBackupInfo(); renderStorageMode(); renderThemePicker();'''
new_init='''    const seeded=await applyEmbeddedSeedIfFresh();
    const shiftsRenamed=await migrateShiftNamesV161();
    bindEvents(); populateSelects(); setPeriod('week'); renderDashboard(); renderBackupInfo(); renderStorageMode(); renderThemePicker();
    if(shiftsRenamed) toast('Vardiyalar 1. Vardiya / 2. Vardiya düzenine geçirildi.');'''
if old_init not in html: raise SystemExit('init anchor missing')
html=html.replace(old_init,new_init,1)

# 5) Update wording in overtime examples and imported shift defaults.
html=html.replace('“Cumartesi Gece Mesaisi”: Cumartesi + Gece vardiyası + Vardiyanın tamamı.','“Cumartesi 2. Vardiya Mesaisi”: Cumartesi + 2. Vardiya + vardiyanın tamamı.')
html=html.replace("'Hafta Sonu Gece Mesaisi'","'Hafta Sonu 2. Vardiya Mesaisi'")

# 6) Imported legacy shift labels should also use numbered naming.
html=html.replace("name,active:true,start:lower==='GÜNDÜZ'?'08:30':lower==='GECE'?'18:30':'',end:lower==='GÜNDÜZ'?'18:30':lower==='GECE'?'04:30':'',breakMin:0,legacySource:'excel-history'", "name:(lower==='GÜNDÜZ'?'1. Vardiya':lower==='GECE'?'2. Vardiya':name),active:true,start:lower==='GÜNDÜZ'?'08:30':lower==='GECE'?'18:30':'',end:lower==='GÜNDÜZ'?'18:30':lower==='GECE'?'04:30':'',breakMin:0,legacySource:'excel-history'")

# 7) Version marker.
html=html.replace('v1.6.0-record-entry','v1.6.1-all-reports-shifts',1)
p.write_text(html,encoding='utf-8')
print('patched-v161',len(html))
