// Real Estate Module JavaScript

$(document).ready(function() {
    console.log('Real Estate module loaded');

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Toggle property details with smooth animation
    $('.property-card').on('click', '.toggle-details', function(e) {
        e.preventDefault();
        var $details = $(this).siblings('.details');
        var $button = $(this);
        $details.slideToggle(300, function() {
            $button.text($details.is(':visible') ? 'Hide Details' : 'View Details');
        });
    });

    // Enhanced search functionality with highlighting
    $('#property-search').on('input', function() {
        var searchTerm = $(this).val().toLowerCase();
        $('.property-item').each(function() {
            var $card = $(this);
            var text = $card.text().toLowerCase();
            if (text.includes(searchTerm) || searchTerm === '') {
                $card.fadeIn(200);
            } else {
                $card.fadeOut(200);
            }
        });
    });

    // Image gallery navigation (placeholder functionality)
    $('.card-img-top').on('click', '.btn', function(e) {
        e.preventDefault();
        // Placeholder for image gallery navigation
        console.log('Image navigation clicked');
    });

    // Contact agent button
    $('.btn-success').on('click', function(e) {
        e.preventDefault();
        alert('Contact form would open here. Phone: +1-234-567-8900');
    });

    // Schedule viewing button
    $('.btn-outline-primary').on('click', function(e) {
        e.preventDefault();
        alert('Calendar booking would open here.');
    });

    // Share property button
    $('.btn-outline-secondary').on('click', function(e) {
        e.preventDefault();
        if (navigator.share) {
            navigator.share({
                title: 'Check out this property',
                text: 'I found this amazing property!',
                url: window.location.href
            });
        } else {
            // Fallback for browsers that don't support Web Share API
            var url = window.location.href;
            navigator.clipboard.writeText(url).then(function() {
                alert('Property link copied to clipboard!');
            });
        }
    });

    // Add loading animation for cards
    $('.property-item').hide().fadeIn(500);

    // Stats counter animation
    $('.display-4').each(function() {
        var $this = $(this);
        var countTo = parseInt($this.text());
        if (!isNaN(countTo)) {
            $({ countNum: 0 }).animate({
                countNum: countTo
            }, {
                duration: 2000,
                easing: 'swing',
                step: function() {
                    $this.text(Math.floor(this.countNum));
                },
                complete: function() {
                    $this.text(this.countNum);
                }
            });
        }
    });

    // Hero section parallax effect (subtle)
    $(window).scroll(function() {
        var scrollTop = $(this).scrollTop();
        $('.hero-section').css('background-position', 'center ' + (scrollTop * 0.5) + 'px');
    });
});