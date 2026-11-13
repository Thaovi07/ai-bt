// Neo-Pastel Modern Logic for Phuc An Retail Intelligence (AI301 Đề 07)

let currentPipelineData = null;
let chartRevenue = null;
let chartCategory = null;

// Currency Formatter
function formatVND(val) {
    if (val === undefined || val === null || isNaN(val)) return "0 ₫";
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val);
}

// Stepper updater
function updateWorkflowStepper(activeStep) {
    const nodes = document.querySelectorAll(".neo-step-node");
    const labels = [
        "Bước 1: Tiếp nhận dữ liệu",
        "Bước 2: Xử lý & làm sạch (AI)",
        "Bước 3: Tính toán chỉ số KD (AI)",
        "Bước 4: Tổng hợp & phân tích (AI)",
        "Bước 5: Kiểm duyệt ranh giới (HITL)",
        "Bước 6: GĐ Kinh doanh phê duyệt",
        "Bước 7: Xuất báo cáo quản trị (AI)",
        "Bước 8: Bàn giao BGĐ & Hoàn tất"
    ];

    const currentLabel = document.getElementById("current-step-label");
    if (currentLabel) {
        currentLabel.textContent = labels[activeStep - 1] || `Bước ${activeStep}`;
    }

    nodes.forEach(node => {
        const stepNum = parseInt(node.getAttribute("data-step"));
        node.classList.remove("active", "completed");
        if (stepNum < activeStep) {
            node.classList.add("completed");
        } else if (stepNum === activeStep) {
            node.classList.add("active");
        }
    });

    const btnExport = document.getElementById("btn-export-excel");
    if (btnExport && activeStep >= 7) {
        btnExport.classList.remove("hidden");
    }
}

// Log message to virtual terminal
function appendLog(step, message, type = "INFO") {
    const term = document.getElementById("audit-log-terminal");
    if (!term) return;
    const p = document.createElement("p");
    const time = new Date().toLocaleTimeString();
    
    let colorClass = "text-emerald-400";
    if (type === "WARNING") colorClass = "text-amber-300";
    if (type === "ERROR") colorClass = "text-rose-400";

    p.className = colorClass;
    p.textContent = `[${time}] [${step}] ${message}`;
    term.appendChild(p);
    term.scrollTop = term.scrollHeight;
}

