document.addEventListener("DOMContentLoaded", () => {
    // Initialize Dashboard Charts and Tables if elements exist
    if (document.getElementById('salesChart')) {
        initCharts();
        populateTables();
    }
    
    // Re-render charts gracefully on theme change without full reload
    window.addEventListener('themeChanged', () => {
        // In a real scenario we'd update Chart.js instances.
        // For simplicity, we just reload the page for now to apply new CSS variables
        location.reload(); 
    });
});

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

function initCharts() {
    const colors = getChartColors();
    
    // Default Chart.js config
    Chart.defaults.color = colors.textColor;
    Chart.defaults.font.family = "'Poppins', sans-serif";
    
    // 1. Monthly Sales Chart (Bar)
    const salesCtx = document.getElementById('salesChart').getContext('2d');
    new Chart(salesCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Revenue ($)',
                data: [12500, 15000, 14200, 18500, 16000, 21000, 19500],
                backgroundColor: colors.primary,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: colors.gridColor } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleFont: { size: 14 },
                    bodyFont: { size: 13 },
                    padding: 10
                }
            }
        }
    });

    // 2. Inventory Distribution (Doughnut)
    const inventoryCtx = document.getElementById('inventoryChart').getContext('2d');
    new Chart(inventoryCtx, {
        type: 'doughnut',
        data: {
            labels: ['Frames', 'Lenses', 'Contact Lenses', 'Accessories'],
            datasets: [{
                data: [45, 30, 15, 10],
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
    
    // 3. Payment Methods (Pie)
    const paymentCtx = document.getElementById('paymentChart').getContext('2d');
    new Chart(paymentCtx, {
        type: 'pie',
        data: {
            labels: ['Card', 'Cash', 'UPI'],
            datasets: [{
                data: [60, 20, 20],
                backgroundColor: [colors.accent, colors.success, colors.primary],
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

function populateTables() {
    // Dummy Data for Recent Customers
    const recentCustomers = [
        { id: '#C001', name: 'John Doe', phone: '555-0101', date: '2023-10-25', status: 'Active' },
        { id: '#C002', name: 'Jane Smith', phone: '555-0102', date: '2023-10-24', status: 'Active' },
        { id: '#C003', name: 'Robert Johnson', phone: '555-0103', date: '2023-10-24', status: 'Inactive' },
        { id: '#C004', name: 'Emily Davis', phone: '555-0104', date: '2023-10-23', status: 'Active' }
    ];

    const customerTbody = document.getElementById('recentCustomersBody');
    if (customerTbody) {
        customerTbody.innerHTML = recentCustomers.map(c => `
            <tr>
                <td class="fw-medium text-secondary">${c.id}</td>
                <td>
                    <div class="d-flex align-items-center">
                        <div class="bg-primary bg-opacity-10 text-primary rounded-circle me-3 d-flex align-items-center justify-content-center fw-bold" style="width: 35px; height: 35px;">
                            ${c.name.charAt(0)}
                        </div>
                        <span class="fw-medium">${c.name}</span>
                    </div>
                </td>
                <td class="text-muted">${c.phone}</td>
                <td class="text-muted">${c.date}</td>
                <td><span class="badge bg-${c.status === 'Active' ? 'success' : 'secondary'} bg-opacity-25 text-${c.status === 'Active' ? 'success' : 'secondary'} px-3 py-2 rounded-pill">${c.status}</span></td>
            </tr>
        `).join('');
    }

    // Dummy Data for Recent Payments
    const recentPayments = [
        { inv: '#INV-2024', customer: 'John Doe', amount: '$250.00', method: 'Card', status: 'Paid' },
        { inv: '#INV-2025', customer: 'Jane Smith', amount: '$120.00', method: 'UPI', status: 'Pending' },
        { inv: '#INV-2026', customer: 'Michael Brown', amount: '$450.00', method: 'Cash', status: 'Paid' },
    ];

    const paymentTbody = document.getElementById('recentPaymentsBody');
    if (paymentTbody) {
        paymentTbody.innerHTML = recentPayments.map(p => `
            <tr>
                <td class="fw-medium text-secondary">${p.inv}</td>
                <td class="fw-medium">${p.customer}</td>
                <td class="fw-bold">${p.amount}</td>
                <td class="text-muted"><i class="bi ${p.method === 'Card' ? 'bi-credit-card' : p.method === 'UPI' ? 'bi-phone' : 'bi-cash'} me-2"></i>${p.method}</td>
                <td><span class="badge bg-${p.status === 'Paid' ? 'success' : 'warning'} px-3 py-2 rounded-pill">${p.status}</span></td>
            </tr>
        `).join('');
    }
}
