window.addEventListener('load', () => {
    // Access webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const video = document.getElementById('video');
            video.srcObject = stream;
            video.play();
        })
        .catch(error => {
            console.error("Error accessing camera:", error);
        });

    // Capture image on button click
    const captureButton = document.getElementById('capture');
    captureButton.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const video = document.getElementById('video');

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Rotate 180 degrees
        context.translate(canvas.width, canvas.height);
        context.rotate(Math.PI);

        // Draw the mirrored and inverted image
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/jpeg');

        // Send image data to Django view using AJAX
        fetch('/process_image', {
            method: 'POST',
            body: imageData
        })
        .then(response => {
            console.log("Image sent to server:", response);
        })
        .catch(error => {
            console.error("Error sending image:", error);
        });
    });
});
// Capture image on button click
const captureButton = document.getElementById('capture');
captureButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    const video = document.getElementById('video');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL('image/jpeg');

    // Send image data to Django view using AJAX
    fetch('/process_image/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
        },
        body: new URLSearchParams({
            'image_data': imageData,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Image sent to server:", data);
    })
    .catch(error => {
        console.error("Error sending image:", error);
    });
});
