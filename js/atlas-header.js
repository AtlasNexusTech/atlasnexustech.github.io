(() => {
  const root = document.documentElement;
  const toggle = document.getElementById('atlas-theme-toggle');

  const safeStorage = {
    get(key) {
      try {
        return localStorage.getItem(key);
      } catch (_) {
        return null;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, value);
      } catch (_) {
        // The header remains usable when storage is unavailable.
      }
    },
  };

  const storedTheme = safeStorage.get('theme');
  if (storedTheme === 'dark') root.classList.add('dark');
  if (storedTheme === 'light') root.classList.remove('dark');

  const syncToggle = () => {
    if (!toggle) return;
    const dark = root.classList.contains('dark');
    toggle.setAttribute('aria-pressed', String(dark));
    toggle.setAttribute(
      'aria-label',
      dark ? 'Utiliser le thème clair' : 'Utiliser le thème sombre'
    );
  };

  if (toggle) {
    syncToggle();
    toggle.addEventListener('click', () => {
      const dark = root.classList.toggle('dark');
      safeStorage.set('theme', dark ? 'dark' : 'light');
      syncToggle();
    });
  }

  document.querySelectorAll('[data-atlas-lang]').forEach((link) => {
    link.addEventListener('click', () => {
      safeStorage.set('atlasnexus.lang', link.dataset.atlasLang);
    });
  });
})();
