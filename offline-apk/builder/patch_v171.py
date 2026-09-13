from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.7.1-pdf-production-fix' in html:
    raise SystemExit('already patched')

# PDF builder: keep the smart window, but align it with the report center requested sections.
start=html.find('<div class="pdf-builder-grid" id="pdfSectionOptions">')
end=html.find('</div>\n      <div class="pdf-note">',start)
if start<0 or end<0: raise SystemExit('pdf builder grid not found')
new_grid='''<div class="pdf-builder-grid" id="pdfSectionOptions">
        <label class="pdf-option"><input type="checkbox" data-pdf-section="summary" checked><div><strong>Yönetici KPI Özeti</strong><span>Net baskı, brüt baskı, fire oranı, toplam duruş, iş geçiş sayısı ve kalıp adedi.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="attention" checked><div><strong>Dikkat Gerektirenler</strong><span>Seçili dönemde öne çıkan üretim, fire ve duruş sapmaları.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="shift" checked><div><strong>Vardiya Performansı</strong><span>1. ve 2. vardiya karşılaştırması, grafik ve tablo.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="machine" checked><div><strong>Makine Performansı</strong><span>Makine bazında net, fire, duruş, kalıp ve iş geçişleri.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="master" checked><div><strong>Usta Performansı</strong><span>Usta bazında üretim, fire ve duruş karşılaştırması.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="scrap" checked><div><strong>Fire Analizi</strong><span>Fire Pareto grafiği ve en büyük kayıp nedenleri.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="downtime" checked><div><strong>Duruş Analizi</strong><span>Duruş Pareto grafiği ve kayıp süreleri.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="overtime" checked><div><strong>Mesai Analizi</strong><span>Mesaide net baskı, iş geçişi, fire, duruş ve dağılım.</span></div></label>
        <label class="pdf-option"><input type="checkbox" data-pdf-section="compare" checked><div><strong>Dönem Karşılaştırma Özeti</strong><span>Seçili dönem ile önceki eşit dönemin temel KPI karşılaştırması.</span></div></label>
      '''
html=html[:start]+new_grid+html[end:]
html=html.replace("<div class=\"pdf-note\">İş Emri Analizi bilinçli olarak PDF seçeneklerinden çıkarıldı; uzun rapor üretmesini engelliyoruz. İş emirleri Rapor Merkezi'ndeki açılır detay penceresinden incelenir.</div>","<div class=\"pdf-note\">Standart yönetici PDF'si Rapor Merkezi ile aynı ana başlıklardan oluşur. İş Emri detay listesi PDF'ye alınmaz; uygulamadaki ayrı detay penceresinden incelenir.</div>",1)

# PDF-specific styling additions.
css=r'''
/* v1.7.1 PDF/report fixes */
.pdf-attention{display:grid;gap:6px}.pdf-attention-item{border-left:4px solid #3b75d7;background:#f3f6fb;padding:8px 10px;border-radius:7px}.pdf-attention-item.warn{border-left-color:#d58e20;background:#fff8ea}.pdf-attention-item.bad{border-left-color:#c54154;background:#fff0f2}.pdf-attention-item.good{border-left-color:#219567;background:#ecfaf4}.pdf-attention-item strong{color:#182238}.production-hub-error{border:1px solid #6f2c35;background:#291319;color:#ffb4bd;border-radius:12px;padding:14px;line-height:1.5}.production-hub-error strong{display:block;margin-bottom:4px}.report-subtabs button{touch-action:manipulation}
'''
html=html.replace('</style>',css+'</style>',1)

