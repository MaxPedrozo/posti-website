#!/usr/bin/env bash
# SUPERSEDED: this VPS deploys postisolutions.com via Coolify
# (git-based, Dockerfile build) -- Coolify handles pulling and
# building the repo itself. This script's rsync-to-docroot flow
# assumed a bare-metal Nginx, which this box doesn't run. Kept
# for reference only.
# ============================================================
# deploy.sh - postisolutions.com
# Run this ON THE VPS (not locally). Pulls the repo into a private
# working copy and rsyncs only the public site into the Nginx docroot.
#
# admin.html / app.py / post_generator.py are the local, no-login
# blog-authoring tool -- they stay in GitHub for history, but this
# script makes sure they never physically land in the docroot, so
# they're not public even if the Nginx "deny" rules ever get dropped
# (e.g. certbot rewriting the vhost). Belt + suspenders.
#
# First run: creates ~/repos, clones the repo, creates the docroot
# (asks for your sudo password once for that). Later runs: just
# pulls + re-syncs, no sudo needed unless the docroot got removed.
# ============================================================
set -euo pipefail

REPO_DIR="$HOME/repos/posti-website"
DOCROOT="/var/www/postisolutions.com"

mkdir -p "$(dirname "$REPO_DIR")"

if [ ! -d "$REPO_DIR/.git" ]; then
  git clone https://github.com/MaxPedrozo/posti-website.git "$REPO_DIR"
fi

cd "$REPO_DIR"
git pull origin main

if [ ! -d "$DOCROOT" ]; then
  echo "Docroot $DOCROOT doesn't exist yet -- creating it (needs sudo once)."
  sudo mkdir -p "$DOCROOT"
  sudo chown "$USER":"$USER" "$DOCROOT"
fi

rsync -av --delete \
  --exclude='.git' \
  --exclude='deploy.sh' \
  --exclude='admin.html' \
  --exclude='app.py' \
  --exclude='post_generator.py' \
  --exclude='index - copia.html' \
  --exclude='File Structure.txt' \
  --exclude='Nginx' \
  --exclude='.htaccess' \
  --exclude='*.md' \
  "$REPO_DIR/" "$DOCROOT/"

echo "Deployed $(git rev-parse --short HEAD) to $DOCROOT"
