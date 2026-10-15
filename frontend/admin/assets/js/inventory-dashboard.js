document.addEventListener('DOMContentLoaded', async () => {
    // Hide metadata buttons for staff
    if (typeof getUserRole === 'function' && getUserRole() !== 'admin') {
        const adminElements = document.querySelectorAll('.admin-only');
        adminElements.forEach(el => el.style.display = 'none');
        
        const staffElements = document.querySelectorAll('.staff-only');
        staffElements.forEach(el => el.style.display = 'block');
    }

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/stats`);
        if (response.ok) {
            const stats = await response.json();
            
            // Animate numbers
            animateValue("statFrames", 0, stats.total_frames, 1000);
            animateValue("statLenses", 0, stats.total_lenses, 1000);
            animateValue("statLowStock", 0, stats.low_stock_items, 1000);
            document.getElementById('statValue').textContent = '₹' + stats.total_value.toLocaleString();
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
