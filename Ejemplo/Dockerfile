# ─────────────────────────────────────────────────────────────
# 🐳 Dockerfile Profesional Multi-stage para Odoo 18
# ─────────────────────────────────────────────────────────────

# --- Etapa 1: Base (Común para todos los entornos) ---
FROM odoo:18.0 AS base
LABEL maintainer="Pedro"
USER root

# Instalamos solo dependencias de sistema críticas
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /mnt/extra-addons

# --- Etapa 2: Test (Incluye Chrome y herramientas de testing) ---
FROM base AS test
USER root

# Instalamos Google Chrome para Integration Tests (Tours)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    && wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Wrapper para que Odoo encuentre Chrome con los flags de seguridad de Docker
RUN printf '#!/bin/bash\nexec google-chrome-stable --no-sandbox --disable-gpu --disable-dev-shm-usage "$@"\n' > /usr/bin/chromium-browser \
    && chmod +x /usr/bin/chromium-browser

# Dependencias Python para tests
RUN pip3 install --no-cache-dir --break-system-packages websocket-client

# Copiamos todo el módulo (incluyendo tests y docs para esta etapa)
COPY . /mnt/extra-addons/Inventario
RUN chown -R odoo:odoo /mnt/extra-addons/Inventario

USER odoo

# --- Etapa 3: Prod (Imagen limpia para el cliente) ---
FROM base AS prod
USER root

# Copiamos solo el código necesario (el .dockerignore se encarga de filtrar)
COPY . /mnt/extra-addons/Inventario

# Limpieza manual extra por seguridad
RUN rm -rf /mnt/extra-addons/Inventario/tests \
    && rm -rf /mnt/extra-addons/Inventario/docs \
    && rm -rf /mnt/extra-addons/Inventario/conductor \
    && rm -rf /mnt/extra-addons/Inventario/.github

RUN chown -R odoo:odoo /mnt/extra-addons/Inventario

USER odoo
