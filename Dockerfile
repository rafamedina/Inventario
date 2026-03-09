# Usar la imagen oficial de Odoo 18.0
FROM odoo:18.0

USER root

# Instalar dependencias para Chrome (necesario para tests de UI de Odoo) y pytest
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /opt/odoo/custom_addons/Inventario

# Copiar el contenido del módulo
COPY . .

# Instalar las dependencias de Python del módulo y herramientas de test
RUN pip3 install --no-cache-dir -r requirements.txt pytest ruff

# Volver al usuario odoo por seguridad
USER odoo
