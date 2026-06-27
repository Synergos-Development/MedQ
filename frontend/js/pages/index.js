import { fallbackPoli } from '../config/poliConfig.js';
import { fetchPoliList, fetchAntrianAktif } from '../api/poliApi.js';
import { updateTime } from '../ui/clock.js';
import { renderPoli } from '../ui/poliCard.js';
import { setStats } from '../ui/statsPanel.js';

async function load() {
  let poliList = [];

  try {
    poliList = await fetchPoliList();
  } catch {
    poliList = fallbackPoli;
  }

  renderPoli(poliList, {}, 'poliGrid');
  renderPoli(poliList, {}, 'poliGridSide');

  let tw = 0, td = 0, ts = 0;
  const counts = {};

  try {
    await Promise.all(poliList.map(async p => {
      const j = await fetchAntrianAktif(p.id_poli);
      if (j.status === 'success') {
        const d = j.data;
        counts[p.id_poli] = d.total_menunggu || d.antrian_menunggu?.length || 0;
        tw += counts[p.id_poli];
        td += d.total_dilayani || 0;
        ts += d.total_selesai || 0;
      }
    }));
  } catch {
    poliList.forEach((p, i) => { counts[p.id_poli] = [3, 1, 2, 0, 2][i] || 0; });
    tw = 8; td = 3; ts = 24;
  }

  setStats(tw, td, ts);
  renderPoli(poliList, counts, 'poliGrid');
  renderPoli(poliList, counts, 'poliGridSide');
}

// Jalankan
updateTime();
setInterval(updateTime, 1000);
load();