# ─────────────────────────────────────────────────────────────
# 🐳 Dockerfile Multi-stage: Eficiencia y Seguridad
# ─────────────────────────────────────────────────────────────

# --- Etapa 1: Base (Común) ---
FROM odoo:18.0 AS base
USER root
ENV DEBIAN_FRONTEND=noninteractive

# Dependencias mínimas de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/odoo/custom_addons/Inventario

# --- Etapa 2: Test (Para CI y Desarrollo) ---
FROM base AS test
USER root

# Instalamos Chrome para tests de UI
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Chrome Wrapper
RUN printf '#!/bin/bash\nexec google-chrome-stable --no-sandbox --disable-gpu --disable-dev-shm-usage "$@"\n' > /usr/bin/chromium-browser \
    && chmod +x /usr/bin/chromium-browser

# 🚀 Instalamos pytest Y pytest-odoo (La clave para unir ambos mundos)
RUN pip3 install --no-cache-dir --break-system-packages pytest pytest-odoo

# Copiamos código
COPY . .
USER odoo

# --- Etapa 3: Prod (Imagen limpia) ---
FROM base AS prod
USER root
COPY . .
RUN rm -rf tests/ conductor/ .github/ .pre-commit-config.yaml Dockerfile pytest.ini pyproject.toml ruff.toml
RUN chown -R odoo:odoo .
USER odoo
