const urlParams = new URLSearchParams(window.location.search);
const customerId = urlParams.get('id');

document.addEventListener('DOMContentLoaded', async () => {
    if (!customerId) {
        alert('No customer ID provided');
        window.location.href = 'customers.html';
        return;
    }
    
    await loadCustomerData();
    
    const form = document.getElementById('editCustomerForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!form.checkValidity()) {
            e.stopPropagation();
            form.classList.add('was-validated');
            return;
        }
        
        const saveBtn = document.getElementById('saveBtn');
        const originalText = saveBtn.innerHTML;
        saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';
        saveBtn.disabled = true;
        
        const customerData = {
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            gender: document.getElementById('gender').value,
            dob: document.getElementById('dob').value || null,
            occupation: document.getElementById('occupation').value,
            
            phone: document.getElementById('phone').value,
            alternate_phone: document.getElementById('alternatePhone').value,
            email: document.getElementById('email').value,
            
            address: document.getElementById('address').value,
            city: document.getElementById('city').value,
            state: document.getElementById('state').value,
            pincode: document.getElementById('pincode').value,
            
            emergency_contact: document.getElementById('emergencyContact').value,
            emergency_phone: document.getElementById('emergencyPhone').value,
            blood_group: document.getElementById('bloodGroup').value,
            
            eye_condition: document.getElementById('eyeCondition').value,
            lens_preference: document.getElementById('lensPreference').value,
            frame_preference: document.getElementById('framePreference').value,
            doctor_name: document.getElementById('doctorName').value,
            
            status: document.getElementById('status').checked ? 'Active' : 'Inactive'
        };
        
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/customers/${customerId}`, {
                method: 'PUT',
                body: JSON.stringify(customerData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Success', 'Customer updated successfully! Redirecting...');
                setTimeout(() => {
                    window.location.href = `customer-details.html?id=${data.customer.id}`;
                }, 1500);
            } else {
                showToast('Error', data.message || 'Failed to update customer');
                saveBtn.innerHTML = originalText;
                saveBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Error', 'Network error occurred while saving.');
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        }
    });
});

async function loadCustomerData() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/${customerId}`);
        if (!response.ok) throw new Error('Customer not found');
        
        const data = await response.json();
        
        document.getElementById('firstName').value = data.first_name || '';
        document.getElementById('lastName').value = data.last_name || '';
        document.getElementById('gender').value = data.gender || '';
        document.getElementById('dob').value = data.dob || '';
        document.getElementById('occupation').value = data.occupation || '';
        
        document.getElementById('phone').value = data.phone || '';
        document.getElementById('alternatePhone').value = data.alternate_phone || '';
        document.getElementById('email').value = data.email || '';
        
        document.getElementById('address').value = data.address || '';
        document.getElementById('city').value = data.city || '';
        document.getElementById('state').value = data.state || '';
        document.getElementById('pincode').value = data.pincode || '';
        
        document.getElementById('emergencyContact').value = data.emergency_contact || '';
        document.getElementById('emergencyPhone').value = data.emergency_phone || '';
        document.getElementById('bloodGroup').value = data.blood_group || '';
        
        document.getElementById('eyeCondition').value = data.eye_condition || '';
        document.getElementById('lensPreference').value = data.lens_preference || '';
        document.getElementById('framePreference').value = data.frame_preference || '';
        document.getElementById('doctorName').value = data.doctor_name || '';
        
        document.getElementById('status').checked = data.status === 'Active';
        
    } catch (error) {
        console.error("Error loading customer details:", error);
        alert('Failed to load customer details');
        window.location.href = 'customers.html';
    }
}

function showToast(title, message) {
    const container = document.getElementById('toastContainer');
    const toastHtml = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-primary text-white">
                <i class="bi bi-info-circle me-2"></i>
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', toastHtml);
    const toastEl = container.lastElementChild;
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}
