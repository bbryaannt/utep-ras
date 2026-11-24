const contactForm = document.querySelector('#contact-form');
if (contactForm) {
  const status = document.querySelector('#form-status');
  const submit = contactForm.querySelector('button[type="submit"]');
  const draft = document.querySelector('#email-draft');
  let lastSubmission = 0;
  try {lastSubmission = Number(sessionStorage.getItem('ras-last-submission')) || 0;} catch {}
  const updateDraft = () => {
    const data = new FormData(contactForm);
    const body = `Name: ${data.get('name') || ''}\nEmail: ${data.get('email') || ''}\nContact details: ${data.get('contact_details') || ''}\n\n${data.get('message') || ''}`;
    draft.href = `mailto:ieeeras@utep.edu?subject=${encodeURIComponent(data.get('topic') || 'Website inquiry')}&body=${encodeURIComponent(body)}`;
  };
  contactForm.addEventListener('input', event => { if(event.target.setCustomValidity) event.target.setCustomValidity(''); updateDraft(); });
  contactForm.addEventListener('submit', event => {
    for (const name of ['name','email','message']) {
      const input=contactForm.elements.namedItem(name);
      input.value=input.value.trim();
      input.setCustomValidity(!input.value ? 'Please complete this field.' : name==='message' && input.value.length<10 ? 'Please include at least 10 characters.' : '');
    }
    if (submit.disabled || !contactForm.reportValidity()) {event.preventDefault();return;}
    if (contactForm.elements.namedItem('_honey').value) {event.preventDefault();status.textContent='We couldn’t submit this form. Please use the email link instead.';return;}
    if (Date.now()-lastSubmission<60000) {event.preventDefault();status.textContent='Please wait a minute before submitting again.';status.focus();return;}
    lastSubmission=Date.now();
    try {sessionStorage.setItem('ras-last-submission',String(lastSubmission));} catch {}
    submit.disabled=true;
    status.textContent='Continuing to spam verification…';
    // Native POST preserves FormSubmit’s server-verified CAPTCHA and honeypot.
  });
  addEventListener('pageshow',()=>{submit.disabled=false;status.textContent='';});
}
const instagramFrame=document.querySelector('.instagram-profile-frame');
if(instagramFrame){
  const placeholder=document.querySelector('#instagram-consent-placeholder');
  const applyMedia=()=>{
    const allowed=document.documentElement.dataset.mediaConsent==='allowed';
    instagramFrame.hidden=!allowed;
    placeholder.hidden=allowed;
    if(!allowed){instagramFrame.removeAttribute('src');return;}
    if(!instagramFrame.hasAttribute('src'))instagramFrame.src=instagramFrame.dataset.src;
  };
  document.addEventListener('ras:privacy',applyMedia);
  applyMedia();
}
