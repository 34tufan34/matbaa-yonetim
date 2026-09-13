from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'naturalReportPagesV186' in s:
    raise SystemExit('already patched')

# Replace the v1.8.5 forced five-page preparation with a natural-width, natural-height layout.
start=s.find('    // v1.8.5-five-page-distribution\n    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
if start < 0:
    start=s.find('    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {')
end=s.find('\n    @SuppressWarnings("deprecation")\n    private void createPdfFromWebView', start)
if start < 0 or end < 0:
    raise SystemExit('prepareFullHeightPdfV182 block not found')
new=r'''    // naturalReportPagesV186
    private void prepareFullHeightPdfV182(String jobTitle, WebView pv) {
        if (printWebView != pv || isFinishing()) return;
        try {
            final boolean fullReport = jobTitle != null && jobTitle.contains("Tum Rapor Merkezi");
            int targetWidth = fullReport ? 1100 : pv.getWidth();
            if (targetWidth <= 0 && rootLayout != null) targetWidth = rootLayout.getWidth();
            if (targetWidth <= 0) targetWidth = 1100;
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
                    final String heightJs = "Math.max(document.documentElement ? document.documentElement.scrollHeight : 0, document.body ? document.body.scrollHeight : 0, document.documentElement ? document.documentElement.offsetHeight : 0, document.body ? document.body.offsetHeight : 0)";
                    pv.evaluateJavascript(heightJs, heightRaw -> {
                        int targetHeight = (int) Math.ceil(parseJsNumberV182(heightRaw)) + 24;
                        targetHeight = Math.max(targetHeight, 900);
                        targetHeight = Math.min(targetHeight, 120000);
                        captureExpandedPdfV182(jobTitle, pv, fixedWidth, targetHeight);
                    });
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

# capturePicture may report a much wider scroll area than the visible report canvas.
# Scale against the actual WebView width so the report fills the A4 landscape page.
old='''            int sourceWidth = picture == null ? 0 : picture.getWidth();
            int sourceHeight = picture == null ? 0 : picture.getHeight();
            if (sourceWidth <= 0 || sourceHeight <= 0) {
                throw new IllegalStateException("Rapor görünümü PDF için ölçülemedi.");
            }'''
new='''            int pictureWidth = picture == null ? 0 : picture.getWidth();
            int sourceHeight = picture == null ? 0 : picture.getHeight();
            int viewWidth = pv.getWidth();
            int sourceWidth = viewWidth > 0 ? Math.min(pictureWidth, viewWidth) : pictureWidth;
            if (sourceWidth <= 0 || sourceHeight <= 0) {
                throw new IllegalStateException("Rapor görünümü PDF için ölçülemedi.");
            }'''
if old not in s:
    raise SystemExit('source size block missing')
s=s.replace(old,new,1)

old='''            float scale = ((float) printableWidth) / ((float) sourceWidth);
            float sourcePerPage = printableHeight / scale;
            int pageCount = Math.max(1, (int) Math.ceil(sourceHeight / sourcePerPage));
            final boolean fixedFivePageFullReportV184 = jobTitle != null && jobTitle.contains("Tum Rapor Merkezi");
            if (fixedFivePageFullReportV184) {
                // Full Report Center export is deliberately normalized to five A4 landscape pages.
                // The narrower report viewport makes the content more readable and naturally taller.
                // If it is still longer than five pages, reduce the scale just enough so no content is cut.
                if (pageCount > 5) {
                    float fivePageScale = ((float) printableHeight * 5f) / ((float) sourceHeight);
                    scale = Math.min(scale, fivePageScale);
                    sourcePerPage = printableHeight / scale;
                }
                pageCount = 5;
            } else {
                // Guard against corrupted/accidentally gigantic HTML creating hundreds of pages.
                pageCount = Math.min(pageCount, 80);
            }'''
new='''            final float scale = ((float) printableWidth) / ((float) sourceWidth);
            final float sourcePerPage = printableHeight / scale;
            int pageCount = Math.max(1, (int) Math.ceil(sourceHeight / sourcePerPage));
            // v1.8.6: page count follows the real report length. No forced blank pages.
            pageCount = Math.min(pageCount, 80);'''
if old not in s:
    raise SystemExit('forced five page block missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('v1.8.6 natural full-width PDF renderer applied')
