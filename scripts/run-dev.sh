#!/bin/bash
# ──────────────────────────────────────────────
#  🚀 Entorno de Desarrollo Local — Odoo 18 (Inventario)
# ──────────────────────────────────────────────
# Uso:
#   ./scripts/run-dev.sh              → Inicia (primera vez: crea BD y módulo)
#   ./scripts/run-dev.sh stop         → Para el entorno (datos preservados)
#   ./scripts/run-dev.sh reset        → Para y borra todos los datos
#   ./scripts/run-dev.sh logs         → Ver logs en tiempo real
#   ./scripts/run-dev.sh update       → Forzar actualización del módulo
# ──────────────────────────────────────────────

set -e

# Solución para Windows/Git Bash: evita que se alteren las rutas de Docker
export MSYS_NO_PATHCONV=1

ACTION="${1:-start}"
DB_NAME="inventario_dev"
PROJECT="inventario-dev"
COMPOSE_FILE="Ejemplo/docker-compose.yml"

case "$ACTION" in
  start)
    echo "══════════════════════════════════════════"
    echo "  🚀 Entorno de Desarrollo — Inventario"
    echo "══════════════════════════════════════════"
    echo ""

    echo "📦 Construyendo imagen..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" build --quiet

    echo "🔄 Levantando servicios..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" up -d

    # Esperar a que Odoo esté listo
    echo "⏳ Esperando a que Odoo responda..."
    for i in $(seq 1 30); do
      if docker compose -p "$PROJECT" -f "$COMPOSE_FILE" exec -T odoo python3 -c "
import xmlrpc.client
try:
    xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common').version()
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
        break
      fi
      sleep 2
    done

    # Detectar si la BD ya existe para auto-actualizar
    DB_EXISTS=$(docker compose -p "$PROJECT" -f "$COMPOSE_FILE" exec -T db psql -U odoo -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>/dev/null || true)

    if [ "$DB_EXISTS" = "1" ]; then
      echo "🔄 BD '$DB_NAME' detectada → Actualizando módulo..."
      docker compose -p "$PROJECT" -f "$COMPOSE_FILE" run --rm -T odoo odoo \
        --db_host=db --db_user=odoo --db_password=odoo \
        --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
        -u Inventario -d "$DB_NAME" --stop-after-init --no-http 2>&1 | tail -5
      echo "⚡ Reiniciando servicio..."
      docker compose -p "$PROJECT" -f "$COMPOSE_FILE" restart odoo
      echo ""
      echo "  ✅ Módulo actualizado en http://localhost:8069"
    else
      echo ""
      echo "  ✅ Odoo disponible en: http://localhost:8069"
      echo ""
      echo "  📋 Primera vez:"
      echo "    1. Crea BD con nombre: $DB_NAME"
      echo "    2. Email: admin  |  Password: admin"
      echo "    3. Instala 'Inventario' desde Apps"
    fi

    echo ""
    echo "  Logs:    ./scripts/run-dev.sh logs"
    echo "  Update:  ./scripts/run-dev.sh update"
    echo "  Parar:   ./scripts/run-dev.sh stop"
    echo "══════════════════════════════════════════"
    ;;
  stop)
    echo "⏹️  Parando entorno (datos preservados)..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" down
    echo "✅ Entorno parado."
    ;;
  reset)
    echo "🗑️  Parando y borrando datos..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" down -v --remove-orphans
    echo "✅ Entorno reseteado."
    ;;
  logs)
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" logs -f odoo
    ;;
  restart)
    echo "🔄 Reiniciando Odoo..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" restart odoo
    echo "✅ Reiniciado."
    ;;
  update)
    DB_TARGET="${2:-$DB_NAME}"
    echo "🔄 Actualizando módulo en BD '$DB_TARGET'..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" run --rm -T odoo odoo \
      --db_host=db --db_user=odoo --db_password=odoo \
      --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
      -u Inventario -d "$DB_TARGET" --stop-after-init --no-http 2>&1 | tail -5
    echo "⚡ Reiniciando servicio..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" restart odoo
    echo "✅ Módulo actualizado en '$DB_TARGET'."
    ;;
  *)
    echo "Uso: $0 [start|stop|reset|logs|restart|update [nombre_db]]"
    exit 1
    ;;
esac
