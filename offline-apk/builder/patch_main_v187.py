from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'pagedPdfV187' in s:
    raise SystemExit('already patched')

# v1.8.7: remove the giant full-height WebView capture path. Render one A4-sized
# viewport at a time, yielding back to Android between pages so the UI stays responsive.
start=s.find('    // naturalReportPagesV186\n    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
if start < 0:
    start=s.find('    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
end=s.find('\n    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView', start)
if start < 0 or end < 0:
    raise SystemExit('prepareFullHeightPdfV182 block not found')

new=r'''    // pagedPdfV187
    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        try {
            final int pageWidth = 842;
            final int pageHeight = 595;
            final int marginX = 24;
            final int marginY = 22;
            final int printableWidth = pageWidth - (marginX * 2);
            final int printableHeight = pageHeight - (marginY * 2);

            // A moderate viewport keeps text readable and avoids enormous bitmap/view sizes.
            final int sourceWidth = 1180;
            final int sourcePageHeight = Math.max(640,
                    Math.round(((float) sourceWidth * (float) printableHeight) / (float) printableWidth));

            ViewGroup.LayoutParams params = pv.getLayoutParams();
            if (params == null) params = new FrameLayout.LayoutParams(sourceWidth, sourcePageHeight);
            params.width = sourceWidth;
            params.height = sourcePageHeight;
            pv.setLayoutParams(params);
            pv.requestLayout();

            int wSpec = android.view.View.MeasureSpec.makeMeasureSpec(sourceWidth, android.view.View.MeasureSpec.EXACTLY);
            int hSpec = android.view.View.MeasureSpec.makeMeasureSpec(sourcePageHeight, android.view.View.MeasureSpec.EXACTLY);
            pv.measure(wSpec, hSpec);
            pv.layout(0, 0, sourceWidth, sourcePageHeight);

            pv.postDelayed(() -> {
                if (printWebView != pv || isFinishing()) return;
                final String widthJs = "Math.max(document.documentElement?document.documentElement.clientWidth:0,document.body?document.body.clientWidth:0,1)";
                final String heightJs = "Math.max(document.documentElement?document.documentElement.scrollHeight:0,document.body?document.body.scrollHeight:0,document.documentElement?document.documentElement.offsetHeight:0,document.body?document.body.offsetHeight:0,1)";
                try {
                    pv.evaluateJavascript(widthJs, widthRaw -> pv.evaluateJavascript(heightJs, heightRaw -> {
                        try {
                            double cssWidth = Math.max(1d, parseJsNumberV182(widthRaw));
                            double cssHeight = Math.max(1d, parseJsNumberV182(heightRaw));
                            double pxPerCss = ((double) sourceWidth) / cssWidth;
                            int contentHeightPx = (int) Math.ceil(cssHeight * pxPerCss);
                            int pageCount = Math.max(1, (int) Math.ceil(((double) contentHeightPx) / sourcePageHeight));
                            pageCount = Math.min(pageCount, 80);
                            renderPagedPdfV187(jobTitle, pv, sourceWidth, sourcePageHeight,
                                    pageWidth, pageHeight, marginX, marginY, printableWidth,
                                    pageCount, 0, new PdfDocument());
                        } catch (Exception ex) {
                            notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(ex.getMessage()) + ");}");
                            cleanupPrintWebView();
                        }
                    }));
                } catch (Exception ex) {
                    notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(ex.getMessage()) + ");}");
                    cleanupPrintWebView();
                }
            }, 320);
        } catch (Exception ex) {
            notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(ex.getMessage()) + ");}");
            cleanupPrintWebView();
        }
    }

    private void renderPagedPdfV187(String jobTitle, WebView pv,
                                    int sourceWidth, int sourcePageHeight,
                                    int pageWidth, int pageHeight,
                                    int marginX, int marginY, int printableWidth,
                                    int pageCount, int pageIndex, PdfDocument document) {
        if (printWebView != pv || isFinishing()) {
            try { document.close(); } catch (Exception ignored) {}
            return;
        }
        if (pageIndex >= pageCount) {
            writePagedPdfV187(jobTitle, document);
            return;
        }

        final int scrollY = pageIndex * sourcePageHeight;
        pv.scrollTo(0, scrollY);
        pv.postDelayed(() -> {
            if (printWebView != pv || isFinishing()) {
                try { document.close(); } catch (Exception ignored) {}
                return;
            }
            try {
                PdfDocument.PageInfo info = new PdfDocument.PageInfo.Builder(pageWidth, pageHeight, pageIndex + 1).create();
                PdfDocument.Page page = document.startPage(info);
                Canvas canvas = page.getCanvas();
                canvas.drawColor(Color.WHITE);
                int save = canvas.save();
                canvas.clipRect(marginX, marginY, pageWidth - marginX, pageHeight - marginY);
                canvas.translate(marginX, marginY);
                float scale = ((float) printableWidth) / ((float) sourceWidth);
                canvas.scale(scale, scale);
                pv.draw(canvas);
                canvas.restoreToCount(save);
                document.finishPage(page);

                // Yield between pages. This is the key ANR fix: no giant synchronous capture.
                pv.postDelayed(() -> renderPagedPdfV187(jobTitle, pv, sourceWidth, sourcePageHeight,
                        pageWidth, pageHeight, marginX, marginY, printableWidth,
                        pageCount, pageIndex + 1, document), 35);
            } catch (Exception ex) {
                try { document.close(); } catch (Exception ignored) {}
                notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(ex.getMessage()) + ");}");
                cleanupPrintWebView();
            }
        }, 45);
    }

    private void writePagedPdfV187(String jobTitle, PdfDocument document) {
        final File out = new File(getCacheDir(), "upm-report-" + System.currentTimeMillis() + ".pdf");
        new Thread(() -> {
            String error = null;
            try (FileOutputStream fos = new FileOutputStream(out, false)) {
                document.writeTo(fos);
                fos.flush();
                fos.getFD().sync();
            } catch (Exception ex) {
                error = ex.getMessage() == null ? ex.toString() : ex.getMessage();
            } finally {
                try { document.close(); } catch (Exception ignored) {}
            }
            final String finalError = error;
            runOnUiThread(() -> {
                if (finalError != null || !out.exists() || out.length() < 256) {
                    try { out.delete(); } catch (Exception ignored) {}
                    notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(finalError == null ? "PDF dosyası oluşturulamadı." : finalError) + ");}");
                    cleanupPrintWebView();
                    return;
                }
                pendingPdfFile = out;
                String base = sanitizeFileName(jobTitle);
                pendingPdfName = base.toLowerCase().endsWith(".pdf") ? base : base + ".pdf";
                cleanupPrintWebView();
                notifyJs("if(window.nativePrintStarted){nativePrintStarted();}");
                try {
                    Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("application/pdf");
                    intent.putExtra(Intent.EXTRA_TITLE, pendingPdfName);
                    startActivityForResult(intent, REQ_SAVE_PDF);
                } catch (Exception ex) {
                    notifyJs("if(window.nativePrintFailed){nativePrintFailed(" + jsQuote(ex.getMessage()) + ");}");
                }
            });
        }, "UPM-PDF-Writer").start();
    }
'''
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
print('v1.8.7 paged non-blocking PDF patch applied')
