/* Atlas Nexus -- suivi de conversion + consentement
 * ---------------------------------------------------------------------------
 * Un seul fichier pour Google Ads / GA4 et Meta. Renseignez les identifiants
 * ci-dessous : tant qu'un identifiant est vide, la plateforme correspondante
 * n'est simplement pas chargee (aucune erreur, aucun cookie depose).
 *
 * REGLE DE CONSENTEMENT : aucune balise publicitaire n'est chargee avant un
 * accord explicite du visiteur. Tant que le consentement n'est pas donne,
 * aucune requete n'est envoyee a Google ou Meta et aucun cookie n'est depose.
 * Le bandeau n'apparait que si au moins un identifiant est renseigne.
 *
 * L'evenement qui compte est " booking_completed " : il se declenche quand un
 * rendez-vous Calendly est REELLEMENT confirme, pas au clic sur le bouton.
 * C'est cette distinction qui separe une depense publicitaire pilotee d'une
 * depense a l'aveugle.
 * ------------------------------------------------------------------------- */
(function () {
  'use strict';

  /* Suivi Google Ads actif, sous consentement. Le bandeau reprend la charte du
     site : capsule de verre identique a la barre de navigation, Rubik / Nunito
     Sans, bleu primaire #2563EB, mode sombre gere. Passer consentBanner a false
     pour charger sans rien afficher. */
  var CONFIG = {
    ga4Id:            '',              // ex. 'G-XXXXXXXXXX'
    googleAdsId:      'AW-801944061',  // identifiant de balise Google Ads
    googleAdsLabel:   '',              // etiquette de conversion -- MANQUANTE :
                                       // tant qu'elle est vide, les evenements
                                       // remontent mais AUCUNE conversion n'est
                                       // comptee dans Google Ads.
    metaPixelId:      '',              // ex. '123456789012345'
    consentBanner:    true,            // false => chargement direct, sans bandeau
    debug:            false            // true => journalise chaque evenement
  };

  var CONSENT_KEY   = 'atlas_consent';
  var CONSENT_MONTHS = 6;              // duree de validite du choix (CNIL)

  var loaded = { google: false, meta: false };

  function log() {
    if (CONFIG.debug && window.console) {
      console.log.apply(console, ['[tracking]'].concat([].slice.call(arguments)));
    }
  }

  function needsConsent() {
    return !!(CONFIG.ga4Id || CONFIG.googleAdsId || CONFIG.metaPixelId);
  }

  // ---- Memoire du choix ----------------------------------------------------
  function readConsent() {
    try {
      var raw = window.localStorage.getItem(CONSENT_KEY);
      if (!raw) return null;
      var v = JSON.parse(raw);
      var age = Date.now() - (v.t || 0);
      if (age > CONSENT_MONTHS * 30 * 24 * 3600 * 1000) return null;
      return v.c === 'granted' ? 'granted' : 'denied';
    } catch (e) { return null; }
  }

  function writeConsent(choice) {
    try {
      window.localStorage.setItem(CONSENT_KEY,
        JSON.stringify({ c: choice, t: Date.now() }));
    } catch (e) { /* navigation privee : le choix vaut pour la session */ }
  }

  // ---- Chargement des balises ---------------------------------------------
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  // Consent Mode v2 : tout est refuse par defaut, avant tout chargement.
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    wait_for_update: 500
  });

  function loadGoogle() {
    if (loaded.google) return;
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
    if (loaded.meta || !CONFIG.metaPixelId) return;
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

  function grant() {
    gtag('consent', 'update', {
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted',
      analytics_storage: 'granted'
    });
    loadGoogle();
    loadMeta();
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

  // ---- Bandeau de consentement --------------------------------------------
  var TXT = {
    fr: {
      msg: 'We use cookies and similar technologies, including necessary cookies to provide our website, and optional cookies to improve and personalize your experience',
      yes: 'Accepter', no: 'Refuser', more: '', href: ''
    },
    en: {
      msg: 'We use cookies and similar technologies, including necessary cookies to provide our website, and optional cookies to improve and personalize your experience',
      yes: 'Accept', no: 'Decline', more: '', href: ''
    }
  };

  function lang() {
    var l = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('fr') === 0) return 'fr';
    return location.pathname.indexOf('/en/') === 0 ? 'en' : 'fr';
  }

  function banner() {
    if (document.getElementById('atlas-consent')) return;
    var t = TXT[lang()];

    /* Atlas Nexus : carte claire et compacte, proche des surfaces du site
       (fond #F8FAFC, bordure bleue tres legere, Rubik / Nunito Sans,
       rayons doux et boutons coherents avec les CTA principaux). */
    var css = document.createElement('style');
    css.textContent =
      '#atlas-consent{position:fixed;left:1rem;right:1rem;bottom:1rem;z-index:9998;' +
      'width:calc(100% - 2rem);max-width:62rem;margin:0 auto;' +
      'display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem 1.5rem;' +
      'align-items:center;padding:1.05rem 1.15rem 1.05rem 1.35rem;' +
      'border:1px solid rgba(34,108,243,.16);border-radius:1.25rem;' +
      'background:rgba(248,250,252,.96);' +
      '-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);' +
      'box-shadow:0 18px 48px rgba(15,23,42,.12),0 3px 12px rgba(34,108,243,.06);' +
      'color:#334155;font-family:"Nunito Sans",Rubik,ui-sans-serif,system-ui,' +
      '-apple-system,"Segoe UI",sans-serif;font-size:14px;line-height:1.55;' +
      'opacity:0;transform:translateY(12px);' +
      'transition:opacity .3s ease,transform .3s ease}' +
      '#atlas-consent::before{content:"";position:absolute;left:0;top:1rem;bottom:1rem;' +
      'width:3px;border-radius:999px;background:linear-gradient(180deg,#226CF3,#5BA2FC)}' +
      '#atlas-consent.is-in{opacity:1;transform:none}' +
      '#atlas-consent p{margin:0;max-width:48rem;letter-spacing:-.005em}' +
      '#atlas-consent .atlas-consent-btns{display:flex;align-items:center;' +
      'gap:.55rem;flex:0 0 auto}' +
      '#atlas-consent button{cursor:pointer;border-radius:999px;' +
      'font-family:Rubik,"Nunito Sans",ui-sans-serif,system-ui,sans-serif;' +
      'font-size:13px;font-weight:700;letter-spacing:.01em;transition:all .2s ease}' +
      '#atlas-consent .atlas-yes{border:1px solid #226CF3;background:#226CF3;' +
      'color:#fff;padding:.62rem 1.25rem;box-shadow:0 8px 18px rgba(34,108,243,.2)}' +
      '#atlas-consent .atlas-yes:hover{background:#1859D8;border-color:#1859D8;' +
      'transform:translateY(-1px)}' +
      '#atlas-consent .atlas-no{border:1px solid #CBD5E1;background:#fff;' +
      'color:#475569;padding:.62rem 1rem}' +
      '#atlas-consent .atlas-no:hover{border-color:#94A3B8;color:#0F172A;' +
      'background:#F8FAFC}' +
      '.dark #atlas-consent{background:rgba(15,23,42,.96);' +
      'border-color:rgba(91,162,252,.22);color:#CBD5E1;' +
      'box-shadow:0 18px 48px rgba(0,0,0,.38)}' +
      '.dark #atlas-consent .atlas-no{background:#111827;border-color:#334155;color:#CBD5E1}' +
      '.dark #atlas-consent .atlas-no:hover{background:#1E293B;border-color:#64748B;color:#F8FAFC}' +
      '@media(max-width:760px){#atlas-consent{bottom:5rem;display:flex;flex-direction:column;' +
      'align-items:stretch;border-radius:1.1rem;padding:1rem 1rem 1rem 1.2rem;gap:.9rem}' +
      '#atlas-consent p{font-size:13.5px;line-height:1.5}' +
      '#atlas-consent .atlas-consent-btns{width:100%;justify-content:flex-end}' +
      '#atlas-consent button{min-height:42px}}' +
      '@media(max-width:420px){#atlas-consent .atlas-consent-btns{display:grid;' +
      'grid-template-columns:1fr 1fr}#atlas-consent button{width:100%}}' +
      '@media(prefers-reduced-motion:reduce){#atlas-consent{transition:none}}';
    document.head.appendChild(css);

    var box = document.createElement('div');
    box.id = 'atlas-consent';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-live', 'polite');
    var texte = '';
    if (t.msg) {
      texte = '<p>' + t.msg +
              (t.more ? ' <a href="' + t.href + '">' + t.more + '</a>' : '') + '</p>';
    } else {
      box.className = 'is-bare';   // sans texte : simple pastille de deux boutons
    }
    box.innerHTML = texte +
      '<div class="atlas-consent-btns">' +
      '<button type="button" class="atlas-no">'  + t.no  + '</button>' +
      '<button type="button" class="atlas-yes">' + t.yes + '</button>' +
      '</div>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { box.classList.add('is-in'); });

    function close(choice) {
      writeConsent(choice);
      if (choice === 'granted') grant();
      box.classList.remove('is-in');
      setTimeout(function () { if (box.parentNode) box.parentNode.removeChild(box); }, 300);
      log('consentement', choice);
    }
    box.querySelector('.atlas-yes').addEventListener('click', function () { close('granted'); });
    box.querySelector('.atlas-no').addEventListener('click',  function () { close('denied'); });
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

    // 2) Rendez-vous CONFIRME dans Calendly -- la vraie conversion
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

  // ---- Demarrage -----------------------------------------------------------
  function start() {
    if (!needsConsent()) return;          // aucun identifiant : rien a charger
    if (!CONFIG.consentBanner) {          // sans bandeau : chargement direct
      if (readConsent() === 'denied') return;   // refus deja exprime : respecte
      grant();
      return;
    }
    var c = readConsent();
    if (c === 'granted') { grant(); return; }
    if (c === 'denied') return;           // choix respecte, pas de relance
    banner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { start(); wire(); });
  } else {
    start(); wire();
  }

  window.atlasTrack = track;              // appel manuel depuis une page
  window.atlasConsent = {                 // pilotage depuis un lien de pied de page
    active: needsConsent() && !!CONFIG.consentBanner,  // bandeau reellement propose ?
    get: readConsent,
    set: function (c) { writeConsent(c); if (c === 'granted') grant(); },
    ask: function () {
      if (!needsConsent() || !CONFIG.consentBanner) return false;  // pas de bandeau
      try { localStorage.removeItem(CONSENT_KEY); } catch (e) {}
      banner();
      return true;
    }
  };
})();
