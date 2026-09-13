from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.7.0-report-command' in html:
    raise SystemExit('already patched')

# 1) Reduce top-level report tabs to manager-focused groups.
old='''          <div class="report-detail-tabs" id="reportDetailTabs">
            <button class="active" data-report-detail="general">Genel</button>
            <button data-report-detail="shift">Vardiya</button>
            <button data-report-detail="overtime">Mesai</button>
            <button data-report-detail="machine">Makine</button>
            <button data-report-detail="master">Usta</button>
            <button data-report-detail="scrap">Fire</button>
            <button data-report-detail="downtime">Duruş</button>
            <button data-report-detail="workorder">İş Emri</button>
            <button data-report-detail="mix">Renk / Kalıp / Lak</button>
            <button data-report-detail="trend">Trend</button>
            <button data-report-detail="compare">Karşılaştırma</button>
            <button data-report-detail="all">Her Şeyi Gör</button>
          </div>'''
new='''          <div class="report-detail-tabs report-main-tabs" id="reportDetailTabs">
            <button class="active" data-report-detail="general">Genel Bakış</button>
            <button data-report-detail="performance">Performans</button>
            <button data-report-detail="losses">Kayıplar</button>
            <button data-report-detail="production">Üretim Analizi</button>
            <button data-report-detail="compare">Karşılaştırma</button>
            <button data-report-detail="all">Her Şeyi Gör</button>
          </div>'''
if old not in html: raise SystemExit('report tabs block missing')
html=html.replace(old,new,1)
html=html.replace('<span id="reportFocusLabel" class="subtle-chip">Genel</span>','<span id="reportFocusLabel" class="subtle-chip">Genel Bakış</span>',1)
html=html.replace('<p>Bir bakışta üretim, kayıp ve performans. Detaya yalnızca gerektiğinde in.</p>','<p>Önce karar özeti, sonra performans ve kayıp analizi. Detaya yalnızca gerektiğinde in.</p>',1)

# 2) Add a production-analysis PDF preset while keeping detailed section selection.
old_presets='''<div class="pdf-presets"><button class="btn ghost" type="button" data-pdf-preset="manager">Yönetici Özeti</button><button class="btn ghost" type="button" data-pdf-preset="performance">Performans</button><button class="btn ghost" type="button" data-pdf-preset="loss">Kayıplar</button><button class="btn ghost" type="button" data-pdf-preset="all">Tüm Bölümler</button></div>'''
new_presets='''<div class="pdf-presets"><button class="btn ghost" type="button" data-pdf-preset="manager">Yönetici Özeti</button><button class="btn ghost" type="button" data-pdf-preset="performance">Performans</button><button class="btn ghost" type="button" data-pdf-preset="loss">Kayıplar</button><button class="btn ghost" type="button" data-pdf-preset="production">Üretim Analizi</button><button class="btn ghost" type="button" data-pdf-preset="all">Tüm Bölümler</button></div>'''
if old_presets in html: html=html.replace(old_presets,new_presets,1)
old_set="""const presets={manager:['summary','consistency','machine','shift','overtime','scrap','downtime','mix','trend'],performance:['summary','machine','shift','overtime','master','trend','compare'],loss:['summary','scrap','downtime','mix'],all:['summary','consistency','machine','shift','overtime','master','scrap','downtime','mix','trend','compare']};"""
new_set="""const presets={manager:['summary','consistency','machine','shift','scrap','downtime','trend'],performance:['summary','machine','shift','master','trend','compare'],loss:['summary','scrap','downtime','mix'],production:['summary','overtime','mix','trend'],all:['summary','consistency','machine','shift','overtime','master','scrap','downtime','mix','trend','compare']};"""
if old_set in html: html=html.replace(old_set,new_set,1)

