const urlParams = new URLSearchParams(window.location.search);
const rxId = urlParams.get('id');

document.addEventListener('DOMContentLoaded', async () => {
    if (!rxId) {
        alert('No prescription ID provided');
        window.location.href = 'prescriptions.html';
        return;
    }
    
    document.getElementById('editBtn').href = `edit-prescription.html?id=${rxId}`;
    
    await loadPrescriptionData();
});

async function loadPrescriptionData() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/${rxId}`);
        if (!response.ok) throw new Error('Prescription not found');
        
        const rx = await response.json();
        
        document.getElementById('rxNumber').textContent = rx.prescription_number;
        document.getElementById('customerName').textContent = rx.customer_name;
        document.getElementById('customerIdTag').textContent = `Customer ID: ${rx.customer_id}`;
        
        document.getElementById('examDate').textContent = rx.date || '-';
        document.getElementById('expiryDate').textContent = rx.expiry_date || '-';
        document.getElementById('doctorName').textContent = rx.doctor_name || 'Optometrist';
        
        if (rx.status === 'Completed') {
            document.getElementById('view_status').className = 'badge bg-success bg-opacity-10 text-success px-2 py-1';
        } else if (rx.status === 'Draft') {
            document.getElementById('view_status').className = 'badge bg-warning bg-opacity-10 text-warning px-2 py-1';
        } else {
            document.getElementById('view_status').className = 'badge bg-secondary bg-opacity-10 text-secondary px-2 py-1';
        }
        document.getElementById('view_status').textContent = rx.status;
        
        const fields = ['distance_pd', 'near_pd', 'lens_type', 'lens_material', 'lens_coating', 'frame_recommendation'];
        fields.forEach(f => {
            if (rx[f]) document.getElementById(`view_${f}`).textContent = rx[f];
        });
        
        if (rx.notes) {
            document.getElementById('view_notes').textContent = rx.notes;
        }

        // Check for AI image
        if (rx.prescription_image) {
            document.getElementById('aiImageContainer').style.display = 'flex';
            // Because API runs on :5000, we need absolute URL for images
            document.getElementById('view_prescription_image').src = API_BASE_URL.replace('/api', '') + rx.prescription_image;
            
            let confText = (rx.confidence_score * 100).toFixed(1) + '%';
            const confSpan = document.getElementById('view_confidence');
            confSpan.textContent = confText;
            
            if (rx.confidence_score < 0.7) {
                confSpan.className = 'fw-bold text-danger';
            } else if (rx.confidence_score < 0.9) {
                confSpan.className = 'fw-bold text-warning';
            } else {
                confSpan.className = 'fw-bold text-success';
            }
        }
        
        const eyeFields = ['sph', 'cyl', 'axis', 'add', 'prism', 'base', 'va'];
        if (rx.od) {
            eyeFields.forEach(f => {
                if (rx.od[f]) document.getElementById(`view_od_${f}`).textContent = rx.od[f];
            });
        }
        
        if (rx.os) {
            eyeFields.forEach(f => {
                if (rx.os[f]) document.getElementById(`view_os_${f}`).textContent = rx.os[f];
            });
        }
        
    } catch (error) {
        console.error("Error loading prescription:", error);
        alert('Failed to load prescription');
        window.location.href = 'prescriptions.html';
    }
}

function downloadPDF() {
    showToast('Info', 'Generating PDF...');
    fetchWithAuth(`${API_BASE_URL}/prescriptions/${rxId}/pdf`)
        .then(async response => {
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.message || 'Failed to generate PDF');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Prescription_${rxId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showToast('Success', 'PDF downloaded successfully');
        })
        .catch(err => {
            console.error('Error downloading PDF:', err);
            showToast('Error', err.message || 'Could not download PDF');
        });
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