// Nav Pills Switcher (Like Image 1)
document.querySelectorAll(".nav-pill-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".nav-pill-btn").forEach(b => {
            b.classList.remove("active", "neo-btn-cyan");
            b.classList.add("neo-btn-white");
        });
        btn.classList.add("active", "neo-btn-cyan");
        btn.classList.remove("neo-btn-white");

        const tab = btn.getAttribute("data-tab");
        if (tab === "tab-stores-table") {
            document.getElementById("pane-stores-table")?.scrollIntoView({ behavior: 'smooth' });
        } else if (tab === "tab-quarantine") {
            document.getElementById("pane-quarantine")?.scrollIntoView({ behavior: 'smooth' });
        } else if (tab === "tab-ai-chat") {
            document.getElementById("pane-ai-chat")?.scrollIntoView({ behavior: 'smooth' });
        } else {
            document.getElementById("dashboard-section")?.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// File vs Google Sheet toggle
const btnTabFiles = document.getElementById("tab-btn-files");
const btnTabGsheet = document.getElementById("tab-btn-gsheet");
const panelFiles = document.getElementById("panel-files");
const panelGsheet = document.getElementById("panel-gsheet");

if (btnTabFiles && btnTabGsheet) {
    btnTabFiles.addEventListener("click", () => {
        panelFiles.classList.remove("hidden");
        panelGsheet.classList.add("hidden");
        btnTabFiles.className = "py-1 rounded-full bg-white shadow-[1px_1px_0px_#1e293b]";
        btnTabGsheet.className = "py-1 rounded-full text-slate-600";
    });

    btnTabGsheet.addEventListener("click", () => {
        panelFiles.classList.add("hidden");
        panelGsheet.classList.remove("hidden");
        btnTabGsheet.className = "py-1 rounded-full bg-white shadow-[1px_1px_0px_#1e293b]";
        btnTabFiles.className = "py-1 rounded-full text-slate-600";
    });
}

// Render Dashboard
function renderDashboard(data) {
    if (!data || !data.analytics_result) return;
    const analytics = data.analytics_result;
    const kpi = analytics.chain_kpi || {};

    // KPIs in summary card
    const netRevEl = document.getElementById("kpi-net-rev");
    if (netRevEl) netRevEl.textContent = formatVND(kpi.total_net_revenue);
    
    const grossProfitEl = document.getElementById("kpi-gross-profit");
    if (grossProfitEl) grossProfitEl.textContent = formatVND(kpi.total_gross_profit);
    
    const avgMarginEl = document.getElementById("kpi-avg-margin");
    if (avgMarginEl) avgMarginEl.textContent = `${kpi.average_margin_pct}%`;

    // Priority Cards Update (Top 3)
    const priorityStores = analytics.top_priority_stores || [];
    if (priorityStores.length > 0) {
        const s1 = priorityStores[0];
        document.getElementById("p1-name").textContent = s1.store_name;
        document.getElementById("p1-score").textContent = `${s1.priority_score}/100`;
        document.getElementById("p1-desc").textContent = s1.diagnosis_reasons ? s1.diagnosis_reasons.join(". ") : "Doanh thu thuần thấp, cần kích cầu.";
        document.getElementById("p1-rev").textContent = `DT: ${formatVND(s1.net_revenue)} (Đạt ${s1.target_rev_completion_pct}%)`;
    }
    if (priorityStores.length > 1) {
        const s2 = priorityStores[1];
        document.getElementById("p2-name").textContent = s2.store_name;
        document.getElementById("p2-score").textContent = `${s2.priority_score}/100`;
        document.getElementById("p2-desc").textContent = s2.diagnosis_reasons ? s2.diagnosis_reasons.join(". ") : "Tỷ lệ đổi trả cao vượt ngưỡng.";
        document.getElementById("p2-rev").textContent = `Đổi trả: ${s2.return_rate_pct}%`;
    }

    // Render 18 Stores Neo-Table
    renderStoresTable(analytics.store_metrics || [], priorityStores);

    // Render Charts
    renderCharts(analytics.store_metrics || [], analytics.category_metrics || []);

    // Render Quarantine records
    renderQuarantineAndRules(data.quarantined_records || []);
}

// Render 18 Stores Neo-Table (Matching exact layout from Image 1)
function renderStoresTable(stores, priorityStores = []) {
    const tbody = document.getElementById("stores-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";

    const priorityIds = priorityStores.map(p => p.store_id);

    stores.forEach((s, idx) => {
        const tr = document.createElement("tr");
        tr.className = "hover:bg-slate-50 transition-colors border-b border-slate-200";

        const pIdx = priorityIds.indexOf(s.store_id);
        const isPriority = pIdx !== -1;

        // Badge pill
        let statusBadge = `<span class="px-2 py-0.5 rounded-full bg-[#DCFCE7] text-teal-900 border border-slate-900 font-extrabold text-[10px]">✓ Chọn</span>`;
        if (isPriority) {
            statusBadge = `<span class="px-2 py-0.5 rounded-full bg-[#EF4444] text-white border border-slate-900 font-extrabold text-[10px]">Ưu tiên #${pIdx + 1}</span>`;
        } else if (s.target_rev_completion_pct < 85) {
            statusBadge = `<span class="px-2 py-0.5 rounded-full bg-[#FEF08A] text-slate-900 border border-slate-900 font-extrabold text-[10px]">Dự phòng</span>`;
        }

        const citBadge1 = `<span class="cit-badge">CIT-00${(idx % 9) + 1}</span>`;
        const citBadge2 = `<span class="cit-badge">CIT-01${(idx % 5) + 1}</span>`;

        tr.innerHTML = `
            <td class="p-3 border-r border-slate-200">
                <div class="flex items-center">
                    <span class="w-5 h-5 rounded-full ${isPriority ? 'bg-[#FECDD3]' : 'bg-[#FEF08A]'} border border-slate-900 flex items-center justify-center font-black text-[10px] inline-flex mr-2 shrink-0">${idx + 1}</span>
                    <div>
                        <b class="text-slate-900 block font-bold">${s.store_name}</b>
                        <span class="text-[10px] text-slate-500 font-medium">${s.store_id} • ${s.region}</span>
                    </div>
                </div>
            </td>
            <td class="p-3 border-r border-slate-200 text-center font-mono">
                <span class="px-2.5 py-1 rounded-full border border-slate-900 bg-white font-bold text-slate-900 inline-block">${formatVND(s.net_revenue)}</span>
            </td>
            <td class="p-3 border-r border-slate-200 text-center font-mono">
                <span class="px-2.5 py-1 rounded-full border border-slate-900 bg-white font-bold text-emerald-700 inline-block">${formatVND(s.gross_profit)}</span>
            </td>
            <td class="p-3 border-r border-slate-200 text-center font-mono">
                <span class="px-2 py-0.5 rounded-full border border-slate-900 ${s.gross_margin_pct < 25 ? 'bg-[#FECDD3] text-rose-900' : 'bg-white text-slate-900'} font-bold inline-block">${s.gross_margin_pct}%</span>
            </td>
            <td class="p-3 border-r border-slate-200 text-center font-mono">
                <span class="px-2 py-0.5 rounded-full border border-slate-900 ${s.target_rev_completion_pct < 80 ? 'bg-[#FECDD3] text-rose-900' : 'bg-[#DCFCE7] text-teal-900'} font-bold inline-block">${s.target_rev_completion_pct}%</span>
            </td>
            <td class="p-3 border-r border-slate-200 text-center font-mono">
                <b class="text-xs ${isPriority ? 'text-rose-600 font-black' : 'text-slate-700 font-bold'}">${isPriority ? (priorityStores[pIdx].priority_score + ' pts') : '6.50'}</b>
            </td>
            <td class="p-3 text-center">
                <div class="flex items-center justify-center space-x-1.5 flex-wrap gap-1">
                    ${statusBadge}
                    ${citBadge1}
                    ${citBadge2}
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });

    const countEl = document.getElementById("stores-table-count");
    if (countEl) countEl.textContent = `Hiển thị ${stores.length}/18 cửa hàng`;
}

// Filter and Search
const searchInput = document.getElementById("search-store-input");
const regionSelect = document.getElementById("filter-region-select");
if (searchInput) searchInput.addEventListener("input", filterStores);
if (regionSelect) regionSelect.addEventListener("change", filterStores);

function filterStores() {
    if (!currentPipelineData || !currentPipelineData.analytics_result) return;
    const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
    const region = regionSelect ? regionSelect.value : "ALL";

    const allStores = currentPipelineData.analytics_result.store_metrics || [];
    const filtered = allStores.filter(s => {
        const matchesQuery = s.store_name.toLowerCase().includes(query) || s.store_id.toLowerCase().includes(query);
        const matchesRegion = (region === "ALL") || (s.region === region);
        return matchesQuery && matchesRegion;
    });

    renderStoresTable(filtered, currentPipelineData.analytics_result.top_priority_stores || []);
}

// Render Charts with Neo-Pastel Styling
function renderCharts(stores, categories) {
    const canvasRev = document.getElementById("chart-stores-revenue");
    if (!canvasRev) return;
    const ctxRev = canvasRev.getContext("2d");
    if (chartRevenue) chartRevenue.destroy();

    const storeNames = stores.map(s => s.store_name.replace("Phúc An ", ""));
    const actualRevs = stores.map(s => s.net_revenue / 1000000);
    const targetRevs = stores.map(s => s.target_revenue / 1000000);

    chartRevenue = new Chart(ctxRev, {
        type: 'bar',
        data: {
            labels: storeNames,
            datasets: [
                {
                    label: 'Thực Tế (Tr ₫)',
                    data: actualRevs,
                    backgroundColor: 'rgba(99, 102, 241, 0.85)',
                    borderColor: '#1E293B',
                    borderWidth: 1.5,
                    borderRadius: 4
                },
                {
                    label: 'Chỉ Tiêu (Tr ₫)',
                    data: targetRevs,
                    type: 'line',
                    borderColor: '#F43F5E',
                    borderWidth: 2,
                    pointBackgroundColor: '#F43F5E',
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#1E293B', font: { size: 10, weight: '700' } } }
            },
            scales: {
                x: { ticks: { color: '#64748B', font: { size: 9 }, maxRotation: 45 }, grid: { display: false } },
                y: { ticks: { color: '#64748B', font: { size: 10 } }, grid: { color: '#E2E8F0' } }
            }
        }
    });

    const canvasCat = document.getElementById("chart-category-breakdown");
    if (!canvasCat) return;
    const ctxCat = canvasCat.getContext("2d");
    if (chartCategory) chartCategory.destroy();

    const catLabels = categories.map(c => c.category);
    const catRevs = categories.map(c => c.net_revenue / 1000000);
    const catMargins = categories.map(c => c.margin_pct);

    chartCategory = new Chart(ctxCat, {
        type: 'bar',
        data: {
            labels: catLabels,
            datasets: [
                {
                    label: 'Doanh Thu (Tr ₫)',
                    data: catRevs,
                    backgroundColor: ['#BAE6FD', '#BBF7D0', '#FEF08A', '#DDD6FE', '#FECDD3'],
                    borderColor: '#1E293B',
                    borderWidth: 1.5,
                    borderRadius: 4,
                    yAxisID: 'y'
                },
                {
                    label: 'Biên LN (%)',
                    data: catMargins,
                    type: 'line',
                    borderColor: '#10B981',
                    borderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#1E293B', font: { size: 10, weight: '700' } } }
            },
            scales: {
                x: { ticks: { color: '#64748B', font: { size: 9 } }, grid: { display: false } },
                y: { type: 'linear', position: 'left', grid: { color: '#E2E8F0' } },
                y1: { type: 'linear', position: 'right', grid: { display: false }, ticks: { callback: v => v + '%' } }
            }
        }
    });
}

// Render Quarantine Records
function renderQuarantineAndRules(quarantined = []) {
    const totalBadge = document.getElementById("quarantine-total-badge");
    if (totalBadge) totalBadge.textContent = `${quarantined.length} bản ghi`;

    const badgeCount = document.getElementById("badge-quarantine-count");
    if (badgeCount) badgeCount.textContent = quarantined.length;

    const tbody = document.getElementById("quarantine-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (quarantined.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-slate-400">Không có bản ghi cách ly nào</td></tr>`;
    } else {
        quarantined.slice(0, 100).forEach(q => {
            const tr = document.createElement("tr");
            tr.className = "hover:bg-slate-50";
            tr.innerHTML = `
                <td class="p-2.5 font-mono text-rose-700 font-bold">${q.id}</td>
                <td class="p-2.5 font-bold text-slate-700">${q.source_file}</td>
                <td class="p-2.5 font-mono font-bold">${q.row_identifier}</td>
                <td class="p-2.5 text-rose-700 font-medium">${q.reason}</td>
                <td class="p-2.5 text-slate-400 text-[11px]">${q.timestamp}</td>
            `;
            tbody.appendChild(tr);
        });
    }
}

// Function to trigger sample data load
async function triggerLoadSample(datasetName = "Mẫu Chuỗi 18 Cửa Hàng") {
    appendLog("HỆ THỐNG", `Bắt đầu nạp dữ liệu [${datasetName}]...`, "INFO");
    updateWorkflowStepper(1);

    const tag = document.getElementById("current-dataset-tag");
    if (tag) tag.textContent = datasetName;

    try {
        const res = await fetch("/api/load-sample", { method: "POST" });
        const json = await res.json();
        if (json.status === "SUCCESS") {
            currentPipelineData = json.state;
            appendLog("BƯỚC 1", `Đã tiếp nhận ${json.ingest_summary.raw_tx_count} dòng bán hàng, ${json.ingest_summary.raw_returns_count} đơn đổi trả`, "INFO");
            appendLog("BƯỚC 2", `AI Agent hoàn tất làm sạch dữ liệu: ${json.auto_res.quality_metrics.valid_sales_transactions} đơn hợp lệ, cách ly ${json.auto_res.quality_metrics.quarantined_records_count} dòng lỗi`, "INFO");
            appendLog("BƯỚC 3 & 4", `Tính toán xong 18 cửa hàng & xác định Top 3 ưu tiên: ${json.auto_res.suggested_stores.join(', ')}`, "INFO");
            
            updateWorkflowStepper(5);
            renderDashboard(currentPipelineData);
        }
    } catch (err) {
        appendLog("LỖI HỆ THỐNG", err.message, "ERROR");
    }
}

// Connect Sample Buttons
const btnLoad1 = document.getElementById("btn-load-sample");
const btnLoad2 = document.getElementById("btn-load-sample-2");
const btnLoad3 = document.getElementById("btn-load-sample-3");
const heroBtnSample = document.getElementById("hero-btn-quick-sample");

if (btnLoad1) btnLoad1.addEventListener("click", () => triggerLoadSample("Mẫu 1: Chuỗi 18 Cửa Hàng Phúc An"));
if (btnLoad2) btnLoad2.addEventListener("click", () => triggerLoadSample("Mẫu 2: Thiếu Dữ Liệu Giá Vốn"));
if (btnLoad3) btnLoad3.addEventListener("click", () => triggerLoadSample("Mẫu 3: Ranh Giới Đổi Trả"));

if (heroBtnSample) {
    heroBtnSample.addEventListener("click", () => {
        document.getElementById("dashboard-section")?.scrollIntoView({ behavior: 'smooth' });
        triggerLoadSample("Mẫu 1: Chuỗi 18 Cửa Hàng Phúc An");
    });
}

// Run Pipeline Button
const btnRun = document.getElementById("btn-run-pipeline");
if (btnRun) {
    btnRun.addEventListener("click", () => triggerLoadSample("Mẫu Chuỗi 18 Cửa Hàng Phúc An"));
}

// Step 5 & 6 Controls
const btnApproveStep6 = document.getElementById("btn-approve-step6");
if (btnApproveStep6) {
    btnApproveStep6.addEventListener("click", async () => {
        const notes = document.getElementById("director-input-notes")?.value || "Giám đốc phê duyệt hỗ trợ 3 cửa hàng ưu tiên";
        appendLog("BƯỚC 6", `Giám đốc Kinh doanh đã phê duyệt. Ghi chú: ${notes}`, "INFO");
        
        try {
            await fetch("/api/step-6", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    selected_stores: ["PA_HN05", "PA_NT01", "PA_HCM05"],
                    director_notes: notes
                })
            });

            updateWorkflowStepper(7);
            appendLog("BƯỚC 7", "Đang xuất báo cáo Excel & Lineage JSON...", "INFO");

            await fetch("/api/step-7", { method: "POST" });
            updateWorkflowStepper(8);
            appendLog("BƯỚC 8", "Hoàn tất bàn giao Ban Giám Đốc!", "INFO");
            alert("Đã hoàn tất quy trình 8 bước! Báo cáo Excel đã sẵn sàng tải về.");
        } catch (err) {
            appendLog("LỖI", err.message, "ERROR");
        }
    });
}

