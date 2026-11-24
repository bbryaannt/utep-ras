# Contact form handoff

The contact page sends visitor submissions to ieeeras@utep.edu using FormSubmit AJAX. No API key is stored or required. The native email-app links remain available and preserve form contents in a draft.

## One-time activation

1. Submit a message through the published contact page.
2. Open the FormSubmit activation email in ieeeras@utep.edu (check spam too).
3. Confirm the form using the activation link.
4. Submit a second message and verify delivery and Reply-To in the chapter inbox.

Delivery has not been tested or confirmed from this workspace. No test email was sent. Form validation and the email draft fallback were checked locally; asset URLs are content-versioned to prevent stale scripts.

FormSubmit handles the supplied name, email, contact details, and message. Its privacy notice is linked beside the Send button. The form has a honeypot, field length bounds, duplicate-click protection, submission timeout, honest error feedback, and preserved values on failure. A successful service response means accepted submission, not confirmed inbox delivery.

## Instagram

The contact page now embeds the public @utep.ras profile using Instagram’s profile frame. The profile and six posts were visually verified in the preview on November 8, 2026. There is one fallback link in the Instagram section. Availability still depends on Instagram and the account’s public embed settings.

Sources:
- https://formsubmit.co/documentation
- https://formsubmit.co/help
- https://formsubmit.co/privacy.pdf
