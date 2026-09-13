from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')
if 'v1.8.0-reportcenter-pdf-command' in html:
    raise SystemExit('already patched')

# Dashboard: replace the former simple summary with a denser command center.
start=html.find('<div class="metric-grid" id="dashboardMetrics"></div>')
end_marker='<div id="dashSummaryNote" class="dashboard-summary-note"></div>'
end=html.find(end_marker,start)
if start<0 or end<0: raise SystemExit('dashboard summary block not found')
end += len(end_marker)
new_dashboard='''<div class="command-kpi-grid" id="dashboardMetrics"></div>
        <div class="command-section-head"><div><div class="eyebrow">MAKİNE DURUM MERKEZİ</div><h2>Makine Nabzı</h2><p>Seçili dönemdeki son kayıt, üretim payı ve kayıp göstergeleri.</p></div><span class="subtle-chip">Detay için karta dokun</span></div>
        <div id="commandMachineGrid" class="command-machine-grid"></div>

        <div class="command-dual-grid">
          <div class="command-block"><div class="command-block-head"><div><div class="eyebrow">VARDİYA YARIŞI</div><h3>1. Vardiya / 2. Vardiya</h3></div></div><div id="commandShiftRace"></div></div>
          <div class="command-block"><div class="command-block-head"><div><div class="eyebrow">OPERASYON DURUMU</div><h3>Bugünün Sağlığı</h3></div></div><div id="commandHealth" class="command-health-grid"></div></div>
        </div>

        <div class="command-section-head"><div><div class="eyebrow">GÖRSEL ÖZET</div><h2>Üretim Akışı</h2><p>Komuta Paneli özet verir; ayrıntılı kırılımlar Rapor Merkezi'ndedir.</p></div></div>
        <div class="dashboard-summary-grid command-chart-grid">
          <button type="button" class="dashboard-summary-panel command-chart-card" data-command-target="general"><h3>Üretim Trendi</h3><p>Günlük net baskı hareketi.</p><div id="dashTrendChart"></div></button>
          <button type="button" class="dashboard-summary-panel command-chart-card" data-command-target="machine"><h3>Makine Üretim Dağılımı</h3><p>Net baskının makinelere dağılımı.</p><div id="dashMachineChart"></div></button>
          <button type="button" class="dashboard-summary-panel command-chart-card" data-command-target="shift"><h3>Vardiya Üretim Dağılımı</h3><p>1. ve 2. vardiya karşılaştırması.</p><div id="dashShiftChart"></div></button>
        </div>

        <div class="command-bottom-grid">
          <div class="command-block command-attention-block"><div class="command-block-head"><div><div class="eyebrow">AKSİYON</div><h3>Dikkat Gerektirenler</h3></div><button type="button" class="btn ghost mini" data-command-target="general">Rapor Merkezi</button></div><div id="commandAttention" class="command-attention-list"></div></div>
          <div id="commandOvertimeCard" class="command-block command-overtime-block"><div class="command-block-head"><div><div class="eyebrow">MESAİ</div><h3>Mesai Özeti</h3></div><button type="button" class="btn ghost mini" data-command-target="overtime">Detay</button></div><div id="commandOvertime"></div></div>
        </div>
        <div id="dashSummaryNote" class="dashboard-summary-note command-summary-note"></div>'''
html=html[:start]+new_dashboard+html[end:]

