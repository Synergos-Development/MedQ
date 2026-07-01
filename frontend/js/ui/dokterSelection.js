export function showDokterSkeleton(listId, sectionId) {
  const sec = document.getElementById(sectionId);
  const list = document.getElementById(listId);
  if (sec) sec.classList.add("show");
  if (list) {
    list.innerHTML = `<div class="skeleton" style="height:60px"></div><div class="skeleton" style="height:60px;margin-top:8px"></div>`;
  }
}

export function renderDokterList(dokterData, targetId) {
  const list = document.getElementById(targetId);
  if (!list) return;

  list.innerHTML = dokterData.map((d) => {
    const initials = d.nama_dokter
      .replace("dr.", "").replace("drg.", "").trim()
      .split(" ").map((w) => w[0]).slice(0, 2).join("");

    return `
      <div class="dokter-item" data-id="${d.id_dokter}" id="di-${d.id_dokter}">
        <div class="dokter-avatar">${initials}</div>
        <div>
          <div class="dokter-name">${d.nama_dokter}</div>
          <div class="dokter-spec">${d.spesialisasi}</div>
        </div>
        <div class="dokter-check"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div>
      </div>
    `;
  }).join("");
}

export function highlightSelectedDokter(id) {
  document.querySelectorAll(".dokter-item").forEach((d) => d.classList.remove("selected"));
  const item = document.getElementById("di-" + id);
  if (item) item.classList.add("selected");
}