document.addEventListener("DOMContentLoaded", function() {
    // 动态加载导航栏
    fetch('nav.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar-container').innerHTML = data;

            // 绑定导航按钮的点击事件
            const navToggleButton = document.querySelector(".nav-toggle");
            if (navToggleButton) {
                navToggleButton.onclick = toggleNavbar;
            } else {
                console.error("Nav toggle button not found!");
            }
        })
        .catch(error => console.error('Error loading navbar:', error));
});


// Function to toggle navbar visibility on small screens
function toggleNavbar() {
    const navLinks = document.querySelector('#nav .nav-links');
    if (navLinks) {
        navLinks.classList.toggle('show'); // Toggle 'show' class to control visibility
    } else {
        console.error("Nav links element not found!");
    }
}

// Change navbar background color on scroll for better visibility
window.addEventListener('scroll', function() {
    const nav = document.getElementById('nav');
    if (window.scrollY > 50) {
        nav.style.backgroundColor = 'rgba(128, 128, 128, 0.8)'; // Semi-transparent gray
    } else {
        nav.style.backgroundColor = 'rgba(128, 128, 128, 1)'; // Fully opaque gray
    }
});
