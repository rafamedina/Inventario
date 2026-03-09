# ─────────────────────────────────────────────────────────────
# 🐳 Dockerfile Multi-stage: Estructura Estándar de Odoo
# ─────────────────────────────────────────────────────────────

# --- Etapa 1: Base ---
FROM odoo:18.0 AS base
USER root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Definimos una carpeta de addons limpia
WORKDIR /mnt/extra-addons

# --- Etapa 2: Test ---
FROM base AS test
USER root

# Instalación de Chrome
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN printf '#!/bin/bash\nexec google-chrome-stable --no-sandbox --disable-gpu --disable-dev-shm-usage "$@"\n' > /usr/bin/chromium-browser \
    && chmod +x /usr/bin/chromium-browser

RUN pip3 install --no-cache-dir --break-system-packages pytest pytest-odoo

# IMPORTANTE: Copiamos el código DENTRO de una carpeta con el nombre del módulo
COPY . ./Inventario
RUN chown -R odoo:odoo /mnt/extra-addons/Inventario

USER odoo

# --- Etapa 3: Prod ---
FROM base AS prod
USER root
COPY . ./Inventario
RUN rm -rf Inventario/tests Inventario/conductor Inventario/.github Inventario/.pre-commit-config.yaml
RUN chown -R odoo:odoo /mnt/extra-addons/Inventario
USER odoo
