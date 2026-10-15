document.addEventListener('DOMContentLoaded', async () => {
    await loadSuppliers();
});

async function loadSuppliers() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/suppliers`);
        if (!response.ok) throw new Error('Failed to fetch');
        
        const suppliers = await response.json();
        const tbody = document.getElementById('suppliersTableBody');
        tbody.innerHTML = '';
        
        if (suppliers.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">No suppliers found.</td></tr>';
            return;
        }
        
        suppliers.forEach(s => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-medium">#${s.id}</td>
                <td class="fw-bold">${s.name}</td>
                <td>${s.phone || '-'}</td>
                <td>${s.email || '-'}</td>
                <td><span class="badge bg-light text-dark border">${s.gst_number || 'N/A'}</span></td>
                <td>${s.city || '-'}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading suppliers:", error);
        document.getElementById('suppliersTableBody').innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function saveSupplier() {
    const data = {
        name: document.getElementById('supName').value.trim(),
        phone: document.getElementById('supPhone').value.trim(),
        email: document.getElementById('supEmail').value.trim(),
        gst_number: document.getElementById('supGST').value.trim(),
        address: document.getElementById('supAddress').value.trim(),
        city: document.getElementById('supCity').value.trim(),
        state: document.getElementById('supState').value.trim(),
        pincode: document.getElementById('supPincode').value.trim()
    };
    
    if (!data.name) return alert('Supplier name is required.');
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/suppliers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('addSupplierModal'));
            modal.hide();
            document.getElementById('addSupplierForm').reset();
            await loadSuppliers();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to save supplier');
        }
    } catch (error) {
        console.error("Save error:", error);
        alert('An error occurred');
    }
}
