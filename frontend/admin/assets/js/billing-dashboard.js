document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/stats`);
        if (response.ok) {
            const stats = await response.json();
            
            // For currency we can just set it, or use a custom decimal animation
            document.getElementById('statToday').textContent = stats.todays_sales.toLocaleString('en-IN', {minimumFractionDigits: 2});
            document.getElementById('statMonth').textContent = stats.monthly_revenue.toLocaleString('en-IN', {minimumFractionDigits: 2});
            
            animateValue("statPending", 0, stats.pending_payments, 1000);
            animateValue("statTotal", 0, stats.total_bills, 1000);
        }
    } catch (e) {
        console.error('Failed to load stats', e);
    }
});

function animateValue(id, start, end, duration) {
    if (start === end) {
        document.getElementById(id).textContent = end;
        return;
    }
    let range = end - start;
    let current = start;
    let increment = end > start ? 1 : -1;
    let stepTime = Math.abs(Math.floor(duration / range));
    if (stepTime < 5) stepTime = 5;
    
    let obj = document.getElementById(id);
    let timer = setInterval(function() {
        current += increment;
        obj.textContent = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}
