import { emojis } from '../config/poliConfig.js';

export function renderPoliGrid(list, selectedPoli, targetGridId, emptyStateId) {
  const grid = document.getElementById(targetGridId);
  const empty = document.getElementById(emptyStateId);
  if (!grid || !empty) return;

  if (list.length === 0) {
    grid.innerHTML = '';
    empty.classList.add('show');
    return;
  }
  empty.classList.remove('show');

  grid.innerHTML = list.map(p => {
    const isSelected = selectedPoli && selectedPoli.id_poli === p.id_poli;
    return `
      <div class="poli-card${isSelected ? ' selected' : ''}" data-id="${p.id_poli}" id="pc-${p.id_poli}">
        <div class="poli-check"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div>
        <span class="poli-emoji">${emojis[p.kode_poli] || '🏥'}</span>
        <div class="poli-name">${p.nama_poli}</div>
        <div class="poli-queue">Antrian: <span>${p.antrian ?? '-'}</span></div>
      </div>`;
  }).join('');
}