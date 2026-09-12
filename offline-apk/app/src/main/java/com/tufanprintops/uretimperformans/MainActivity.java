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

    private String patchHtmlForAndroid(String html) {
        html = html.replace("v0.9.0", "v0.9.1");
        html = html.replace(
                "const raw=localStorage.getItem(lsKey(name));",
                "const raw=isAndroidNative()?AndroidApp.readStore(name):localStorage.getItem(lsKey(name));"
        );
        html = html.replace(
                "function lsWrite(name,rows){ localStorage.setItem(lsKey(name),JSON.stringify(rows)); }",
                "function lsWrite(name,rows){ if(isAndroidNative()){ if(AndroidApp.writeStore(name,JSON.stringify(rows))!==true) throw new Error('Android yerel veri yazılamadı: '+name); return; } localStorage.setItem(lsKey(name),JSON.stringify(rows)); }"
        );
        html = html.replace(
                "return new Promise((resolve)=>{\n    if(!('indexedDB' in window))",
                "return new Promise((resolve)=>{\n    if(isAndroidNative()){ storageMode='localStorage'; db=null; return resolve(null); }\n    if(!('indexedDB' in window))"
        );
        html = html.replace(
                "else if(storageMode==='localStorage') el.innerHTML='<span style=\"background:#f0b84b\"></span> Uyumlu offline depolama';",
                "else if(storageMode==='localStorage') el.innerHTML=isAndroidNative()?'<span></span> Yerel veri hazır • APK':'<span style=\"background:#f0b84b\"></span> Uyumlu offline depolama';"
        );
        html = html.replace(
                "const s=ANDROID_EMBEDDED_SEED;\n  for(const row of s.people) await dbPut('people',row);",
                "const s=ANDROID_EMBEDDED_SEED;\n  if(isAndroidNative()){\n    AndroidApp.writeStore('people',JSON.stringify(s.people||[]));\n    AndroidApp.writeStore('machines',JSON.stringify(s.machines||[]));\n    AndroidApp.writeStore('shifts',JSON.stringify(s.shifts||[]));\n    AndroidApp.writeStore('scrapReasons',JSON.stringify(s.scrapReasons||[]));\n    AndroidApp.writeStore('downtimeReasons',JSON.stringify(s.downtimeReasons||[]));\n    AndroidApp.writeStore('productionRecords',JSON.stringify(s.productionRecords||[]));\n    AndroidApp.writeStore('settings',JSON.stringify([state.settings&&state.settings.id?state.settings:defaultSettings()]));\n    AndroidApp.writeStore('meta',JSON.stringify([{id:'meta',lastBackupAt:null,recordsAtBackup:0,seedVersion:s.version,seedAppliedAt:new Date().toISOString()}]));\n    await loadState(); return true;\n  }\n  for(const row of s.people) await dbPut('people',row);"
        );
        html = html.replace(
                "alert('Yerel depolama başlatılamadı. Uygulamayı kapatıp yeniden açın. Sorun sürerse yedek dosyanızı koruyun.');",
                "alert('Yerel depolama başlatılamadı.\\n\\nTeknik ayrıntı: '+((err&&err.message)?err.message:String(err||'Bilinmeyen hata')));"
        );
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
                byte[] buf = new byte[8192];
                int n;
                while ((n = in.read(buf)) >= 0) out.write(buf, 0, n);
                String text = out.toString(StandardCharsets.UTF_8.name()).trim();
                return text.isEmpty() ? "[]" : text;
            }
        } catch (Exception e) {
            return "[]";
        }
    }

    private synchronized boolean writeStoreFile(String name, String json) {
        try {
            File target = storeFile(name);
            File tmp = new File(target.getParentFile(), target.getName() + ".tmp");
            byte[] bytes = (json == null || json.trim().isEmpty() ? "[]" : json).getBytes(StandardCharsets.UTF_8);
            try (FileOutputStream out = new FileOutputStream(tmp, false)) {
                out.write(bytes);
                out.flush();
                out.getFD().sync();
            }
            if (target.exists() && !target.delete()) return false;
            if (!tmp.renameTo(target)) return false;
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public class AndroidBridge {
        @JavascriptInterface
        public String getVersion() { return "0.9.1"; }

        @JavascriptInterface
        public boolean isOfflineApp() { return true; }

        @JavascriptInterface
        public String readStore(String name) { return readStoreFile(name); }

        @JavascriptInterface
        public boolean writeStore(String name, String json) { return writeStoreFile(name, json); }

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
                    @Override
                    public void onPageFinished(WebView view, String url) {
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
                    if (out != null) {
                        out.write(pendingSaveText.getBytes(StandardCharsets.UTF_8));
                        out.flush();
                        ok = true;
                    }
                } catch (Exception ignored) {}
            }
            final boolean saved = ok;
            final String name = pendingSaveName;
            pendingSaveText = null;
            pendingSaveName = null;
            pendingSaveMime = null;
            webView.post(() -> webView.evaluateJavascript(
                    saved ? "nativeFileSaved(" + jsQuote(name) + ")" : "nativeFileSaveCancelled()",
                    null
            ));
        }
    }

    private String jsQuote(String s) {
        if (s == null) return "''";
        return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "") + "'";
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.removeJavascriptInterface("AndroidApp");
            webView.destroy();
        }
        if (printWebView != null) printWebView.destroy();
        super.onDestroy();
    }
}
