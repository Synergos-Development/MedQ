import { emojis } from "../config/poliConfig.js";

export function updateSidebarSummary(selectedPoli, selectedDokter) {
  const empty = document.getElementById("summaryEmpty");
  const selected = document.getElementById("summarySelected");
  if (!empty || !selected) return;

  if (!selectedPoli) {
    empty.style.display = "block";
    selected.classList.remove("show");
    return;
  }
  empty.style.display = "none";
  selected.classList.add("show");

  // Mengisi data Ringkasan Poli
  const poliRow = document.getElementById("summaryPoliRow");
  const poliEmoji = document.getElementById("summaryPoliEmoji");
  const poliName = document.getElementById("summaryPoliName");

  if (poliRow) poliRow.style.display = "flex";
  if (poliEmoji) poliEmoji.textContent = emojis[selectedPoli.kode_poli] || "🏥";
  if (poliName) poliName.textContent = selectedPoli.nama_poli;

  // Mengisi data Ringkasan Dokter (jika sudah dipilih)
  if (selectedDokter) {
    const initials = selectedDokter.nama_dokter
      .replace(/dr\.|drg\./gi, "")
      .trim()
      .split(" ")
      .map((w) => w[0])
      .slice(0, 2)
      .join("");

    const docRow = document.getElementById("summaryDokterRow");
    const docAvatar = document.getElementById("summaryDokterAvatar");
    const docName = document.getElementById("summaryDokterName");

    if (docRow) docRow.style.display = "flex";
    if (docAvatar) docAvatar.textContent = initials;
    if (docName) docName.textContent = selectedDokter.nama_dokter;
  }
}
