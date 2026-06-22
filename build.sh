#!/bin/bash
# Build le frontend et le copie dans freezer-api/frontend_dist/
set -e

echo "==> Build du frontend..."
cd freezer-pwa
npm install --silent
npm run build

echo "==> Copie dans freezer-api/frontend_dist/..."
cd ..
rm -rf freezer-api/frontend_dist
cp -r freezer-pwa/dist freezer-api/frontend_dist

echo "==> Build terminé. Les fichiers sont dans freezer-api/frontend_dist/"
