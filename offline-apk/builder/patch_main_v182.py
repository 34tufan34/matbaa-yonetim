from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'createPdfFromWebViewV182' in s:
    raise SystemExit('already patched')

imports=[
('import android.print.PrintAttributes;','import android.print.PrintManager;\n'),
('import android.print.PrintDocumentAdapter;','import android.print.PrintManager;\n'),
('import android.print.PageRange;','import android.print.PrintManager;\n'),
('import android.os.CancellationSignal;','import android.os.Bundle;\n'),
('import android.os.ParcelFileDescriptor;','import android.os.Bundle;\n'),
]
for line,anchor in imports:
    if line not in s:
        if anchor not in s: raise SystemExit('import anchor missing: '+anchor)
        s=s.replace(anchor,anchor+line+'\n',1)

old='pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 700);'
new='pv.postDelayed(() -> createPdfFromWebViewV182(jobTitle, pv), 700);'
if old not in s: raise SystemExit('PDF start call missing')
s=s.replace(old,new,1)

marker='    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView(String jobTitle, WebView pv) {'
if marker not in s: raise SystemExit('legacy PDF method anchor missing')

method=r'''    private void failPdfV182(File out, ParcelFileDescriptor pfd, String message) {
        try { if (pfd != null) pfd.close(); } catch (Exception ignored) {}
        try { if (out != null && out.exists()) out.delete(); } catch (Exception ignored) {}
        String msg = (message == null || message.trim().isEmpty()) ? "PDF oluşturulamadı." : message;
        notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
        cleanupPrintWebView();
    }

    private void finishPdfV182(String jobTitle, File out, ParcelFileDescriptor pfd) {
        try { if (pfd != null) pfd.close(); } catch (Exception ignored) {}
        try {
            if (out == null || !out.exists() || out.length() < 256) throw new IllegalStateException("PDF dosyası oluşturulamadı.");
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
            String msg = ex.getMessage() == null ? ex.toString() : ex.getMessage();
            failPdfV182(out, null, msg);
        }
    }

    private void createPdfFromWebViewV182(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        final File out = new File(getCacheDir(), "upm-report-" + System.currentTimeMillis() + ".pdf");
        ParcelFileDescriptor opened = null;
        try {
            final PrintDocumentAdapter adapter = pv.createPrintDocumentAdapter(jobTitle);
            final PrintAttributes attrs = new PrintAttributes.Builder()
                    .setMediaSize(PrintAttributes.MediaSize.ISO_A4.asLandscape())
                    .setResolution(new PrintAttributes.Resolution("upm_pdf", "UPM PDF", 300, 300))
                    .setMinMargins(new PrintAttributes.Margins(0, 0, 0, 0))
                    .setColorMode(PrintAttributes.COLOR_MODE_COLOR)
                    .build();
            final CancellationSignal signal = new CancellationSignal();
            opened = ParcelFileDescriptor.open(out,
                    ParcelFileDescriptor.MODE_CREATE | ParcelFileDescriptor.MODE_TRUNCATE | ParcelFileDescriptor.MODE_READ_WRITE);
            final ParcelFileDescriptor pfd = opened;
            adapter.onLayout(null, attrs, signal, new PrintDocumentAdapter.LayoutResultCallback() {
                @Override
                public void onLayoutFinished(android.print.PrintDocumentInfo info, boolean changed) {
                    try {
                        adapter.onWrite(new PageRange[]{PageRange.ALL_PAGES}, pfd, signal,
                                new PrintDocumentAdapter.WriteResultCallback() {
                                    @Override
                                    public void onWriteFinished(PageRange[] pages) {
                                        finishPdfV182(jobTitle, out, pfd);
                                    }
                                    @Override
                                    public void onWriteFailed(CharSequence error) {
                                        failPdfV182(out, pfd, error == null ? "PDF sayfaları oluşturulamadı." : error.toString());
                                    }
                                    @Override
                                    public void onWriteCancelled() {
                                        failPdfV182(out, pfd, "PDF oluşturma işlemi iptal edildi.");
                                    }
                                });
                    } catch (Exception ex) {
                        failPdfV182(out, pfd, ex.getMessage() == null ? ex.toString() : ex.getMessage());
                    }
                }
                @Override
                public void onLayoutFailed(CharSequence error) {
                    failPdfV182(out, pfd, error == null ? "PDF sayfa düzeni hazırlanamadı." : error.toString());
                }
                @Override
                public void onLayoutCancelled() {
                    failPdfV182(out, pfd, "PDF sayfa düzeni iptal edildi.");
                }
            }, new Bundle());
        } catch (Exception ex) {
            String msg = ex.getMessage() == null ? ex.toString() : ex.getMessage();
            failPdfV182(out, opened, msg);
        }
    }

'''
s=s.replace(marker,method+marker,1)
p.write_text(s,encoding='utf-8')
print('v1.8.2 Android PDF pagination patch applied')
