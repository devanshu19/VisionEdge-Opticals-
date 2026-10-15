document.addEventListener("DOMContentLoaded", () => {
    // Initialize Dashboard with REAL SQLite Database Data
    if (document.getElementById('salesChart')) {
        loadDashboardRealData();
    }
    
    window.addEventListener('themeChanged', () => {
        location.reload(); 
    });
});

async function loadDashboardRealData() {
    try {
        const response = await fetchWithAuth('/reports/dashboard');
        if (response.ok) {
            const data = await response.json();
            const summary = data.summary || {};
            
            // Update KPI cards with real database numbers
            const custEl = document.getElementById('kpiTotalCustomers');
            if (custEl) custEl.innerText = (summary.customers || 0).toLocaleString();
            
            const salesEl = document.getElementById('kpiTotalSales');
            if (salesEl) salesEl.innerText = '₹' + (summary.sales || 0).toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            
            const invEl = document.getElementById('kpiInventoryItems');
            if (invEl) invEl.innerText = (summary.low_stock_items !== undefined ? summary.low_stock_items : 0) + " low stock";

            const pendingEl = document.getElementById('kpiPendingPayments');
            if (pendingEl) pendingEl.innerText = (summary.pending_orders || 0).toLocaleString();
            
            // Render Charts with live data
            initCharts(data.charts);
        } else {
            initCharts();
        }
    } catch (e) {
        console.error("Dashboard DB fetch error:", e);
        initCharts();
    }

    // Populate Recent Customers & Recent Payments from Database APIs
    loadRecentCustomers();
    loadRecentPayments();
}

function getChartColors() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const computedStyle = getComputedStyle(document.documentElement);
    
    return {
        textColor: isDark ? '#F8FAFC' : '#334155',
        gridColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        primary: computedStyle.getPropertyValue('--secondary-color').trim() || '#2563EB',
        accent: computedStyle.getPropertyValue('--accent-color').trim() || '#06B6D4',
        success: computedStyle.getPropertyValue('--success-color').trim() || '#22C55E',
        warning: computedStyle.getPropertyValue('--warning-color').trim() || '#F59E0B',
        danger: computedStyle.getPropertyValue('--danger-color').trim() || '#EF4444'
    };
}

