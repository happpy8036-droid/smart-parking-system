// Smart Parking System - Main JS

// Mobile Nav Toggle
function toggleNav() {
    const navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}

// Close mobile nav when clicking outside
document.addEventListener('click', function(e) {
    const nav = document.querySelector('.brutalist-nav');
    const navLinks = document.getElementById('navLinks');
    if (nav && navLinks && !nav.contains(e.target)) {
        navLinks.classList.remove('active');
    }
});

// Add fade-in animation on scroll
document.addEventListener('DOMContentLoaded', function() {
    // Animate elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                entry.target.style.opacity = '1';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all cards and sections
    document.querySelectorAll('.location-card, .stat-box, .step-card, .info-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // Button click ripple effect
    document.querySelectorAll('.brutalist-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Auto-dismiss flash messages after 5 seconds
    document.querySelectorAll('.flash-messages .flash').forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            flash.style.transition = 'all 0.3s ease';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
});