# PDF chooser: the PDF is now a direct printable snapshot of Report Center, not a second report engine.
pdf_pos=html.find('<div id="pdfReportModal" class="modal hidden">')
card_start=html.find('<div class="modal-card pdf-builder-card">',pdf_pos)
card_end=html.find('  </div>\n\n  <div id="qualityModal"',card_start)
if pdf_pos<0 or card_start<0 or card_end<0: raise SystemExit('pdf modal block not found')
new_card='''<div class="modal-card pdf-builder-card pdf-v180-card">
      <div class="modal-head"><div><div class="eyebrow">RAPOR MERKEZİ PDF</div><h2>Hangi görünümü PDF yapalım?</h2><p>PDF, ekrandaki Rapor Merkezi ile aynı rapor bloklarını, aynı hesaplamaları ve aynı sıralamaları kullanır.</p></div><button class="icon-btn" type="button" data-close-pdfreport>×</button></div>
      <div class="pdf-v180-choice-grid">
        <button id="createActiveReportPdfBtn" class="pdf-v180-choice" type="button"><span>AKTİF RAPOR</span><strong id="pdfActiveReportName">Genel Bakış</strong><small>Şu anda Rapor Merkezi'nde açık olan görünümü PDF yap.</small></button>
        <button id="createAllReportPdfBtn" class="pdf-v180-choice primary-choice" type="button"><span>TÜM RAPOR MERKEZİ</span><strong>Her Şeyi Gör</strong><small>Genel, performans, kayıplar, üretim analizi ve karşılaştırmayı tek PDF'de birleştir.</small></button>
      </div>
      <div class="pdf-note">İş Emri bölümünde uzun detay listesi PDF'ye dökülmez; Rapor Merkezi'ndeki kompakt iş emri özeti kullanılır. Böylece rapor gereksiz yere uzamaz.</div>
      <div class="pdf-actions"><button class="btn ghost" type="button" data-close-pdfreport>Vazgeç</button></div>
    </div>\n'''
html=html[:card_start]+new_card+html[card_end:]

