from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'printAdapterPdfV187' in s:
    raise SystemExit('already patched')

# Imports for direct asynchronous WebView PDF writing. This avoids capturePicture()
# and giant full-height WebView measure/layout operations on the UI thread.
anchor='import android.print.PrintManager;\n'
imports='import android.print.PrintDocumentAdapter;\nimport android.print.PrintAttributes;\nimport android.print.PageRange;\nimport android.os.CancellationSignal;\nimport android.os.ParcelFileDescriptor;\n'
if imports.splitlines()[0] not in s:
    if anchor not in s: raise SystemExit('print import anchor missing')
    s=s.replace(anchor,anchor+imports,1)

# Replace the expensive full-height pre-capture routine with the async print adapter path.
start=s.find('    // naturalReportPagesV186\n    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
if start < 0:
    start=s.find('    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
end=s.find('\n    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView', start)
if start < 0 or end < 0:
    raise SystemExit('prepareFullHeightPdfV182 block not found')

new=r'''    // printAdapterPdfV187
    // v1.8.7: do not expand/capture a many-thousand-pixel WebView on the main thread.
    // Android WebView's PrintDocumentAdapter paginates and writes the PDF asynchronously.
    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        pv.postDelayed(() -> writePdfWithPrintAdapterV187(jobTitle, pv), 180);
    }

    private void closeQuietlyV187(ParcelFileDescriptor pfd) {
        if (pfd != null) try { pfd.close(); } catch (Exception ignored) {}
    }

    private void failPdfV187(String message, File out, ParcelFileDescriptor pfd) {
        closeQuietlyV187(pfd);
        if (out != null) try { out.delete(); } catch (Exception ignored) {}
        String msg = (message == null || message.trim().isEmpty()) ? "PDF oluşturulamadı." : message;
        notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(msg) + ");}");
        cleanupPrintWebView();
    }

    private void finishPdfV187(String jobTitle, File out, ParcelFileDescriptor pfd) {
        closeQuietlyV187(pfd);
        try {
            if (out == null || !out.exists() || out.length() < 256) {
                failPdfV187("PDF dosyası oluşturulamadı.", out, null);
                return;
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
            failPdfV187(ex.getMessage(), out, null);
        }
    }

    private void writePdfWithPrintAdapterV187(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        final File out = new File(getCacheDir(), "upm-report-" + System.currentTimeMillis() + ".pdf");
        final ParcelFileDescriptor pfd;
        try {
            pfd = ParcelFileDescriptor.open(out,
                    ParcelFileDescriptor.MODE_CREATE |
                    ParcelFileDescriptor.MODE_TRUNCATE |
                    ParcelFileDescriptor.MODE_READ_WRITE);
        } catch (Exception ex) {
            failPdfV187(ex.getMessage(), out, null);
            return;
        }

        try {
            final PrintDocumentAdapter adapter = pv.createPrintDocumentAdapter(jobTitle);
            final PrintAttributes attrs = new PrintAttributes.Builder()
                    .setMediaSize(PrintAttributes.MediaSize.ISO_A4.asLandscape())
                    .setResolution(new PrintAttributes.Resolution("upm_pdf", "UPM PDF", 300, 300))
                    .setMinMargins(new PrintAttributes.Margins(280, 280, 280, 280))
                    .setColorMode(PrintAttributes.COLOR_MODE_COLOR)
                    .build();
            final CancellationSignal signal = new CancellationSignal();

            adapter.onLayout(null, attrs, signal,
                    new PrintDocumentAdapter.LayoutResultCallback() {
                        @Override
                        public void onLayoutFinished(android.print.PrintDocumentInfo info, boolean changed) {
                            if (signal.isCanceled()) {
                                failPdfV187("PDF işlemi iptal edildi.", out, pfd);
                                return;
                            }
                            try {
                                adapter.onWrite(new PageRange[]{PageRange.ALL_PAGES}, pfd, signal,
                                        new PrintDocumentAdapter.WriteResultCallback() {
                                            @Override
                                            public void onWriteFinished(PageRange[] pages) {
                                                finishPdfV187(jobTitle, out, pfd);
                                            }

                                            @Override
                                            public void onWriteFailed(CharSequence error) {
                                                failPdfV187(error == null ? "PDF yazılamadı." : error.toString(), out, pfd);
                                            }

                                            @Override
                                            public void onWriteCancelled() {
                                                failPdfV187("PDF işlemi iptal edildi.", out, pfd);
                                            }
                                        });
                            } catch (Exception ex) {
                                failPdfV187(ex.getMessage(), out, pfd);
                            }
                        }

                        @Override
                        public void onLayoutFailed(CharSequence error) {
                            failPdfV187(error == null ? "PDF sayfaları hazırlanamadı." : error.toString(), out, pfd);
                        }

                        @Override
                        public void onLayoutCancelled() {
                            failPdfV187("PDF işlemi iptal edildi.", out, pfd);
                        }
                    }, null);
        } catch (Exception ex) {
            failPdfV187(ex.getMessage(), out, pfd);
        }
    }
'''
s=s[:start]+new+s[end:]

p.write_text(s,encoding='utf-8')
print('v1.8.7 async print-adapter PDF patch applied')
