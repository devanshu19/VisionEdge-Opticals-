document.addEventListener('DOMContentLoaded', async () => {
    await loadBrands();
});

async function loadBrands() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/brands`);
        if (!response.ok) throw new Error('Failed to fetch');
        
        const brands = await response.json();
        const tbody = document.getElementById('brandsTableBody');
        tbody.innerHTML = '';
        
        if (brands.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center py-4">No brands found.</td></tr>';
            return;
        }
        
        brands.forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-medium">#${b.id}</td>
                <td>${b.name}</td>
                <td><span class="badge bg-${b.status === 'Active' ? 'success' : 'secondary'} bg-opacity-10 text-${b.status === 'Active' ? 'success' : 'secondary'}">${b.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading brands:", error);
        document.getElementById('brandsTableBody').innerHTML = '<tr><td colspan="3" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function saveBrand() {
    const name = document.getElementById('brandName').value.trim();
    const status = document.getElementById('brandStatus').value;
    
    if (!name) return alert('Brand name is required.');
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/brands`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, status })
        });
        
        if (response.ok) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('addBrandModal'));
            modal.hide();
            document.getElementById('addBrandForm').reset();
            await loadBrands();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to save brand');
        }
    } catch (error) {
        console.error("Save error:", error);
        alert('An error occurred');
    }
}
