export function updateTime() {
  const t = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  ['topTime', 'heroTime'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = t;
  });
}