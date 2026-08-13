(function () {
  'use strict';

  var confirmed = document.getElementById('booking-confirmed');
  var storageKey = 'atlasNexusBookingConfirmed';

  function initMotion() {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced || !('IntersectionObserver' in window)) return;

    var selectors = [
      '.booking-grid-three article',
      '.booking-benefits > div',
      '.booking-timeline > li',
      '.booking-prep > *',
      '.booking-calendar-head',
      '.calendly-frame',
      '.booking-fallback details'
    ];
    var targets = Array.prototype.slice.call(document.querySelectorAll(selectors.join(',')));
    targets.forEach(function (target, index) {
      target.classList.add('booking-reveal');
      target.style.setProperty('--booking-delay', Math.min(index % 4, 3) * 70 + 'ms');
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });

    targets.forEach(function (target) { observer.observe(target); });
    document.documentElement.classList.add('booking-motion-ready');
  }

  initMotion();

  function safeGet() {
    try { return window.sessionStorage.getItem(storageKey); } catch (_) { return null; }
  }

  function safeSet(value) {
    try { window.sessionStorage.setItem(storageKey, value); } catch (_) {}
  }

  function revealPreparation(scroll) {
    if (!confirmed) return;
    confirmed.hidden = false;
    safeSet('true');
    if (scroll) confirmed.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  }

  function hidePreparation() {
    if (!confirmed) return;
    confirmed.hidden = true;
    safeSet('false');
  }

  if (safeGet() === 'true') revealPreparation(false);

  window.addEventListener('message', function (event) {
    if (event.origin !== 'https://calendly.com') return;
    if (!window.Calendly || typeof window.Calendly.isCalendlyEvent !== 'function') return;
    if (window.Calendly.isCalendlyEvent(event) && event.data.event === 'calendly.event_scheduled') {
      revealPreparation(true);
    }
  });

  document.addEventListener('click', function (event) {
    var confirmButton = event.target.closest('[data-confirm-booking]');
    if (confirmButton) revealPreparation(true);
    var resetButton = event.target.closest('[data-reset-booking]');
    if (resetButton) hidePreparation();
  });
})();
