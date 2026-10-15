const urlParams = new URLSearchParams(window.location.search);
const rxId = urlParams.get('id');

document.addEventListener('DOMContentLoaded', async () => {
    if (!rxId) {
        alert('No prescription ID provided');
        window.location.href = 'prescriptions.html';
        return;
    }
    
    await loadCustomers();
    await loadPrescriptionData();
    
    document.getElementById('addRxForm').addEventListener('submit', handleUpdateRx);
});

async function loadCustomers() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/`);
        if (response.ok) {
            const customers = await response.json();
            const select = document.getElementById('customerId');
            select.innerHTML = '<option value="" selected disabled>Select a customer...</option>';
            
            customers.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = `${c.name} (${c.phone})`;
                select.appendChild(opt);
            });
        }
    } catch (error) {
        console.error("Failed to load customers:", error);
    }
}

async function loadPrescriptionData() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/${rxId}`);
        if (!response.ok) throw new Error('Prescription not found');
        
        const rx = await response.json();
        
        document.getElementById('customerId').value = rx.customer_id;
        document.getElementById('customerId').disabled = true; // Don't allow changing customer
        document.getElementById('doctorName').value = rx.doctor_name || '';
        document.getElementById('date').value = rx.date;
        if(rx.expiry_date) document.getElementById('expiryDate').value = rx.expiry_date;
        document.getElementById('status').value = rx.status;
        
        document.getElementById('distance_pd').value = rx.distance_pd || '';
        document.getElementById('near_pd').value = rx.near_pd || '';
        document.getElementById('lensType').value = rx.lens_type || '';
        document.getElementById('lensMaterial').value = rx.lens_material || '';
        document.getElementById('lensCoating').value = rx.lens_coating || '';
        document.getElementById('frameRecommendation').value = rx.frame_recommendation || '';
        document.getElementById('notes').value = rx.notes || '';
        
        if (rx.od) {
            document.getElementById('od_sph').value = rx.od.sph || '';
            document.getElementById('od_cyl').value = rx.od.cyl || '';
            document.getElementById('od_axis').value = rx.od.axis || '';
            document.getElementById('od_add').value = rx.od.add || '';
            document.getElementById('od_prism').value = rx.od.prism || '';
            document.getElementById('od_base').value = rx.od.base || '';
            document.getElementById('od_va').value = rx.od.va || '';
            document.getElementById('od_pd').value = rx.od.pd || '';
        }
        
        if (rx.os) {
            document.getElementById('os_sph').value = rx.os.sph || '';
            document.getElementById('os_cyl').value = rx.os.cyl || '';
            document.getElementById('os_axis').value = rx.os.axis || '';
            document.getElementById('os_add').value = rx.os.add || '';
            document.getElementById('os_prism').value = rx.os.prism || '';
            document.getElementById('os_base').value = rx.os.base || '';
            document.getElementById('os_va').value = rx.os.va || '';
            document.getElementById('os_pd').value = rx.os.pd || '';
        }
        
    } catch (error) {
        console.error("Error loading prescription:", error);
        alert('Failed to load prescription');
        window.location.href = 'prescriptions.html';
    }
}

async function handleUpdateRx(e) {
    e.preventDefault();
    const form = e.target;
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const btn = document.getElementById('saveBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Updating...';
    btn.disabled = true;
    
    const data = {
        doctor_name: document.getElementById('doctorName').value,
        date: document.getElementById('date').value,
        expiry_date: document.getElementById('expiryDate').value,
        status: document.getElementById('status').value,
        distance_pd: document.getElementById('distance_pd').value,
        near_pd: document.getElementById('near_pd').value,
        lens_type: document.getElementById('lensType').value,
        lens_material: document.getElementById('lensMaterial').value,
        lens_coating: document.getElementById('lensCoating').value,
        frame_recommendation: document.getElementById('frameRecommendation').value,
        notes: document.getElementById('notes').value,
        od: {
            sph: document.getElementById('od_sph').value,
            cyl: document.getElementById('od_cyl').value,
            axis: document.getElementById('od_axis').value,
            add: document.getElementById('od_add').value,
            prism: document.getElementById('od_prism').value,
            base: document.getElementById('od_base').value,
            va: document.getElementById('od_va').value,
            pd: document.getElementById('od_pd').value
        },
        os: {
            sph: document.getElementById('os_sph').value,
            cyl: document.getElementById('os_cyl').value,
            axis: document.getElementById('os_axis').value,
            add: document.getElementById('os_add').value,
            prism: document.getElementById('os_prism').value,
            base: document.getElementById('os_base').value,
            va: document.getElementById('os_va').value,
            pd: document.getElementById('os_pd').value
        }
    };
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/${rxId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('Success', 'Prescription updated successfully!');
            setTimeout(() => {
                window.location.href = `view-prescription.html?id=${rxId}`;
            }, 1000);
        } else {
            alert(result.message || 'Failed to update prescription');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error while updating prescription');
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function showToast(title, message) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toastHtml = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-primary text-white">
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', toastHtml);
    const toast = new bootstrap.Toast(container.lastElementChild, { delay: 2000 });
    toast.show();
}