css=r'''
/* v1.8.0 report-center PDF + command center */
.command-kpi-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin:14px 0}.command-kpi{position:relative;overflow:hidden;text-align:left;border:1px solid var(--line);border-radius:15px;background:linear-gradient(155deg,color-mix(in srgb,var(--panel2) 94%,transparent),color-mix(in srgb,var(--panel) 98%,#000));padding:14px 14px 13px;color:var(--text);cursor:pointer;min-height:108px}.command-kpi:before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:var(--accent);opacity:.85}.command-kpi:hover,.command-machine-card:hover,.command-chart-card:hover{border-color:color-mix(in srgb,var(--accent) 55%,var(--line));transform:translateY(-1px)}.command-kpi span{display:block;color:var(--muted);font-size:9px;font-weight:850;letter-spacing:.7px;text-transform:uppercase}.command-kpi strong{display:block;font-size:23px;line-height:1.1;margin-top:9px;letter-spacing:-.5px}.command-kpi small{display:block;color:var(--muted);font-size:9px;margin-top:7px;line-height:1.4}.command-kpi small.good{color:var(--good)}.command-kpi small.bad{color:var(--bad)}.command-kpi small.warn{color:var(--warn)}
.command-section-head{display:flex;align-items:end;justify-content:space-between;gap:14px;margin:20px 2px 10px}.command-section-head h2{font-size:17px;margin:2px 0 3px}.command-section-head p{color:var(--muted);font-size:10px;margin:0}.command-machine-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}.command-machine-card{border:1px solid var(--line);border-radius:16px;background:linear-gradient(145deg,color-mix(in srgb,var(--panel2) 97%,transparent),color-mix(in srgb,var(--panel) 94%,#000));padding:15px;color:var(--text);text-align:left;cursor:pointer}.command-machine-top{display:flex;justify-content:space-between;gap:10px;align-items:center}.command-machine-top strong{font-size:17px}.command-machine-state{font-size:9px;font-weight:850;padding:5px 8px;border-radius:999px;border:1px solid color-mix(in srgb,var(--good) 45%,var(--line));color:var(--good);background:color-mix(in srgb,var(--good) 8%,transparent)}.command-machine-state.empty{color:var(--muted);border-color:var(--line);background:transparent}.command-machine-job{margin:12px 0 10px;padding:10px;border-radius:11px;background:color-mix(in srgb,var(--bg) 48%,transparent);border:1px solid color-mix(in srgb,var(--line) 75%,transparent)}.command-machine-job span{display:block;color:var(--muted);font-size:9px}.command-machine-job strong{display:block;font-size:13px;margin-top:3px}.command-machine-meta{display:grid;grid-template-columns:1fr 1fr;gap:8px}.command-machine-meta div{padding:7px 8px;border-radius:9px;background:color-mix(in srgb,var(--panel2) 60%,transparent)}.command-machine-meta span{display:block;color:var(--muted);font-size:8px;text-transform:uppercase}.command-machine-meta strong{display:block;margin-top:3px;font-size:11px}.command-share-track{height:5px;border-radius:99px;background:color-mix(in srgb,var(--line) 65%,transparent);overflow:hidden;margin-top:11px}.command-share-track i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 55%,#fff))}
.command-dual-grid,.command-bottom-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:12px;margin-top:12px}.command-block{border:1px solid var(--line);border-radius:16px;background:linear-gradient(180deg,color-mix(in srgb,var(--panel2) 92%,transparent),color-mix(in srgb,var(--panel) 97%,transparent));padding:15px}.command-block-head{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:11px}.command-block-head h3{font-size:14px;margin:2px 0 0}.btn.mini{font-size:9px;padding:7px 9px}.command-shift-grid{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:stretch}.command-shift-card{border:1px solid var(--line);border-radius:13px;padding:12px;background:color-mix(in srgb,var(--bg) 35%,transparent);cursor:pointer;color:var(--text);text-align:left}.command-shift-card.active{border-color:color-mix(in srgb,var(--accent) 45%,var(--line))}.command-shift-card span{font-size:9px;color:var(--muted)}.command-shift-card>strong{display:block;font-size:20px;margin:5px 0 9px}.command-shift-mini{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}.command-shift-mini div{border-radius:8px;background:color-mix(in srgb,var(--panel2) 65%,transparent);padding:6px}.command-shift-mini small{display:block;color:var(--muted);font-size:8px}.command-shift-mini b{display:block;font-size:10px;margin-top:2px}.command-vs{display:flex;align-items:center;justify-content:center;color:var(--muted);font-weight:900;font-size:10px;letter-spacing:1px}.command-health-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.command-health-item{border:1px solid var(--line);border-radius:11px;padding:10px;background:color-mix(in srgb,var(--bg) 30%,transparent)}.command-health-item span{display:block;color:var(--muted);font-size:8px;text-transform:uppercase}.command-health-item strong{display:block;margin-top:5px;font-size:12px}.command-health-item.good strong{color:var(--good)}.command-health-item.warn strong{color:var(--warn)}.command-health-item.bad strong{color:var(--bad)}.command-health-item small{display:block;color:var(--muted);font-size:8px;margin-top:3px}.command-chart-card{width:100%;color:var(--text);text-align:left;cursor:pointer}.command-chart-card h3,.command-chart-card p{pointer-events:none}.command-attention-list{display:grid;gap:7px}.command-attention-item{display:grid;grid-template-columns:8px 1fr;gap:9px;align-items:start;padding:9px;border-radius:10px;background:color-mix(in srgb,var(--bg) 32%,transparent)}.command-attention-item i{width:7px;height:7px;border-radius:50%;background:var(--accent);margin-top:4px}.command-attention-item.good i{background:var(--good)}.command-attention-item.warn i{background:var(--warn)}.command-attention-item.bad i{background:var(--bad)}.command-attention-item div{font-size:10px;line-height:1.45;color:var(--text)}.command-overtime-kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px}.command-overtime-kpis div{padding:10px;border-radius:10px;background:color-mix(in srgb,var(--bg) 34%,transparent)}.command-overtime-kpis span{display:block;color:var(--muted);font-size:8px}.command-overtime-kpis strong{display:block;font-size:14px;margin-top:4px}.command-summary-note{margin-bottom:18px}.pdf-v180-card{width:min(720px,96vw)}.pdf-v180-choice-grid{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin:16px 0}.pdf-v180-choice{border:1px solid var(--line);border-radius:15px;background:linear-gradient(155deg,var(--panel2),var(--panel));color:var(--text);padding:16px;text-align:left;cursor:pointer;min-height:128px}.pdf-v180-choice:hover{border-color:color-mix(in srgb,var(--accent) 55%,var(--line));transform:translateY(-1px)}.pdf-v180-choice.primary-choice{border-color:color-mix(in srgb,var(--accent) 35%,var(--line));background:linear-gradient(145deg,color-mix(in srgb,var(--accent) 12%,var(--panel2)),var(--panel))}.pdf-v180-choice span{display:block;color:var(--muted);font-size:9px;font-weight:850;letter-spacing:.8px}.pdf-v180-choice strong{display:block;font-size:18px;margin-top:8px}.pdf-v180-choice small{display:block;color:var(--muted);font-size:10px;line-height:1.5;margin-top:8px}
@media(max-width:1120px){.command-kpi-grid{grid-template-columns:repeat(3,1fr)}.command-machine-grid{grid-template-columns:1fr}.command-dual-grid,.command-bottom-grid{grid-template-columns:1fr}}
@media(max-width:680px){.command-kpi-grid{grid-template-columns:repeat(2,1fr)}.command-shift-grid{grid-template-columns:1fr}.command-vs{padding:2px}.pdf-v180-choice-grid{grid-template-columns:1fr}}
'''
html=html.replace('</style>',css+'</style>',1)

