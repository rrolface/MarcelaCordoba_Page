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
// Sin auto-avance — solo swipe/drag manual

// Pausa al hacer hover (ya no necesaria pero la dejamos limpia)
const sliderWrap = document.querySelector('.testimonios-slider');

// ── DRAG CON MOUSE (desktop) ─────────────────────────────────────
let isDragging = false;
let dragStartX = 0;

track.addEventListener('mousedown', e => {
  isDragging = true;
  dragStartX = e.clientX;
  track.style.cursor = 'grabbing';
});

window.addEventListener('mouseup', e => {
  if (!isDragging) return;
  isDragging = false;
  track.style.cursor = 'grab';
  const diff = dragStartX - e.clientX;
  if (Math.abs(diff) > 40) goToSlide(currentSlide + (diff > 0 ? 1 : -1));
});

window.addEventListener('mousemove', e => {
  if (!isDragging) return;
  e.preventDefault();
});

// ── SWIPE CON DEDO (mobile) ──────────────────────────────────────
let touchStartX = 0;
track.addEventListener('touchstart', e => {
  touchStartX = e.touches[0].clientX;
}, { passive: true });

track.addEventListener('touchend', e => {
  const diff = touchStartX - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 40) goToSlide(currentSlide + (diff > 0 ? 1 : -1));
});

// ── PAUSA CARRUSEL CUANDO HAY VIDEO REPRODUCIÉNDOSE ─────────────
document.querySelectorAll('.galeria-card--video video').forEach(video => {
  video.addEventListener('play', () => {
    // sin autoSlide que pausar, no hace falta
  });
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

// ── GALERÍA MOMENTOS — LIGHTBOX ──────────────────────────────────
(function () {
  const items = Array.from(document.querySelectorAll('.momento-item'));
  const modal   = document.getElementById('momentosModal');
  const img     = document.getElementById('modalImg');
  const counter = document.getElementById('modalCounter');
  let current   = 0;

  function getSrc(i) { return items[i].querySelector('img').src; }

  function showModal(index) {
    current = index;
    img.src = getSrc(current);
    img.alt = items[current].querySelector('img').alt;
    counter.textContent = (current + 1) + ' / ' + items.length;
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  function navigate(dir) {
    current = (current + dir + items.length) % items.length;
    img.style.opacity = '0';
    img.style.transform = 'scale(0.96)';
    setTimeout(() => {
      img.src = getSrc(current);
      img.alt = items[current].querySelector('img').alt;
      counter.textContent = (current + 1) + ' / ' + items.length;
      img.style.opacity = '1';
      img.style.transform = 'scale(1)';
    }, 180);
  }

  img.style.transition = 'opacity 0.18s ease, transform 0.18s ease';

  items.forEach((item, i) => item.addEventListener('click', () => showModal(i)));
  document.getElementById('modalClose').addEventListener('click', closeModal);
  document.getElementById('modalBackdrop').addEventListener('click', closeModal);
  document.getElementById('modalPrev').addEventListener('click', () => navigate(-1));
  document.getElementById('modalNext').addEventListener('click', () => navigate(1));

  document.addEventListener('keydown', e => {
    if (!modal.classList.contains('open')) return;
    if (e.key === 'Escape')     closeModal();
    if (e.key === 'ArrowLeft')  navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
  });

  let touchStartX = 0;
  modal.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
  modal.addEventListener('touchend',   e => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 40) navigate(dx < 0 ? 1 : -1);
  });
})();

// ── TABS TRAYECTORIA ─────────────────────────────────────────────
document.querySelectorAll('.tray-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tray-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tray-tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
  });
});

});