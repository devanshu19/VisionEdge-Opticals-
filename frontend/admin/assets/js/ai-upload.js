document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const btnExtract = document.getElementById('btnExtract');
    const btnCancel = document.getElementById('btnCancel');
    const uploadView = document.getElementById('uploadView');
    const processingView = document.getElementById('processingView');
    const errorAlert = document.getElementById('errorAlert');
    const mockWarning = document.getElementById('mockWarning');
    
    let selectedFile = null;

    // Drag and Drop Events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    // File Input Event
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            handleFileSelection(this.files[0]);
        }
    });

    function handleFileSelection(file) {
        errorAlert.style.display = 'none';
        
        const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            showError("Invalid file type. Please upload a JPG, PNG, or WEBP image.");
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            showError("File size exceeds 5MB limit.");
            return;
        }

        selectedFile = file;
        
        // Show Preview
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            dropZone.style.display = 'none';
            previewContainer.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }

    btnCancel.addEventListener('click', () => {
        selectedFile = null;
        fileInput.value = '';
        dropZone.style.display = 'block';
        previewContainer.style.display = 'none';
        errorAlert.style.display = 'none';
    });

    btnExtract.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Switch to Processing View
        uploadView.style.display = 'none';
        processingView.style.display = 'block';
        document.getElementById('scannerBgImage').src = imagePreview.src;
        
        // Prepare FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const token = localStorage.getItem('ve_token');
            const response = await fetch(`${API_BASE_URL}/ai/extract`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                // Store AI data in sessionStorage to auto-fill the prescription form
                const prescriptionData = {
                    ai_extracted: true,
                    image_url: result.image_url,
                    confidence: result.confidence,
                    raw_text: result.raw_text,
                    data: result.data,
                    is_mocked: result.mocked
                };
                
                sessionStorage.setItem('ai_prescription_data', JSON.stringify(prescriptionData));
                
                // Redirect to Add Prescription page
                window.location.href = 'add-prescription.html';
            } else {
                throw new Error(result.message || "Failed to extract data");
            }
        } catch (error) {
            // Revert back to upload view and show error
            uploadView.style.display = 'block';
            processingView.style.display = 'none';
            showError(error.message);
        }
    });

    function showError(msg) {
        errorAlert.textContent = msg;
        errorAlert.style.display = 'block';
    }
});
