# Usar la imagen oficial de Odoo 18.0
FROM odoo:18.0

USER root

# Evitar diálogos interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar solo Google Chrome (necesario para tests de UI) y certificados
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /opt/odoo/custom_addons/Inventario

# Copiar el módulo
COPY . .

# Instalar los requerimientos ligeros (solo herramientas de test y extras)
# Usamos --break-system-packages para Python 3.12+ en Debian
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Volver al usuario odoo
USER odoo
