export function setStats(w, d, s) {
  ['W', 'D', 'S'].forEach((k, i) => {
    const vals = [w, d, s];
    ['mStat', 'dStat', 'sStat'].forEach(pfx => {
      const el = document.getElementById(pfx + k);
      if (el) el.textContent = vals[i];
    });
  });
}