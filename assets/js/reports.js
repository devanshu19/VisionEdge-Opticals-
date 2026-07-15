document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById('salesTrendChart')) {
        initReportCharts();
    }
});

function initReportCharts() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const computedStyle = getComputedStyle(document.documentElement);
    
    const textColor = isDark ? '#F8FAFC' : '#334155';
    const gridColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
    const primary = computedStyle.getPropertyValue('--secondary-color').trim() || '#2563EB';
    const accent = computedStyle.getPropertyValue('--accent-color').trim() || '#06B6D4';
    
    Chart.defaults.color = textColor;
    Chart.defaults.font.family = "'Poppins', sans-serif";
    
    // Line Chart for Sales Trend
    const salesCtx = document.getElementById('salesTrendChart').getContext('2d');
    
    // Create gradient
    let gradient = salesCtx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, `${primary}80`); // 50% opacity
    gradient.addColorStop(1, `${primary}00`); // 0% opacity

    new Chart(salesCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Revenue 2026',
                data: [12000, 19000, 15000, 22000, 18000, 25000, 21000, 28000, 24000, 32000, 30000, 38000],
                borderColor: primary,
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#fff',
                pointBorderColor: primary,
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: gridColor }, beginAtZero: true },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Polar Area Chart for Demographics
    const demoCtx = document.getElementById('demoChart').getContext('2d');
    new Chart(demoCtx, {
        type: 'polarArea',
        data: {
            labels: ['18-25 Yrs', '26-40 Yrs', '41-60 Yrs', '60+ Yrs'],
            datasets: [{
                data: [15, 45, 30, 10],
                backgroundColor: [
                    computedStyle.getPropertyValue('--accent-color').trim() || '#06B6D4',
                    computedStyle.getPropertyValue('--secondary-color').trim() || '#2563EB',
                    computedStyle.getPropertyValue('--warning-color').trim() || '#F59E0B',
                    computedStyle.getPropertyValue('--success-color').trim() || '#22C55E'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });
}
