document.addEventListener("DOMContentLoaded", function() {
    const observer = new MutationObserver((mutations) => {
        const sidebar = document.querySelector(".sidebar");
        if (sidebar && !document.querySelector("#antigravity-nav")) {
            // Mencari kontainer menu navigasi (di bawah tombol Search)
            const searchBtn = document.querySelector("#sidebar-search-button");
            const navContainer = searchBtn ? searchBtn.parentElement.parentElement : null;
            
            if (navContainer) {
                const ideHtml = `
                <div id="antigravity-nav" class="px-[0.4375rem] flex flex-col gap-1 mt-2">
                    <a href="/workspace/ide" class="flex items-center space-x-3 rounded-2xl px-2.5 py-2 hover:bg-gray-100 dark:hover:bg-gray-900 transition text-gray-800 dark:text-gray-200">
                        <div class="self-center">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4.5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                            </svg>
                        </div>
                        <div class="text-sm font-medium">Antigravity IDE</div>
                    </a>
                    <a href="#" id="antigravity-update-btn" class="flex items-center space-x-3 rounded-2xl px-2.5 py-2 hover:bg-gray-100 dark:hover:bg-gray-900 transition text-yellow-500">
                        <div class="self-center">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4.5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                            </svg>
                        </div>
                        <div class="text-sm font-medium">🚀 Safe Update</div>
                    </a>
                </div>`;
                navContainer.insertAdjacentHTML("beforeend", ideHtml);
                
                // Menambahkan event listener untuk tombol update
                document.getElementById("antigravity-update-btn").onclick = function(e) {
                    e.preventDefault();
                    if (confirm("Mulai Update Aman ke v0.9.2? Fitur Antigravity akan dicadangkan dan dipulihkan otomatis.")) {
                        const chatInput = document.getElementById("chat-input");
                        if (chatInput) {
                            chatInput.value = "/execute_safe_update";
                            chatInput.dispatchEvent(new Event('input', { bubbles: true }));
                            const submitBtn = document.querySelector('button[type="submit"]');
                            if (submitBtn) submitBtn.click();
                        } else {
                            alert("Silakan buka Chat terlebih dahulu.");
                        }
                    }
                };
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
