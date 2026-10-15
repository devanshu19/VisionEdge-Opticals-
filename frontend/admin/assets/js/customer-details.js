const urlParams = new URLSearchParams(window.location.search);
const customerId = urlParams.get('id');

document.addEventListener('DOMContentLoaded', async () => {
    if (!customerId) {
        alert('No customer ID provided');
        window.location.href = 'customers.html';
        return;
    }
    
    document.getElementById('editCustomerBtn').href = `edit-customer.html?id=${customerId}`;
    document.getElementById('newRxBtn').href = `add-prescription.html?customer_id=${customerId}`;
    
    // Add customer ID to new recommendation button
    const newRecBtn = document.getElementById('newRecBtn');
    if(newRecBtn) newRecBtn.href = `frame-recommendation.html?customer_id=${customerId}`;
    
    // Add customer ID to VTO button
    const newVtoBtn = document.getElementById('newVtoBtn');
    if(newVtoBtn) newVtoBtn.href = `vto-studio.html?customer_id=${customerId}`;
    
    await loadCustomerDetails();
    await loadCustomerPrescriptions();
    await loadAiHistory();
    await loadVtoHistory();
    
    // Check if we need to switch tabs
    const tab = urlParams.get('tab');
    if (tab === 'ai') {
        const aiTabBtn = new bootstrap.Tab(document.querySelector('#ai-tab'));
        aiTabBtn.show();
    }
});

