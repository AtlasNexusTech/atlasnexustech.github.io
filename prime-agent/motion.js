/* ─────────────────────────────────────────────────────────
 * PRIME AGENT MOTION STORYBOARD
 *
 * Static shell and primary CTA remain visible and interactive.
 * Only supporting hero content and cockpit details cascade in.
 *
 *    0ms   navigation, CTA and page structure are available
 *   70ms   hero label, title and context settle into view
 *  190ms   cockpit frame appears from the right
 *  330ms   model bar, navigation and prompt become active
 *  520ms   mission cards and activity indicators resolve
 *  920ms   entrance sequence is fully complete
 * ───────────────────────────────────────────────────────── */
(() => {
  'use strict';

  const TIMING = Object.freeze({
    hero: 70,
    cockpit: 190,
    controls: 330,
    activity: 520,
  });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducedMotion) {
    document.documentElement.classList.add('prime-motion-reduced');
    return;
  }

  document.documentElement.classList.add('prime-motion-ready');

  const setStage = (stage) => {
    document.body.classList.add(`prime-stage-${stage}`);
    document.body.dataset.primeMotionStage = String(stage);
  };

  const orderedGroups = [
    '.prime-compare-card',
    '.prime-feature',
    '.step',
  ];

  orderedGroups.forEach((selector) => {
    document.querySelectorAll(selector).forEach((element, index) => {
      element.style.setProperty('--prime-motion-order', String(index));
    });
  });

  const timers = [];
  const schedule = (stage, delay) => {
    timers.push(window.setTimeout(() => setStage(stage), delay));
  };

  schedule(1, TIMING.hero);
  schedule(2, TIMING.cockpit);
  schedule(3, TIMING.controls);
  schedule(4, TIMING.activity);

  window.addEventListener('pagehide', () => {
    timers.forEach(window.clearTimeout);
  }, { once: true });
})();
