let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    // Set default date to today
    const filterDate = document.getElementById('filterDate');
    if (filterDate) {
        filterDate.valueAsDate = new Date();
    }

    const aptDate = document.getElementById('aptDate');
    if (aptDate) {
        aptDate.valueAsDate = new Date();
    }

    await Promise.all([
        loadAppointmentStats(),
        loadAppointments(),
        loadCustomersDropdown()
    ]);

    // Attach search and filter event listeners
    const searchInput = document.getElementById('searchAppointment');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                loadAppointments();
            }, 300);
        });
    }

    if (filterDate) {
        filterDate.addEventListener('change', () => loadAppointments());
    }

    const filterStatus = document.getElementById('filterStatus');
    if (filterStatus) {
        filterStatus.addEventListener('change', () => loadAppointments());
    }

    // Forms
    const bookForm = document.getElementById('bookAppointmentForm');
    if (bookForm) {
        bookForm.addEventListener('submit', handleBookSubmit);
    }

    const editForm = document.getElementById('editStatusForm');
    if (editForm) {
        editForm.addEventListener('submit', handleEditStatusSubmit);
    }
});

async function loadAppointmentStats() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/appointments/stats`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('kpiTotal').textContent = data.total || 0;
            document.getElementById('kpiPending').textContent = data.pending || 0;
            document.getElementById('kpiConfirmed').textContent = data.confirmed || 0;
            document.getElementById('kpiCompleted').textContent = data.completed || 0;
        }
    } catch (e) {
        console.error('Error loading appointment stats:', e);
    }
}

async function loadCustomersDropdown() {
    try {
        const select = document.getElementById('aptCustomerSelect');
        if (!select) return;
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/`);
        if (response.ok) {
            const customers = await response.json();
            select.innerHTML = '<option value="">Select Customer...</option>';
            customers.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.name || (c.first_name + ' ' + c.last_name)} (${c.phone || c.email || 'ID: ' + c.id})</option>`;
            });
        }
    } catch (e) {
        console.error('Error loading customers dropdown:', e);
    }
}

async function loadAppointments() {
    try {
        const search = document.getElementById('searchAppointment')?.value.trim() || '';
        const status = document.getElementById('filterStatus')?.value || 'all';
        const date = document.getElementById('filterDate')?.value || '';

        let url = `${API_BASE_URL}/appointments/?status=${encodeURIComponent(status)}`;
        if (search) url += `&search=${encodeURIComponent(search)}`;
        if (date) url += `&date=${encodeURIComponent(date)}`;

        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch appointments');

        const appointments = await response.json();
        const tbody = document.getElementById('appointmentTableBody');
        tbody.innerHTML = '';

        if (appointments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted"><i class="bi bi-calendar-x fs-2 d-block mb-2"></i>No appointments found for the selected filters.</td></tr>';
            return;
        }

        const role = typeof getUserRole === 'function' ? getUserRole() : 'staff';

        appointments.forEach(apt => {
            let badgeClass = 'bg-secondary';
            if (apt.status === 'Pending') badgeClass = 'bg-warning text-dark';
            else if (apt.status === 'Confirmed') badgeClass = 'bg-info text-white';
            else if (apt.status === 'Completed') badgeClass = 'bg-success text-white';
            else if (apt.status === 'Cancelled') badgeClass = 'bg-danger text-white';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-medium text-primary">#APT-${apt.id}</td>
                <td>
                    <div class="fw-bold">${apt.appointment_date || '-'}</div>
                    <small class="text-muted"><i class="bi bi-clock me-1"></i>${apt.appointment_time || ''}</small>
                </td>
                <td class="fw-medium">${apt.customer_name || 'Unknown'}</td>
                <td><span class="badge bg-light text-dark border">${apt.appointment_type || 'Eye Test'}</span></td>
                <td>${apt.doctor_name || 'Dr. Sharma'}</td>
                <td><span class="badge ${badgeClass} px-3 py-1 rounded-pill">${apt.status}</span></td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary rounded-circle me-1" title="Edit Status" onclick="openEditModal(${apt.id}, '${apt.status}', '${(apt.doctor_name || '').replace(/'/g, "\\'")}', '${(apt.notes || '').replace(/'/g, "\\'")}')">
                        <i class="bi bi-pencil"></i>
                    </button>
                    ${role === 'admin' ? `
                    <button class="btn btn-sm btn-outline-danger rounded-circle" title="Delete" onclick="deleteAppointment(${apt.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error('Error loading appointments:', e);
        document.getElementById('appointmentTableBody').innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function handleBookSubmit(e) {
    e.preventDefault();

    const data = {
        customer_id: document.getElementById('aptCustomerSelect').value,
        appointment_date: document.getElementById('aptDate').value,
        appointment_time: document.getElementById('aptTime').value,
        appointment_type: document.getElementById('aptType').value,
        doctor_name: document.getElementById('aptDoctor').value.trim(),
        notes: document.getElementById('aptNotes').value.trim()
    };

    if (!data.customer_id) return alert('Please select a customer');

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/appointments/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const modalEl = document.getElementById('bookAppointmentModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            document.getElementById('bookAppointmentForm').reset();
            if (window.showToast) window.showToast('Booked', 'Appointment booked successfully');
            
            await Promise.all([loadAppointments(), loadAppointmentStats()]);
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to book appointment');
        }
    } catch (err) {
        alert('Network Error');
    }
}

function openEditModal(id, status, doctor, notes) {
    document.getElementById('editAptId').value = id;
    document.getElementById('editAptStatus').value = status || 'Pending';
    document.getElementById('editAptDoctor').value = doctor || '';
    document.getElementById('editAptNotes').value = notes || '';

    const modal = new bootstrap.Modal(document.getElementById('editStatusModal'));
    modal.show();
}

async function handleEditStatusSubmit(e) {
    e.preventDefault();

    const id = document.getElementById('editAptId').value;
    const data = {
        status: document.getElementById('editAptStatus').value,
        doctor_name: document.getElementById('editAptDoctor').value.trim(),
        notes: document.getElementById('editAptNotes').value.trim()
    };

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/appointments/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const modalEl = document.getElementById('editStatusModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            if (window.showToast) window.showToast('Updated', 'Appointment updated successfully');

            await Promise.all([loadAppointments(), loadAppointmentStats()]);
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to update appointment');
        }
    } catch (err) {
        alert('Network Error');
    }
}

async function deleteAppointment(id) {
    if (!confirm('Are you sure you want to delete this appointment?')) return;

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/appointments/${id}`, { method: 'DELETE' });
        if (response.ok) {
            if (window.showToast) window.showToast('Deleted', 'Appointment deleted successfully');
            await Promise.all([loadAppointments(), loadAppointmentStats()]);
        } else {
            alert('Failed to delete appointment');
        }
    } catch (e) {
        alert('Network error');
    }
}
