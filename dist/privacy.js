(() => {
  const KEY = 'ras-privacy-v1';
  const MAX_AGE = 180 * 86400000;
  const dialog = document.querySelector('#privacy-dialog');
  const banner = document.querySelector('#privacy-banner');
  if (!dialog || !banner) return;
  const media = document.querySelector('#consent-media');
  let choice = null;
  try {
    const saved = JSON.parse(localStorage.getItem(KEY));
    if (saved?.version === 1 && typeof saved.media === 'boolean' && Number.isFinite(saved.savedAt) && Date.now() - saved.savedAt < MAX_AGE && saved.savedAt <= Date.now()) choice = saved;
  } catch {}
  const apply = () => {
    document.documentElement.dataset.mediaConsent = choice?.media ? 'allowed' : 'denied';
    document.dispatchEvent(new CustomEvent('ras:privacy', {detail:{media:!!choice?.media}}));
  };
  const save = allowMedia => {
    choice = {version:1,media:allowMedia,savedAt:Date.now()};
    try {localStorage.setItem(KEY,JSON.stringify(choice));} catch {}
    banner.hidden = true;
    if (dialog.open) dialog.close();
    apply();
  };
  document.querySelectorAll('[data-privacy-open]').forEach(button => button.addEventListener('click', () => {
    media.checked = !!choice?.media;
    dialog.showModal();
  }));
  document.querySelectorAll('[data-privacy-reject]').forEach(button => button.addEventListener('click', () => save(false)));
  document.querySelectorAll('[data-privacy-accept]').forEach(button => button.addEventListener('click', () => save(true)));
  document.querySelector('#privacy-save').addEventListener('click', () => save(media.checked));
  document.querySelector('#privacy-close').addEventListener('click', () => dialog.close());
  if (!choice) banner.hidden = false;
  apply();
})();
