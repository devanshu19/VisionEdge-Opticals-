document.addEventListener('DOMContentLoaded', async () => {
    await loadCustomers();
    await loadFrames();
    
    // UI Elements
    const videoElement = document.getElementById('webcamVideo');
    const canvasElement = document.getElementById('overlayCanvas');
    const canvasCtx = canvasElement.getContext('2d');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const btnToggleCamera = document.getElementById('btnToggleCamera');
    const btnSnapshot = document.getElementById('btnSnapshot');
    
    // Snapshot UI
    const snapshotResultArea = document.getElementById('snapshotResultArea');
    const waitingSnapshotState = document.getElementById('waitingSnapshotState');
    const snapshotPreview = document.getElementById('snapshotPreview');
    const btnSaveHistory = document.getElementById('btnSaveHistory');
    const btnRetake = document.getElementById('btnRetake');
    
    let camera = null;
    let isCameraRunning = false;
    let selectedFrameImage = null; // HTMLImageElement
    let selectedFrameData = null; // Object {id, name...}
    let currentSnapshotBase64 = null;
    
    // Resize canvas to match video stream
    function resizeCanvas() {
        if(videoElement.videoWidth) {
            canvasElement.width = videoElement.videoWidth;
            canvasElement.height = videoElement.videoHeight;
        }
    }
    videoElement.addEventListener('loadedmetadata', resizeCanvas);
    window.addEventListener('resize', resizeCanvas);
    
    // Initialize FaceMesh
    const faceMesh = new FaceMesh({locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
    }});
    
    faceMesh.setOptions({
        maxNumFaces: 1,
        refineLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });
    
    faceMesh.onResults(onResults);
    
    // Start Camera
    async function startCamera() {
        try {
            camera = new Camera(videoElement, {
                onFrame: async () => {
                    await faceMesh.send({image: videoElement});
                },
                width: 640,
                height: 480
            });
            await camera.start();
            isCameraRunning = true;
            loadingOverlay.style.display = 'none';
            btnToggleCamera.innerHTML = '<i class="bi bi-camera-fill me-1"></i>Stop Camera';
            btnSnapshot.disabled = false;
        } catch (error) {
            console.error("Camera Error:", error);
            loadingOverlay.innerHTML = '<div class="text-danger"><i class="bi bi-exclamation-triangle fs-1"></i><h5 class="mt-2">Camera Access Denied</h5></div>';
        }
    }
    
    btnToggleCamera.addEventListener('click', () => {
        if (isCameraRunning) {
            camera.stop();
            isCameraRunning = false;
            btnToggleCamera.innerHTML = '<i class="bi bi-camera-fill me-1"></i>Start Camera';
            btnSnapshot.disabled = true;
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        } else {
            loadingOverlay.style.display = 'flex';
            startCamera();
        }
    });
    
    startCamera();
    
    // Process FaceMesh Results
    function onResults(results) {
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        
        // Ensure dimensions match
        if (canvasElement.width !== videoElement.videoWidth) {
            resizeCanvas();
        }
        
        if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0 && selectedFrameImage) {
            const landmarks = results.multiFaceLandmarks[0];
            
            // MediaPipe Coordinates are normalized [0, 1]
            const w = canvasElement.width;
            const h = canvasElement.height;
            
            // Outer eye corners for width and angle
            // Left eye outer: 33, Right eye outer: 263
            const leftEye = landmarks[33]; 
            const rightEye = landmarks[263];
            
            // Bridge of nose for center: 168
            const bridge = landmarks[168];
            
            const p1 = { x: leftEye.x * w, y: leftEye.y * h };
            const p2 = { x: rightEye.x * w, y: rightEye.y * h };
            const center = { x: bridge.x * w, y: bridge.y * h };
            
            // Calculate distance between eyes (width of glasses should be proportional)
            const eyeDist = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
            
            // Calculate angle
            const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
            
            // Scale frame based on eye distance
            // Usually glasses width is about 2 to 2.2 times the distance between outer eye corners
            const frameScale = (eyeDist * 2.1) / selectedFrameImage.width;
            
            const frameWidth = selectedFrameImage.width * frameScale;
            const frameHeight = selectedFrameImage.height * frameScale;
            
            // Save context
            canvasCtx.save();
            
            // Translate to bridge of nose
            canvasCtx.translate(center.x, center.y);
            
            // Rotate based on eye angle
            canvasCtx.rotate(angle);
            
            // Draw image centered (slightly offset Y to sit on nose properly)
            // Tweak the Y offset depending on the specific frame asset
            const yOffset = frameHeight * 0.1;
            canvasCtx.drawImage(
                selectedFrameImage, 
                -frameWidth / 2, 
                -frameHeight / 2 + yOffset, 
                frameWidth, 
                frameHeight
            );
            
            // Restore context
            canvasCtx.restore();
        }
    }
    
    // Take Snapshot
    btnSnapshot.addEventListener('click', () => {
        if (!selectedFrameData) {
            showToast('Warning', 'Please select a frame first.');
            return;
        }
        
        // Create a temporary canvas to composite video + overlay
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = videoElement.videoWidth;
        tempCanvas.height = videoElement.videoHeight;
        const tempCtx = tempCanvas.getContext('2d');
        
        // Draw video (it is mirrored in CSS, so we must mirror it on canvas too)
        tempCtx.translate(tempCanvas.width, 0);
        tempCtx.scale(-1, 1);
        tempCtx.drawImage(videoElement, 0, 0, tempCanvas.width, tempCanvas.height);
        
        // Draw overlay (already mirrored correctly relative to the mirrored video space)
        // Actually, the canvasElement is also mirrored via CSS. 
        // When we draw it onto tempCanvas (which is currently scaled -1,1), we need to revert scale?
        // Let's just reset transform, because the overlay logic was drawn over un-mirrored coordinates, 
        // but displayed mirrored via CSS.
        tempCtx.setTransform(1, 0, 0, 1, 0, 0);
        
        // Draw video normally first, but flipped horizontally
        tempCtx.translate(tempCanvas.width, 0);
        tempCtx.scale(-1, 1);
        tempCtx.drawImage(videoElement, 0, 0);
        
        // Draw the overlay (it was drawn using raw mediapipe coords over the raw video coords)
        tempCtx.drawImage(canvasElement, 0, 0);
        
        currentSnapshotBase64 = tempCanvas.toDataURL('image/jpeg', 0.9);
        
        snapshotPreview.src = currentSnapshotBase64;
        waitingSnapshotState.style.display = 'none';
        snapshotResultArea.style.display = 'block';
    });
    
    btnRetake.addEventListener('click', () => {
        snapshotResultArea.style.display = 'none';
        waitingSnapshotState.style.display = 'block';
        currentSnapshotBase64 = null;
    });
    
    // Save to backend
    btnSaveHistory.addEventListener('click', async () => {
        const cid = document.getElementById('customerId').value;
        if (!cid) {
            showToast('Error', 'Please select a customer first to save history.');
            return;
        }
        
        if (!currentSnapshotBase64 || !selectedFrameData) return;
        
        const btn = document.getElementById('btnSaveHistory');
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Saving...';
        btn.disabled = true;
        
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/vto/save-history`, {
                method: 'POST',
                body: JSON.stringify({
                    customer_id: cid,
                    frame_id: selectedFrameData.id,
                    snapshot: currentSnapshotBase64
                })
            });
            
            if (response.ok) {
                showToast('Success', 'VTO Snapshot saved to customer profile!');
                setTimeout(() => {
                    window.location.href = `view-customer.html?id=${cid}&tab=ai`;
                }, 1500);
            } else {
                const data = await response.json();
                throw new Error(data.message);
            }
        } catch (error) {
            showToast('Error', error.message || 'Failed to save');
            btn.innerHTML = '<i class="bi bi-cloud-arrow-up-fill me-2"></i>Save to Customer Profile';
            btn.disabled = false;
        }
    });
    
    // Load Data Functions
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
    
    async function loadFrames() {
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/vto/frames`);
            if (response.ok) {
                const frames = await response.json();
                const container = document.getElementById('frameSelector');
                container.innerHTML = '';
                
                if (frames.length === 0) {
                    container.innerHTML = '<div class="text-muted p-3">No VTO-ready frames available.</div>';
                    return;
                }
                
                frames.forEach((f, idx) => {
                    const imgUrl = f.vto_image.startsWith('/api') ? API_BASE_URL.replace('/api', '') + f.vto_image : f.vto_image;
                    
                    const div = document.createElement('div');
                    div.className = 'frame-item';
                    if (idx === 0) div.classList.add('active'); // Select first by default
                    
                    div.innerHTML = `
                        <img src="${imgUrl}" alt="${f.name}">
                        <div class="fw-bold small text-truncate" style="max-width: 120px;">${f.name}</div>
                        <div class="text-muted" style="font-size: 0.75rem;">₹${f.price}</div>
                    `;
                    
                    div.addEventListener('click', () => {
                        document.querySelectorAll('.frame-item').forEach(el => el.classList.remove('active'));
                        div.classList.add('active');
                        setFrame(f, imgUrl);
                    });
                    
                    container.appendChild(div);
                    
                    if (idx === 0) setFrame(f, imgUrl);
                });
            }
        } catch (e) {
            console.error("Failed to load VTO frames", e);
        }
    }
    
    function setFrame(frameObj, imgUrl) {
        selectedFrameData = frameObj;
        
        // Preload image for canvas
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
            selectedFrameImage = img;
        };
        // For local dev where no real image exists, we'll draw a dummy fallback if it fails
        img.onerror = () => {
            console.warn("Failed to load frame image, creating programmatic fallback");
            const cvs = document.createElement('canvas');
            cvs.width = 400; cvs.height = 150;
            const ctx = cvs.getContext('2d');
            ctx.fillStyle = 'rgba(255,255,255,0)';
            ctx.fillRect(0,0,400,150);
            
            ctx.strokeStyle = 'rgba(50,50,50,0.9)';
            ctx.lineWidth = 10;
            // left lens
            ctx.beginPath(); ctx.roundRect(20, 20, 160, 110, 20); ctx.stroke();
            // right lens
            ctx.beginPath(); ctx.roundRect(220, 20, 160, 110, 20); ctx.stroke();
            // bridge
            ctx.beginPath(); ctx.moveTo(180, 75); ctx.lineTo(220, 75); ctx.stroke();
            
            const fallbackImg = new Image();
            fallbackImg.src = cvs.toDataURL();
            selectedFrameImage = fallbackImg;
        };
        img.src = imgUrl;
    }
});

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
