from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'v1.8.5-five-page-distribution' in s:
    raise SystemExit('already patched')

start=s.find('    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
end=s.find('\n    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView', start)
if start < 0 or end < 0:
    raise SystemExit('prepareFullHeightPdfV182 block not found')

new=r'''    // v1.8.5-five-page-distribution
    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        try {
            final boolean fullReport = jobTitle != null && jobTitle.contains("Tum Rapor Merkezi");
            int targetWidth = fullReport ? 920 : pv.getWidth();
            if (targetWidth <= 0 && rootLayout != null) targetWidth = rootLayout.getWidth();
            if (targetWidth <= 0) targetWidth = 1200;
            final int fixedWidth = targetWidth;

            ViewGroup.LayoutParams params = pv.getLayoutParams();
            if (params == null) params = new FrameLayout.LayoutParams(fixedWidth, 1000);
            params.width = fixedWidth;
            params.height = 1000;
            pv.setLayoutParams(params);
            pv.requestLayout();
            int wSpec = android.view.View.MeasureSpec.makeMeasureSpec(fixedWidth, android.view.View.MeasureSpec.EXACTLY);
            int hSpec = android.view.View.MeasureSpec.makeMeasureSpec(1000, android.view.View.MeasureSpec.EXACTLY);
            pv.measure(wSpec, hSpec);
            pv.layout(0, 0, fixedWidth, 1000);

            pv.postDelayed(() -> {
                if (printWebView != pv || isFinishing()) return;
                try {
                    if (fullReport) {
                        // At the final capture width, distribute any missing vertical room BETWEEN
                        // report sections. This gives five populated pages instead of one content page
                        // followed by four empty pages.
                        final double desiredHeight = ((551d * 5d * fixedWidth) / 794d) + 80d;
                        String js = "(function(){" +
                                "var s=Array.from(document.querySelectorAll('.all-report-section'));" +
                                "s.forEach(function(e){e.style.marginBottom='0px';});" +
                                "var h=Math.max(document.documentElement?document.documentElement.scrollHeight:0,document.body?document.body.scrollHeight:0);" +
                                "var d=" + desiredHeight + ";" +
                                "if(h<d&&s.length>1){var x=(d-h)/(s.length-1);for(var i=0;i<s.length-1;i++){s[i].style.marginBottom=x+'px';}}" +
                                "return Math.max(document.documentElement?document.documentElement.scrollHeight:0,document.body?document.body.scrollHeight:0);" +
                                "})()";
                        pv.evaluateJavascript(js, heightRaw -> {
                            int targetHeight = (int) Math.ceil(parseJsNumberV182(heightRaw)) + 24;
                            targetHeight = Math.max(targetHeight, 1000);
                            targetHeight = Math.min(targetHeight, 120000);
                            captureExpandedPdfV182(jobTitle, pv, fixedWidth, targetHeight);
                        });
                    } else {
                        final String heightJs = "Math.max(document.documentElement ? document.documentElement.scrollHeight : 0, document.body ? document.body.scrollHeight : 0, document.documentElement ? document.documentElement.offsetHeight : 0, document.body ? document.body.offsetHeight : 0)";
                        pv.evaluateJavascript(heightJs, heightRaw -> {
                            int targetHeight = (int) Math.ceil(parseJsNumberV182(heightRaw)) + 24;
                            targetHeight = Math.max(targetHeight, 800);
                            targetHeight = Math.min(targetHeight, 120000);
                            captureExpandedPdfV182(jobTitle, pv, fixedWidth, targetHeight);
                        });
                    }
                } catch (Exception ex) {
                    pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 250);
                }
            }, 450);
        } catch (Exception ex) {
            pv.postDelayed(() -> createPdfFromWebView(jobTitle, pv), 250);
        }
    }
'''
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
print('v1.8.5 five-page distribution patch applied')
