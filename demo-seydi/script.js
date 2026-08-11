(() => {
  const items = [...document.querySelectorAll('[data-lightbox]')];
  const dialog = document.querySelector('.lightbox');
  const image = dialog?.querySelector('figure img');
  const caption = dialog?.querySelector('figcaption');
  const closeButton = dialog?.querySelector('.lightbox-close');
  const previousButton = dialog?.querySelector('.lightbox-prev');
  const nextButton = dialog?.querySelector('.lightbox-next');
  let current = 0;

  if (!dialog || !image || !caption || items.length === 0) return;

  const show = (index) => {
    current = (index + items.length) % items.length;
    const item = items[current];
    image.src = item.dataset.src;
    image.alt = item.querySelector('img')?.alt || '';
    caption.textContent = `${item.dataset.caption || image.alt} · ${current + 1}/${items.length}`;
  };

  items.forEach((item, index) => {
    item.addEventListener('click', () => {
      show(index);
      dialog.showModal();
      closeButton?.focus();
    });
  });

  closeButton?.addEventListener('click', () => dialog.close());
  previousButton?.addEventListener('click', () => show(current - 1));
  nextButton?.addEventListener('click', () => show(current + 1));

  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      show(current - 1);
    }
    if (event.key === 'ArrowRight') {
      event.preventDefault();
      show(current + 1);
    }
  });
})();
