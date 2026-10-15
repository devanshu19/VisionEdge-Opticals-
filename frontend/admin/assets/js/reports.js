document.addEventListener('DOMContentLoaded', async () => {
    // Check role and hide admin-only elements if necessary
    const role = typeof getUserRole === 'function' ? getUserRole() : 'staff';
    if (role !== 'admin') {
        const adminElements = document.querySelectorAll('.admin-only');
        adminElements.forEach(el => el.style.display = 'none');
    }

    await loadDashboardSummary();
    await loadInventoryAlerts();
});

async function loadDashboardSummary() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/reports/dashboard`);
        if (response.ok) {
            const data = await response.json();
            
            // Populate metrics safely
            if (document.getElementById('statCustomers')) document.getElementById('statCustomers').textContent = data.summary?.customers || 0;
            if (document.getElementById('statOrders')) document.getElementById('statOrders').textContent = data.summary?.orders || 0;
            if (document.getElementById('statAppointments')) document.getElementById('statAppointments').textContent = data.summary?.appointments || 0;
            if (document.getElementById('statPendingOrders')) document.getElementById('statPendingOrders').textContent = data.summary?.pending_orders || 0;
            
            if (document.getElementById('statSales')) {
                const salesVal = data.summary?.sales || 0;
                document.getElementById('statSales').textContent = `₹${salesVal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
            }

            // Revenue Chart
            const revCanvas = document.getElementById('revenueChart');
            if (revCanvas && data.charts?.revenue) {
                const revCtx = revCanvas.getContext('2d');
                new Chart(revCtx, {
                    type: 'line',
                    data: {
                        labels: data.charts.revenue.labels,
                        datasets: [{
                            label: 'Monthly Revenue (₹)',
                            data: data.charts.revenue.data,
                            borderColor: '#0d6efd',
                            backgroundColor: 'rgba(13, 110, 253, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

            // Distribution Chart
            const distCanvas = document.getElementById('distributionChart');
            if (distCanvas && data.charts?.distribution?.labels?.length > 0) {
                const distCtx = distCanvas.getContext('2d');
                new Chart(distCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.charts.distribution.labels,
                        datasets: [{
                            data: data.charts.distribution.data,
                            backgroundColor: ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#0dcaf0'],
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            }
        }
    } catch (e) {
        console.error("Failed to load dashboard data", e);
    }
}

async function loadInventoryAlerts() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/reports/inventory`);
        if (response.ok) {
            const data = await response.json();
            
            const alertsList = document.getElementById('inventoryAlertsList');
            if (document.getElementById('alertCount')) {
                document.getElementById('alertCount').textContent = data.metrics?.low_stock_count || 0;
            }
            
            if (alertsList) {
                if (!data.alerts || data.alerts.length === 0) {
                    alertsList.innerHTML = '<li class="list-group-item text-center text-muted border-0 py-4">No low stock items.</li>';
                } else {
                    alertsList.innerHTML = '';
                    data.alerts.forEach(alert => {
                        const bgClass = alert.status === 'Out of Stock' ? 'danger' : 'warning';
                        const icon = alert.type === 'Frame' ? 'eyeglasses' : 'circle';
                        alertsList.innerHTML += `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-0 fw-bold"><i class="bi bi-${icon} me-2 text-muted"></i>${alert.name}</h6>
                                    <small class="text-muted">${alert.type}</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-${bgClass} mb-1">${alert.status}</span><br>
                                    <small class="fw-bold">${alert.stock} left</small>
                                </div>
                            </li>
                        `;
                    });
                }
            }

            // Top Frames
            const framesList = document.getElementById('topFramesList');
            if (framesList) {
                if (!data.top_frames || data.top_frames.length === 0) {
                    framesList.innerHTML = '<li class="list-group-item text-center text-muted">No sales data yet</li>';
                } else {
                    framesList.innerHTML = '';
                    data.top_frames.forEach((f, index) => {
                        framesList.innerHTML += `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><span class="text-muted me-2">#${index+1}</span> ${f.name}</span>
                                <span class="badge bg-primary rounded-pill">${f.sold} sold</span>
                            </li>
                        `;
                    });
                }
            }

            // Top Lenses
            const lensesList = document.getElementById('topLensesList');
            if (lensesList) {
                if (!data.top_lenses || data.top_lenses.length === 0) {
                    lensesList.innerHTML = '<li class="list-group-item text-center text-muted">No sales data yet</li>';
                } else {
                    lensesList.innerHTML = '';
                    data.top_lenses.forEach((l, index) => {
                        lensesList.innerHTML += `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><span class="text-muted me-2">#${index+1}</span> ${l.name}</span>
                                <span class="badge bg-success rounded-pill">${l.sold} sold</span>
                            </li>
                        `;
                    });
                }
            }
        }
    } catch (e) {
        console.error("Failed to load inventory alerts", e);
    }
}

function exportReport(type, format) {
    const token = typeof getToken === 'function' ? getToken() : (localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken'));
    if (!token) return alert('Session expired. Please log in again.');
    
    fetch(`${API_BASE_URL}/reports/export/${format}?type=${type}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to export report");
        return res.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        let filename = `${type}_report.${format === 'excel' ? 'xlsx' : 'pdf'}`;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    })
    .catch(err => {
        alert("Failed to export report. " + err.message);
    });
}
