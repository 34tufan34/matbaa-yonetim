from pathlib import Path
p=Path('app/src/main/java/com/tufanprintops/uretimperformans/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'fixedFivePageFullReportV184' in s:
    raise SystemExit('already patched')

old_sig='    private void captureExpandedPdfV182(String jobTitle, WebView pv, int targetHeight) {'
new_sig='    private void captureExpandedPdfV182(String jobTitle, WebView pv, int targetWidth, int targetHeight) {'
if old_sig not in s: raise SystemExit('capture signature missing')
s=s.replace(old_sig,new_sig,1)

old='            params.width = ViewGroup.LayoutParams.MATCH_PARENT;\n            params.height = targetHeight;'
new='            params.width = targetWidth;\n            params.height = targetHeight;'
if old not in s: raise SystemExit('capture params block missing')
s=s.replace(old,new,1)

old='                    int width = pv.getWidth();\n                    if (width <= 0 && rootLayout != null) width = rootLayout.getWidth();\n                    if (width <= 0) width = 1200;'
new='                    int width = targetWidth > 0 ? targetWidth : pv.getWidth();\n                    if (width <= 0 && rootLayout != null) width = rootLayout.getWidth();\n                    if (width <= 0) width = 1200;'
if old not in s: raise SystemExit('capture width block missing')
s=s.replace(old,new,1)

old='''                    int viewportWidth = pv.getWidth();
                    if (viewportWidth <= 0 && rootLayout != null) viewportWidth = rootLayout.getWidth();
                    if (viewportWidth <= 0) viewportWidth = 1200;'''
new='''                    boolean fixedFivePageFullReportV184 = jobTitle != null && jobTitle.contains("Tum Rapor Merkezi");
                    int viewportWidth = fixedFivePageFullReportV184 ? 1040 : pv.getWidth();
                    if (viewportWidth <= 0 && rootLayout != null) viewportWidth = rootLayout.getWidth();
                    if (viewportWidth <= 0) viewportWidth = 1200;'''
if old not in s: raise SystemExit('prepare viewport block missing')
s=s.replace(old,new,1)

old='                    captureExpandedPdfV182(jobTitle, pv, targetHeight);'
new='                    captureExpandedPdfV182(jobTitle, pv, viewportWidth, targetHeight);'
if old not in s: raise SystemExit('capture call missing')
s=s.replace(old,new,1)

old='''            final float scale = ((float) printableWidth) / ((float) sourceWidth);
            final float sourcePerPage = printableHeight / scale;
            int pageCount = Math.max(1, (int) Math.ceil(sourceHeight / sourcePerPage));
            // Guard against corrupted/accidentally gigantic HTML creating hundreds of pages.
            pageCount = Math.min(pageCount, 80);'''
new='''            float scale = ((float) printableWidth) / ((float) sourceWidth);
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
if old not in s: raise SystemExit('page count block missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('v1.8.4 five-page full report renderer patch applied')