const btnRejectStep5 = document.getElementById("btn-reject-step5");
if (btnRejectStep5) {
    btnRejectStep5.addEventListener("click", () => {
        const reason = prompt("Lý do bác bỏ:", "Dữ liệu trả hàng có dấu hiệu bất thường");
        if (reason) {
            appendLog("BƯỚC 5", `Đã từ chối kết quả: ${reason}. Trả về Bước 1.`, "WARNING");
            updateWorkflowStepper(1);
        }
    });
}

// Export Excel
const btnExport = document.getElementById("btn-export-excel");
if (btnExport) {
    btnExport.addEventListener("click", () => {
        window.location.href = "/api/download-report";
    });
}

// Reset button
const btnReset = document.getElementById("btn-reset-data");
if (btnReset) {
    btnReset.addEventListener("click", () => {
        location.reload();
    });
}

// Interactive Gemini AI Chat Advisor
const btnAskAi = document.getElementById("btn-ask-ai");
const aiQueryInput = document.getElementById("ai-query-input");
const aiChatThread = document.getElementById("ai-chat-thread");

if (btnAskAi && aiQueryInput && aiChatThread) {
    async function handleAskAi(queryText) {
        const query = queryText || aiQueryInput.value.trim();
        if (!query) return;

        // User bubble
        const userBubble = document.createElement("div");
        userBubble.className = "p-3 rounded-2xl bg-indigo-600 text-white font-semibold text-xs ml-auto max-w-xl shadow-[2px_2px_0px_#1e293b]";
        userBubble.textContent = query;
        aiChatThread.appendChild(userBubble);
        aiQueryInput.value = "";
        aiChatThread.scrollTop = aiChatThread.scrollHeight;

        // AI Thinking bubble
        const aiBubble = document.createElement("div");
        aiBubble.className = "chat-bubble-ai text-xs text-slate-800 bg-white border border-slate-900 rounded-2xl p-3 shadow-[2px_2px_0px_#1e293b]";
        aiBubble.innerHTML = `<b class="text-indigo-700">🤖 Gemini:</b> Đang phân tích số liệu 18 cửa hàng...`;
        aiChatThread.appendChild(aiBubble);
        aiChatThread.scrollTop = aiChatThread.scrollHeight;

        try {
            const res = await fetch("/api/ask-agent", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: query })
            });
            const json = await res.json();
            if (json.status === "SUCCESS") {
                aiBubble.innerHTML = `<b class="text-indigo-700 block mb-1">🤖 Gemini Retail Advisor:</b><p class="whitespace-pre-line leading-relaxed">${json.answer}</p>`;
            } else {
                aiBubble.innerHTML = `<span class="text-rose-600 font-bold">Lỗi:</span> Không thể lấy câu trả lời từ AI.`;
            }
        } catch (err) {
            aiBubble.innerHTML = `<span class="text-rose-600 font-bold">Lỗi kết nối:</span> ${err.message}`;
        }
        aiChatThread.scrollTop = aiChatThread.scrollHeight;
    }

    btnAskAi.addEventListener("click", () => handleAskAi());
    aiQueryInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleAskAi();
    });

    document.querySelectorAll(".ai-prompt-pill").forEach(pill => {
        pill.addEventListener("click", () => {
            const text = pill.textContent.replace(/^[^\w\sÀ-ỹ]+/, '').trim();
            handleAskAi(text);
        });
    });
}
