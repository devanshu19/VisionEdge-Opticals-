let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    await loadPrescriptionHistory();

    const searchInput = document.getElementById('searchHistory');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(loadPrescriptionHistory, 300);
        });
    }
});

async function loadPrescriptionHistory() {
    try {
        const search = document.getElementById('searchHistory')?.value.trim() || '';
        let url = `${API_BASE_URL}/prescriptions/`;
        if (search) url += `?search=${encodeURIComponent(search)}`;

        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch prescriptions');

        const list = await response.json();
        const tbody = document.getElementById('historyTableBody');
        tbody.innerHTML = '';

        if (list.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted"><i class="bi bi-journal-medical fs-2 d-block mb-2"></i>No digital prescription history records found.</td></tr>';
            return;
        }

        list.forEach(rx => {
            const dateStr = rx.issue_date || rx.date || rx.created_at || 'N/A';
            const rSph = rx.right_sph || rx.od_sph || '0.00';
            const lSph = rx.left_sph || rx.os_sph || '0.00';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-bold text-primary">#RX-${rx.id}</td>
                <td class="text-muted">${dateStr}</td>
                <td class="fw-bold">${rx.customer_name || 'Customer'}</td>
                <td>${rx.doctor_name || 'Dr. Sharma'}</td>
                <td><span class="badge bg-light text-dark border">SPH: ${rSph}</span></td>
                <td><span class="badge bg-light text-dark border">SPH: ${lSph}</span></td>
                <td class="text-end pe-4">
                    <a href="view-prescription.html?id=${rx.id}" class="btn btn-sm btn-outline-primary" title="View Prescription">
                        <i class="bi bi-eye me-1"></i>View Record
                    </a>
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error('Error loading history:', e);
        document.getElementById('historyTableBody').innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error loading history data.</td></tr>';
    }
}
