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
function nativePrintStarted(){toast('Android yazdırma ekranı açılıyor...');}
function nativePrintFailed(message){alert('Android yazdırma ekranı açılamadı.\n\nTeknik ayrıntı: '+String(message||'Bilinmeyen hata'));}
'''
html=html.replace(marker,helper+'\n'+marker,1)

start=html.find('function printSmartReportV140(){')
end=html.find('\n\nfunction printReportFullV130()',start)
if start<0 or end<0:
    raise SystemExit('smart print function block missing')
old=html[start:end]
body=old[len('function printSmartReportV140(){'):]
if body.endswith('}'):
    body=body[:-1]
old_tail="""  try{
    if(isAndroidNative()&&window.AndroidApp){toast('Yazdırma penceresi hazırlanıyor...');window.AndroidApp.printHtml('Uretim Performans Raporu',doc);closePdfReportModal();return;}
    const w=window.open('','_blank');if(!w){toast('Yazdırma penceresi engellendi.');return}w.document.write(doc.replace('</body>','<script>window.onload=()=>setTimeout(()=>window.print(),250)<\\/script></body>'));w.document.close();closePdfReportModal();
  }catch(err){console.error(err);alert('PDF / Yazdır işlemi başlatılamadı.\\n\\nTeknik ayrıntı: '+((err&&err.message)?err.message:String(err)));}
"""
new_tail="""  if(isAndroidNative()&&window.AndroidApp&&typeof window.AndroidApp.printHtml==='function'){toast('Rapor hazırlanıyor...');const accepted=window.AndroidApp.printHtml('Uretim Performans Raporu',doc);if(accepted===false)throw new Error('Android yazdırma köprüsü isteği kabul etmedi.');closePdfReportModal();return;}
  const w=window.open('','_blank');if(!w)throw new Error('Yazdırma penceresi engellendi.');w.document.write(doc.replace('</body>','<script>window.onload=()=>setTimeout(()=>window.print(),250)<\\/script></body>'));w.document.close();closePdfReportModal();
"""
if old_tail not in body:
    raise SystemExit('smart print tail missing')
body=body.replace(old_tail,new_tail,1)
new='function printSmartReportV151(){\n  try{\n'+body+'\n  }catch(err){smartPrintError(err);}\n}'
html=html[:start]+new+html[end:]
html=html.replace("if($('createSmartPdfBtn'))$('createSmartPdfBtn').onclick=printSmartReportV140;","if($('createSmartPdfBtn'))$('createSmartPdfBtn').onclick=printSmartReportV151;",1)
html=html.replace('v1.5.0-professional-ui','v1.5.1-print-hotfix')
html=html.replace('v1.5.0 • Android / tamamen offline','v1.5.1 • Android / tamamen offline')
p.write_text(html,encoding='utf-8')
print('patched-v151',len(html))
