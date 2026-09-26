const dialog = document.querySelector('#lightbox');
const image = document.querySelector('#lightbox-image');
const caption = document.querySelector('#lightbox-caption');
const closeButton = document.querySelector('#lightbox-close');

document.querySelectorAll('.image-open').forEach((button) => {
  button.addEventListener('click', () => {
    image.src = button.dataset.image;
    image.alt = button.querySelector('img')?.alt || '';
    caption.textContent = button.dataset.caption || '';
    dialog.showModal();
    closeButton.focus();
  });
});

closeButton.addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});
dialog.addEventListener('close', () => {
  image.removeAttribute('src');
});
