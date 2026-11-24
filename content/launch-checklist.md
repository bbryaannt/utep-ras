# Launch checklist — November 8, 2026

Implemented: privacy and terms pages; optional-media consent and settings; per-page metadata and canonical URLs; social preview; favicon and touch icon; sitemap and robots; descriptive image alternatives; compressed responsive WebP images; local performance diagnostics; improved contrast and keyboard focus; responsive layouts; custom 404 document; local link validation; trimmed contact validation; honeypot and provider CAPTCHA; one primary Join RAS action.

Verification: automated audit passes all 13 HTML documents, local links/fragments, image sources and alternatives, metadata, sitemap, secret patterns, and native CAPTCHA form configuration. Principal text contrast pairs exceed 4.5:1. Browser checks verified that Instagram makes no request before optional-media consent, loads after consent, and unloads after withdrawal. Whitespace-only form messages are rejected without submitting.

HTTPS redirects were verified at the host. Security headers are configured in dist/_headers. No credentials were found in frontend source. No analytics or telemetry is sent by the local performance diagnostics.

## Remaining external setup

- Analytics is disabled: the chapter does not yet have an analytics account/property ID. Consent-aware integration is ready for a real Google Analytics measurement ID.
- Contact email delivery requires FormSubmit inbox activation by ieeeras@utep.edu. No test message has been sent or delivery verified. FormSubmit handles CAPTCHA and delivery; browser cooldown and honeypot are supplementary controls.
- The site remains owner-private. Search indexing is intentionally disabled until publication to a public audience is authorized. Sitemap is generated and ready.
- Production custom 404 verified: unknown URL returns HTTP 404 with the custom page. HTTPS redirects work. The static hosting layer did not apply the additional HSTS/CSP response headers from _headers; those require hosting support or a server-backed deployment.
- One production browser sample: TTFB 85 ms, FCP/LCP 1.62 s, load 1.676 s, CLS 0.0005. These are one observed session, not a Lighthouse score or field performance guarantee. Mobile policy document width matched the 390 px viewport without horizontal overflow.

These policies describe the implemented service; they are not a guarantee of legal compliance.
