// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const navMobile = document.querySelector('.nav-mobile');

navToggle.addEventListener('click', () => {
  navMobile.classList.toggle('open');
});

document.querySelectorAll('.nav-mobile a').forEach(link => {
  link.addEventListener('click', () => navMobile.classList.remove('open'));
});

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    const answer = item.querySelector('.faq-answer');
    const isOpen = item.classList.contains('open');

    document.querySelectorAll('.faq-item.open').forEach(open => {
      open.classList.remove('open');
      open.querySelector('.faq-answer').style.display = 'none';
    });

    if (!isOpen) {
      item.classList.add('open');
      answer.style.display = 'block';
    }
  });
});

// Scroll: nav border
window.addEventListener('scroll', () => {
  document.getElementById('nav').style.borderBottomColor =
    window.scrollY > 10 ? 'var(--border)' : 'var(--border-light)';
}, { passive: true });
