from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'v1.8.7-webview-print-adapter-pdf' in s:
    raise SystemExit('already patched')

# Replace the old full-height/capturePicture preparation with the Android WebView print engine.
start=s.find('    // v1.8.5-five-page-distribution\n    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
if start < 0:
    start=s.find('    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
end=s.find('\n    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView', start)
if start < 0 or end < 0:
    raise SystemExit('prepareFullHeightPdfV182 block not found')
prep='''    // v1.8.7-webview-print-adapter-pdf\n    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {\n        if (printWebView != pv || isFinishing()) return;\n        // Let WebView finish fonts/layout, then ask its native print adapter to paginate HTML.\n        // This avoids capturePicture(), which only painted the first viewport and created blank pages.\n        pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 650);\n    }\n'''
s=s[:start]+prep+s[end:]

mstart=s.find('    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView(String jobTitle, WebView pv) {')
mend=s.find('\n    private String sanitizeFileName', mstart)
if mstart < 0 or mend < 0:
    raise SystemExit('createPdfFromWebView block not found')

method=r'''    private void finishNativePdfV187(String jobTitle, File out) {
        try {
            if (out == null || !out.exists() || out.length() < 256) {
                throw new IllegalStateException("PDF dosyası oluşturulamadı.");
            }
            pendingPdfFile = out;
            String base = sanitizeFileName(jobTitle);
            pendingPdfName = base.toLowerCase().endsWith(".pdf") ? base : base + ".pdf";
            cleanupPrintWebView();
            notifyJs("if(window.nativePrintStarted){nativePrintStarted();}");
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/pdf");
            intent.putExtra(Intent.EXTRA_TITLE, pendingPdfName);
            startActivityForResult(intent, REQ_SAVE_PDF);
        } catch (Exception ex) {
            try { if (out != null) out.delete(); } catch (Exception ignored) {}
            String msg = ex.getMessage() == null ? ex.toString() : ex.getMessage();
            notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
            cleanupPrintWebView();
        }
    }

    private void createPdfFromWebView(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        final File out = new File(getCacheDir(), "upm-report-" + System.currentTimeMillis() + ".pdf");
        try {
            notifyJs("if(window.nativePrintPreparing){nativePrintPreparing();}");
            final android.print.PrintDocumentAdapter adapter = pv.createPrintDocumentAdapter(jobTitle);
            final android.print.PrintAttributes attrs = new android.print.PrintAttributes.Builder()
                    .setMediaSize(android.print.PrintAttributes.MediaSize.ISO_A4.asLandscape())
                    .setResolution(new android.print.PrintAttributes.Resolution("upm_pdf", "UPM PDF", 300, 300))
                    .setMinMargins(new android.print.PrintAttributes.Margins(180, 180, 180, 180))
                    .setColorMode(android.print.PrintAttributes.COLOR_MODE_COLOR)
                    .build();
            final android.os.CancellationSignal layoutCancel = new android.os.CancellationSignal();
            adapter.onStart();
            adapter.onLayout(null, attrs, layoutCancel, new android.print.PrintDocumentAdapter.LayoutResultCallback() {
                @Override
                public void onLayoutFinished(android.print.PrintDocumentInfo info, boolean changed) {
                    try {
                        final android.os.ParcelFileDescriptor pfd = android.os.ParcelFileDescriptor.open(
                                out,
                                android.os.ParcelFileDescriptor.MODE_CREATE |
                                android.os.ParcelFileDescriptor.MODE_TRUNCATE |
                                android.os.ParcelFileDescriptor.MODE_READ_WRITE);
                        final android.os.CancellationSignal writeCancel = new android.os.CancellationSignal();
                        adapter.onWrite(new android.print.PageRange[]{android.print.PageRange.ALL_PAGES}, pfd, writeCancel,
                                new android.print.PrintDocumentAdapter.WriteResultCallback() {
                            @Override
                            public void onWriteFinished(android.print.PageRange[] pages) {
                                try { pfd.close(); } catch (Exception ignored) {}
                                try { adapter.onFinish(); } catch (Exception ignored) {}
                                finishNativePdfV187(jobTitle, out);
                            }
                            @Override
                            public void onWriteFailed(CharSequence error) {
                                try { pfd.close(); } catch (Exception ignored) {}
                                try { adapter.onFinish(); } catch (Exception ignored) {}
                                try { out.delete(); } catch (Exception ignored) {}
                                String msg = error == null ? "PDF yazımı başarısız." : error.toString();
                                notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
                                cleanupPrintWebView();
                            }
                            @Override
                            public void onWriteCancelled() {
                                try { pfd.close(); } catch (Exception ignored) {}
                                try { adapter.onFinish(); } catch (Exception ignored) {}
                                try { out.delete(); } catch (Exception ignored) {}
                                notifyJs("if(window.nativePrintFailed){nativePrintFailed('PDF oluşturma iptal edildi.');}");
                                cleanupPrintWebView();
                            }
                        });
                    } catch (Exception ex) {
                        try { adapter.onFinish(); } catch (Exception ignored) {}
                        try { out.delete(); } catch (Exception ignored) {}
                        String msg = ex.getMessage() == null ? ex.toString() : ex.getMessage();
                        notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
                        cleanupPrintWebView();
                    }
                }
                @Override
                public void onLayoutFailed(CharSequence error) {
                    try { adapter.onFinish(); } catch (Exception ignored) {}
                    try { out.delete(); } catch (Exception ignored) {}
                    String msg = error == null ? "PDF sayfa düzeni hazırlanamadı." : error.toString();
                    notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
                    cleanupPrintWebView();
                }
                @Override
                public void onLayoutCancelled() {
                    try { adapter.onFinish(); } catch (Exception ignored) {}
                    try { out.delete(); } catch (Exception ignored) {}
                    notifyJs("if(window.nativePrintFailed){nativePrintFailed('PDF sayfa düzeni iptal edildi.');}");
                    cleanupPrintWebView();
                }
            }, new android.os.Bundle());
        } catch (Exception ex) {
            try { out.delete(); } catch (Exception ignored) {}
            String msg = ex.getMessage() == null ? ex.toString() : ex.getMessage();
            notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
            cleanupPrintWebView();
        }
    }
'''
s=s[:mstart]+method+s[mend:]
p.write_text(s,encoding='utf-8')
print('v1.8.7 native WebView PrintDocumentAdapter PDF patch applied')
