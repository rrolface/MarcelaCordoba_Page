/* ================================
   MARCELA CÓRDOBA — script.js
   ================================ */

// ── NAVBAR: scroll effect + active link ──────────────────────────
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }

  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 90;
    if (window.scrollY >= sectionTop) {
      current = section.getAttribute('id');
    }
  });
  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) {
      link.classList.add('active');
    }
  });
});

// ── HAMBURGER MENU ───────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinksEl = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
  navLinksEl.classList.toggle('open');
  hamburger.classList.toggle('active');
});

navLinksEl.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinksEl.classList.remove('open');
    hamburger.classList.remove('active');
  });
});

document.addEventListener('click', (e) => {
  if (!navLinksEl.contains(e.target) && !hamburger.contains(e.target)) {
    navLinksEl.classList.remove('open');
    hamburger.classList.remove('active');
  }
});

// ── SCROLL FADE-IN ANIMATIONS ────────────────────────────────────
const fadeEls = document.querySelectorAll('.service-card, .feature, .testimonio-card, .idrea-step, .about-content, .contacto-info, .contacto-form');

fadeEls.forEach((el, i) => {
  el.classList.add('fade-in');
  if (i % 3 === 1) el.classList.add('fade-in-delay-1');
  if (i % 3 === 2) el.classList.add('fade-in-delay-2');
});

const sectionHeaders = document.querySelectorAll('.hero-content, .about-title, .services-title, .testimonios-title, .contacto-title, .idrea-title, .libro-title');
sectionHeaders.forEach(el => el.classList.add('fade-in'));

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// ── TESTIMONIOS SLIDER ───────────────────────────────────────────
// ── GALERÍA SLIDER ───────────────────────────────────────────────
const track = document.getElementById('testimoniosTrack');
const dotsContainer = document.getElementById('sliderDots');

let currentSlide = 0;
let slidesPerView = getSlidesPerView();
const cards = track.querySelectorAll('.galeria-card');
const totalCards = cards.length;

function getSlidesPerView() {
  if (window.innerWidth <= 640) return 1;
  if (window.innerWidth <= 960) return 2;
  return 3;
}

function getTotalSlides() {
  return Math.ceil(totalCards / slidesPerView);
}

function buildDots() {
  dotsContainer.innerHTML = '';
  const total = getTotalSlides();
  for (let i = 0; i < total; i++) {
    const dot = document.createElement('button');
    dot.className = 'slider-dot' + (i === currentSlide ? ' active' : '');
    dot.setAttribute('aria-label', 'Ir a foto ' + (i + 1));
    dot.addEventListener('click', () => goToSlide(i));
    dotsContainer.appendChild(dot);
  }
}

function updateDots() {
  const dots = dotsContainer.querySelectorAll('.slider-dot');
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === currentSlide);
  });
}

function goToSlide(index) {
  const total = getTotalSlides();
  currentSlide = Math.max(0, Math.min(index, total - 1));
  const gap = slidesPerView === 1 ? 0 : 24;
  const cardWidth = cards[0].offsetWidth + gap;
  track.style.transform = `translateX(-${currentSlide * slidesPerView * cardWidth}px)`;
  updateDots();
}

// Auto-avance automático
let autoSlide = setInterval(() => {
  const total = getTotalSlides();
  const next = currentSlide >= total - 1 ? 0 : currentSlide + 1;
  goToSlide(next);
}, 3000);

// Pausa al hacer hover
const sliderWrap = document.querySelector('.testimonios-slider');
sliderWrap.addEventListener('mouseenter', () => clearInterval(autoSlide));
sliderWrap.addEventListener('mouseleave', () => {
  autoSlide = setInterval(() => {
    const total = getTotalSlides();
    const next = currentSlide >= total - 1 ? 0 : currentSlide + 1;
    goToSlide(next);
  }, 3000);
});

// Swipe en móvil
let touchStartX = 0;
track.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
track.addEventListener('touchend', e => {
  const diff = touchStartX - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 40) goToSlide(currentSlide + (diff > 0 ? 1 : -1));
});

// Rebuild en resize
window.addEventListener('resize', () => {
  const newSpv = getSlidesPerView();
  if (newSpv !== slidesPerView) {
    slidesPerView = newSpv;
    currentSlide = 0;
    track.style.transform = 'translateX(0)';
    buildDots();
  }
});

buildDots();

// ── CONTACT FORM ─────────────────────────────────────────────────
const form = document.getElementById('contactoForm');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = form.querySelector('button[type="submit"]');
  const original = btn.textContent;

  btn.textContent = 'Enviando...';
  btn.disabled = true;

  const formData = new FormData(form);

  const response = await fetch("https://api.web3forms.com/submit", {
    method: "POST",
    body: formData
  });

  const result = await response.json();

  if (result.success) {
    btn.textContent = '¡Mensaje enviado! ✓';
    btn.style.background = '#3A8A5A';
    setTimeout(() => {
      btn.textContent = original;
      btn.style.background = '';
      btn.disabled = false;
      form.reset();
    }, 3500);
  } else {
    btn.textContent = 'Error al enviar. Intenta de nuevo.';
    btn.style.background = '#c0392b';
    btn.disabled = false;
    setTimeout(() => {
      btn.textContent = original;
      btn.style.background = '';
    }, 3500);
  }
});

// ── SMOOTH SCROLL for all anchor links ───────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 70;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});