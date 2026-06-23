// Logic chính: quản lý 2 tab (Studio thu âm / Thử giọng).

// ---------- Chuyển tab ----------
document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.add("hidden"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.remove("hidden");
  });
});

// ============================================================
// TAB 1: STUDIO THU ÂM
// ============================================================
const sentenceList = document.getElementById("sentenceList");
const progressText = document.getElementById("progressText");
const progressFill = document.getElementById("progressFill");
const downloadDataset = document.getElementById("downloadDataset");
const consentStudio = document.getElementById("consentStudio");

let sentences = [];
let activeRecorder = null;
let activeId = null;

async function loadSentences() {
  const res = await fetch("/api/sentences");
  const data = await res.json();
  sentences = data.sentences;
  renderSentences();
  updateProgress();
}

function renderSentences() {
  sentenceList.innerHTML = "";
  sentences.forEach((s) => {
    const item = document.createElement("div");
    item.className = "sentence-item" + (s.recorded ? " done" : "");
    item.innerHTML = `
      <div class="sentence-head">
        <span class="badge">${s.id + 1}</span>
        <span class="sentence-text">${s.text}</span>
        ${s.recorded ? '<span class="check">✓</span>' : ""}
      </div>
      <div class="sentence-actions">
        <button class="btn btn-sm rec-btn" data-id="${s.id}">● Thu</button>
        <audio class="player sm hidden" data-player="${s.id}" controls></audio>
        <button class="btn btn-sm del-btn hidden" data-del="${s.id}">Xóa</button>
      </div>`;
    sentenceList.appendChild(item);
  });
  attachSentenceEvents();
  loadExistingAudio();
}

function attachSentenceEvents() {
  document.querySelectorAll(".rec-btn").forEach((b) => {
    b.addEventListener("click", () => toggleRecord(parseInt(b.dataset.id, 10), b));
  });
  document.querySelectorAll(".del-btn").forEach((b) => {
    b.addEventListener("click", () => deleteSample(parseInt(b.dataset.del, 10)));
  });
}

function loadExistingAudio() {
  // Hiển thị audio đã thu (nếu có) để nghe lại
  sentences.filter((s) => s.recorded).forEach((s) => {
    const player = document.querySelector(`[data-player="${s.id}"]`);
    const del = document.querySelector(`[data-del="${s.id}"]`);
    if (player) {
      player.src = `/storage/dataset/wavs/${String(s.id).padStart(4, "0")}.wav?t=${Date.now()}`;
      player.classList.remove("hidden");
    }
    if (del) del.classList.remove("hidden");
  });
}

async function toggleRecord(id, btn) {
  if (!consentStudio.checked) {
    alert("Vui lòng tích xác nhận đồng ý trước khi thu âm.");
    return;
  }

  // Đang thu câu này -> dừng và lưu
  if (activeRecorder && activeId === id) {
    const blob = activeRecorder.stop();
    activeRecorder = null;
    activeId = null;
    btn.textContent = "● Thu";
    btn.classList.remove("recording");
    await uploadSample(id, blob);
    return;
  }

  // Đang thu câu khác -> bỏ qua
  if (activeRecorder) {
    alert("Đang thu một câu khác, hãy dừng trước.");
    return;
  }

  try {
    activeRecorder = new WavRecorder(22050);
    await activeRecorder.start();
    activeId = id;
    btn.textContent = "■ Dừng & lưu";
    btn.classList.add("recording");
  } catch (err) {
    activeRecorder = null;
    activeId = null;
    alert("Không truy cập được micro: " + err.message);
  }
}

async function uploadSample(id, blob) {
  const form = new FormData();
  form.append("sentence_id", id);
  form.append("audio", blob, `${String(id).padStart(4, "0")}.wav`);
  const res = await fetch("/api/record", { method: "POST", body: form });
  if (res.ok) {
    const s = sentences.find((x) => x.id === id);
    if (s) s.recorded = true;
    renderSentences();
    updateProgress();
  } else {
    alert("Lưu thất bại.");
  }
}

async function deleteSample(id) {
  await fetch(`/api/record/${id}`, { method: "DELETE" });
  const s = sentences.find((x) => x.id === id);
  if (s) s.recorded = false;
  renderSentences();
  updateProgress();
}

function updateProgress() {
  const done = sentences.filter((s) => s.recorded).length;
  const total = sentences.length;
  progressText.textContent = `${done}/${total}`;
  progressFill.style.width = total ? `${(done / total) * 100}%` : "0%";
  downloadDataset.disabled = done === 0;
}

downloadDataset.addEventListener("click", () => {
  window.location.href = "/api/dataset/download";
});

// ============================================================
// TAB 2: THỬ GIỌNG
// ============================================================
const refFile = document.getElementById("refFile");
const refStatus = document.getElementById("refStatus");
const testText = document.getElementById("testText");
const testCount = document.getElementById("testCount");
const consentTest = document.getElementById("consentTest");
const genBtn = document.getElementById("genBtn");
const genStatus = document.getElementById("genStatus");
const resultCard = document.getElementById("resultCard");
const resultPlayer = document.getElementById("resultPlayer");
const downloadResult = document.getElementById("downloadResult");

let refBlob = null;

refFile.addEventListener("change", (e) => {
  refBlob = e.target.files[0] || null;
  refStatus.textContent = refBlob ? "Đã chọn: " + refBlob.name : "";
});

testText.addEventListener("input", () => {
  testCount.textContent = testText.value.length;
  updateGenState();
});
consentTest.addEventListener("change", updateGenState);

function updateGenState() {
  genBtn.disabled = !(testText.value.trim() && consentTest.checked);
}

genBtn.addEventListener("click", async () => {
  genBtn.disabled = true;
  genStatus.textContent = "Đang xử lý... (lần đầu sẽ tải model, hơi lâu)";
  resultCard.classList.add("hidden");

  const form = new FormData();
  form.append("text", testText.value.trim());
  form.append("consent", consentTest.checked);
  if (refBlob) form.append("audio", refBlob, refBlob.name || "ref.wav");

  try {
    const res = await fetch("/api/tts", { method: "POST", body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Lỗi không xác định" }));
      throw new Error(err.detail || res.statusText);
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    resultPlayer.src = url;
    downloadResult.href = url;
    resultCard.classList.remove("hidden");
    genStatus.textContent = "Hoàn tất.";
  } catch (err) {
    genStatus.textContent = "Lỗi: " + err.message;
  } finally {
    updateGenState();
  }
});

// Khởi tạo
loadSentences();
