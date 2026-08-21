package com.patrolambalaj.baskitakip;

import android.app.Activity;
import android.app.DownloadManager;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.print.PrintDocumentAdapter;
import android.print.PrintManager;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.MimeTypeMap;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.core.content.FileProvider;

import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class MainActivity extends Activity {
    private static final String APP_URL = "https://matbaa-baski-takip.gamzekomurcu9.chatgpt.site/";
    private static final String APP_HOST = "matbaa-baski-takip.gamzekomurcu9.chatgpt.site";
    private static final int FILE_CHOOSER_REQUEST = 1201;

    private WebView webView;
    private ProgressBar progressBar;
    private ValueCallback<Uri[]> pendingFileCallback;
    private Uri pendingCameraUri;
    private File pendingCameraFile;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(11, 24, 38));
        getWindow().setNavigationBarColor(Color.rgb(11, 24, 38));

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.rgb(11, 24, 38));

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(11, 24, 38));
        root.addView(webView, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));

        progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setMax(100);
        FrameLayout.LayoutParams progressParams = new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                Math.max(3, Math.round(getResources().getDisplayMetrics().density * 3))
        );
        progressParams.gravity = Gravity.TOP;
        root.addView(progressBar, progressParams);

        setContentView(root);
        configureWebView();
        webView.loadUrl(APP_URL);
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccess(true);
        settings.setLoadsImagesAutomatically(true);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setUserAgentString(settings.getUserAgentString() + " PatrolBaskiTakipAPK/1.0.0");

        CookieManager cookies = CookieManager.getInstance();
        cookies.setAcceptCookie(true);
        cookies.setAcceptThirdPartyCookies(webView, true);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WebView.startSafeBrowsing(this, null);
        }

        webView.addJavascriptInterface(new PatrolAndroidBridge(), "PatrolAndroid");
        webView.setWebViewClient(new PatrolWebViewClient());
        webView.setWebChromeClient(new PatrolWebChromeClient());
        webView.setDownloadListener(this::handleDownload);
    }

    private final class PatrolWebViewClient extends WebViewClient {
        @Override
        public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
            progressBar.setProgress(5);
            progressBar.setVisibility(View.VISIBLE);
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            progressBar.setVisibility(View.GONE);
            if (isTrustedUrl(Uri.parse(url))) {
                view.evaluateJavascript(nativeBridgeScript(), null);
            }
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            return handleNavigation(request.getUrl());
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            return handleNavigation(Uri.parse(url));
        }

        @Override
        public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
            if (request.isForMainFrame()) {
                progressBar.setVisibility(View.GONE);
                showOfflinePage();
            }
        }
    }

    private final class PatrolWebChromeClient extends WebChromeClient {
        @Override
        public void onProgressChanged(WebView view, int progress) {
            progressBar.setProgress(progress);
            progressBar.setVisibility(progress >= 100 ? View.GONE : View.VISIBLE);
        }

        @Override
        public boolean onShowFileChooser(
                WebView view,
                ValueCallback<Uri[]> filePathCallback,
                FileChooserParams fileChooserParams
        ) {
            if (pendingFileCallback != null) {
                pendingFileCallback.onReceiveValue(null);
            }
            pendingFileCallback = filePathCallback;

            String[] mimeTypes = cleanMimeTypes(fileChooserParams.getAcceptTypes());
            Intent filesIntent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            filesIntent.addCategory(Intent.CATEGORY_OPENABLE);
            filesIntent.setType(resolvePrimaryMime(mimeTypes));
            if (mimeTypes.length > 1) {
                filesIntent.putExtra(Intent.EXTRA_MIME_TYPES, mimeTypes);
            }
            filesIntent.putExtra(
                    Intent.EXTRA_ALLOW_MULTIPLE,
                    fileChooserParams.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE
            );

            List<Intent> extraIntents = new ArrayList<>();
            if (acceptsImages(mimeTypes)) {
                Intent cameraIntent = createCameraIntent();
                if (cameraIntent != null) extraIntents.add(cameraIntent);
            }

            Intent chooser = Intent.createChooser(filesIntent, "PDF, fotoğraf veya dosya seçin");
            if (!extraIntents.isEmpty()) {
                chooser.putExtra(Intent.EXTRA_INITIAL_INTENTS, extraIntents.toArray(new Intent[0]));
            }

            try {
                startActivityForResult(chooser, FILE_CHOOSER_REQUEST);
                return true;
            } catch (ActivityNotFoundException error) {
                pendingFileCallback = null;
                Toast.makeText(MainActivity.this, "Dosya seçici açılamadı.", Toast.LENGTH_LONG).show();
                return false;
            }
        }
    }

    private final class PatrolAndroidBridge {
        @JavascriptInterface
        public void printPage() {
            runOnUiThread(() -> {
                PrintManager manager = (PrintManager) getSystemService(Context.PRINT_SERVICE);
                PrintDocumentAdapter adapter = webView.createPrintDocumentAdapter("Patrol_Ambalaj_Rapor");
                manager.print("Patrol Ambalaj Raporu", adapter, null);
            });
        }

        @JavascriptInterface
        public void saveBase64File(String fileName, String mimeType, String base64Data) {
            try {
                byte[] bytes = Base64.decode(base64Data, Base64.DEFAULT);
                saveBytes(safeFileName(fileName), safeMimeType(mimeType), bytes);
            } catch (Exception error) {
                runOnUiThread(() -> Toast.makeText(
                        MainActivity.this,
                        "Dosya kaydedilemedi.",
                        Toast.LENGTH_LONG
                ).show());
            }
        }
    }

    private Intent createCameraIntent() {
        try {
            File pictureRoot = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
            if (pictureRoot == null) pictureRoot = new File(getCacheDir(), "camera");
            File cameraDirectory = new File(pictureRoot, "camera");
            if (!cameraDirectory.exists() && !cameraDirectory.mkdirs()) return null;

            pendingCameraFile = File.createTempFile("patrol_", ".jpg", cameraDirectory);
            pendingCameraUri = FileProvider.getUriForFile(
                    this,
                    getPackageName() + ".fileprovider",
                    pendingCameraFile
            );

            Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            intent.putExtra(MediaStore.EXTRA_OUTPUT, pendingCameraUri);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            return intent.resolveActivity(getPackageManager()) == null ? null : intent;
        } catch (Exception error) {
            pendingCameraFile = null;
            pendingCameraUri = null;
            return null;
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != FILE_CHOOSER_REQUEST || pendingFileCallback == null) return;

        Uri[] results = null;
        if (resultCode == RESULT_OK) {
            if (data != null && data.getClipData() != null) {
                ClipData clipData = data.getClipData();
                results = new Uri[clipData.getItemCount()];
                for (int index = 0; index < clipData.getItemCount(); index++) {
                    results[index] = clipData.getItemAt(index).getUri();
                }
            } else if (data != null && data.getData() != null) {
                results = new Uri[]{data.getData()};
            } else if (pendingCameraUri != null && pendingCameraFile != null && pendingCameraFile.length() > 0) {
                results = new Uri[]{pendingCameraUri};
            }
        }

        if (results == null && pendingCameraFile != null && pendingCameraFile.exists()) {
            //noinspection ResultOfMethodCallIgnored
            pendingCameraFile.delete();
        }

        pendingFileCallback.onReceiveValue(results);
        pendingFileCallback = null;
        pendingCameraUri = null;
        pendingCameraFile = null;
    }

    private boolean handleNavigation(Uri uri) {
        if (uri == null) return false;
        if (isTrustedUrl(uri)) return false;

        String scheme = uri.getScheme();
        if ("blob".equalsIgnoreCase(scheme) || "data".equalsIgnoreCase(scheme)) return false;

        try {
            startActivity(new Intent(Intent.ACTION_VIEW, uri));
        } catch (ActivityNotFoundException error) {
            Toast.makeText(this, "Bağlantı açılamadı.", Toast.LENGTH_SHORT).show();
        }
        return true;
    }

    private boolean isTrustedUrl(Uri uri) {
        return uri != null
                && "https".equalsIgnoreCase(uri.getScheme())
                && APP_HOST.equalsIgnoreCase(uri.getHost());
    }

    private void handleDownload(
            String url,
            String userAgent,
            String contentDisposition,
            String mimeType,
            long contentLength
    ) {
        String fileName = URLUtil.guessFileName(url, contentDisposition, mimeType);
        if (url != null && url.startsWith("blob:")) {
            downloadBlob(url, fileName, mimeType);
            return;
        }

        try {
            DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
            request.setMimeType(safeMimeType(mimeType));
            request.addRequestHeader("User-Agent", userAgent);
            String cookie = CookieManager.getInstance().getCookie(url);
            if (cookie != null) request.addRequestHeader("Cookie", cookie);
            request.setTitle(fileName);
            request.setDescription("Patrol Baskı Takip dosyası indiriliyor");
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName);
            ((DownloadManager) getSystemService(DOWNLOAD_SERVICE)).enqueue(request);
            Toast.makeText(this, "Dosya indiriliyor…", Toast.LENGTH_SHORT).show();
        } catch (Exception error) {
            Toast.makeText(this, "İndirme başlatılamadı.", Toast.LENGTH_LONG).show();
        }
    }

    private void downloadBlob(String url, String fileName, String mimeType) {
        String script = "(async function(){try{"
                + "const r=await fetch(" + JSONObject.quote(url) + ");"
                + "const b=await r.blob();const f=new FileReader();"
                + "f.onloadend=function(){const p=String(f.result).split(',')[1]||'';"
                + "PatrolAndroid.saveBase64File(" + JSONObject.quote(fileName) + ","
                + JSONObject.quote(safeMimeType(mimeType)) + ",p);};"
                + "f.readAsDataURL(b);}catch(e){}})();";
        webView.evaluateJavascript(script, null);
    }

    private void saveBytes(String fileName, String mimeType, byte[] bytes) throws Exception {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            ContentValues values = new ContentValues();
            values.put(MediaStore.Downloads.DISPLAY_NAME, fileName);
            values.put(MediaStore.Downloads.MIME_TYPE, mimeType);
            values.put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/PatrolBaskiTakip");
            values.put(MediaStore.Downloads.IS_PENDING, 1);

            Uri uri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
            if (uri == null) throw new IllegalStateException("Download URI oluşturulamadı");
            try (OutputStream output = getContentResolver().openOutputStream(uri)) {
                if (output == null) throw new IllegalStateException("Dosya açılamadı");
                output.write(bytes);
            }
            values.clear();
            values.put(MediaStore.Downloads.IS_PENDING, 0);
            getContentResolver().update(uri, values, null, null);
        } else {
            File directory = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS);
            if (directory == null) directory = getFilesDir();
            if (!directory.exists() && !directory.mkdirs()) {
                throw new IllegalStateException("İndirme klasörü açılamadı");
            }
            try (OutputStream output = new FileOutputStream(new File(directory, fileName))) {
                output.write(bytes);
            }
        }

        runOnUiThread(() -> Toast.makeText(
                this,
                "Dosya İndirilenler klasörüne kaydedildi.",
                Toast.LENGTH_LONG
        ).show());
    }

    private String nativeBridgeScript() {
        return "(function(){if(window.__patrolAndroidReady)return;window.__patrolAndroidReady=true;"
                + "window.print=function(){PatrolAndroid.printPage();};"
                + "document.addEventListener('click',function(event){"
                + "var anchor=event.target&&event.target.closest?event.target.closest('a[download]'):null;"
                + "if(!anchor||!anchor.href||anchor.href.indexOf('blob:')!==0)return;"
                + "event.preventDefault();fetch(anchor.href).then(function(r){return r.blob();}).then(function(blob){"
                + "var reader=new FileReader();reader.onloadend=function(){"
                + "var payload=String(reader.result).split(',')[1]||'';"
                + "PatrolAndroid.saveBase64File(anchor.download||'patrol-dosya',blob.type||'application/octet-stream',payload);};"
                + "reader.readAsDataURL(blob);});},true);})();";
    }

    private void showOfflinePage() {
        String html = "<!doctype html><html lang='tr'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                + "<body style='margin:0;background:#0b1826;color:#eef4fb;font-family:sans-serif;display:grid;place-items:center;min-height:100vh'>"
                + "<main style='max-width:420px;padding:32px;text-align:center'><h2>Bağlantı kurulamadı</h2>"
                + "<p style='color:#9fb0c2;line-height:1.5'>İlk açılış için internet bağlantısını kontrol edin. Daha önce açılan sayfalar çevrimdışı kullanılabilir.</p>"
                + "<button onclick=\"location.href='" + APP_URL + "'\" style='border:0;border-radius:10px;padding:12px 18px;background:#e52322;color:white;font-weight:700'>Tekrar Dene</button>"
                + "</main></body></html>";
        webView.loadDataWithBaseURL(APP_URL, html, "text/html", "UTF-8", null);
    }

    private String[] cleanMimeTypes(String[] values) {
        Set<String> types = new LinkedHashSet<>();
        if (values != null) {
            for (String value : values) {
                if (value == null) continue;
                for (String item : value.split(",")) {
                    String type = item.trim();
                    if (!type.isEmpty() && type.contains("/")) types.add(type);
                }
            }
        }
        return types.toArray(new String[0]);
    }

    private String resolvePrimaryMime(String[] mimeTypes) {
        if (mimeTypes.length == 1) return mimeTypes[0];
        if (mimeTypes.length > 1) {
            String family = mimeTypes[0].split("/")[0];
            boolean sameFamily = true;
            for (String type : mimeTypes) {
                if (!type.startsWith(family + "/")) {
                    sameFamily = false;
                    break;
                }
            }
            if (sameFamily) return family + "/*";
        }
        return "*/*";
    }

    private boolean acceptsImages(String[] mimeTypes) {
        for (String type : mimeTypes) {
            if (type.startsWith("image/")) return true;
        }
        return false;
    }

    private String safeFileName(String name) {
        String fallback = "patrol-dosya";
        if (name == null || name.trim().isEmpty()) return fallback;
        String cleaned = name.replaceAll("[\\\\/:*?\"<>|]", "_").trim();
        return cleaned.isEmpty() ? fallback : cleaned;
    }

    private String safeMimeType(String mimeType) {
        if (mimeType != null && mimeType.contains("/")) return mimeType;
        String extension = MimeTypeMap.getFileExtensionFromUrl(mimeType == null ? "" : mimeType);
        String inferred = MimeTypeMap.getSingleton().getMimeTypeFromExtension(extension);
        return inferred == null ? "application/octet-stream" : inferred;
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.removeJavascriptInterface("PatrolAndroid");
            webView.destroy();
        }
        super.onDestroy();
    }
}
