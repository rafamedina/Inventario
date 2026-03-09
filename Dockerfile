# Usar la imagen oficial de Odoo 18.0
FROM odoo:18.0

USER root

# Instalar dependencias del sistema para Chrome, compilación de paquetes Python y herramientas de test
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    gnupg \
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libcairo2-dev \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /opt/odoo/custom_addons/Inventario

# Copiar el contenido del módulo
COPY . .

# Instalar las dependencias de Python
# Usamos --break-system-packages si es necesario en Python 3.12+ para instalar sobre el sistema en Docker
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt pytest ruff

# Volver al usuario odoo por seguridad
USER odoo