function initCharts(chartData) {
    const colors = getChartColors();
    
    Chart.defaults.color = colors.textColor;
    Chart.defaults.font.family = "'Poppins', sans-serif";
    
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const revLabels = (chartData && chartData.revenue && chartData.revenue.labels) || months;
    const revData = (chartData && chartData.revenue && chartData.revenue.data) || new Array(12).fill(0);

    // 1. Monthly Sales Chart (Bar)
    const salesCanvas = document.getElementById('salesChart');
    if (salesCanvas) {
        const salesCtx = salesCanvas.getContext('2d');
        new Chart(salesCtx, {
            type: 'bar',
            data: {
                labels: revLabels,
                datasets: [{
                    label: 'Revenue (₹)',
                    data: revData,
                    backgroundColor: colors.primary,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { 
                        beginAtZero: true, 
                        grid: { color: colors.gridColor },
                        ticks: {
                            callback: function(value) { return '₹' + value.toLocaleString('en-IN'); }
                        }
                    },
                    x: { grid: { display: false } }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) { return 'Revenue: ₹' + Number(context.raw).toLocaleString('en-IN'); }
                        },
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleFont: { size: 14 },
                        bodyFont: { size: 13 },
                        padding: 10
                    }
                }
            }
        });
    }

    // 2. Inventory Distribution (Doughnut)
    const invLabels = (chartData && chartData.inventory && chartData.inventory.labels) || (chartData && chartData.distribution && chartData.distribution.labels) || ['Frames', 'Lenses'];
    const invData = (chartData && chartData.inventory && chartData.inventory.data) || (chartData && chartData.distribution && chartData.distribution.data) || [0, 0];
    
    const inventoryCanvas = document.getElementById('inventoryChart');
    if (inventoryCanvas) {
        const inventoryCtx = inventoryCanvas.getContext('2d');
        new Chart(inventoryCtx, {
            type: 'doughnut',
            data: {
                labels: invLabels,
                datasets: [{
                    data: invData,
                    backgroundColor: [colors.primary, colors.accent, colors.success, colors.warning],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
    
    // 3. Payment Methods (Pie)
    const pmtLabels = (chartData && chartData.payment_methods && chartData.payment_methods.labels) || ['Credit Card', 'Cash on Delivery'];
    const pmtData = (chartData && chartData.payment_methods && chartData.payment_methods.data) || [0, 0];

    const paymentCanvas = document.getElementById('paymentChart');
    if (paymentCanvas) {
        const paymentCtx = paymentCanvas.getContext('2d');
        new Chart(paymentCtx, {
            type: 'pie',
            data: {
                labels: pmtLabels,
                datasets: [{
                    data: pmtData,
                    backgroundColor: [colors.primary, colors.success, colors.accent, colors.warning],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}

async function loadRecentCustomers() {
    const customerTbody = document.getElementById('recentCustomersBody');
    if (!customerTbody) return;
    try {
        const res = await fetchWithAuth('/customers/');
        if (res.ok) {
            const customers = await res.json();
            const recent = Array.isArray(customers) ? customers.slice(-5).reverse() : [];
            if (recent.length === 0) {
                customerTbody.innerHTML = `<tr><td colspan="5" class="text-center py-3 text-muted fw-medium"><i class="bi bi-info-circle me-1"></i> No customers registered in Database yet.</td></tr>`;
                return;
            }
            customerTbody.innerHTML = recent.map(c => `
                <tr>
                    <td class="fw-medium text-secondary">#C${String(c.id).padStart(3, '0')}</td>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="bg-primary bg-opacity-10 text-primary rounded-circle me-3 d-flex align-items-center justify-content-center fw-bold" style="width: 35px; height: 35px;">
                                ${(c.first_name || c.name || 'C').charAt(0).toUpperCase()}
                            </div>
                            <span class="fw-medium">${c.first_name ? (c.first_name + ' ' + (c.last_name || '')) : (c.name || 'Customer')}</span>
                        </div>
                    </td>
                    <td class="text-muted">${c.phone || c.email || 'N/A'}</td>
                    <td class="text-muted">${c.created_at ? c.created_at.split('T')[0] : 'Today'}</td>
                    <td><span class="badge bg-success bg-opacity-25 text-success px-3 py-2 rounded-pill">Active</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error("Customers error:", err);
    }
}

async function loadRecentPayments() {
    const paymentTbody = document.getElementById('recentPaymentsBody');
    if (!paymentTbody) return;
    try {
        const res = await fetchWithAuth('/billing/');
        if (res.ok) {
            const billings = await res.json();
            const recent = Array.isArray(billings) ? billings.slice(-5).reverse() : [];
            if (recent.length === 0) {
                paymentTbody.innerHTML = `<tr><td colspan="5" class="text-center py-3 text-muted fw-medium"><i class="bi bi-info-circle me-1"></i> No billing invoices in Database yet.</td></tr>`;
                return;
            }
            paymentTbody.innerHTML = recent.map(p => `
                <tr>
                    <td class="fw-medium text-secondary">${p.invoice_number || ('#INV-' + p.id)}</td>
                    <td class="fw-medium">${p.customer_name || ('Customer #' + (p.customer_id || '1'))}</td>
                    <td class="fw-bold">$${parseFloat(p.total_amount || 0).toFixed(2)}</td>
                    <td class="text-muted"><i class="bi bi-credit-card me-2"></i>${p.payment_method || 'Card'}</td>
                    <td><span class="badge bg-${p.payment_status === 'Paid' ? 'success' : 'warning'} px-3 py-2 rounded-pill">${p.payment_status || 'Paid'}</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error("Billing error:", err);
    }
}
