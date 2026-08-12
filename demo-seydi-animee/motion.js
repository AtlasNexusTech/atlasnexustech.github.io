(() => {
  const root = document.documentElement;
  const page = document.body;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = [...document.querySelectorAll('[data-reveal], [data-stagger]')];
  const sections = [...document.querySelectorAll('[data-motion-section]')];
  const parallaxItems = [...document.querySelectorAll('[data-parallax]')];
  const hero = document.querySelector('[data-motion-hero]');

  root.classList.add('motion-ready');
  requestAnimationFrame(() => root.classList.add('motion-loaded'));

  document.querySelectorAll('[data-stagger]').forEach((group) => {
    [...group.children].forEach((child, index) => {
      child.style.setProperty('--stagger-index', index);
    });
  });

  if (reducedMotion) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
    sections.forEach((section) => section.classList.add('section-visible'));
    page.style.setProperty('--scroll-progress', '1');
    return;
  }

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -9% 0px', threshold: 0.12 });

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      entry.target.classList.toggle('section-visible', entry.isIntersecting);
    });
  }, { rootMargin: '-18% 0px -18% 0px', threshold: 0.08 });

  revealItems.forEach((item) => revealObserver.observe(item));
  sections.forEach((section) => sectionObserver.observe(section));

  let framePending = false;
  const updateScrollMotion = () => {
    const scrollRange = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    page.style.setProperty('--scroll-progress', Math.min(1, Math.max(0, window.scrollY / scrollRange)).toFixed(4));

    parallaxItems.forEach((item) => {
      const rect = item.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      const centerOffset = (rect.top + rect.height / 2 - window.innerHeight / 2) / window.innerHeight;
      item.style.setProperty('--parallax-y', `${Math.max(-22, Math.min(22, centerOffset * -30)).toFixed(1)}px`);
    });
    framePending = false;
  };

  const requestScrollMotion = () => {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(updateScrollMotion);
  };

  window.addEventListener('scroll', requestScrollMotion, { passive: true });
  window.addEventListener('resize', requestScrollMotion, { passive: true });
  updateScrollMotion();

  if (hero && window.matchMedia('(pointer: fine)').matches) {
    hero.addEventListener('pointermove', (event) => {
      const rect = hero.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      page.style.setProperty('--motion-x', `${x.toFixed(1)}%`);
      page.style.setProperty('--motion-y', `${y.toFixed(1)}%`);
    }, { passive: true });

    hero.addEventListener('pointerleave', () => {
      page.style.setProperty('--motion-x', '50%');
      page.style.setProperty('--motion-y', '35%');
    });
  }
})();
