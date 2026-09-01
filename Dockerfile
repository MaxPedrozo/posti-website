# ============================================================
# Dockerfile - postisolutions.com
# Static site, served by nginx inside the container. Built and
# deployed by Coolify (same pattern as aiops:main-restoquest-web),
# with Traefik handling the domain routing and TLS -- there is no
# host-level Nginx or Certbot involved on this VPS.
#
# Only an explicit allowlist of public files is copied in, so
# admin.html / app.py / post_generator.py (the local, no-login
# blog-authoring tool) and the internal docs never end up inside
# the image at all.
# ============================================================
FROM nginx:alpine

COPY nginx.docker.conf /etc/nginx/conf.d/default.conf

COPY index.html blog.html robots.txt sitemap.xml data.json /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/
COPY legal/ /usr/share/nginx/html/legal/
COPY posts/ /usr/share/nginx/html/posts/

EXPOSE 80