anchor='function bindEvents(){'
if anchor not in html: raise SystemExit('bindEvents anchor missing')
js=r'''
function commandDeltaV180(cur,prev,inverse=false){
  if(!prev)return {text:'Önceki dönem verisi yok',tone:''};
  const d=pctChange(cur,prev),good=inverse?d<0:d>0,bad=inverse?d>0:d<0;
  return {text:`${deltaText(d,'%')} önceki döneme göre`,tone:good?'good':bad?'bad':''};
}
function commandKpiV180(label,value,sub,target,tone=''){
  return `<button type="button" class="command-kpi" data-command-target="${target}"><span>${label}</span><strong>${value}</strong><small class="${tone}">${sub||''}</small></button>`;
}
function dashboardAttentionV180(rows,oldRows){
  const out=[],st=statsOf(rows),old=statsOf(oldRows||[]);
  if((oldRows||[]).length){
    const net=pctChange(st.good,old.good),fire=st.rate-old.rate,down=pctChange(st.down,old.down);
    if(net<=-10)out.push(['bad',`Net baskı önceki eşit döneme göre <strong>${Math.abs(net).toLocaleString('tr-TR',{maximumFractionDigits:1})}% azaldı</strong>.`]);
    else if(net>=10)out.push(['good',`Net baskı önceki eşit döneme göre <strong>${net.toLocaleString('tr-TR',{maximumFractionDigits:1})}% arttı</strong>.`]);
    if(fire>=.5)out.push(['bad',`Fire oranı <strong>${fire.toLocaleString('tr-TR',{maximumFractionDigits:2})} puan yükseldi</strong>.`]);
    else if(fire<=-.5)out.push(['good',`Fire oranı <strong>${Math.abs(fire).toLocaleString('tr-TR',{maximumFractionDigits:2})} puan iyileşti</strong>.`]);
    if(down>=20)out.push(['warn',`Toplam duruş önceki döneme göre <strong>${down.toLocaleString('tr-TR',{maximumFractionDigits:1})}% arttı</strong>.`]);
  }
  const machines=enhancedGroupStats(rows,'machineId',state.machines),shifts=enhancedGroupStats(rows,'shiftId',state.shifts),reasons=downtimeStatsCombined(rows);
  const risky=[...machines].filter(x=>x.gross>0).sort((a,b)=>b.rate-a.rate)[0];if(risky&&risky.rate>Math.max(2,st.rate*1.35))out.push(['warn',`Fire açısından dikkat çeken makine <strong>${esc(risky.name)}</strong>: ${fmtPct(risky.rate)}.`]);
  const slow=[...shifts].sort((a,b)=>b.downPerJob-a.downPerJob)[0];if(slow&&slow.downPerJob>0)out.push(['warn',`İş başına en yüksek duruş <strong>${esc(slow.name)}</strong>: ${fmtNum(Math.round(slow.downPerJob))} dk/iş.`]);
  const reason=reasons[0];if(reason&&st.down>0&&reason.value/st.down>=.25)out.push(['warn',`Duruşların <strong>%${Math.round(reason.value*100/st.down)}</strong>'i ${esc(reason.name)} kaynaklı.`]);
  if(!out.length&&rows.length)out.push(['good','Seçili dönemde otomatik eşiklere göre belirgin bir sapma görünmüyor.']);
  return out.slice(0,4);
}
function latestMachineRecordV180(rows,machineId){
  return [...rows].filter(r=>r.machineId===machineId).sort((a,b)=>`${b.date||''} ${b.endTime||b.startTime||''} ${b.updatedAt||''}`.localeCompare(`${a.date||''} ${a.endTime||a.startTime||''} ${a.updatedAt||''}`))[0]||null;
}
function openDashboardReportV180(target,id=''){
  const ref=$('dashDate')?.value||todayISO(),shift=$('dashShift')?.value||'',range=dashboardPeriodRange(ref,dashboardPeriod);
  navTo('reports'); populateSelects();
  if($('reportStart'))$('reportStart').value=range[0];if($('reportEnd'))$('reportEnd').value=range[1];
  if($('reportShiftFilter'))$('reportShiftFilter').value=shift;if($('reportMachineFilter'))$('reportMachineFilter').value='';if($('reportMasterFilter'))$('reportMasterFilter').value='';
  if(target==='machine'){currentReportDetail='performance';reportHubSub.performance='machine';if($('reportMachineFilter'))$('reportMachineFilter').value=id||'';}
  else if(target==='shift'){currentReportDetail='performance';reportHubSub.performance='shift';if(id&&$('reportShiftFilter'))$('reportShiftFilter').value=id;}
  else if(target==='fire'){currentReportDetail='losses';reportHubSub.losses='scrap';}
  else if(target==='downtime'){currentReportDetail='losses';reportHubSub.losses='downtime';}
  else if(target==='overtime'){currentReportDetail='production';reportHubSub.production='overtime';}
  else if(target==='mix'){currentReportDetail='production';reportHubSub.production='mix';}
  else currentReportDetail='general';
  runReport();
}
function bindCommandClicksV180(){
  qsa('[data-command-target]').forEach(el=>el.onclick=()=>openDashboardReportV180(el.dataset.commandTarget,el.dataset.commandId||''));
}
function renderDashboardV180(){
  populateSelects();if(!$('dashDate').value)$('dashDate').value=todayISO();
  const refDate=$('dashDate').value,shiftId=$('dashShift').value,[startDate,endDate]=dashboardPeriodRange(refDate,dashboardPeriod);
  const allRows=state.productionRecords.filter(r=>r.date>=startDate&&r.date<=endDate),rows=allRows.filter(r=>!shiftId||r.shiftId===shiftId);
  const [ps,pe]=previousPeriodRange(startDate,endDate),oldRows=state.productionRecords.filter(r=>r.date>=ps&&r.date<=pe&&(!shiftId||r.shiftId===shiftId));
  const st=statsOf(rows),old=statsOf(oldRows),gross=st.good+st.scrap,fireRate=st.rate;
  if($('dashPeriodLabel'))$('dashPeriodLabel').textContent=`${dashboardPeriodName(dashboardPeriod)} • ${formatRange(startDate,endDate)}${shiftId?' • '+(getById(state.shifts,shiftId)?.name||'Vardiya'):''}`;
  const dNet=commandDeltaV180(st.good,old.good),dGross=commandDeltaV180(gross,old.good+old.scrap),dFire=oldRows.length?{text:`${(fireRate-old.rate)>=0?'+':''}${(fireRate-old.rate).toLocaleString('tr-TR',{maximumFractionDigits:2})} puan önceki döneme göre`,tone:fireRate<=old.rate?'good':'bad'}:{text:'Önceki dönem verisi yok',tone:''},dDown=commandDeltaV180(st.down,old.down,true);
  $('dashboardMetrics').innerHTML=[commandKpiV180('Net Baskı',fmtNum(st.good),dNet.text,'general',dNet.tone),commandKpiV180('Brüt Baskı',fmtNum(gross),dGross.text,'general',dGross.tone),commandKpiV180('Fire Oranı',fmtPct(fireRate),dFire.text,'fire',dFire.tone),commandKpiV180('Toplam Duruş',fmtNum(st.down)+' dk',dDown.text,'downtime',dDown.tone),commandKpiV180('İş Geçiş Sayısı',fmtNum(st.jobs),'benzersiz iş emri','general'),commandKpiV180('Kalıp Adedi',fmtNum(st.plates),st.jobs?`${(st.plates/st.jobs).toLocaleString('tr-TR',{maximumFractionDigits:1})} kalıp / iş`:'kayıt yok','mix')].join('');

  const machineStats=enhancedGroupStats(rows,'machineId',state.machines),shiftStats=enhancedGroupStats(rows,'shiftId',state.shifts),trendStats=groupByPeriod(rows,'day');
  const allGood=Math.max(1,st.good),machines=(state.machines||[]).filter(m=>m.active!==false);
  if($('commandMachineGrid'))$('commandMachineGrid').innerHTML=machines.map(m=>{const x=machineStats.find(v=>v.id===m.id)||{good:0,scrap:0,rate:0,down:0,jobs:0,plates:0},last=latestMachineRecordV180(rows,m.id),share=x.good*100/allGood,sh=getById(state.shifts,last?.shiftId),ma=getById(state.people,last?.masterId);return `<button type="button" class="command-machine-card" data-command-target="machine" data-command-id="${m.id}"><div class="command-machine-top"><strong>${esc(m.name)}</strong><span class="command-machine-state ${last?'':'empty'}">${last?'DÖNEM KAYDI VAR':'KAYIT YOK'}</span></div><div class="command-machine-job"><span>Son İş Emri</span><strong>${esc(last?.workOrder||'-')}</strong><small>${esc(sh?.name||'-')} • ${esc(ma?.name||'Usta bilgisi yok')}</small></div><div class="command-machine-meta"><div><span>Net Baskı</span><strong>${fmtNum(x.good)}</strong></div><div><span>Fire</span><strong>${fmtPct(x.rate)}</strong></div><div><span>Duruş</span><strong>${fmtNum(x.down)} dk</strong></div><div><span>İş</span><strong>${fmtNum(x.jobs)}</strong></div></div><div class="command-share-track"><i style="width:${Math.min(100,share).toFixed(1)}%"></i></div><small>Üretim payı ${fmtPct(share)}</small></button>`}).join('');

  const orderedShifts=(state.shifts||[]).filter(s=>s.active!==false).map(s=>shiftStats.find(x=>x.id===s.id)||{id:s.id,name:s.name,good:0,rate:0,down:0,jobs:0,hourly:0});
  const shiftCards=orderedShifts.slice(0,2).map(x=>`<button type="button" class="command-shift-card" data-command-target="shift" data-command-id="${x.id}"><span>${esc(x.name)}</span><strong>${fmtNum(x.good)} tbk</strong><div class="command-shift-mini"><div><small>Net / Saat</small><b>${x.hourly?fmtNum(Math.round(x.hourly)):'—'}</b></div><div><small>Fire</small><b>${fmtPct(x.rate)}</b></div><div><small>Duruş</small><b>${fmtNum(x.down)} dk</b></div><div><small>İş</small><b>${fmtNum(x.jobs)}</b></div></div></button>`);
  if($('commandShiftRace'))$('commandShiftRace').innerHTML=shiftCards.length?`<div class="command-shift-grid">${shiftCards[0]||''}<div class="command-vs">VS</div>${shiftCards[1]||''}</div>`:'<div class="empty">Vardiya verisi yok.</div>';

  const netDelta=oldRows.length?pctChange(st.good,old.good):0,downDelta=oldRows.length?pctChange(st.down,old.down):0,totalDuration=rows.reduce((a,r)=>a+recordMinutes(r),0),hourly=totalDuration?st.good*60/totalDuration:0,oldDuration=oldRows.reduce((a,r)=>a+recordMinutes(r),0),oldHourly=oldDuration?old.good*60/oldDuration:0,tempoDelta=oldHourly?pctChange(hourly,oldHourly):0;
  const health=[['Üretim',!oldRows.length?'Veri Bekleniyor':netDelta>=-5?'İyi':netDelta>=-12?'Dikkat':'Kritik',!oldRows.length?'karşılaştırma yok':deltaText(netDelta,'%'),!oldRows.length?'':netDelta>=-5?'good':netDelta>=-12?'warn':'bad'],['Fire',!oldRows.length?'Veri Bekleniyor':fireRate<=old.rate+.25?'İyi':fireRate<=old.rate+.7?'Dikkat':'Kritik',fmtPct(fireRate),!oldRows.length?'':fireRate<=old.rate+.25?'good':fireRate<=old.rate+.7?'warn':'bad'],['Duruş',!oldRows.length?'Veri Bekleniyor':downDelta<=10?'İyi':downDelta<=30?'Dikkat':'Kritik',`${fmtNum(st.down)} dk`,!oldRows.length?'':downDelta<=10?'good':downDelta<=30?'warn':'bad'],['Tempo',!hourly?'Veri Yok':!oldRows.length?'Ölçülüyor':tempoDelta>=-5?'İyi':tempoDelta>=-12?'Dikkat':'Kritik',hourly?`${fmtNum(Math.round(hourly))} tbk/s`:'süre verisi yok',!hourly||!oldRows.length?'':tempoDelta>=-5?'good':tempoDelta>=-12?'warn':'bad']];
  if($('commandHealth'))$('commandHealth').innerHTML=health.map(([n,s,v,t])=>`<div class="command-health-item ${t}"><span>${n}</span><strong>${s}</strong><small>${v}</small></div>`).join('');

  if($('dashMachineChart'))$('dashMachineChart').innerHTML=visualBars(machineStats,'good','');if($('dashShiftChart'))$('dashShiftChart').innerHTML=visualBars(shiftStats,'good','');if($('dashTrendChart'))$('dashTrendChart').innerHTML=visualBars(trendStats,'good','');
  const attention=dashboardAttentionV180(rows,oldRows);if($('commandAttention'))$('commandAttention').innerHTML=attention.map(([c,t])=>`<div class="command-attention-item ${c}"><i></i><div>${t}</div></div>`).join('')||'<div class="empty">Dikkat gerektiren bulgu yok.</div>';
  const ot=overtimeRows(rows),otst=statsOf(ot),otCard=$('commandOvertimeCard');if(otCard){otCard.style.display=ot.length?'':'none';if(ot.length&&$('commandOvertime'))$('commandOvertime').innerHTML=`<div class="command-overtime-kpis"><div><span>Net Baskı</span><strong>${fmtNum(otst.good)}</strong></div><div><span>İş Geçişi</span><strong>${fmtNum(otst.jobs)}</strong></div><div><span>Fire</span><strong>${fmtPct(otst.rate)}</strong></div><div><span>Duruş</span><strong>${fmtNum(otst.down)} dk</strong></div></div>`;}
  const bestMachine=machineStats[0],bestShift=shiftStats[0];if($('commandHeroText'))$('commandHeroText').innerHTML=`<strong>${fmtNum(st.good)}</strong> net tabaka • <strong>${fmtPct(fireRate)}</strong> fire • <strong>${fmtNum(st.down)} dk</strong> duruş${bestMachine?` • Lider makine <strong>${esc(bestMachine.name)}</strong>`:''}`;if($('commandPeriodChip'))$('commandPeriodChip').textContent=`${dashboardPeriodName(dashboardPeriod)} • ${formatRange(startDate,endDate)}`;if($('commandStatusChip')){const risky=attention.some(x=>x[0]==='bad');$('commandStatusChip').classList.toggle('good',!risky);$('commandStatusChip').textContent=risky?'● Dikkat Gerekiyor':'● Operasyon Dengeli';}
  if($('dashSummaryNote'))$('dashSummaryNote').innerHTML=`<strong>${dashboardPeriodName(dashboardPeriod)} özet:</strong> ${bestMachine?`Lider makine <strong>${esc(bestMachine.name)}</strong> (${fmtNum(bestMachine.good)} tbk). `:''}${bestShift?`Lider vardiya <strong>${esc(bestShift.name)}</strong> (${fmtNum(bestShift.good)} tbk). `:''}Detaylı karar için kartlara dokunarak Rapor Merkezi'ne geçebilirsin.`;
  bindCommandClicksV180();
}

function reportBlockForPdfV180(view,rows){
  if(view==='general')return executiveOverviewV170(rows);
  if(view==='performance')return performanceHubV170(rows);
  if(view==='losses')return lossesHubV170(rows);
  if(view==='production')return productionHubV171(rows);
  if(view==='compare')return comparisonExtended(rows);
  return allExtendedReport(rows);
}
function cleanReportHtmlForPdfV180(markup){
  const box=document.createElement('div');box.innerHTML=markup;
  box.querySelectorAll('.report-subtabs,button').forEach(x=>x.remove());
  box.querySelectorAll('[onclick],[data-xscope],[data-drill-scope],[data-command-target]').forEach(x=>{x.removeAttribute('onclick');x.removeAttribute('data-xscope');x.removeAttribute('data-drill-scope');x.removeAttribute('data-command-target');});
  return box.innerHTML;
}
function reportCssV180(){return [...document.querySelectorAll('style')].map(x=>x.textContent||'').join('\n')}
function buildReportCenterPdfV180(mode='active'){
  const rows=currentReportRows||[];if(!rows.length)throw new Error('PDF için rapor verisi yok.');
  const view=mode==='all'?'all':(currentReportDetail||'general'),title=mode==='all'?'Tüm Rapor Merkezi':reportDetailLabel(view),range=formatRange($('reportStart').value,$('reportEnd').value),body=cleanReportHtmlForPdfV180(reportBlockForPdfV180(view,rows));
  const extra=`@page{size:A4 landscape;margin:8mm}*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important;box-sizing:border-box}.pdf-report-v180{max-width:none!important;padding:0!important}.pdf-report-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-end;padding:16px 18px;margin-bottom:12px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 12%,var(--panel2)),var(--panel))}.pdf-report-head h1{font-size:21px;margin:3px 0 5px}.pdf-report-head p{margin:0;color:var(--muted);font-size:10px}.pdf-report-head .pdf-meta{text-align:right;color:var(--muted);font-size:9px}.pdf-report-head .pdf-meta strong{display:block;color:var(--text);font-size:12px;margin-bottom:3px}.pdf-report-v180 .report-hub-intro,.pdf-report-v180 .xreport-section-title,.pdf-report-v180 .attention-panel,.pdf-report-v180 .hub-section,.pdf-report-v180 .xreport-panel,.pdf-report-v180 .xreport-card,.pdf-report-v180 .decision-kpi{break-inside:avoid}.pdf-report-v180 .workorder-open-panel{display:none!important}.pdf-report-v180 .all-group-divider{break-before:auto}body{margin:0!important;padding:0!important;background:var(--bg)!important;color:var(--text)!important}`;
  return `<!doctype html><html><head><meta charset="utf-8"><title>${esc(title)}</title><style>${reportCssV180()}\n${extra}</style></head><body data-app-theme="${esc(currentTheme())}"><div class="pdf-report-v180"><div class="pdf-report-head"><div><div class="eyebrow">ÜRETİM PERFORMANS MERKEZİ</div><h1>${esc(title)}</h1><p>Rapor Merkezi'nin aynı hesaplama ve görsel bloklarından üretilmiştir.</p></div><div class="pdf-meta"><strong>${esc(range)}</strong>${fmtNum(rows.length)} üretim kaydı</div></div>${body}</div></body></html>`;
}
function createReportCenterPdfV180(mode){
  try{
    const title=mode==='all'?'Uretim Performans - Tum Rapor Merkezi':`Uretim Performans - ${reportDetailLabel(currentReportDetail||'general')}`,doc=buildReportCenterPdfV180(mode);
    if(isAndroidNative()&&window.AndroidApp&&typeof window.AndroidApp.printHtml==='function'){const ok=window.AndroidApp.printHtml(title,doc);if(ok===false)throw new Error('Android PDF köprüsü raporu kabul etmedi.');closePdfReportModal();return;}
    const w=window.open('','_blank');if(!w)throw new Error('PDF penceresi engellendi.');w.document.write(doc.replace('</body>','<script>window.onload=()=>setTimeout(()=>window.print(),350)<\\/script></body>'));w.document.close();closePdfReportModal();
  }catch(err){smartPrintError(err)}
}
function openPdfReportModalV180(){
  if(!(currentReportRows||[]).length){toast('PDF için rapor verisi yok.');return}
  if($('pdfActiveReportName'))$('pdfActiveReportName').textContent=reportDetailLabel(currentReportDetail||'general');
  if($('createActiveReportPdfBtn'))$('createActiveReportPdfBtn').onclick=()=>createReportCenterPdfV180('active');
  if($('createAllReportPdfBtn'))$('createAllReportPdfBtn').onclick=()=>createReportCenterPdfV180('all');
  $('pdfReportModal').classList.remove('hidden');
}
renderDashboard=renderDashboardV180;
openPdfReportModal=openPdfReportModalV180;
'''
html=html.replace(anchor,js+'\n'+anchor,1)

# v1.8 marker for workflow validation.
html=html.replace('</body>','<div id="v180Marker" data-version="v1.8.0-reportcenter-pdf-command" style="display:none"></div></body>',1)
p.write_text(html,encoding='utf-8')
print('patched-v180',len(html))
