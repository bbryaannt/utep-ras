# UTEP IEEE Robotics & Automation Society

The UTEP IEEE RAS chapter website: projects, chapter information, joining details, and contact information. It is a static website built with Python's standard library, HTML, CSS, and JavaScript. No ChatGPT account, frontend framework, database, or application server is needed to run this copy.

## Run with Docker

Install Docker Engine with Compose, or Docker Desktop. Then, from this repository:

```sh
docker compose up --build -d
```

Open <http://localhost:8080>. The image runs NGINX as a non-root user, with health checks, gzip, asset caching, clean URLs, and the custom 404 page. Compose uses a read-only root filesystem and publishes the port on localhost. To stop it:

```sh
docker compose down
```

The multi-stage image regenerates and validates the website during build; the runtime contains only NGINX and the exported site, not Python or the project source.

## Update the website

- `content/chapter.json`: chapter contact and meeting information.
- `build_site.py`: page copy, shared navigation, and project descriptions.
- `templates/home-hero.html`: homepage hero and decorative pins.
- `dist/style.css`, `dist/script.js`, `dist/privacy.js`, `dist/contact.js`: maintained styles and behavior.
- `dist/assets/`: images and local fonts, including optimized AVIF/WebP variants.

The `dist/` folder intentionally contains both maintained assets and generated HTML. Keep it tracked. Python 3.9+ with timezone data is sufficient to build locally; the Docker builder supplies its own timezone data.

```sh
python3 build_site.py
python3 scripts/check-launch.py
python3 -m http.server 8080 --directory dist
```

Python's preview server serves `/join.html`; NGINX also supports `/join` and real custom-404 responses. Rebuild the container after making changes. Pillow is only needed when regenerating image variants with `scripts/optimize-assets.py`.

## Container checks

GitHub Actions builds and starts the production container on pushes to `main` and pull requests. It checks page routes, the health endpoint, missing-page status, security headers, caching, and gzip. To run the same checks locally while the container is running:

```sh
python3 scripts/smoke-container.py
```

## Use your own domain

Register the domain and configure a container host and an HTTPS reverse proxy or load balancer. Set the public HTTPS origin at build time so canonical URLs, social cards, sitemap, and contact-form redirects use the right address:

```sh
SITE_ORIGIN=https://utepras.org docker compose up --build -d
```

That example does not register the domain or configure DNS. NGINX listens on port 8080 inside the container; TLS belongs at the hosting proxy. The Compose port is intentionally local. Expose the container through your hosting provider or reverse proxy when deploying.

Search indexing is controlled by `public_indexing` in `content/site-settings.json`; it is currently disabled. Enable it when ready for search indexing and rebuild.

For a host that accepts static files instead of containers:

```sh
python3 scripts/export-static.py
```

Upload the contents of `exports/utep-ras-static.zip`. Configure caching, HTTPS, and custom 404 routing on the host. The `.openai` configuration in the original checkout belongs only to the existing Sites deployment and is not required here.

## Contact form and privacy

The form submits to FormSubmit for delivery to `ieeeras@utep.edu`; the chapter inbox must activate it. No mail credentials are stored here. Instagram loads only after the visitor permits it; analytics is not connected. Do not add tokens, passwords, private member information, or `.env` files to GitHub.

No project license is granted implicitly. Chapter logos, photographs, and artwork retain their respective rights. Local font licenses are included in `dist/assets/fonts/`.
