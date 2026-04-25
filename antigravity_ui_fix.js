document.addEventListener("DOMContentLoaded", function() {
    const observer = new MutationObserver((mutations) => {
        const sidebar = document.querySelector(".sidebar");
        if (sidebar && !document.querySelector("#antigravity-nav")) {
            const searchBtn = document.querySelector("#sidebar-search-button");
            const navContainer = searchBtn ? searchBtn.parentElement.parentElement : null;
            if (navContainer) {
                const navHtml = `
                <div id="antigravity-nav" class="px-2 flex flex-col gap-1 mt-4 border-t border-gray-200 dark:border-gray-800 pt-4">
                    <div class="text-[10px] font-bold text-gray-400 px-3 mb-2 tracking-widest uppercase text-gray-400">Antigravity Suite</div>
                    <a href="#" id="antigravity-ide-btn" class="flex items-center space-x-3 rounded-xl px-3 py-2.5 hover:bg-blue-500/10 hover:text-blue-500 transition-all duration-200 group text-gray-800 dark:text-gray-200">
                        <div class="text-gray-400 group-hover:text-blue-500"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline><line x1="12" y1="2" x2="12" y2="22"></line></svg></div>
                        <div class="text-sm font-semibold">Zenith IDE</div>
                    </a>
                    <a href="#" id="antigravity-update-btn" class="flex items-center space-x-3 rounded-xl px-3 py-2.5 hover:bg-yellow-500/10 hover:text-yellow-500 transition-all duration-200 group text-gray-800 dark:text-gray-200">
                        <div class="text-gray-400 group-hover:text-yellow-500"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2v6h-6"></path><path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path><path d="M3 22v-6h6"></path><path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path></svg></div>
                        <div class="text-sm font-semibold">Safe Update</div>
                    </a>
                </div>`;
                navContainer.insertAdjacentHTML("beforeend", navHtml);
                document.getElementById("antigravity-ide-btn").onclick = (e) => { e.preventDefault(); showAntigravityIDE(); };
                document.getElementById("antigravity-update-btn").onclick = handleSafeUpdate;
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Observer Pesan Proposal
    const chatObserver = new MutationObserver((mutations) => {
        const messages = document.querySelectorAll(".prose");
        messages.forEach(msg => {
            if (msg.textContent.includes("---ANTIGRAVITY_PROPOSAL---") && !msg.querySelector(".proposal-active")) {
                renderProposalUI(msg);
            }
        });
    });
    chatObserver.observe(document.body, { childList: true, subtree: true });
});

function renderProposalUI(messageElement) {
    const rawContent = messageElement.textContent;
    const jsonMatch = rawContent.match(/```json\n([\s\S]*?)\n```/);
    if (!jsonMatch) return;
    try {
        const proposalData = JSON.parse(jsonMatch[1]);
        const proposalHtml = `
        <div class="proposal-active mt-4 p-5 rounded-2xl border border-blue-500/30 bg-blue-500/5 backdrop-blur-md">
            <div class="flex items-center gap-3 mb-4">
                <div class="p-2 bg-blue-500 rounded-lg text-white"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.7-3.7a1 1 0 0 0-1.4-1.4l-3.7 3.7a1 1 0 0 0-1.6-1.6z"/><path d="M2 22 7.58 16.42"/><path d="m5 11 4-4"/><path d="m11 15 4-4"/><circle cx="12" cy="12" r="10"/></svg></div>
                <div><h3 class="text-sm font-bold text-blue-500 uppercase tracking-wider">System Architect Proposal</h3><p class="text-xs text-gray-400">Blueprint: ${proposalData.project_name}</p></div>
            </div>
            <div class="flex gap-3 mt-4">
                <button onclick="handleProposalRevision()" class="flex-1 py-2 rounded-xl bg-gray-800 hover:bg-gray-700 text-white text-xs font-bold transition-all">🔄 REVISI</button>
                <button onclick="handleProposalExecution('${encodeURIComponent(JSON.stringify(proposalData))}')" class="flex-1 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all">🚀 EKSEKUSI</button>
            </div>
        </div>`;
        messageElement.insertAdjacentHTML("beforeend", proposalHtml);
    } catch(e) {}
}

function handleProposalRevision() {
    const feedback = prompt("Detail revisi Anda:");
    if (feedback) { sendMessage(`Saya ingin merevisi desain: ${feedback}`); }
}

function handleProposalExecution(encodedData) {
    const data = JSON.parse(decodeURIComponent(encodedData));
    if (confirm(`Eksekusi pembuatan projek "${data.project_name}"?`)) {
        sendMessage(`EKSEKUSI_PROYEK: ${JSON.stringify(data)}`);
    }
}

function sendMessage(text) {
    const chatInput = document.getElementById("chat-input");
    if (chatInput) {
        chatInput.value = text;
        chatInput.dispatchEvent(new Event('input', { bubbles: true }));
        document.querySelector('button[type="submit"]').click();
    }
}

// ... (Zenith IDE Core) ...
let currentPath = "";
let currentOpenFile = "";

async function showAntigravityIDE() {
    if (document.getElementById("antigravity-ide-overlay")) return;
    let webuiVersion = "v0.9.2";
    try { const r = await fetch('/api/config'); const c = await r.json(); webuiVersion = c.version; } catch(e) {}
    const overlayHtml = `
    <div id="antigravity-ide-overlay" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); backdrop-filter:blur(10px); z-index:9999; display:flex; justify-content:center; align-items:center;">
        <div style="width:94%; height:92%; background:#0d1117; border-radius:16px; border:1px solid rgba(255,255,255,0.1); display:flex; flex-direction:column; overflow:hidden;">
            <div style="padding:12px 24px; background:#161b22; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:700; font-size:0.85rem; color:#58a6ff;">ZENITH IDE</div>
                <div style="display:flex; gap:12px;"><span id="save-status" style="font-size:0.7rem; color:#3fb950; opacity:0;">SAVED</span><button id="ide-save-btn" style="background:#238636; border:none; color:white; padding:5px 15px; border-radius:5px; font-size:0.75rem; display:none;">SAVE</button><button onclick="document.getElementById('antigravity-ide-overlay').remove()" style="color:#8b949e; cursor:pointer;">&times;</button></div>
            </div>
            <div style="flex:1; display:flex; overflow:hidden;">
                <div style="width:260px; background:#161b22; border-right:1px solid rgba(255,255,255,0.05); display:flex; flex-direction:column; overflow-y:auto;">
                    <div style="padding:16px 20px; font-size:0.7rem; color:#8b949e; display:flex; justify-content:space-between;">EXPLORER <a href="#" id="ide-back-btn" style="color:#58a6ff; display:none;">← BACK</a></div>
                    <div id="file-tree"></div>
                </div>
                <div style="flex:1; background:#0d1117; display:flex; flex-direction:column;">
                    <div id="current-file-label" style="padding:8px 20px; color:#c9d1d9; font-size:0.75rem; background:#161b22;">Select File</div>
                    <textarea id="code-area" spellcheck="false" style="flex:1; background:transparent; color:#c9d1d9; padding:20px; font-family:monospace; outline:none; resize:none;"></textarea>
                </div>
            </div>
            <div style="height:28px; background:#007acc; color:white; padding:0 12px; display:flex; align-items:center; font-size:0.7rem;">Engine: ${webuiVersion} | Patch: ACTIVE</div>
        </div>
    </div><style>.ide-item { padding:8px 12px; cursor:pointer; color:#c9d1d9; font-size:0.8rem; } .ide-item:hover { background:rgba(255,255,255,0.05); }</style>`;
    document.body.insertAdjacentHTML("beforeend", overlayHtml);
    loadProjectFiles("");
    document.getElementById("ide-save-btn").onclick = saveCurrentFile;
    document.getElementById("ide-back-btn").onclick = (e) => { e.preventDefault(); const p = currentPath.split("/"); p.pop(); loadProjectFiles(p.join("/")); };
}

async function loadProjectFiles(path) {
    currentPath = path;
    const tree = document.getElementById("file-tree");
    document.getElementById("ide-back-btn").style.display = path ? "inline" : "none";
    try {
        const r = await fetch(`/api/v1/workspace/fs/list?path=${encodeURIComponent(path)}`);
        const f = await r.json();
        tree.innerHTML = "";
        f.sort((a,b) => b.is_dir - a.is_dir).forEach(file => {
            const item = document.createElement("div");
            item.className = "ide-item";
            item.innerHTML = `<span>${file.is_dir ? '📁' : '📄'}</span> ${file.name}`;
            item.onclick = () => file.is_dir ? loadProjectFiles(file.path) : openFile(file.path);
            tree.appendChild(item);
        });
    } catch (e) {}
}

async function openFile(path) {
    currentOpenFile = path;
    document.getElementById("current-file-label").innerText = path.split("/").pop();
    document.getElementById("ide-save-btn").style.display = "block";
    try { const r = await fetch(`/api/v1/workspace/fs/read?path=${encodeURIComponent(path)}`); const d = await r.json(); document.getElementById("code-area").value = d.content; } catch(e) {}
}

async function saveCurrentFile() {
    if (!currentOpenFile) return;
    try { await fetch(`/api/v1/workspace/fs/write?path=${encodeURIComponent(currentOpenFile)}`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({content: document.getElementById("code-area").value}) }); document.getElementById("save-status").style.opacity = 1; setTimeout(() => document.getElementById("save-status").style.opacity = 0, 2000); } catch (e) {}
}

async function handleSafeUpdate(e) {
    e.preventDefault();
    const btn = document.getElementById("antigravity-update-btn");
    btn.innerHTML = "Checking...";
    try {
        const cRes = await fetch('/api/config'); const c = await cRes.json();
        const gRes = await fetch('https://api.github.com/repos/open-webui/open-webui/releases/latest'); const g = await gRes.json();
        if (c.version.replace('v','') === g.tag_name.replace('v','')) { alert("Sudah versi terbaru."); btn.innerHTML = "Safe Update"; return; }
        if (confirm("Update tersedia! Mulai?")) { sendMessage("/execute_safe_update"); location.reload(); }
    } catch(e) { btn.innerHTML = "Safe Update"; }
}