async function loadCustomerDetails() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/${customerId}`);
        if (!response.ok) throw new Error('Customer not found');
        
        const data = await response.json();
        
        // Header
        document.getElementById('profileName').textContent = data.name;
        document.getElementById('profileCode').textContent = data.customer_code || 'N/A';
        
        // Parse date for Joined
        const createdDate = new Date(data.created_at);
        document.getElementById('profileJoined').textContent = createdDate.toLocaleDateString();
        
        document.getElementById('profilePhone').textContent = data.phone;
        document.getElementById('profileEmail').textContent = data.email || 'No email';
        document.getElementById('profileCity').textContent = data.city || 'No city provided';
        
        if (data.photo) {
            document.getElementById('profilePhoto').src = data.photo;
        }
        
        // Status Badge
        const statusDiv = document.getElementById('profileStatusBadge');
        if (data.status === 'Active') {
            statusDiv.innerHTML = '<span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 px-3 py-2 rounded-pill">Active Customer</span>';
        } else if (data.status === 'Inactive') {
            statusDiv.innerHTML = '<span class="badge bg-warning bg-opacity-10 text-warning border border-warning border-opacity-25 px-3 py-2 rounded-pill">Inactive Customer</span>';
        } else {
            statusDiv.innerHTML = '<span class="badge bg-danger bg-opacity-10 text-danger border border-danger border-opacity-25 px-3 py-2 rounded-pill">Blocked Customer</span>';
        }
        
        // Personal Details
        document.getElementById('detGender').textContent = data.gender || '-';
        
        let ageStr = '-';
        if (data.age && data.dob) {
            ageStr = `${data.age} yrs (${data.dob})`;
        } else if (data.age) {
            ageStr = `${data.age} yrs`;
        }
        document.getElementById('detAge').textContent = ageStr;
        document.getElementById('detOccupation').textContent = data.occupation || '-';
        document.getElementById('detBloodGroup').textContent = data.blood_group || '-';
        
        // Optical & Medical
        document.getElementById('detCondition').textContent = data.eye_condition || 'None reported';
        document.getElementById('detLens').textContent = data.lens_preference || 'No preference';
        document.getElementById('detFrame').textContent = data.frame_preference || 'No preference';
        document.getElementById('detDoctor').textContent = data.doctor_name || 'Not assigned';
        
    } catch (error) {
        console.error("Error loading customer details:", error);
        alert('Failed to load customer details');
        window.location.href = 'customers.html';
    }
}

async function loadCustomerPrescriptions() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/?customer_id=${customerId}`);
        if (!response.ok) throw new Error('Failed to load prescriptions');
        
        const rxList = await response.json();
        const tbody = document.getElementById('rxHistoryBody');
        tbody.innerHTML = '';
        
        if (rxList.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-muted">No prescriptions found for this customer.</td></tr>';
            return;
        }
        
        rxList.forEach(rx => {
            let statusBadge = rx.status === 'Completed' ? 'success' : (rx.status === 'Draft' ? 'warning' : 'secondary');
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="fw-medium text-primary">${rx.prescription_number || '-'}</td>
                <td>${rx.date}</td>
                <td>${rx.doctor_name || '-'}</td>
                <td><span class="badge bg-${statusBadge} bg-opacity-10 text-${statusBadge} px-2 py-1">${rx.status}</span></td>
                <td class="text-end">
                    <a href="view-prescription.html?id=${rx.id}" class="btn btn-sm btn-outline-info rounded-circle me-1" title="View"><i class="bi bi-eye"></i></a>
                    <a href="edit-prescription.html?id=${rx.id}" class="btn btn-sm btn-outline-primary rounded-circle" title="Edit"><i class="bi bi-pencil"></i></a>
                </td>
            `;
            tbody.appendChild(tr);
        });
        
    } catch (error) {
        console.error("Error loading prescriptions:", error);
        document.getElementById('rxHistoryBody').innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading prescription history.</td></tr>';
    }
}

async function loadAiHistory() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/recommendations/history/${customerId}`);
        if (!response.ok) throw new Error('Failed to load AI history');
        
        const historyList = await response.json();
        const tbody = document.getElementById('aiHistoryBody');
        tbody.innerHTML = '';
        
        if (historyList.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-muted">No AI Frame Recommendations found.</td></tr>';
            return;
        }
        
        historyList.forEach(rec => {
            const date = new Date(rec.created_at).toLocaleDateString();
            const shapeBadge = `<span class="badge bg-primary bg-opacity-10 text-primary">${rec.face_shape}</span>`;
            
            let frameStr = rec.selected_frame || '-';
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${date}</td>
                <td>${shapeBadge}</td>
                <td class="fw-bold">${frameStr}</td>
                <td><small class="text-muted d-block" style="max-width: 300px; white-space: normal;">${rec.ai_reason}</small></td>
            `;
            tbody.appendChild(tr);
        });
        
    } catch (error) {
        console.error("Error loading AI history:", error);
        document.getElementById('aiHistoryBody').innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error loading AI history.</td></tr>';
    }
}

async function loadVtoHistory() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/vto/history/${customerId}`);
        if (!response.ok) throw new Error('Failed to load VTO history');
        
        const historyList = await response.json();
        const grid = document.getElementById('vtoHistoryGrid');
        grid.innerHTML = '';
        
        if (historyList.length === 0) {
            grid.innerHTML = '<div class="col-12 text-center text-muted py-4 border rounded bg-light">No Virtual Try-On snapshots found.</div>';
            return;
        }
        
        historyList.forEach(rec => {
            const date = new Date(rec.created_at).toLocaleDateString();
            
            const div = document.createElement('div');
            div.className = 'col-md-4 col-lg-3';
            div.innerHTML = `
                <div class="card h-100 shadow-sm">
                    <img src="${API_BASE_URL.replace('/api', '')}${rec.tryon_image}" class="card-img-top" alt="VTO Snapshot">
                    <div class="card-body p-2 text-center">
                        <small class="fw-bold d-block text-truncate">${rec.frame_name}</small>
                        <small class="text-muted">${date}</small>
                    </div>
                </div>
            `;
            grid.appendChild(div);
        });
        
    } catch (error) {
        console.error("Error loading VTO history:", error);
        document.getElementById('vtoHistoryGrid').innerHTML = '<div class="col-12 text-center text-danger py-4 border rounded bg-light">Error loading VTO history.</div>';
    }
}
