from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'prepareFullHeightPdfV182' in s:
    raise SystemExit('already patched')

# The old capturePicture PDF path was slicing a document taller than the actually
# rasterized WebView, which produced the dark blank pages seen in the exported PDF.
# Keep the proven local PdfDocument writer, but expand the attached print WebView to
# the complete HTML document height before capture so every report block is rendered.
old_js='            ps.setJavaScriptEnabled(false);\n'
if old_js not in s:
    raise SystemExit('print WebView JavaScript setting not found')
s=s.replace(old_js,'            ps.setJavaScriptEnabled(true);\n',1)

old_call='                pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 700);\n'
if old_call not in s:
    raise SystemExit('legacy PDF capture call not found')
s=s.replace(old_call,'                pv.postDelayed(() -> prepareFullHeightPdfV182(jobTitle, pv), 700);\n',1)

marker='    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView(String jobTitle, WebView pv) {'
if marker not in s:
    raise SystemExit('legacy createPdfFromWebView marker missing')

method=r'''    private double parseJsNumberV182(String raw) {
        if (raw == null) return 0d;
        String v = raw.trim();
        if (v.startsWith("\"") && v.endsWith("\"") && v.length() >= 2) v = v.substring(1, v.length() - 1);
        try { return Double.parseDouble(v); } catch (Exception ignored) { return 0d; }
    }

    private void captureExpandedPdfV182(String jobTitle, WebView pv, int targetHeight) {
        if (printWebView != pv || isFinishing()) return;
        try {
            ViewGroup.LayoutParams params = pv.getLayoutParams();
            if (params == null) params = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, targetHeight);
            params.width = ViewGroup.LayoutParams.MATCH_PARENT;
            params.height = targetHeight;
            pv.setLayoutParams(params);
            pv.requestLayout();
            pv.postDelayed(() -> {
                if (printWebView != pv || isFinishing()) return;
                try {
                    int width = pv.getWidth();
                    if (width <= 0 && rootLayout != null) width = rootLayout.getWidth();
                    if (width <= 0) width = 1200;
                    int wSpec = android.view.View.MeasureSpec.makeMeasureSpec(width, android.view.View.MeasureSpec.EXACTLY);
                    int hSpec = android.view.View.MeasureSpec.makeMeasureSpec(targetHeight, android.view.View.MeasureSpec.EXACTLY);
                    pv.measure(wSpec, hSpec);
                    pv.layout(0, 0, width, targetHeight);
                    pv.invalidate();
                    pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 900);
                } catch (Exception ex) {
                    pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 250);
                }
            }, 500);
        } catch (Exception ex) {
            pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 250);
        }
    }

    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        try {
            final String widthJs = "Math.max(document.documentElement ? document.documentElement.scrollWidth : 0, document.body ? document.body.scrollWidth : 0, document.documentElement ? document.documentElement.clientWidth : 0)";
            final String heightJs = "Math.max(document.documentElement ? document.documentElement.scrollHeight : 0, document.body ? document.body.scrollHeight : 0, document.documentElement ? document.documentElement.offsetHeight : 0, document.body ? document.body.offsetHeight : 0)";
            pv.evaluateJavascript(widthJs, widthRaw -> pv.evaluateJavascript(heightJs, heightRaw -> {
                try {
                    double cssWidth = parseJsNumberV182(widthRaw);
                    double cssHeight = parseJsNumberV182(heightRaw);
                    int viewportWidth = pv.getWidth();
                    if (viewportWidth <= 0 && rootLayout != null) viewportWidth = rootLayout.getWidth();
                    if (viewportWidth <= 0) viewportWidth = 1200;
                    double ratio = cssWidth > 1d ? ((double) viewportWidth) / cssWidth : 1d;
                    int targetHeight = (int) Math.ceil(Math.max(cssHeight, 1d) * ratio) + 48;
                    targetHeight = Math.max(targetHeight, Math.max(pv.getHeight(), 800));
                    // Safety guard: enough for a long management report without allowing a corrupt
                    // document to request an unbounded Android view.
                    targetHeight = Math.min(targetHeight, 120000);
                    captureExpandedPdfV182(jobTitle, pv, targetHeight);
                } catch (Exception ex) {
                    pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 250);
                }
            }));
        } catch (Exception ex) {
            pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 250);
        }
    }

'''
s=s.replace(marker,method+marker,1)
p.write_text(s,encoding='utf-8')
print('v1.8.2 full-height WebView PDF patch applied')
