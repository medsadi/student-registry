// ==========================================
// STUDENT REGISTRY - INTERACTIVE JAVASCRIPT
// ==========================================

// Auto-close alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// ===== TITRE INTERACTIF - Change couleur au clic =====
const title = document.querySelector('.page-header h1');
if (title) {
    const colors = ['#d4af37', '#00d4ff', '#9333ea', '#f4d03f', '#10b981'];
    let colorIndex = 0;
    
    title.addEventListener('click', function() {
        colorIndex = (colorIndex + 1) % colors.length;
        this.style.color = colors[colorIndex];
        this.style.textShadow = `0 0 30px ${colors[colorIndex]}`;
        
        // Animation de rebond
        this.style.transform = 'scale(1.2) rotate(5deg)';
        setTimeout(() => {
            this.style.transform = 'scale(1) rotate(0deg)';
        }, 200);
    });
}

// ===== ICONS INTERACTIFS - Changent de couleur au clic =====
const icons = document.querySelectorAll('.stat-icon, .section-header h2 i, .form-group label i, .students-table th i, .footer-section h4 i');
const iconColors = ['#d4af37', '#00d4ff', '#9333ea', '#10b981', '#f59e0b', '#ef4444'];

icons.forEach(icon => {
    icon.addEventListener('click', function(e) {
        e.stopPropagation();
        
        // Couleur aléatoire
        const randomColor = iconColors[Math.floor(Math.random() * iconColors.length)];
        this.style.color = randomColor;
        this.style.filter = `drop-shadow(0 0 10px ${randomColor})`;
        
        // Animation
        this.style.transform = 'scale(1.5) rotate(360deg)';
        setTimeout(() => {
            this.style.transform = 'scale(1) rotate(0deg)';
        }, 500);
        
        // Effet de particules
        createParticles(e.clientX, e.clientY, randomColor);
    });
});

// ===== EFFET PARTICULES au clic sur icons =====
function createParticles(x, y, color) {
    for (let i = 0; i < 8; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '8px';
        particle.style.height = '8px';
        particle.style.borderRadius = '50%';
        particle.style.background = color;
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';
        particle.style.boxShadow = `0 0 10px ${color}`;
        
        document.body.appendChild(particle);
        
        const angle = (Math.PI * 2 * i) / 8;
        const velocity = 100;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        let posX = 0;
        let posY = 0;
        let opacity = 1;
        
        const animate = () => {
            posX += vx * 0.01;
            posY += vy * 0.01;
            opacity -= 0.02;
            
            particle.style.transform = `translate(${posX}px, ${posY}px)`;
            particle.style.opacity = opacity;
            
            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                particle.remove();
            }
        };
        
        animate();
    }
}

// ===== CARTES STATISTIQUES - Effet au clic =====
const statCards = document.querySelectorAll('.stat-card');
statCards.forEach(card => {
    card.addEventListener('click', function() {
        // Effet de flash
        this.style.background = 'rgba(212, 175, 55, 0.3)';
        setTimeout(() => {
            this.style.background = '';
        }, 300);
        
        // Animation de l'icon
        const icon = this.querySelector('.stat-icon');
        if (icon) {
            icon.style.transform = 'scale(1.3) rotate(360deg)';
            setTimeout(() => {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }, 500);
        }
    });
});

// ===== BOUTON SUBMIT - Animation au clic =====
const submitBtn = document.querySelector('.btn-primary');
if (submitBtn) {
    submitBtn.addEventListener('click', function() {
        const icon = this.querySelector('i');
        if (icon) {
            icon.style.animation = 'spin 0.5s linear';
            setTimeout(() => {
                icon.style.animation = '';
            }, 500);
        }
    });
}

// ===== LIGNES DU TABLEAU - Effet au clic =====
const tableRows = document.querySelectorAll('.students-table tbody tr');
tableRows.forEach(row => {
    row.addEventListener('click', function() {
        // Retirer la sélection précédente
        tableRows.forEach(r => {
            r.style.background = '';
            r.style.borderLeft = '';
        });
        
        // Sélectionner la ligne cliquée
        this.style.background = 'rgba(212, 175, 55, 0.15)';
        this.style.borderLeft = '4px solid #d4af37';
    });
});

