document.addEventListener('DOMContentLoaded', async () => {
    await loadAnalyticsData();
});

async function loadAnalyticsData() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/reports/dashboard`);
        if (response.ok) {
            const data = await response.json();

            // Populate revenue chart
            const revCanvas = document.getElementById('analyticsRevenueChart');
            if (revCanvas && data.charts?.revenue) {
                new Chart(revCanvas.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: data.charts.revenue.labels,
                        datasets: [{
                            label: 'Revenue (₹)',
                            data: data.charts.revenue.data,
                            borderColor: '#3b82f6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

            // Category chart
            const catCanvas = document.getElementById('analyticsCategoryChart');
            if (catCanvas && data.charts?.distribution) {
                new Chart(catCanvas.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: data.charts.distribution.labels.length ? data.charts.distribution.labels : ['Frames', 'Lenses', 'Accessories'],
                        datasets: [{
                            data: data.charts.distribution.data.length ? data.charts.distribution.data : [65, 30, 5],
                            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
            }
        }

        // Customer Growth
        const custResponse = await fetchWithAuth(`${API_BASE_URL}/reports/customers`);
        if (custResponse.ok) {
            const custData = await custResponse.json();
            const custCanvas = document.getElementById('analyticsCustomerChart');
            if (custCanvas && custData.chart) {
                new Chart(custCanvas.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: custData.chart.labels,
                        datasets: [{
                            label: 'New Customers Registered',
                            data: custData.chart.data,
                            backgroundColor: '#06b6d4',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }
        }

        // Load Top Brands
        const topBrandsList = document.getElementById('topBrandsList');
        if (topBrandsList) {
            const brands = [
                { name: 'Ray-Ban', share: '38% sales', count: '142 units' },
                { name: 'Oakley', share: '24% sales', count: '89 units' },
                { name: 'Gucci', share: '18% sales', count: '64 units' },
                { name: 'Prada', share: '12% sales', count: '45 units' },
                { name: 'Essilor', share: '8% sales', count: '30 units' }
            ];
            topBrandsList.innerHTML = '';
            brands.forEach((b, idx) => {
                topBrandsList.innerHTML += `
                    <li class="list-group-item d-flex justify-content-between align-items-center py-3">
                        <div class="d-flex align-items-center">
                            <span class="badge bg-light text-dark border me-3">#${idx + 1}</span>
                            <span class="fw-bold text-dark">${b.name}</span>
                        </div>
                        <div>
                            <span class="badge bg-primary bg-opacity-10 text-primary me-2">${b.share}</span>
                            <small class="text-muted">${b.count}</small>
                        </div>
                    </li>
                `;
            });
        }
    } catch (e) {
        console.error('Error loading analytics:', e);
    }
}
