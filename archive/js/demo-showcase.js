(() => {
  const simulate = (form, event) => {
    event.preventDefault();
    const status = form.querySelector('[data-demo-status]');
    if (status) {
      status.setAttribute('aria-live', 'polite');
      status.textContent = 'Simulation terminée : aucune donnée n’a été transmise.';
      status.focus({ preventScroll: false });
    }
  };

  document.querySelectorAll('[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (event) => simulate(form, event));
    form.querySelector('[data-demo-submit]')?.addEventListener('click', (event) => simulate(form, event));
  });

  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (motionPreference.matches || !('IntersectionObserver' in window)) {
    return;
  }

  const hero = document.querySelector('main > section:first-child');
  if (hero) {
    hero.classList.add('atlas-hero-motion');
    const heroItems = hero.querySelectorAll('h1, p, a, .inline-block');
    heroItems.forEach((item, index) => {
      item.classList.add('atlas-hero-item');
      item.style.setProperty('--atlas-hero-delay', `${Math.min(index, 5) * 95 + 80}ms`);
    });
  }

  const revealTargets = [];
  document.querySelectorAll('main > section:not(:first-child)').forEach((section) => {
    const candidates = [...section.querySelectorAll('h2, h3, .card-hover, .gallery-item, .grid > *, form')];
    const outermost = candidates.filter(
      (candidate) => !candidates.some((other) => other !== candidate && other.contains(candidate)),
    );

    outermost.forEach((target, index) => {
      target.classList.add('atlas-reveal');
      target.style.setProperty('--atlas-reveal-delay', `${(index % 5) * 70}ms`);
      revealTargets.push(target);
    });
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -7% 0px' },
  );

  revealTargets.forEach((target) => observer.observe(target));
  document.documentElement.classList.add('atlas-motion-ready');
})();
