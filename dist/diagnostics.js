// Local-only timing observations; no network transmission or persistent storage.
(() => {
  const root = document.documentElement;
  const update = () => {
    const nav = performance.getEntriesByType('navigation')[0];
    if (nav) {
      root.dataset.ttfbMs = Math.round(nav.responseStart - nav.requestStart);
      root.dataset.domReadyMs = Math.round(nav.domContentLoadedEventEnd);
      root.dataset.loadMs = Math.round(nav.loadEventEnd || performance.now());
    }
    const fcp = performance.getEntriesByName('first-contentful-paint')[0];
    if (fcp) root.dataset.fcpMs = Math.round(fcp.startTime);
  };
  addEventListener('load', () => setTimeout(update,0), {once:true});
  if ('PerformanceObserver' in window) {
    try {new PerformanceObserver(list => {const last=list.getEntries().at(-1); if(last) root.dataset.lcpMs=Math.round(last.startTime);}).observe({type:'largest-contentful-paint',buffered:true});} catch {}
    let cls = 0;
    try {new PerformanceObserver(list => {for(const entry of list.getEntries()) if(!entry.hadRecentInput) cls+=entry.value;root.dataset.cls=cls.toFixed(4);}).observe({type:'layout-shift',buffered:true});} catch {}
  }
})();
