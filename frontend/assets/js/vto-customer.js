document.addEventListener('DOMContentLoaded', () => {
    // VTO Modal Elements
    const vtoModalEl = document.getElementById('vtoModal');
    if (!vtoModalEl) return;
    
    const vtoModal = new bootstrap.Modal(vtoModalEl);
    const videoElement = document.getElementById('vtoVideo');
    const canvasElement = document.getElementById('vtoCanvas');
    const canvasCtx = canvasElement ? canvasElement.getContext('2d') : null;
    const loadingOverlay = document.getElementById('vtoLoadingOverlay');
    const frameInfoContainer = document.getElementById('vtoFrameInfo');
    
    let camera = null;
    let isCameraRunning = false;
    let selectedFrameImage = null; // HTMLImageElement
    let faceMesh = null;

    // Listen for VTO button clicks (using event delegation for dynamically loaded products)
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-vto');
        if (btn) {
            e.preventDefault();
            const frameName = btn.dataset.itemName;
            const imgUrl = btn.dataset.itemImage;
            
            openVTO(frameName, imgUrl);
        }
    });
    
    function resizeCanvas() {
        if(videoElement && videoElement.videoWidth && canvasElement) {
            canvasElement.width = videoElement.videoWidth;
            canvasElement.height = videoElement.videoHeight;
        }
    }
    
    if (videoElement) {
        videoElement.addEventListener('loadedmetadata', resizeCanvas);
        window.addEventListener('resize', resizeCanvas);
    }

    function openVTO(frameName, imgUrl) {
        if (frameInfoContainer) {
            frameInfoContainer.innerHTML = `<h5 class="fw-bold mb-1">${frameName}</h5><p class="text-muted small mb-0">Look straight at the camera to try on</p>`;
        }
        
        // Preload frame image
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => { selectedFrameImage = img; };
        img.onerror = () => {
            console.warn("Failed to load frame image, creating programmatic fallback");
            const cvs = document.createElement('canvas');
            cvs.width = 400; cvs.height = 150;
            const ctx = cvs.getContext('2d');
            ctx.fillStyle = 'rgba(255,255,255,0)';
            ctx.fillRect(0,0,400,150);
            ctx.strokeStyle = 'rgba(20,20,20,0.95)';
            ctx.lineWidth = 12;
            ctx.beginPath(); ctx.roundRect(20, 20, 160, 110, 25); ctx.stroke();
            ctx.beginPath(); ctx.roundRect(220, 20, 160, 110, 25); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(180, 75); ctx.lineTo(220, 75); ctx.stroke();
            const fallbackImg = new Image();
            fallbackImg.src = cvs.toDataURL();
            selectedFrameImage = fallbackImg;
        };
        if (imgUrl.startsWith('/')) {
            const base = (window.API_BASE_URL || 'http://127.0.0.1:5000/api').replace('/api', '');
            img.src = base + imgUrl;
        } else {
            img.src = imgUrl;
        }

        vtoModal.show();
        startVTOEngine();
    }

    async function startVTOEngine() {
        if (loadingOverlay) loadingOverlay.style.display = 'flex';
        
        if (!faceMesh) {
            faceMesh = new FaceMesh({locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
            }});
            
            faceMesh.setOptions({
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });
            
            faceMesh.onResults(onResults);
        }

        if (!isCameraRunning && videoElement) {
            try {
                camera = new Camera(videoElement, {
                    onFrame: async () => {
                        if(videoElement.readyState >= 2) {
                            await faceMesh.send({image: videoElement});
                        }
                    },
                    width: 640,
                    height: 480
                });
                await camera.start();
                isCameraRunning = true;
                if (loadingOverlay) loadingOverlay.style.display = 'none';
            } catch (error) {
                console.error("Camera Error:", error);
                if (loadingOverlay) {
                    loadingOverlay.innerHTML = '<div class="text-danger"><i class="bi bi-exclamation-triangle fs-1"></i><h5 class="mt-2">Camera Access Denied</h5><p>Please allow camera permissions to use AR Try-On.</p></div>';
                }
            }
        }
    }

    function onResults(results) {
        if (!canvasCtx || !canvasElement) return;
        
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        
        if (canvasElement.width !== videoElement.videoWidth) {
            resizeCanvas();
        }
        
        if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0 && selectedFrameImage) {
            const landmarks = results.multiFaceLandmarks[0];
            const w = canvasElement.width;
            const h = canvasElement.height;
            
            const leftEye = landmarks[33]; 
            const rightEye = landmarks[263];
            const bridge = landmarks[168];
            
            const p1 = { x: leftEye.x * w, y: leftEye.y * h };
            const p2 = { x: rightEye.x * w, y: rightEye.y * h };
            const center = { x: bridge.x * w, y: bridge.y * h };
            
            const eyeDist = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
            const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
            
            const frameScale = (eyeDist * 2.2) / selectedFrameImage.width;
            const frameWidth = selectedFrameImage.width * frameScale;
            const frameHeight = selectedFrameImage.height * frameScale;
            
            canvasCtx.save();
            canvasCtx.translate(center.x, center.y);
            canvasCtx.rotate(angle);
            
            const yOffset = frameHeight * 0.15;
            canvasCtx.drawImage(
                selectedFrameImage, 
                -frameWidth / 2, 
                -frameHeight / 2 + yOffset, 
                frameWidth, 
                frameHeight
            );
            
            canvasCtx.restore();
        }
    }

    // Stop camera when modal is closed
    vtoModalEl.addEventListener('hidden.bs.modal', () => {
        if (camera && isCameraRunning) {
            camera.stop();
            isCameraRunning = false;
        }
        if (canvasCtx && canvasElement) {
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        }
    });
});