# 3) Styling for the new report hierarchy.
css=r'''
/* v1.7.0 manager report command center */
.report-main-tabs{display:grid!important;grid-template-columns:repeat(6,minmax(0,1fr));gap:7px;padding:8px!important;background:#0b1016;border:1px solid #202a37;border-radius:14px}.report-main-tabs button{min-height:40px;border-radius:10px!important;font-size:11px!important;font-weight:850!important}.report-main-tabs button.active{background:linear-gradient(135deg,#28476d,#1a2d46)!important;border-color:#5479a5!important;color:#fff!important;box-shadow:0 7px 18px rgba(0,0,0,.22)}
.report-subtabs{display:flex;gap:7px;flex-wrap:wrap;padding:7px;border:1px solid #25303d;border-radius:12px;background:#0b1118;margin:0 0 14px}.report-subtabs button{border:1px solid #2b3745;background:#111821;color:#9ba8b9;border-radius:9px;padding:8px 12px;font-size:10px;font-weight:850;cursor:pointer}.report-subtabs button.active{background:#1b2b40;color:#fff;border-color:#48668c}.report-hub-intro{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;margin-bottom:12px}.report-hub-intro h2{margin:2px 0 0;font-size:19px}.report-hub-intro p{margin:4px 0 0;color:#8996a6;font-size:10px}.decision-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.decision-kpi{border:1px solid #26313f;background:linear-gradient(180deg,#101720,#0d1218);border-radius:13px;padding:13px}.decision-kpi span{display:block;color:#7f8c9d;font-size:9px;text-transform:uppercase;font-weight:850}.decision-kpi strong{display:block;margin-top:6px;font-size:20px}.decision-kpi small{display:block;margin-top:5px;color:#8793a2;font-size:9px}.decision-kpi.good strong,.decision-kpi.good small{color:#8edbb2}.decision-kpi.bad strong,.decision-kpi.bad small{color:#ff9da7}.attention-panel{border:1px solid #344052;background:linear-gradient(135deg,#101923,#0e141c);border-radius:14px;padding:14px;margin-bottom:14px}.attention-head{display:flex;justify-content:space-between;align-items:center;gap:10px}.attention-head h3{margin:0;font-size:14px}.attention-list{display:grid;gap:7px;margin-top:10px}.attention-item{display:flex;gap:9px;align-items:flex-start;border:1px solid #26313e;background:#0b1118;border-radius:10px;padding:9px 10px;font-size:10px;line-height:1.45}.attention-item i{width:7px;height:7px;border-radius:99px;background:#5fa5ff;margin-top:4px;flex:0 0 auto}.attention-item.warn i{background:#e2b85e}.attention-item.bad i{background:#ed6d79}.attention-item.good i{background:#54c991}.report-compact-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.hub-section{border:1px solid #26313f;background:#0d131a;border-radius:14px;padding:14px}.hub-section h3{margin:0 0 4px;font-size:14px}.hub-section>p{margin:0 0 12px;color:#8490a0;font-size:10px}.all-group-label{display:flex;align-items:center;gap:9px;margin:4px 0 12px}.all-group-label span{border:1px solid #3a4b60;background:#122033;border-radius:999px;padding:6px 11px;color:#c7d7eb;font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:.5px}.all-group-divider{height:1px;background:linear-gradient(90deg,transparent,#344355 15%,#344355 85%,transparent);margin:26px 0}.quick-note{border:1px solid #2d3b4b;background:#0e1620;border-radius:10px;padding:9px 11px;color:#93a1b2;font-size:10px;margin-top:10px}
@media(max-width:1050px){.report-main-tabs{grid-template-columns:repeat(3,1fr)}.decision-kpis{grid-template-columns:repeat(2,1fr)}}@media(max-width:700px){.report-main-tabs{grid-template-columns:repeat(2,1fr)}.report-compact-grid{grid-template-columns:1fr}.decision-kpis{grid-template-columns:1fr 1fr}}
'''
if '</style>' not in html: raise SystemExit('style close missing')
html=html.replace('</style>',css+'</style>',1)

