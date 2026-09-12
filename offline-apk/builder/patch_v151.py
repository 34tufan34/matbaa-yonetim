from pathlib import Path
p=Path('app/src/main/assets/index.html')
html=p.read_text(encoding='utf-8')

marker='function openPdfReportModal(){'
if marker not in html:
    raise SystemExit('openPdfReportModal marker missing')
helper=r'''
function plateColorStats(rows){
  const groups=new Map();
  for(const r of rows||[]){
    let key='unknown';
    const explicit=Number(r.colors||0),plates=Number(r.plateQty||0);
    if(explicit>0)key=String(Math.round(explicit));
    else if(plates>0)key=String(Math.round(plates));
    if(!groups.has(key))groups.set(key,[]);
    groups.get(key).push(r);
  }
  return [...groups.entries()].map(([key,rr])=>{
    const s=statsOf(rr);
    return {id:key,name:key==='unknown'?'Renk/Kalıp Belirtilmemiş':key+' Renk',rows:rr,...s};
  }).sort((a,b)=>a.id==='unknown'?1:b.id==='unknown'?-1:Number(a.id)-Number(b.id));
}
function smartPrintError(err){
  console.error(err);
  const msg=(err&&err.message)?err.message:String(err||'Bilinmeyen hata');
  alert('PDF / Yazdır işlemi başlatılamadı.\n\nTeknik ayrıntı: '+msg);
}
function printSmartReportV151(){
  try{return printSmartReportV140();}
  catch(err){smartPrintError(err);}
}
'''
html=html.replace(marker,helper+'\n'+marker,1)

bind="if($('createSmartPdfBtn'))$('createSmartPdfBtn').onclick=printSmartReportV140;"
if bind not in html:
    raise SystemExit('smart PDF button binding missing')
html=html.replace(bind,"if($('createSmartPdfBtn'))$('createSmartPdfBtn').onclick=printSmartReportV151;",1)
html=html.replace('v1.5.0-professional-ui','v1.5.1-print-hotfix')
html=html.replace('v1.5.0 • Android / tamamen offline','v1.5.1 • Android / tamamen offline')
p.write_text(html,encoding='utf-8')
print('patched-v151',len(html))
