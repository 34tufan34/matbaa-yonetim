package com.tufanprintops.uretimperformans;

import android.app.Activity;
import android.print.PrintManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {
    private static final int REQ_FILE_CHOOSER = 2201;
    private static final int REQ_SAVE_FILE = 2202;

    private WebView webView;
    private WebView printWebView;
    private ValueCallback<Uri[]> fileCallback;
    private String pendingSaveText;
    private String pendingSaveName;
    private String pendingSaveMime;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(9, 11, 16));
        getWindow().setNavigationBarColor(Color.rgb(9, 11, 16));
        webView = new WebView(this);
        setContentView(webView);
        configureWebView();
        loadEmbeddedApp();
    }

    private void configureWebView() {
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowContentAccess(true);
        s.setAllowFileAccess(false);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);

        webView.setBackgroundColor(Color.rgb(9, 11, 16));
        webView.addJavascriptInterface(new AndroidBridge(), "AndroidApp");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                return !("app.local".equals(u.getHost()));
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = filePathCallback;
                Intent intent;
                try {
                    intent = fileChooserParams.createIntent();
                } catch (Exception e) {
                    intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("*/*");
                }
                try {
                    startActivityForResult(intent, REQ_FILE_CHOOSER);
                } catch (Exception e) {
                    fileCallback.onReceiveValue(null);
                    fileCallback = null;
                    return false;
                }
                return true;
            }
        });
    }

    private void loadEmbeddedApp() {
        try {
            InputStream in = getAssets().open("index.html");
            BufferedReader br = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) sb.append(line).append('\n');
            br.close();
            String html = patchHtmlForAndroid(sb.toString());
            webView.loadDataWithBaseURL("https://app.local/", html, "text/html", "UTF-8", null);
        } catch (Exception e) {
            webView.loadData("<h2>Uygulama dosyası açılamadı.</h2><pre>" + e.getMessage() + "</pre>", "text/html", "UTF-8");
        }
    }

    private static final String QUALITY_PATCH = """
function recordSnapshot(r){if(!r)return null;return {date:r.date||'',shiftId:r.shiftId||'',machineId:r.machineId||'',masterId:r.masterId||'',workOrder:r.workOrder||'',goodQty:Number(r.goodQty||0),plateQty:Number(r.plateQty||0),scrapQty:Number(r.scrapQty||0),scrapReasonId:r.scrapReasonId||'',downtimeMin:Number(r.downtimeMin||0),downtimeReasonId:r.downtimeReasonId||'',colors:r.colors??null,uvLak:r.uvLak??null,lak:r.lak??null,note:r.note||''};}
async function logAudit(action,row,before,after,note=''){await dbPut('auditLogs',{id:uid(),createdAt:new Date().toISOString(),action,recordId:row?.id||'',workOrder:row?.workOrder||'',before:before||null,after:after||null,note:note||''});}
function qualityLabel(s){return s==='critical'?'Kritik':s==='warn'?'Kontrol':'Normal';}
function assessRecord(r){const issues=[];const add=(severity,message)=>issues.push({severity,message});const good=Number(r.goodQty||0),scrap=Number(r.scrapQty||0),down=Number(r.downtimeMin||0),total=good+scrap,rate=total?scrap*100/total:0;if(!r.date||!r.shiftId||!r.machineId||!String(r.workOrder||'').trim())add('critical','Temel kayıt alanlarından biri eksik.');if(!r.masterId||!getById(state.people,r.masterId))add('warn','Usta bilgisi belirtilmemiş.');if(rate>=10)add('critical','Fire oranı çok yüksek: '+fmtPct(rate)+'.');else if(rate>=5)add('warn','Fire oranı yüksek: '+fmtPct(rate)+'.');if(scrap>0&&!r.scrapReasonId)add('warn','Fire var ancak fire nedeni seçilmemiş.');if(down>0&&!r.downtimeReasonId&&!r.downtimeBreakdown)add('warn','Duruş var ancak duruş nedeni seçilmemiş.');if(Number(r.jobDurationMin||0)>0&&down>Number(r.jobDurationMin||0))add('critical','Duruş süresi iş süresini aşıyor.');const dup=state.productionRecords.some(x=>x.id!==r.id&&x.date===r.date&&x.shiftId===r.shiftId&&x.machineId===r.machineId&&String(x.workOrder||'')===String(r.workOrder||'')&&Number(x.goodQty||0)===good);if(dup)add('warn','Benzer/mükerrer kayıt bulundu.');(r.dataQualityWarnings||[]).forEach(w=>add('warn',String(w)));return {severity:issues.some(x=>x.severity==='critical')?'critical':issues.length?'warn':'ok',issues};}
function renderQualityDashboard(rows){if(!$('qualityDashboard'))return;const q=rows.map(assessRecord),c=q.filter(x=>x.severity==='critical').length,w=q.filter(x=>x.severity==='warn').length,o=q.filter(x=>x.severity==='ok').length;$('qualityDashboard').innerHTML='<div class="quality-card"><span>Toplam Kayıt</span><strong>'+fmtNum(rows.length)+'</strong><small>Seçili filtre</small></div><div class="quality-card critical"><span>Kritik</span><strong>'+fmtNum(c)+'</strong><small>Öncelikli kontrol</small></div><div class="quality-card warn"><span>Kontrol</span><strong>'+fmtNum(w)+'</strong><small>Şüpheli / eksik</small></div><div class="quality-card good"><span>Normal</span><strong>'+fmtNum(o)+'</strong><small>Kontrolden geçti</small></div>';}
function updateSelectionUi(){if($('selectionCount'))$('selectionCount').textContent=selectedRecordIds.size+' kayıt seçildi';if($('bulkApplyBtn'))$('bulkApplyBtn').disabled=selectedRecordIds.size===0;}
async function bulkApplyCorrection(){const ids=[...selectedRecordIds];if(!ids.length){toast('Önce en az bir kayıt seç.');return;}const masterId=$('bulkMaster')?.value||'',shiftId=$('bulkShift')?.value||'',machineId=$('bulkMachine')?.value||'';if(!masterId&&!shiftId&&!machineId){toast('Değiştirilecek usta, vardiya veya makineyi seç.');return;}if(!confirm(ids.length+' seçili kayıt güncellenecek. Devam edilsin mi?'))return;let changed=0;for(const id of ids){const r=getById(state.productionRecords,id);if(!r)continue;const before=recordSnapshot(r),next={...r};if(masterId)next.masterId=masterId;if(shiftId)next.shiftId=shiftId;if(machineId)next.machineId=machineId;next.updatedAt=new Date().toISOString();await dbPut('productionRecords',next);await logAudit('Toplu düzeltme',next,before,recordSnapshot(next),'Toplu usta/vardiya/makine düzeltmesi.');changed++;}selectedRecordIds.clear();if($('bulkMaster'))$('bulkMaster').value='';if($('bulkShift'))$('bulkShift').value='';if($('bulkMachine'))$('bulkMachine').value='';await loadState();renderRecords();renderDashboard();runReport();toast(changed+' kayıt güncellendi.');}
function openQualityModal(id){const r=getById(state.productionRecords,id);if(!r)return;const q=assessRecord(r);$('qualityModalSubtitle').textContent=(r.date||'-')+' • '+(getById(state.machines,r.machineId)?.name||'-')+' • '+(r.workOrder||'İş emri yok');$('qualityModalBody').innerHTML='<div class="quality-detail-head"><span class="quality-badge '+q.severity+'">'+qualityLabel(q.severity)+'</span><strong>'+q.issues.length+' kontrol notu</strong></div><div class="quality-issues">'+(q.issues.length?q.issues.map(x=>'<div class="quality-issue '+x.severity+'">'+esc(x.message)+'</div>').join(''):'<div class="quality-issue">Belirgin veri kalite sorunu bulunmadı.</div>')+'</div>';$('qualityModal').classList.remove('hidden');}
async function restoreTrashRecord(id){const t=state.recycleBin.find(x=>x.id===id);if(!t?.record)return;await dbPut('productionRecords',{...t.record,updatedAt:new Date().toISOString()});await dbDelete('recycleBin',id);await loadState();renderRecords();renderDashboard();runReport();toast('Kayıt geri alındı.');}
async function purgeTrashRecord(id){if(!confirm('Bu kayıt kalıcı olarak silinsin mi?'))return;await dbDelete('recycleBin',id);await loadState();renderAuditAndTrash();}
function renderAuditAndTrash(){if($('auditList')){const a=[...state.auditLogs].sort((x,y)=>String(y.createdAt||'').localeCompare(String(x.createdAt||''))).slice(0,30);$('auditList').innerHTML=a.length?a.map(x=>'<div class="audit-row"><div><strong>'+esc(x.action||'Değişiklik')+(x.workOrder?' • '+esc(x.workOrder):'')+'</strong><span>'+(x.createdAt?new Date(x.createdAt).toLocaleString('tr-TR'):'-')+'</span></div></div>').join(''):'<div class="empty">Henüz değişiklik geçmişi yok.</div>';}if($('trashList')){const t=[...state.recycleBin].sort((x,y)=>String(y.deletedAt||'').localeCompare(String(x.deletedAt||''))).slice(0,30);$('trashList').innerHTML=t.length?t.map(x=>'<div class="trash-row"><div><strong>'+esc(x.record?.workOrder||'İş emri yok')+'</strong><span>'+esc(x.record?.date||'-')+'</span></div><div class="trash-actions"><button type="button" data-restore-trash="'+x.id+'">Geri Al</button><button type="button" data-purge-trash="'+x.id+'">Kalıcı Sil</button></div></div>').join(''):'<div class="empty">Silinen kayıt yok.</div>';qsa('[data-restore-trash]').forEach(b=>b.onclick=()=>restoreTrashRecord(b.dataset.restoreTrash));qsa('[data-purge-trash]').forEach(b=>b.onclick=()=>purgeTrashRecord(b.dataset.purgeTrash));}}
""";

    private String patchHtmlForAndroid(String html) {
        html = html.replace("v0.9.0", "v0.9.2");
        html = html.replace("const raw=localStorage.getItem(lsKey(name));", "const raw=isAndroidNative()?AndroidApp.readStore(name):localStorage.getItem(lsKey(name));");
        html = html.replace("function lsWrite(name,rows){ localStorage.setItem(lsKey(name),JSON.stringify(rows)); }", "function lsWrite(name,rows){ if(isAndroidNative()){ if(AndroidApp.writeStore(name,JSON.stringify(rows))!==true) throw new Error('Android yerel veri yazılamadı: '+name); return; } localStorage.setItem(lsKey(name),JSON.stringify(rows)); }");
        html = html.replace("return new Promise((resolve)=>{\n    if(!('indexedDB' in window))", "return new Promise((resolve)=>{\n    if(isAndroidNative()){ storageMode='localStorage'; db=null; return resolve(null); }\n    if(!('indexedDB' in window))");
        html = html.replace("else if(storageMode==='localStorage') el.innerHTML='<span style=\"background:#f0b84b\"></span> Uyumlu offline depolama';", "else if(storageMode==='localStorage') el.innerHTML=isAndroidNative()?'<span></span> Yerel veri hazır • APK':'<span style=\"background:#f0b84b\"></span> Uyumlu offline depolama';");
        html = html.replace("const s=ANDROID_EMBEDDED_SEED;\n  for(const row of s.people) await dbPut('people',row);", "const s=ANDROID_EMBEDDED_SEED;\n  if(isAndroidNative()){\n    AndroidApp.writeStore('people',JSON.stringify(s.people||[]));\n    AndroidApp.writeStore('machines',JSON.stringify(s.machines||[]));\n    AndroidApp.writeStore('shifts',JSON.stringify(s.shifts||[]));\n    AndroidApp.writeStore('scrapReasons',JSON.stringify(s.scrapReasons||[]));\n    AndroidApp.writeStore('downtimeReasons',JSON.stringify(s.downtimeReasons||[]));\n    AndroidApp.writeStore('productionRecords',JSON.stringify(s.productionRecords||[]));\n    AndroidApp.writeStore('settings',JSON.stringify([state.settings&&state.settings.id?state.settings:defaultSettings()]));\n    AndroidApp.writeStore('meta',JSON.stringify([{id:'meta',lastBackupAt:null,recordsAtBackup:0,seedVersion:s.version,seedAppliedAt:new Date().toISOString()}]));\n    await loadState(); return true;\n  }\n  for(const row of s.people) await dbPut('people',row);");
        html = html.replace("alert('Yerel depolama başlatılamadı. Uygulamayı kapatıp yeniden açın. Sorun sürerse yedek dosyanızı koruyun.');", "alert('Yerel depolama başlatılamadı.\\n\\nTeknik ayrıntı: '+((err&&err.message)?err.message:String(err||'Bilinmeyen hata')));");
        if (!html.contains("function recordSnapshot(r){")) html = html.replace("function filteredRecords(){", QUALITY_PATCH + "\nfunction filteredRecords(){");
        return html;
    }

    private File storageDir() throws Exception {
        File dir = new File(getFilesDir(), "offline-store");
        if (!dir.exists() && !dir.mkdirs()) throw new Exception("Yerel veri klasörü oluşturulamadı");
        return dir;
    }

    private File storeFile(String name) throws Exception {
        if (name == null || !name.matches("[A-Za-z0-9_-]{1,64}")) throw new Exception("Geçersiz veri alanı");
        return new File(storageDir(), name + ".json");
    }

    private synchronized String readStoreFile(String name) {
        try {
            File file = storeFile(name);
            if (!file.exists()) return "[]";
            try (FileInputStream in = new FileInputStream(file); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
                byte[] buf = new byte[8192]; int n;
                while ((n = in.read(buf)) >= 0) out.write(buf, 0, n);
                String text = out.toString(StandardCharsets.UTF_8.name()).trim();
                return text.isEmpty() ? "[]" : text;
            }
        } catch (Exception e) { return "[]"; }
    }

    private synchronized boolean writeStoreFile(String name, String json) {
        try {
            File target = storeFile(name);
            File tmp = new File(target.getParentFile(), target.getName() + ".tmp");
            byte[] bytes = (json == null || json.trim().isEmpty() ? "[]" : json).getBytes(StandardCharsets.UTF_8);
            try (FileOutputStream out = new FileOutputStream(tmp, false)) {
                out.write(bytes); out.flush(); out.getFD().sync();
            }
            if (target.exists() && !target.delete()) return false;
            return tmp.renameTo(target);
        } catch (Exception e) { return false; }
    }

    public class AndroidBridge {
        @JavascriptInterface public String getVersion() { return "0.9.2"; }
        @JavascriptInterface public boolean isOfflineApp() { return true; }
        @JavascriptInterface public String readStore(String name) { return readStoreFile(name); }
        @JavascriptInterface public boolean writeStore(String name, String json) { return writeStoreFile(name, json); }

        @JavascriptInterface
        public void saveTextFile(String fileName, String mimeType, String content) {
            runOnUiThread(() -> {
                pendingSaveName = sanitizeFileName(fileName);
                pendingSaveMime = (mimeType == null || mimeType.isEmpty()) ? "text/plain" : mimeType;
                pendingSaveText = content == null ? "" : content;
                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType(pendingSaveMime);
                intent.putExtra(Intent.EXTRA_TITLE, pendingSaveName);
                startActivityForResult(intent, REQ_SAVE_FILE);
            });
        }

        @JavascriptInterface
        public void printHtml(String title, String html) {
            runOnUiThread(() -> {
                printWebView = new WebView(MainActivity.this);
                printWebView.getSettings().setJavaScriptEnabled(false);
                printWebView.setWebViewClient(new WebViewClient() {
                    @Override public void onPageFinished(WebView view, String url) {
                        PrintManager pm = (PrintManager) getSystemService(Context.PRINT_SERVICE);
                        String job = (title == null || title.trim().isEmpty()) ? "Üretim Raporu" : title;
                        pm.print(job, view.createPrintDocumentAdapter(job), null);
                    }
                });
                printWebView.loadDataWithBaseURL("https://print.local/", html, "text/html", "UTF-8", null);
            });
        }
    }

    private String sanitizeFileName(String n) {
        if (n == null || n.trim().isEmpty()) return "uretim_performans_yedek.json";
        return n.replaceAll("[\\\\/:*?\"<>|]", "_");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQ_FILE_CHOOSER) {
            if (fileCallback != null) {
                Uri[] results = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
                fileCallback.onReceiveValue(results);
                fileCallback = null;
            }
            return;
        }
        if (requestCode == REQ_SAVE_FILE) {
            boolean ok = false;
            if (resultCode == RESULT_OK && data != null && data.getData() != null && pendingSaveText != null) {
                try (OutputStream out = getContentResolver().openOutputStream(data.getData(), "w")) {
                    if (out != null) { out.write(pendingSaveText.getBytes(StandardCharsets.UTF_8)); out.flush(); ok = true; }
                } catch (Exception ignored) {}
            }
            final boolean saved = ok; final String name = pendingSaveName;
            pendingSaveText = null; pendingSaveName = null; pendingSaveMime = null;
            webView.post(() -> webView.evaluateJavascript(saved ? "nativeFileSaved(" + jsQuote(name) + ")" : "nativeFileSaveCancelled()", null));
        }
    }

    private String jsQuote(String s) {
        if (s == null) return "''";
        return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "") + "'";
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack(); else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) { webView.removeJavascriptInterface("AndroidApp"); webView.destroy(); }
        if (printWebView != null) printWebView.destroy();
        super.onDestroy();
    }
}