# 4) Inject v1.7 report functions AFTER old functions so these declarations win.
anchor='''function drillScopeName(scope){'''
if anchor not in html: raise SystemExit('drillScopeName anchor missing')
js=r'''
let reportHubSub={performance:'shift',losses:'scrap',production:'overtime'};
function reportDetailLabel(view){return({general:'Genel Bakış',performance:'Performans',losses:'Kayıplar',production:'Üretim Analizi',compare:'Karşılaştırma',all:'Her Şeyi Gör'})[view]||'Genel Bakış'}
function reportDeltaBadge(cur,prev,inverse=false,suffix='%'){
  const d=pctChange(cur,prev),good=inverse?d<0:d>0,bad=inverse?d>0:d<0;
  return `<small class="${good?'good':bad?'bad':''}">${deltaText(d,suffix)} önceki döneme göre</small>`;
}
function decisionAttentionV170(rows){
  const out=[],st=statsOf(rows),start=$('reportStart').value,end=$('reportEnd').value;
  let prev=[];if(start&&end){const [ps,pe]=previousPeriodRange(start,end);prev=filterReportRows(ps,pe)}const old=statsOf(prev);
  if(prev.length){const net=pctChange(st.good,old.good),fire=st.rate-old.rate,down=pctChange(st.down,old.down);if(net<=-10)out.push(['bad',`Net baskı önceki eşit döneme göre <strong>${Math.abs(net).toLocaleString('tr-TR',{maximumFractionDigits:1})}% azaldı</strong>.`]);else if(net>=10)out.push(['good',`Net baskı önceki eşit döneme göre <strong>${net.toLocaleString('tr-TR',{maximumFractionDigits:1})}% arttı</strong>.`]);if(fire>=.5)out.push(['bad',`Fire oranı önceki döneme göre <strong>${fire.toLocaleString('tr-TR',{maximumFractionDigits:2})} puan yükseldi</strong>.`]);else if(fire<=-.5)out.push(['good',`Fire oranı önceki döneme göre <strong>${Math.abs(fire).toLocaleString('tr-TR',{maximumFractionDigits:2})} puan iyileşti</strong>.`]);if(down>=20)out.push(['warn',`Toplam duruş önceki döneme göre <strong>${down.toLocaleString('tr-TR',{maximumFractionDigits:1})}% arttı</strong>.`]);}
  const machines=enhancedGroupStats(rows,'machineId',state.machines),shifts=enhancedGroupStats(rows,'shiftId',state.shifts),reasons=downtimeStatsCombined(rows),gross=st.good+st.scrap;
  const riskyMachine=[...machines].filter(x=>x.gross>0).sort((a,b)=>b.rate-a.rate)[0];if(riskyMachine&&riskyMachine.rate>Math.max(2,st.rate*1.35))out.push(['warn',`Fire açısından dikkat çeken makine <strong>${esc(riskyMachine.name)}</strong>: ${fmtPct(riskyMachine.rate)}.`]);
  const slowShift=[...shifts].sort((a,b)=>b.downPerJob-a.downPerJob)[0];if(slowShift&&slowShift.downPerJob>0)out.push(['warn',`İş başına en yüksek duruş <strong>${esc(slowShift.name)}</strong>: ${fmtNum(Math.round(slowShift.downPerJob))} dk/iş.`]);
  const topReason=reasons[0];if(topReason&&st.down>0&&topReason.value/st.down>=.25)out.push(['warn',`Duruşların <strong>%${Math.round(topReason.value*100/st.down)}</strong>'i ${esc(topReason.name)} kaynaklı.`]);
  const colorCoverage=coveragePct(rows,r=>inferredColorCount(r)>0);if(colorCoverage<60)out.push(['warn',`Renk/kalıp analizinde veri tamlığı <strong>${fmtPct(colorCoverage)}</strong>. Yeni kayıtlarda renk/kalıp bilgisini düzenli girmek analizi güçlendirir.`]);
  if(!out.length&&rows.length)out.push(['good','Seçili dönemde otomatik eşiklere göre belirgin bir performans sapması görünmüyor.']);
  return out.slice(0,5);
}
function executiveOverviewV170(rows){
  const st=statsOf(rows),start=$('reportStart').value,end=$('reportEnd').value;let old={good:0,rate:0,down:0,jobs:0};if(start&&end){const [ps,pe]=previousPeriodRange(start,end);old=statsOf(filterReportRows(ps,pe))}
  const gross=st.good+st.scrap,att=decisionAttentionV170(rows),machines=enhancedGroupStats(rows,'machineId',state.machines),shifts=enhancedGroupStats(rows,'shiftId',state.shifts),days=groupByPeriod(rows,'day').map(x=>({...x,name:x.label}));
  return `<div class="report-hub-intro"><div><div class="eyebrow">YÖNETİCİ EKRANI</div><h2>Genel Bakış</h2><p>Seçilen dönemin sonucu, değişim yönü ve dikkat gerektiren noktaları.</p></div><span class="subtle-chip">${fmtNum(rows.length)} kayıt</span></div>
  <div class="decision-kpis"><div class="decision-kpi"><span>Net Baskı</span><strong>${fmtNum(st.good)}</strong>${reportDeltaBadge(st.good,old.good,false)}</div><div class="decision-kpi"><span>Fire Oranı</span><strong>${fmtPct(st.rate)}</strong><small>${old.good||old.scrap?`${(st.rate-old.rate)>=0?'+':''}${(st.rate-old.rate).toLocaleString('tr-TR',{maximumFractionDigits:2})} puan önceki dönem`:'önceki dönem yok'}</small></div><div class="decision-kpi"><span>Toplam Duruş</span><strong>${fmtNum(st.down)} dk</strong>${reportDeltaBadge(st.down,old.down,true)}</div><div class="decision-kpi"><span>İş Sayısı</span><strong>${fmtNum(st.jobs)}</strong>${reportDeltaBadge(st.jobs,old.jobs,false)}</div><div class="decision-kpi"><span>Brüt Baskı</span><strong>${fmtNum(gross)}</strong><small>net + fire</small></div><div class="decision-kpi"><span>Kalıp</span><strong>${fmtNum(st.plates)}</strong><small>${st.jobs?(st.plates/st.jobs).toLocaleString('tr-TR',{maximumFractionDigits:1}):0} kalıp / iş</small></div><div class="decision-kpi"><span>Fire / İş</span><strong>${fmtNum(st.jobs?Math.round(st.scrap/st.jobs):0)}</strong><small>tabaka / iş</small></div><div class="decision-kpi"><span>Duruş / İş</span><strong>${fmtNum(st.jobs?Math.round(st.down/st.jobs):0)} dk</strong><small>ortalama kayıp</small></div></div>
  <div class="attention-panel"><div class="attention-head"><h3>Dikkat Gerektirenler</h3><span class="subtle-chip">${att.length} bulgu</span></div><div class="attention-list">${att.map(([c,t])=>`<div class="attention-item ${c}"><i></i><div>${t}</div></div>`).join('')}</div></div>
  <div class="report-compact-grid"><div class="hub-section"><h3>Günlük Üretim Trendi</h3><p>Net baskının seçili dönem içindeki dağılımı.</p>${visualBars(days,'good','')}</div><div class="hub-section"><h3>Makine Üretim Dağılımı</h3><p>Net baskıya göre.</p>${visualBars(machines,'good','')}</div><div class="hub-section"><h3>Vardiya Üretim Dağılımı</h3><p>1. ve 2. vardiya karşılaştırması.</p>${visualBars(shifts,'good','')}</div><div class="hub-section"><h3>Veri Güveni</h3><p>Karar kalitesini etkileyen alanların doluluk oranı.</p>${generalExtended(rows).match(/<div class="coverage-grid">[\s\S]*?<\/div><\/div>/)?.[0]||'<div class="quick-note">Veri tamlık bilgisi hesaplanamadı.</div>'}</div></div>`;
}
function reportSubTabsV170(group,active,items){return `<div class="report-subtabs">${items.map(([id,label])=>`<button type="button" data-report-sub-group="${group}" data-report-sub="${id}" class="${active===id?'active':''}">${label}</button>`).join('')}</div>`}
function performanceHubV170(rows){const active=reportHubSub.performance||'shift',items=[['shift','Vardiya'],['machine','Makine'],['master','Usta']];return `<div class="report-hub-intro"><div><div class="eyebrow">PERFORMANS</div><h2>Performans Merkezi</h2><p>Vardiya, makine ve usta performansını aynı mantıkla karşılaştır.</p></div></div>${reportSubTabsV170('performance',active,items)}${groupExtended(rows,active)}`}
function lossesHubV170(rows){const active=reportHubSub.losses||'scrap',items=[['scrap','Fire'],['downtime','Duruş']];return `<div class="report-hub-intro"><div><div class="eyebrow">KAYIPLAR</div><h2>Kayıp Analizi</h2><p>Fire ve duruşu neden, makine, vardiya ve usta bazında incele.</p></div></div>${reportSubTabsV170('losses',active,items)}${active==='scrap'?scrapExtended(rows):downtimeExtended(rows)}`}
function productionHubV170(rows){const active=reportHubSub.production||'overtime',items=[['overtime','Mesai'],['workorder','İş Emri'],['mix','Renk / Kalıp / Lak']];let body=active==='overtime'?overtimeExtended(rows):active==='workorder'?workOrderExtended(rows):mixExtended(rows);return `<div class="report-hub-intro"><div><div class="eyebrow">ÜRETİM ANALİZİ</div><h2>Üretim Analizi</h2><p>Mesai, iş emri geçmişi ve işin teknik karmaşıklığını birlikte incele.</p></div></div>${reportSubTabsV170('production',active,items)}${body}`}
function allExtendedReport(rows){
  const groups=[['Genel Bakış',executiveOverviewV170(rows)],['Performans — Vardiya',groupExtended(rows,'shift')],['Performans — Makine',groupExtended(rows,'machine')],['Performans — Usta',groupExtended(rows,'master')],['Kayıplar — Fire',scrapExtended(rows)],['Kayıplar — Duruş',downtimeExtended(rows)],['Üretim — Mesai',overtimeExtended(rows)],['Üretim — İş Emri',workOrderExtended(rows)],['Üretim — Renk / Kalıp / Lak',mixExtended(rows)],['Karşılaştırma',comparisonExtended(rows)]];
  return `<div class="report-hub-intro v1.7.0-report-command"><div><div class="eyebrow">TÜM RAPORLAR</div><h2>Her Şeyi Gör</h2><p>Üst menüdeki bütün rapor grupları ve alt analizleri tek akışta.</p></div><span class="subtle-chip">${groups.length} bölüm</span></div>`+groups.map(([label,body],i)=>`${i?'<div class="all-group-divider"></div>':''}<div class="all-group-label"><span>${label}</span></div>${body}`).join('');
}
function renderExtendedReport(view,rows){
  currentReportDetail=view||currentReportDetail||'general';
  if(!['general','performance','losses','production','compare','all'].includes(currentReportDetail))currentReportDetail='general';
  qsa('#reportDetailTabs button').forEach(b=>b.classList.toggle('active',b.dataset.reportDetail===currentReportDetail));
  if($('reportFocusLabel'))$('reportFocusLabel').textContent=reportDetailLabel(currentReportDetail);
  if($('reportConsistencyHost'))$('reportConsistencyHost').classList.toggle('hidden-focus',!['general','all'].includes(currentReportDetail));
  const host=$('reportDetailHost');if(!host)return;
  if(!rows.length){host.innerHTML='<div class="xreport-panel"><div class="xreport-empty">Seçilen filtrelerde rapor verisi yok.</div></div>';return}
  let out='';
  if(currentReportDetail==='general')out=executiveOverviewV170(rows);
  else if(currentReportDetail==='performance')out=performanceHubV170(rows);
  else if(currentReportDetail==='losses')out=lossesHubV170(rows);
  else if(currentReportDetail==='production')out=productionHubV170(rows);
  else if(currentReportDetail==='compare')out=comparisonExtended(rows);
  else if(currentReportDetail==='all')out=allExtendedReport(rows);
  host.innerHTML=out;
  qsa('[data-report-sub]',host).forEach(btn=>btn.onclick=()=>{const g=btn.dataset.reportSubGroup,id=btn.dataset.reportSub;if(g&&id){reportHubSub[g]=id;renderExtendedReport(currentReportDetail,currentReportRows)}});
  bindExtendedDrill(host,rows);
}

'''
html=html.replace(anchor,js+anchor,1)

# 5) Update version marker.
html=html.replace('v1.6.1-all-reports-shifts','v1.7.0-report-command',1)
p.write_text(html,encoding='utf-8')
print('patched-v170',len(html))