// ===== BADGES DE MOYENNE - Animation au clic =====
const moyenneBadges = document.querySelectorAll('.moyenne-badge');
moyenneBadges.forEach(badge => {
    badge.addEventListener('click', function(e) {
        e.stopPropagation();
        
        // Animation de rotation
        this.style.transform = 'scale(1.3) rotate(360deg)';
        setTimeout(() => {
            this.style.transform = 'scale(1) rotate(0deg)';
        }, 500);
    });
});

// ===== FORM VALIDATION =====
const form = document.querySelector('.student-form');
if (form) {
    form.addEventListener('submit', function(e) {
        const moyenne = document.getElementById('moyenne');
        if (moyenne && (parseFloat(moyenne.value) < 0 || parseFloat(moyenne.value) > 20)) {
            e.preventDefault();
            showNotification('La moyenne doit être entre 0 et 20', 'error');
            return false;
        }
        
        // Animation du bouton
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
            submitBtn.disabled = true;
        }
    });
}

// ===== NOTIFICATION PERSONNALISÉE =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} glass-effect`;
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.minWidth = '300px';
    
    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
    notification.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
        <button class="close-alert" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(500px)';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// ===== SMOOTH SCROLL =====
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

// ===== INTERSECTION OBSERVER - Animations au scroll =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-card, .glass-effect').forEach(el => {
    observer.observe(el);
});

// ===== RIPPLE EFFECT sur les boutons =====
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');
    
    circle.style.position = 'absolute';
    circle.style.borderRadius = '50%';
    circle.style.background = 'rgba(255, 255, 255, 0.5)';
    circle.style.animation = 'ripple 0.6s ease-out';

    const ripple = button.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }

    button.appendChild(circle);
    
    setTimeout(() => circle.remove(), 600);
}

const buttons = document.querySelectorAll('.btn');
buttons.forEach(button => {
    button.style.position = 'relative';
    button.style.overflow = 'hidden';
    button.addEventListener('click', createRipple);
});

// ===== EASTER EGG - Double clic sur le logo =====
const logo = document.querySelector('.nav-brand i');
if (logo) {
    let clickCount = 0;
    logo.addEventListener('click', function() {
        clickCount++;
        if (clickCount === 3) {
            showNotification('🎉 Mode fête activé!', 'success');
            activatePartyMode();
            clickCount = 0;
        }
        setTimeout(() => clickCount = 0, 1000);
    });
}

// ===== MODE FÊTE - Animations partout =====
function activatePartyMode() {
    const elements = document.querySelectorAll('.stat-icon, .moyenne-badge, .badge');
    let colorIndex = 0;
    
    const interval = setInterval(() => {
        elements.forEach(el => {
            el.style.color = iconColors[colorIndex % iconColors.length];
            el.style.transform = 'scale(1.1) rotate(5deg)';
            setTimeout(() => {
                el.style.transform = 'scale(1) rotate(0deg)';
            }, 200);
        });
        colorIndex++;
    }, 300);
    
    setTimeout(() => {
        clearInterval(interval);
        elements.forEach(el => {
            el.style.color = '';
            el.style.transform = '';
        });
    }, 5000);
}

// ===== CSS ANIMATION pour le spin =====
const animationStyle = document.createElement('style');
animationStyle.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes ripple {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(animationStyle);

// ===== CONSOLE MESSAGE =====
console.log('%c🎓 Student Registry Blockchain', 'color: #d4af37; font-size: 24px; font-weight: bold;');
console.log('%cDéveloppé avec Django + Web3.py', 'color: #00d4ff; font-size: 16px;');
console.log('%c💡 Cliquez sur les icons pour les animer!', 'color: #10b981; font-size: 14px;');
console.log('%c🎉 Astuce: Triple-cliquez sur le logo pour activer le mode fête!', 'color: #9333ea; font-size: 12px;');