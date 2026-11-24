const menu = document.querySelector('.menu');
const nav = document.querySelector('#navigation');
function closeMenu() {
  menu.setAttribute('aria-expanded', 'false');
  nav.classList.remove('open');
}
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menu.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.header')) closeMenu();
});
// Decorative pins move only while in view and while the tab is active.
const pins = [...document.querySelectorAll('.pin')];
if (pins.length && 'IntersectionObserver' in window) {
  const visiblePins = new Set();
  const updatePins = () => pins.forEach(pin => {
    pin.classList.toggle('is-visible', visiblePins.has(pin) && !document.hidden);
  });
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) visiblePins.add(entry.target);
      else visiblePins.delete(entry.target);
    });
    updatePins();
  });
  pins.forEach(pin => observer.observe(pin));
  document.addEventListener('visibilitychange', updatePins);
}

// Fit complete, evenly spaced grid rows between the banner and footer.
const gridMain = document.querySelector('main');
if (gridMain && 'ResizeObserver' in window) {
  const alignGrid = () => {
    const height = gridMain.getBoundingClientRect().height;
    if (height > 0) gridMain.style.setProperty('--grid-row', `${height / Math.max(1, Math.round(height / 40))}px`);
  };
  new ResizeObserver(alignGrid).observe(gridMain);
  alignGrid();
}
