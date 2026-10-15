document.addEventListener('DOMContentLoaded', async () => {
    await loadCategories();
});

async function loadCategories() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/categories`);
        if (!response.ok) throw new Error('Failed to fetch');
        
        const categories = await response.json();
        const tbody = document.getElementById('categoriesTableBody');
        tbody.innerHTML = '';
        
        if (categories.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4">No categories found.</td></tr>';
            return;
        }
        
        categories.forEach(c => {
            const tr = document.createElement('tr');
            const badgeType = c.type === 'Frame' ? 'primary' : 'info';
            tr.innerHTML = `
                <td class="ps-4 fw-medium">#${c.id}</td>
                <td class="fw-bold">${c.name}</td>
                <td><span class="badge bg-${badgeType} bg-opacity-10 text-${badgeType}">${c.type}</span></td>
                <td class="text-muted">${c.description || '-'}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading categories:", error);
        document.getElementById('categoriesTableBody').innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function saveCategory() {
    const name = document.getElementById('catName').value.trim();
    const type = document.getElementById('catType').value;
    const description = document.getElementById('catDesc').value.trim();
    
    if (!name || !type) return alert('Name and Type are required.');
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/categories`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, type, description })
        });
        
        if (response.ok) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('addCategoryModal'));
            modal.hide();
            document.getElementById('addCategoryForm').reset();
            await loadCategories();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to save category');
        }
    } catch (error) {
        console.error("Save error:", error);
        alert('An error occurred');
    }
}
