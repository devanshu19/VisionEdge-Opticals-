document.addEventListener('DOMContentLoaded', async () => {
    // Set default dates
    document.getElementById('date').valueAsDate = new Date();
    const expiry = new Date();
    expiry.setFullYear(expiry.getFullYear() + 1);
    document.getElementById('expiryDate').valueAsDate = expiry;
    
    // Load customers for dropdown
    await loadCustomers();
    
    // Check for AI Extracted Data
    const aiData = sessionStorage.getItem('ai_prescription_data');
    if (aiData) {
        try {
            const data = JSON.parse(aiData);
            
            // Auto-fill values
            if (data.data.right_sphere) document.getElementById('od_sph').value = data.data.right_sphere;
            if (data.data.right_cylinder) document.getElementById('od_cyl').value = data.data.right_cylinder;
            if (data.data.right_axis) document.getElementById('od_axis').value = data.data.right_axis;
            
            if (data.data.left_sphere) document.getElementById('os_sph').value = data.data.left_sphere;
            if (data.data.left_cylinder) document.getElementById('os_cyl').value = data.data.left_cylinder;
            if (data.data.left_axis) document.getElementById('os_axis').value = data.data.left_axis;
            
            if (data.data.add_power) {
                document.getElementById('od_add').value = data.data.add_power;
                document.getElementById('os_add').value = data.data.add_power;
            }
            if (data.data.pd) {
                document.getElementById('distance_pd').value = data.data.pd;
            }
            
            document.getElementById('source').value = 'AI Extraction';
            
            // Show toast notification
            let msg = 'Values auto-filled from AI extraction.';
            if (data.confidence < 0.70) {
                msg = '<span class="text-danger fw-bold"><i class="bi bi-exclamation-triangle"></i> Low confidence. Please verify manually.</span>';
            }
            showToast('AI Analysis Complete', msg);
            
        } catch (e) {
            console.error("Failed to parse AI data", e);
        }
    }
    
    // Handle form submit
    document.getElementById('addRxForm').addEventListener('submit', handleAddRx);
});

async function loadCustomers() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/`);
        if (response.ok) {
            const customers = await response.json();
            const select = document.getElementById('customerId');
            select.innerHTML = '<option value="" selected disabled>Select a customer...</option>';
            
            const urlParams = new URLSearchParams(window.location.search);
            const predefinedCustomer = urlParams.get('customer_id');
            
            customers.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = `${c.name} (${c.phone})`;
                if (predefinedCustomer && c.id == predefinedCustomer) {
                    opt.selected = true;
                }
                select.appendChild(opt);
            });
        }
    } catch (error) {
        console.error("Failed to load customers:", error);
    }
}

async function handleAddRx(e) {
    e.preventDefault();
    const form = e.target;
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const btn = document.getElementById('saveBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';
    btn.disabled = true;
    
    const data = {
        customer_id: document.getElementById('customerId').value,
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
        source: document.getElementById('source').value,
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
    
    // Inject AI metadata if available
    const aiData = sessionStorage.getItem('ai_prescription_data');
    if (aiData) {
        try {
            const parsed = JSON.parse(aiData);
            data.prescription_image = parsed.image_url;
            data.ai_raw_text = parsed.raw_text;
            data.confidence_score = parsed.confidence;
        } catch(e) {}
    }
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            sessionStorage.removeItem('ai_prescription_data');
            showToast('Success', 'Prescription created successfully!');
            setTimeout(() => {
                window.location.href = `view-prescription.html?id=${result.prescription.id}`;
            }, 1000);
        } else {
            alert(result.message || 'Failed to create prescription');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error while saving prescription');
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
