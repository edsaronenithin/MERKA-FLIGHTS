
// Smooth scrolling for navigation links
function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({
        behavior: 'smooth'
    });
}

// Navigation transparency on scroll
window.addEventListener('scroll', function () {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        // Add off-white background and shadow
        navbar.classList.add('bg-[#fdfdfd]', 'shadow-lg', 'backdrop-blur-md');
        navbar.classList.remove('bg-transparent');
        document.querySelectorAll('.nav-link, .nav-text-toggle').forEach(el => {
            el.classList.add('text-gray-700');
            el.classList.remove('text-white');
        });
    } else {
        // Completely transparent
        navbar.classList.add('bg-transparent');
        navbar.classList.remove('bg-[#fdfdfd]', 'shadow-lg', 'backdrop-blur-md');
        document.querySelectorAll('.nav-link, .nav-text-toggle').forEach(el => {
            el.classList.add('text-white');
            el.classList.remove('text-gray-700');
        });
    }
});

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.classList.toggle('hidden');
}



function submitContactForm(event) {
    event.preventDefault();
    alert('Thank you for your message! We will get back to you soon.');
    event.target.reset();
}

function subscribeNewsletter(event) {
    event.preventDefault();
    alert('Thank you for subscribing to our newsletter!');
    event.target.reset();
}

// Cruise detail functions
function viewCruiseDetails(cruiseType) {
    const cruiseDetails = {
        'mediterranean': {
            name: 'Mediterranean Explorer',
            description: 'Explore ancient civilizations and stunning coastlines across Italy, Greece, and Spain.',
            itinerary: 'Rome → Naples → Athens → Mykonos → Barcelona',
            duration: '7 Days',
            price: 'RS10,899'
        },
        'caribbean': {
            name: 'Caribbean Paradise',
            description: 'Relax in tropical paradise with pristine beaches and crystal-clear waters.',
            itinerary: 'Miami → Nassau → Cozumel → Jamaica → Miami',
            duration: '5 Days',
            price: 'RS10,299'
        },
        'northern-lights': {
            name: 'Northern Lights Adventure',
            description: 'Witness the magical aurora borealis while cruising through stunning Norwegian fjords.',
            itinerary: 'Bergen → Geiranger → Tromsø → Kirkenes → Bergen',
            duration: '10 Days',
            price: 'RS20,999'
        }
    };

    const cruise = cruiseDetails[cruiseType];
    alert(`${cruise.name}\n\n${cruise.description}\n\nItinerary: ${cruise.itinerary}\nDuration: ${cruise.duration}\nPrice: ${cruise.price} per person\n\nClick "Book Now" to reserve your spot!`);
}

function viewAllCruises() {
    alert('Redirecting to our full cruise catalog with over 50 destinations worldwide!');
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.cruise-card, .destination-card, .testimonial-card').forEach(el => {
    observer.observe(el);
});

// Initialize animations on page load
window.addEventListener('load', function () {
    const heroElements = document.querySelectorAll('.fade-in');
    heroElements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
});
