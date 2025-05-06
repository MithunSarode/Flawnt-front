async function openCamera() {
    try {
        const video = document.getElementById('camera');
        const captureBtn = document.getElementById('capture-btn');
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        video.srcObject = stream;
        video.style.display = 'block';
        captureBtn.style.display = 'block';
    } catch (err) {
        alert('Camera Error: ' + err.message);
    }
}

function captureImage() {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current video frame on the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to image and save to localStorage
    const imageData = canvas.toDataURL('image/jpeg');
    localStorage.setItem('capturedImage', imageData);

    // Stop the camera stream
    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());

    // Redirect to the captured image page
    window.location.href = 'captured.html';
}

// Add event listener when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log("Fiawnt UI loaded.");
}); 