anchor='function bindEvents(){'
if anchor not in html: raise SystemExit('bindEvents anchor missing')
js=r'''
function productionBlockV171(id,rows){
  try{
    if(id==='overtime') return overtimeExtended(rows);
    if(id==='workorder') return workOrderExtended(rows);
    if(id==='mix') return mixExtended(rows);
    return overtimeExtended(rows);
  }catch(err){
    console.error('production analysis',id,err);
    return `<div class="production-hub-error"><strong>Üretim Analizi hazırlanamadı.</strong>${esc((err&&err.message)||String(err||'Bilinmeyen hata'))}</div>`;
  }
}
function productionHubV171(rows){
  const active=reportHubSub.production||'overtime';
  const items=[['overtime','Mesai'],['workorder','İş Emri'],['mix','Renk / Kalıp / Lak']];
  return `<div class="report-hub-intro"><div><div class="eyebrow">ÜRETİM ANALİZİ</div><h2>Üretim Analizi</h2><p>Mesai, iş emri geçmişi ve teknik iş karmasını tek merkezden incele.</p></div></div>${reportSubTabsV170('production',active,items)}${productionBlockV171(active,rows)}`;
}
function renderExtendedReport(view,rows){
  try{
    currentReportDetail=view||currentReportDetail||'general';
    if(!['general','performance','losses','production','compare','all'].includes(currentReportDetail))currentReportDetail='general';
    qsa('#reportDetailTabs button').forEach(b=>b.classList.toggle('active',b.dataset.reportDetail===currentReportDetail));
    if($('reportFocusLabel'))$('reportFocusLabel').textContent=reportDetailLabel(currentReportDetail);
    if($('reportConsistencyHost'))$('reportConsistencyHost').classList.toggle('hidden-focus',!['general','all'].includes(currentReportDetail));
    const host=$('reportDetailHost');if(!host)return;
    if(!rows.length){host.innerHTML='<div class="xreport-panel"><div class="xreport-empty">Seçilen filtrelerde rapor verisi yok.</div></div>';return;}
    let out='';
    if(currentReportDetail==='general')out=executiveOverviewV170(rows);
    else if(currentReportDetail==='performance')out=performanceHubV170(rows);
    else if(currentReportDetail==='losses')out=lossesHubV170(rows);
    else if(currentReportDetail==='production')out=productionHubV171(rows);
    else if(currentReportDetail==='compare')out=comparisonExtended(rows);
    else if(currentReportDetail==='all')out=allExtendedReport(rows);
    host.innerHTML=out;
    host.querySelectorAll('[data-report-sub]').forEach(btn=>btn.onclick=()=>{const g=btn.dataset.reportSubGroup,id=btn.dataset.reportSub;if(g&&id){reportHubSub[g]=id;renderExtendedReport(currentReportDetail,currentReportRows);}});
    bindExtendedDrill(host,rows);
  }catch(err){
    console.error('report render failed',err);
    const host=$('reportDetailHost');if(host)host.innerHTML=`<div class="production-hub-error"><strong>Rapor hazırlanamadı.</strong>${esc((err&&err.message)||String(err||'Bilinmeyen hata'))}</div>`;
  }
}
function setPdfPresetV171(name){
  const presets={
    manager:['summary','attention','shift','machine','master','scrap','downtime','overtime','compare'],
    performance:['summary','shift','machine','master','compare'],
    loss:['summary','attention','scrap','downtime'],
    production:['summary','attention','overtime'],
    all:['summary','attention','shift','machine','master','scrap','downtime','overtime','compare']
  };
  const selected=new Set(presets[name]||presets.manager);
  qsa('[data-pdf-section]').forEach(x=>x.checked=selected.has(x.dataset.pdfSection));
}
function printSmartReportV171(){
  try{
    const rows=currentReportRows||[];if(!rows.length){toast('PDF için rapor verisi yok.');return;}
    const sel=selectedPdfSections();if(!sel.size){toast('En az bir PDF bölümü seç.');return;}
    const st=statsOf(rows),range=formatRange($('reportStart').value,$('reportEnd').value),gross=st.good+st.scrap;
    const machines=enhancedGroupStats(rows,'machineId',state.machines),shifts=enhancedGroupStats(rows,'shiftId',state.shifts),masters=enhancedGroupStats(rows,'masterId',state.people).filter(x=>x.id!=='none');
    const ot=overtimeRows(rows),otst=statsOf(ot),rules=overtimeRuleGroups(rows),scrap=knownReasonStats(rows,'scrapReasonId',state.scrapReasons,'scrapQty','Nedeni belirtilmemiş'),down=downtimeStatsCombined(rows);
    const attention=decisionAttentionV170(rows);
    const max=(a,k)=>Math.max(1,...a.map(x=>Number(x[k]||0)));
    const bars=(title,data,k='good',unit='')=>{const m=max(data,k);return `<section><h2>${title}</h2><div class="bars">${data.slice(0,12).map((x,i)=>`<div class="barrow"><span>${esc(x.name||x.label||'-')}</span><i><b class="c${i%6}" style="width:${Math.max(2,Number(x[k]||0)*100/m).toFixed(1)}%"></b></i><strong>${fmtNum(Math.round(Number(x[k]||0)))}${unit}</strong></div>`).join('')||'<p>Veri yok.</p>'}</div></section>`};
    const perfTable=(title,data)=>`<section><h2>${title}</h2><table><thead><tr><th>Grup</th><th>Net Baskı</th><th>İş Geçişi</th><th>Kalıp</th><th>Fire</th><th>Fire %</th><th>Duruş</th><th>Net / İş</th></tr></thead><tbody>${data.map(x=>`<tr><td>${esc(x.name)}</td><td>${fmtNum(x.good)}</td><td>${fmtNum(x.jobs)}</td><td>${fmtNum(x.plates)}</td><td>${fmtNum(x.scrap)}</td><td>${fmtPct(x.rate)}</td><td>${fmtNum(x.down)} dk</td><td>${fmtNum(Math.round(x.avgJob||0))}</td></tr>`).join('')||'<tr><td colspan="8">Veri yok</td></tr>'}</tbody></table></section>`;
    const parts=[];
    if(sel.has('summary'))parts.push(`<div class="kpis"><div class="kpi cblue"><small>Net Baskı</small><b>${fmtNum(st.good)}</b></div><div class="kpi cgreen"><small>Brüt Baskı</small><b>${fmtNum(gross)}</b></div><div class="kpi corange"><small>Fire Oranı</small><b>${fmtPct(st.rate)}</b></div><div class="kpi cred"><small>Toplam Duruş</small><b>${fmtNum(st.down)} dk</b></div><div class="kpi cpurple"><small>İş Geçiş Sayısı</small><b>${fmtNum(st.jobs)}</b></div><div class="kpi cteal"><small>Kalıp Adedi</small><b>${fmtNum(st.plates)}</b></div></div>`);
    if(sel.has('attention'))parts.push(`<section><h2>Dikkat Gerektirenler</h2><div class="pdf-attention">${attention.map(([c,t])=>`<div class="pdf-attention-item ${c}">${t}</div>`).join('')||'<div class="pdf-attention-item good">Belirgin bir sapma bulunmadı.</div>'}</div></section>`);
    if(sel.has('shift'))parts.push(bars('Vardiya Net Baskı Grafiği',shifts)+perfTable('Vardiya Performansı',shifts));
    if(sel.has('machine'))parts.push(bars('Makine Net Baskı Grafiği',machines)+perfTable('Makine Performansı',machines));
    if(sel.has('master'))parts.push(bars('Usta Net Baskı Grafiği',masters)+perfTable('Usta Performansı',masters));
    if(sel.has('scrap'))parts.push(bars('Fire Analizi — Pareto',scrap,'value')+`<section><h2>Fire Analizi Özeti</h2><table><thead><tr><th>Neden</th><th>Fire</th><th>Pay</th></tr></thead><tbody>${scrap.slice(0,12).map(x=>`<tr><td>${esc(x.name)}</td><td>${fmtNum(x.value)}</td><td>${st.scrap?fmtPct(x.value*100/st.scrap):'0,0%'}</td></tr>`).join('')||'<tr><td colspan="3">Fire nedeni verisi yok.</td></tr>'}</tbody></table></section>`);
    if(sel.has('downtime'))parts.push(bars('Duruş Analizi — Pareto',down,'value',' dk')+`<section><h2>Duruş Analizi Özeti</h2><table><thead><tr><th>Neden</th><th>Duruş</th><th>Pay</th></tr></thead><tbody>${down.slice(0,12).map(x=>`<tr><td>${esc(x.name)}</td><td>${fmtNum(x.value)} dk</td><td>${st.down?fmtPct(x.value*100/st.down):'0,0%'}</td></tr>`).join('')||'<tr><td colspan="3">Duruş nedeni verisi yok.</td></tr>'}</tbody></table></section>`);
    if(sel.has('overtime'))parts.push(`<section><h2>Mesai Analizi</h2><div class="mesai-kpis"><div><small>Mesaide Net Baskı</small><b>${fmtNum(otst.good)}</b></div><div><small>İş Geçişi</small><b>${fmtNum(otst.jobs)}</b></div><div><small>Fire Oranı</small><b>${fmtPct(otst.rate)}</b></div><div><small>Duruş</small><b>${fmtNum(otst.down)} dk</b></div></div></section>${bars('Mesai Kurallarına Göre Net Baskı',rules)}${perfTable('Mesaide Makine Performansı',enhancedGroupStats(ot,'machineId',state.machines))}`);
    if(sel.has('compare')){
      const [ps,pe]=previousPeriodRange($('reportStart').value,$('reportEnd').value),old=statsOf(filterReportRows(ps,pe));
      parts.push(`<section><h2>Dönem Karşılaştırma Özeti</h2><p class="section-sub">${esc(range)} ↔ ${esc(formatRange(ps,pe))}</p><table><thead><tr><th>Gösterge</th><th>Seçili Dönem</th><th>Önceki Dönem</th><th>Değişim</th></tr></thead><tbody><tr><td>Net Baskı</td><td>${fmtNum(st.good)}</td><td>${fmtNum(old.good)}</td><td>${deltaText(pctChange(st.good,old.good),'%')}</td></tr><tr><td>Brüt Baskı</td><td>${fmtNum(gross)}</td><td>${fmtNum(old.good+old.scrap)}</td><td>${deltaText(pctChange(gross,old.good+old.scrap),'%')}</td></tr><tr><td>Fire Oranı</td><td>${fmtPct(st.rate)}</td><td>${fmtPct(old.rate)}</td><td>${deltaText(st.rate-old.rate,' puan')}</td></tr><tr><td>Toplam Duruş</td><td>${fmtNum(st.down)} dk</td><td>${fmtNum(old.down)} dk</td><td>${deltaText(pctChange(st.down,old.down),'%')}</td></tr><tr><td>İş Geçiş Sayısı</td><td>${fmtNum(st.jobs)}</td><td>${fmtNum(old.jobs)}</td><td>${deltaText(pctChange(st.jobs,old.jobs),'%')}</td></tr><tr><td>Kalıp Adedi</td><td>${fmtNum(st.plates)}</td><td>${fmtNum(old.plates)}</td><td>${deltaText(pctChange(st.plates,old.plates),'%')}</td></tr></tbody></table></section>`);
    }
    const doc=`<!doctype html><html><head><meta charset="utf-8"><title>Üretim Performans Raporu</title><style>@page{size:A4 landscape;margin:8mm}*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important;box-sizing:border-box}body{font-family:Arial,sans-serif;color:#17202b;font-size:9px;margin:0;background:#fff}.hero{background:linear-gradient(120deg,#132542,#245ca9 52%,#5d3d8a);color:#fff;padding:18px;border-radius:11px}.hero h1{font-size:22px;margin:0 0 4px}.hero p{margin:0;color:#e4edff}.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:7px;margin:10px 0}.kpi{padding:10px;border-radius:9px;color:#fff}.kpi small{display:block;opacity:.86}.kpi b{display:block;font-size:14px;margin-top:4px}.cblue{background:#2e68c7}.cgreen{background:#168a68}.corange{background:#c97a21}.cred{background:#a73c52}.cpurple{background:#6247a1}.cteal{background:#2d7183}section{margin:12px 0;break-inside:avoid}h2{font-size:13px;margin:0 0 6px;color:#20304b;border-left:4px solid #3d6fe0;padding-left:7px}.section-sub{color:#69768a;margin:0 0 7px}table{width:100%;border-collapse:collapse}th,td{border-bottom:1px solid #d9e0e9;padding:4px 5px;text-align:right}th{background:#eaf0fb;color:#24334a}th:first-child,td:first-child{text-align:left}.bars{display:grid;gap:5px}.barrow{display:grid;grid-template-columns:150px 1fr 82px;gap:7px;align-items:center}.barrow>i{height:11px;background:#edf1f6;border-radius:99px;overflow:hidden}.barrow b{display:block;height:100%;border-radius:99px}.c0{background:#3d72e6}.c1{background:#16a074}.c2{background:#e0922c}.c3{background:#c13d58}.c4{background:#7750be}.c5{background:#2c91a5}.barrow strong{text-align:right}.pdf-attention{display:grid;gap:6px}.pdf-attention-item{border-left:4px solid #3b75d7;background:#f3f6fb;padding:8px 10px;border-radius:7px}.pdf-attention-item.warn{border-left-color:#d58e20;background:#fff8ea}.pdf-attention-item.bad{border-left-color:#c54154;background:#fff0f2}.pdf-attention-item.good{border-left-color:#219567;background:#ecfaf4}.mesai-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.mesai-kpis>div{padding:9px;border-radius:8px;background:#eef3fb}.mesai-kpis small{display:block;color:#647287}.mesai-kpis b{display:block;font-size:13px;margin-top:3px}.footer-note{margin-top:11px;color:#687488;font-size:8px}</style></head><body><div class="hero"><h1>Üretim Performans Merkezi — Yönetici Raporu</h1><p>${esc(range)} • ${fmtNum(rows.length)} üretim kaydı</p></div>${parts.join('')}<div class="footer-note">Rapor, Rapor Merkezi'ndeki seçili tarih ve filtreler üzerinden üretilmiştir. İş emri detay listesi bilinçli olarak PDF kapsamına alınmaz.</div></body></html>`;
    if(isAndroidNative()&&window.AndroidApp&&typeof window.AndroidApp.printHtml==='function'){
      const ok=window.AndroidApp.printHtml('Uretim Performans Raporu',doc);
      if(ok===false)throw new Error('Android PDF köprüsü raporu kabul etmedi.');
      closePdfReportModal();return;
    }
    const w=window.open('','_blank');if(!w)throw new Error('Yazdırma penceresi engellendi.');w.document.write(doc.replace('</body>','<script>window.onload=()=>setTimeout(()=>window.print(),250)<\\/script></body>'));w.document.close();closePdfReportModal();
  }catch(err){smartPrintError(err);}
}

'''
html=html.replace(anchor,js+anchor,1)

# Bind presets and PDF output to v1.7.1 implementations.
html=html.replace("qsa('[data-close-pdfreport]').forEach(x=>x.onclick=closePdfReportModal); qsa('[data-pdf-preset]').forEach(x=>x.onclick=()=>setPdfPreset(x.dataset.pdfPreset)); if($('createSmartPdfBtn'))$('createSmartPdfBtn').onclick=printSmartReportV151;","qsa('[data-close-pdfreport]').forEach(x=>x.onclick=closePdfReportModal); qsa('[data-pdf-preset]').forEach(x=>x.onclick=()=>setPdfPresetV171(x.dataset.pdfPreset)); if($('createSmartPdfBtn'))$('createSmartPdfBtn').onclick=printSmartReportV171;",1)

# Visible version marker.
html=html.replace('v1.7.0-report-command','v1.7.1-pdf-production-fix',1)
p.write_text(html,encoding='utf-8')
print('patched-v171',len(html))
