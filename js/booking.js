(function () {
  'use strict';

  var confirmed = document.getElementById('booking-confirmed');
  var storageKey = 'atlasNexusBookingConfirmed';

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
