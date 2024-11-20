// Array of background images
const backgrounds = [
    '/static/assets/background.jpg',
    '/static/assets/background1.jpg',
    '/static/assets/background2.jpg',
    '/static/assets/background3.jpg',
];

let currentIndex = 0;  // Keep track of the current background index

// Function to change the background image
function changeBackground() {
    currentIndex = (currentIndex + 1) % backgrounds.length;
    document.body.style.backgroundImage = `url('${backgrounds[currentIndex]}')`;
}

// Change background every 12 seconds
setInterval(changeBackground, 12000);  // 12000 milliseconds = 12 seconds

// Initial background change when page loads
window.onload = changeBackground;
