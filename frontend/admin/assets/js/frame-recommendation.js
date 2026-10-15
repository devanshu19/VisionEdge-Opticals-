document.addEventListener('DOMContentLoaded', async () => {
    await loadCustomers();
    
    // UI Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadUi = document.getElementById('uploadUi');
    const analysisUi = document.getElementById('analysisUi');
    const facePreview = document.getElementById('facePreview');
    const scanLine = document.getElementById('scanLine');
    const shapeResult = document.getElementById('shapeResult');
    const detectedShape = document.getElementById('detectedShape');
    const detectedConfidence = document.getElementById('detectedConfidence');
    const btnResetFace = document.getElementById('btnResetFace');
    const btnGenerate = document.getElementById('btnGenerate');
    const form = document.getElementById('recommendationForm');
    
    let currentAiData = null;
    let selectedFrameId = null;
    
    // Drag and Drop
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave', (e) => { e.preventDefault(); dropZone.classList.remove('dragover'); });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
    
    fileInput.addEventListener('change', function() {
        if (this.files.length) handleFile(this.files[0]);
    });
    
    function handleFile(file) {
        if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
            showToast('Error', 'Invalid file type. Use JPG or PNG.');
            return;
        }
        
        // Show preview and scan animation
        const reader = new FileReader();
        reader.onload = (e) => {
            facePreview.src = e.target.result;
            uploadUi.style.display = 'none';
            analysisUi.style.display = 'block';
            shapeResult.style.display = 'none';
            scanLine.style.display = 'block';
            btnGenerate.disabled = true;
            
            // Upload to backend for analysis
            analyzeFace(file);
        };
        reader.readAsDataURL(file);
    }
    
    async function analyzeFace(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/recommendations/analyze-face`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            scanLine.style.display = 'none';
            
            if (response.ok) {
                shapeResult.style.display = 'block';
                detectedShape.textContent = data.face_shape;
                detectedConfidence.textContent = (data.confidence * 100).toFixed(1) + '%';
                document.getElementById('faceShapeValue').value = data.face_shape;
                document.getElementById('faceImageUrl').value = data.image_url;
                
                if(data.is_mock) {
                    document.getElementById('mockWarning').style.display = 'block';
                }
                
                checkFormValidity();
            } else {
                showToast('Analysis Failed', data.message);
                resetFace();
            }
        } catch (error) {
            scanLine.style.display = 'none';
            showToast('Error', 'Network error during analysis');
            resetFace();
        }
    }
    
    btnResetFace.addEventListener('click', resetFace);
    
    function resetFace() {
        uploadUi.style.display = 'block';
        analysisUi.style.display = 'none';
        fileInput.value = '';
        document.getElementById('faceShapeValue').value = '';
        checkFormValidity();
    }
    
    document.getElementById('customerId').addEventListener('change', checkFormValidity);
    
    function checkFormValidity() {
        const cid = document.getElementById('customerId').value;
        const shape = document.getElementById('faceShapeValue').value;
        btnGenerate.disabled = !(cid && shape);
    }
    
    // Generate AI
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            customer_id: document.getElementById('customerId').value,
            budget: document.getElementById('budget').value,
            size: document.getElementById('size').value,
            usage: document.getElementById('usage').value,
            face_shape: document.getElementById('faceShapeValue').value
        };
        
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('successState').style.display = 'none';
        document.getElementById('loadingState').style.display = 'block';
        document.getElementById('resultStatus').textContent = 'Generating...';
        document.getElementById('resultStatus').className = 'badge bg-warning text-dark';
        
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/recommendations/generate`, {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            document.getElementById('loadingState').style.display = 'none';
            
            if (response.ok) {
                document.getElementById('successState').style.display = 'block';
                document.getElementById('resultStatus').textContent = 'Analysis Complete';
                document.getElementById('resultStatus').className = 'badge bg-success';
                
                currentAiData = data;
                renderRecommendations(data);
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            document.getElementById('loadingState').style.display = 'none';
            document.getElementById('emptyState').style.display = 'block';
            showToast('Error', error.message || 'Failed to generate recommendations');
        }
    });
    
    function renderRecommendations(data) {
        document.getElementById('aiReasoningText').textContent = data.ai_analysis.reason;
        
        const grid = document.getElementById('recommendedFramesGrid');
        grid.innerHTML = '';
        selectedFrameId = null;
        document.getElementById('actionButtons').style.display = 'none';
        
        if (data.recommended_frames.length === 0) {
            grid.innerHTML = '<div class="col-12 text-center text-muted p-4">No matching frames found in inventory for these criteria.</div>';
            return;
        }
        
        data.recommended_frames.forEach(frame => {
            const imgPath = frame.image ? API_BASE_URL.replace('/api', '') + frame.image : 'assets/images/placeholder.jpg';
            
            const div = document.createElement('div');
            div.className = 'col-md-6';
            div.innerHTML = `
                <div class="card frame-card h-100" data-id="${frame.id}" data-name="${frame.name}" style="cursor:pointer;">
                    <div class="card-body text-center p-4">
                        <img src="${imgPath}" alt="${frame.name}" class="img-fluid mb-3" style="max-height: 120px;">
                        <h6 class="fw-bold mb-1">${frame.name}</h6>
                        <p class="text-muted small mb-2">${frame.brand} • ${frame.shape}</p>
                        <h5 class="text-primary mb-3">₹${frame.price.toFixed(2)}</h5>
                        <span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25">Stock: ${frame.stock}</span>
                    </div>
                </div>
            `;
            
            div.querySelector('.frame-card').addEventListener('click', function() {
                document.querySelectorAll('.frame-card').forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                selectedFrameId = { id: frame.id, name: frame.name };
                document.getElementById('actionButtons').style.display = 'block';
            });
            
            grid.appendChild(div);
        });
    }
    
    // Save Selection
    document.getElementById('btnSaveSelection').addEventListener('click', async () => {
        if (!selectedFrameId || !currentAiData) return;
        
        const payload = {
            customer_id: document.getElementById('customerId').value,
            face_shape: document.getElementById('faceShapeValue').value,
            face_image: document.getElementById('faceImageUrl').value,
            recommended_frames: currentAiData.recommended_frames,
            ai_reason: currentAiData.ai_analysis.reason,
            selected_frame: selectedFrameId.name
        };
        
        const btn = document.getElementById('btnSaveSelection');
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Saving...';
        btn.disabled = true;
        
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/recommendations/save`, {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                showToast('Success', 'Recommendation saved successfully!');
                setTimeout(() => {
                    window.location.href = `view-customer.html?id=${payload.customer_id}&tab=ai`;
                }, 1000);
            } else {
                const data = await response.json();
                throw new Error(data.message);
            }
        } catch (error) {
            showToast('Error', error.message || 'Failed to save');
            btn.innerHTML = '<i class="bi bi-check2-circle me-2"></i>Save Selection & Proceed';
            btn.disabled = false;
        }
    });
});

async function loadCustomers() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/`);
        if (response.ok) {
            const customers = await response.json();
            const select = document.getElementById('customerId');
            
            const urlParams = new URLSearchParams(window.location.search);
            const preselectId = urlParams.get('customer_id');
            
            customers.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = `${c.name} (${c.phone})`;
                if (preselectId && c.id == preselectId) opt.selected = true;
                select.appendChild(opt);
            });
        }
    } catch (e) {
        console.error("Failed to load customers", e);
    }
}

function showToast(title, message) {
    let container = document.getElementById('toastContainer');
    const toastHtml = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-primary text-white">
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', toastHtml);
    const toast = new bootstrap.Toast(container.lastElementChild, { delay: 3000 });
    toast.show();
}
