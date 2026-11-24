# New domain and portable hosting

The website is static HTML, CSS, JavaScript, fonts, and images. It does not depend on ChatGPT sign-in or a Sites JavaScript runtime. The export can be deployed on a static host with a custom domain.

No domain has been purchased or attached. Choose and register a chapter-owned domain first. Then either attach it to the existing Sites project using its custom-domain controls and supplied DNS verification records, or upload exports/utep-ras-static.zip to the chosen static host. Do not invent DNS targets: obtain the actual records from the hosting service.

Before the final deployment, change `origin` in content/site-settings.json to the new HTTPS origin, run `python3 build_site.py`, then `python3 scripts/export-static.py`. This updates canonical URLs, social previews, sitemap, and contact-form return URLs together. Confirm the new domain and TLS certificate are active before replacing the old link. The existing address stays available until the new domain works.

The static export includes a custom 404 and _headers. On a host that supports _headers, these configure security and asset caching. Verify response headers and unknown-URL routing after upload. Configure equivalent rules in hosts that use a different format.

The site currently keeps search indexing disabled. Turn `public_indexing` on when the chapter is ready for search engines. FormSubmit inbox activation is still required for email delivery. No analytics account is connected.
