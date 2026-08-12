/* Atlas Nexus — suivi de conversion
 * ---------------------------------------------------------------------------
 * Un seul fichier pour Google Ads / GA4 et Meta. Renseignez les identifiants
 * ci-dessous : tant qu'un identifiant est vide, la plateforme correspondante
 * n'est simplement pas chargee (aucune erreur, aucun cookie depose).
 *
 * L'evenement qui compte est « booking_completed » : il se declenche quand un
 * rendez-vous Calendly est REELLEMENT confirme, pas au clic sur le bouton.
 * C'est cette distinction qui separe une depense publicitaire pilotee d'une
 * depense a l'aveugle.
 * ------------------------------------------------------------------------- */
(function () {
  'use strict';

  var CONFIG = {
    ga4Id:            '',   // ex. 'G-XXXXXXXXXX'
    googleAdsId:      '',   // ex. 'AW-123456789'
    googleAdsLabel:   '',   // ex. 'AbCdEfGhIj-KLmnOp'  (etiquette de conversion)
    metaPixelId:      '',   // ex. '123456789012345'
    debug:            false // true => journalise chaque evenement en console
  };

  var loaded = { google: false, meta: false };

  function log() {
    if (CONFIG.debug && window.console) {
      console.log.apply(console, ['[tracking]'].concat([].slice.call(arguments)));
    }
  }

  // ---- Chargement des balises ---------------------------------------------
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  function loadGoogle() {
    var id = CONFIG.ga4Id || CONFIG.googleAdsId;
    if (!id) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    gtag('js', new Date());
    if (CONFIG.ga4Id)       gtag('config', CONFIG.ga4Id);
    if (CONFIG.googleAdsId) gtag('config', CONFIG.googleAdsId);
    loaded.google = true;
    log('Google charge', id);
  }

  function loadMeta() {
    if (!CONFIG.metaPixelId) return;
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
    (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq('init', CONFIG.metaPixelId);
    window.fbq('track', 'PageView');
    loaded.meta = true;
    log('Meta charge', CONFIG.metaPixelId);
  }

  // ---- Emission d'un evenement --------------------------------------------
  function track(name, params, opts) {
    params = params || {};
    opts = opts || {};
    log(name, params);

    window.dataLayer.push(Object.assign({ event: name }, params));

    if (loaded.google) {
      gtag('event', name, params);
      // Conversion Google Ads : uniquement sur les evenements qui la meritent
      if (opts.adsConversion && CONFIG.googleAdsId && CONFIG.googleAdsLabel) {
        gtag('event', 'conversion', {
          send_to: CONFIG.googleAdsId + '/' + CONFIG.googleAdsLabel,
          value: opts.value || 0,
          currency: 'EUR'
        });
      }
    }
    if (loaded.meta) {
      if (opts.metaStandard) window.fbq('track', opts.metaStandard, params);
      else window.fbq('trackCustom', name, params);
    }
  }

  // ---- Evenements suivis ---------------------------------------------------
  function wire() {
    // 1) Clic sur un bouton de prise de rendez-vous (intention, pas conversion)
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('[data-calendly]');
      if (a) {
        track('booking_intent',
              { cta_text: (a.textContent || '').trim().slice(0, 60),
                page: location.pathname },
              { metaStandard: 'InitiateCheckout' });
        return;
      }
      var link = e.target.closest && e.target.closest('a[href^="tel:"], a[href^="mailto:"]');
      if (link) {
        var tel = link.getAttribute('href').indexOf('tel:') === 0;
        track(tel ? 'phone_click' : 'email_click',
              { page: location.pathname },
              { adsConversion: tel, metaStandard: 'Contact' });
      }
    }, true);

    // 2) Rendez-vous CONFIRME dans Calendly — la vraie conversion
    window.addEventListener('message', function (e) {
      if (!e.origin || e.origin.indexOf('calendly.com') === -1) return;
      var d = e.data;
      if (!d || typeof d.event !== 'string') return;
      if (d.event === 'calendly.event_scheduled') {
        track('booking_completed',
              { page: location.pathname },
              { adsConversion: true, metaStandard: 'Schedule', value: 150 });
      }
    });

    // 3) Envoi du formulaire de contact (voie de secours)
    var form = document.querySelector('form.contact-form, form[action*="formsubmit"]');
    if (form) {
      form.addEventListener('submit', function () {
        track('form_submit', { page: location.pathname },
              { adsConversion: true, metaStandard: 'Lead' });
      });
    }

    // 4) Lecture reelle de la page : 75 % de defilement, une seule fois
    var fired = false;
    window.addEventListener('scroll', function () {
      if (fired) return;
      var h = document.documentElement;
      var pct = (h.scrollTop + window.innerHeight) / h.scrollHeight;
      if (pct >= 0.75) { fired = true; track('scroll_75', { page: location.pathname }); }
    }, { passive: true });
  }

  loadGoogle();
  loadMeta();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }

  window.atlasTrack = track;   // permet un appel manuel depuis une page
})();
