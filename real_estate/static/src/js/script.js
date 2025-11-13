// Real Estate Module JavaScript - Vanilla JS Version
document.addEventListener('DOMContentLoaded', function() {
    console.log('Real Estate module loaded');

    // Toggle property details with smooth animation
    document.querySelectorAll('.toggle-details').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const details = this.parentElement.querySelector('.details');
            if (details) {
                if (details.style.display === 'none' || details.style.display === '') {
                    details.style.display = 'block';
                    this.textContent = 'Hide Details';
                } else {
                    details.style.display = 'none';
                    this.textContent = 'View Details';
                }
            }
        });
    });

    // Enhanced search functionality
    const searchInput = document.getElementById('property-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            document.querySelectorAll('.property-item').forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm) || searchTerm === '') {
                    item.style.display = '';
                    item.style.opacity = '1';
                } else {
                    item.style.opacity = '0';
                    setTimeout(function() {
                        if (item.style.opacity === '0') {
                            item.style.display = 'none';
                        }
                    }, 200);
                }
            });
        });
    }

    // Contact agent button
    document.querySelectorAll('.btn-success').forEach(function(btn) {
        if (btn.textContent.includes('Contact Agent')) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                alert('Contact form would open here. Phone: +1-234-567-8900');
            });
        }
    });

    // Schedule viewing button
    document.querySelectorAll('.btn-outline-primary').forEach(function(btn) {
        if (btn.textContent.includes('Schedule Viewing')) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                alert('Calendar booking would open here.');
            });
        }
    });

    // Share property button
    document.querySelectorAll('.btn-outline-secondary').forEach(function(btn) {
        if (btn.textContent.includes('Share Property')) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                if (navigator.share) {
                    navigator.share({
                        title: 'Check out this property',
                        text: 'I found this amazing property!',
                        url: window.location.href
                    }).catch(function(err) {
                        console.log('Share failed:', err);
                    });
                } else {
                    // Fallback for browsers that don't support Web Share API
                    const url = window.location.href;
                    navigator.clipboard.writeText(url).then(function() {
                        alert('Property link copied to clipboard!');
                    }).catch(function() {
                        alert('Could not copy link. URL: ' + url);
                    });
                }
            });
        }
    });

    // Fade in property items
    document.querySelectorAll('.property-item').forEach(function(item, index) {
        item.style.opacity = '0';
        setTimeout(function() {
            item.style.transition = 'opacity 0.5s';
            item.style.opacity = '1';
        }, index * 100);
    });

    // Stats counter animation
    document.querySelectorAll('.stats-section .display-4').forEach(function(element) {
        const text = element.textContent.trim();
        const countTo = parseInt(text);

        if (!isNaN(countTo)) {
            let current = 0;
            const increment = countTo / 50;
            const timer = setInterval(function() {
                current += increment;
                if (current >= countTo) {
                    element.textContent = countTo;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.floor(current);
                }
            }, 40);
        }
    });

    // Simple parallax effect for hero section
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                const scrollTop = window.pageYOffset;
                const heroSection = document.querySelector('.hero-section');
                if (heroSection) {
                    heroSection.style.backgroundPosition = 'center ' + (scrollTop * 0.5) + 'px';
                }
                ticking = false;
            });
            ticking = true;
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const offsetTop = target.offsetTop - 70;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});