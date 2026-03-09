#!/bin/bash
# ──────────────────────────────────────────────
#  🧪 Ejecutar Tests en Docker Local (Efímero)
# ──────────────────────────────────────────────
# Uso:
#   ./scripts/run-tests.sh          → Todos los tests
#   ./scripts/run-tests.sh unit     → Solo unit tests (TransactionCase)
#   ./scripts/run-tests.sh int      → Solo integration tests (HTTP + Tours JS)
#
# Los tests se auto-descubren desde tests/__init__.py.
# No necesitas listar clases manualmente.
# Al terminar, los contenedores se eliminan automáticamente.
# ──────────────────────────────────────────────

set -e

COMPOSE_FILE="docker-compose.test.yml"
PROJECT="elearning-test"
MODE="${1:-all}"

# Asegurar limpieza incluso si el script falla
cleanup() {
    echo ""
    echo "🧹 Limpiando contenedores y volúmenes..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" down -v --remove-orphans 2>/dev/null || true
}
trap cleanup EXIT

echo "══════════════════════════════════════════"
echo "  🧪 Tests Docker Local — elearning_universidad"
echo "══════════════════════════════════════════"
echo ""

# Build
echo "📦 Construyendo imagen..."
docker compose -p "$PROJECT" -f "$COMPOSE_FILE" build --quiet

# Limpiar estado previo (por si quedaron contenedores huérfanos)
docker compose -p "$PROJECT" -f "$COMPOSE_FILE" down -v --remove-orphans 2>/dev/null || true

EXIT_CODE=0

case "$MODE" in
  unit)
    echo "🔬 Ejecutando Unit Tests..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" run --rm odoo-test-unit || EXIT_CODE=$?
    ;;
  int|integration)
    echo "🌐 Ejecutando Integration Tests (HTTP + Tours)..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" run --rm odoo-test-integration || EXIT_CODE=$?
    ;;
  all)
    echo "🔬 Ejecutando Unit Tests..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" run --rm odoo-test-unit || EXIT_CODE=$?
    echo ""
    echo "🌐 Ejecutando Integration Tests..."
    docker compose -p "$PROJECT" -f "$COMPOSE_FILE" run --rm odoo-test-integration || EXIT_CODE=$?
    ;;
  *)
    echo "❌ Modo no reconocido: $MODE"
    echo "   Uso: $0 [unit|int|all]"
    exit 1
    ;;
esac

echo ""
echo "══════════════════════════════════════════"
if [ "$EXIT_CODE" -eq 0 ]; then
  echo "  ✅ Tests completados exitosamente"
else
  echo "  ❌ Tests completados con errores (exit code: $EXIT_CODE)"
fi
echo "══════════════════════════════════════════"

exit $EXIT_CODE
