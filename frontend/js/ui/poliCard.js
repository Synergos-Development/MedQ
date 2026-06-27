import { emojis } from '../config/poliConfig.js';

export function renderPoli(list, counts, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;

  target.innerHTML = list.map(p => {
    const n = counts[p.id_poli];
    const has = n > 0;
    return `<div class="poli-chip">
      <span class="poli-emoji">${emojis[p.kode_poli] || '🏥'}</span>
      <div class="poli-name">${p.nama_poli.replace('Poli ', '')}</div>
      <div class="poli-count${has ? ' active' : ''}">${n === undefined ? '…' : (has ? n + ' antrian' : 'kosong')}</div>
    </div>`;
  }).join('');
}