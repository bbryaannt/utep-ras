# Build and validate the static website; Python is absent from the runtime image.
FROM python:3.13-alpine AS build
RUN apk add --no-cache tzdata
WORKDIR /site
COPY build_site.py ./
COPY content/ ./content/
COPY templates/ ./templates/
COPY scripts/ ./scripts/
COPY dist/ ./dist/
ARG SITE_ORIGIN
ENV SITE_ORIGIN=${SITE_ORIGIN}
RUN python build_site.py \
    && python scripts/check-launch.py \
    && python scripts/export-static.py \
    && python -m zipfile -e exports/utep-ras-static.zip /out

FROM nginxinc/nginx-unprivileged:1.28-alpine AS runtime
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build --chown=101:101 /out/ /usr/share/nginx/html/
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
