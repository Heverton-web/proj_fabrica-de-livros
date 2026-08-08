#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Deploy Script — Máquina de Vendas
# Suporta: Docker Compose (produção), Vercel (frontend), VPS (backend)
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${PROJECT_DIR}/.env"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${GREEN}[DEPLOY]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()  { echo -e "${RED}[ERRO]${NC} $*" >&2; }

# ---------------------------------------------------------------------------
# Validações
# ---------------------------------------------------------------------------
check_deps() {
    local missing=()
    for cmd in docker docker-compose curl git; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        err "Dependências faltando: ${missing[*]}"
        exit 1
    fi
}

check_env() {
    if [ ! -f "$ENV_FILE" ]; then
        err "Arquivo .env não encontrado em ${ENV_FILE}"
        err "Copie .env.example e preencha as variáveis"
        exit 1
    fi
    log "Arquivo .env encontrado"
}

# ---------------------------------------------------------------------------
# Build & Deploy Docker
# ---------------------------------------------------------------------------
deploy_docker() {
    log "Iniciando deploy Docker Compose..."
    cd "$PROJECT_DIR"

    check_env

    # Build
    log "Construindo imagens..."
    docker-compose build --no-cache

    # Parar containers antigos
    log "Parando containers antigos..."
    docker-compose down --remove-orphans

    # Subir
    log "Subindo containers..."
    docker-compose up -d

    # Health check
    log "Verificando saúde dos containers..."
    sleep 10
    local unhealthy
    unhealthy=$(docker-compose ps --filter "status=unhealthy" -q | wc -l)
    if [ "$unhealthy" -gt 0 ]; then
        err "$unhealthy container(s) unhealthy!"
        docker-compose logs --tail=20
        exit 1
    fi

    log "Deploy Docker concluído com sucesso!"
    docker-compose ps
}

# ---------------------------------------------------------------------------
# Deploy Vercel (frontend)
# ---------------------------------------------------------------------------
deploy_vercel() {
    log "Deploying frontend no Vercel..."
    cd "$PROJECT_DIR/frontend"

    if ! command -v vercel &>/dev/null; then
        warn "Vercel CLI não encontrado. Instalando..."
        npm install -g vercel
    fi

    # Deploy
    if [ "${PRODUCTION:-false}" = "true" ]; then
        vercel --prod --yes
    else
        vercel --yes
    fi

    log "Deploy Vercel concluído!"
}

# ---------------------------------------------------------------------------
# Deploy VPS (backend)
# ---------------------------------------------------------------------------
deploy_vps() {
    log "Deploy backend na VPS..."

    local VPS_HOST="${VPS_HOST:-}"
    local VPS_USER="${VPS_USER:-root}"
    local VPS_PATH="${VPS_PATH:-/opt/maquina-vendas}"

    if [ -z "$VPS_HOST" ]; then
        err "VPS_HOST não definido no .env"
        exit 1
    fi

    check_env

    # Sync arquivos
    log "Sincronizando arquivos com VPS..."
    rsync -avz --delete \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='.env' \
        --exclude='database/*.db' \
        "$PROJECT_DIR/" "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/"

    # Deploy remoto
    log "Executando deploy remoto..."
    ssh "${VPS_USER}@${VPS_HOST}" << REMOTE
        set -euo pipefail
        cd "${VPS_PATH}"

        # Instalar dependências Python
        cd backend
        pip install -r requirements.txt --quiet

        # Rodar migrações
        python manage.py migrate --noinput

        # Reiniciar serviço
        sudo systemctl restart maquina-vendas
        sudo systemctl status maquina-vendas --no-pager

        echo "Deploy VPS concluído!"
REMOTE

    log "Deploy VPS concluído!"
}

# ---------------------------------------------------------------------------
# Deploy Completo (Docker + Vercel)
# ---------------------------------------------------------------------------
deploy_full() {
    log "Deploy completo (Docker + Vercel)..."
    deploy_docker
    deploy_vercel
    log "Deploy completo finalizado!"
}

# ---------------------------------------------------------------------------
# Rollback
# ---------------------------------------------------------------------------
rollback() {
    log "Executando rollback..."
    cd "$PROJECT_DIR"

    local tag="${1:-previous}"
    log "Revertendo para tag: ${tag}"

    git checkout "$tag"
    deploy_docker

    log "Rollback concluído!"
}

# ---------------------------------------------------------------------------
# Database Backup
# ---------------------------------------------------------------------------
backup_db() {
    log "Criando backup do banco de dados..."
    local backup_dir="${PROJECT_DIR}/database/backups"
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="${backup_dir}/leads_${timestamp}.db"

    mkdir -p "$backup_dir"

    if [ -f "${PROJECT_DIR}/database/leads.db" ]; then
        cp "${PROJECT_DIR}/database/leads.db" "$backup_file"
        gzip "$backup_file"
        log "Backup salvo em: ${backup_file}.gz"

        # Manter apenas últimos 30 backups
        ls -t "${backup_dir}"/*.gz 2>/dev/null | tail -n +31 | xargs -r rm
        log "Backups antigos limpos"
    else
        warn "Banco de dados não encontrado"
    fi
}

# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------
status() {
    log "Status da máquina de vendas:"
    echo ""

    # Docker
    if command -v docker-compose &>/dev/null; then
        echo -e "${BLUE}=== Containers Docker ===${NC}"
        cd "$PROJECT_DIR"
        docker-compose ps 2>/dev/null || echo "  (sem containers)"
        echo ""
    fi

    # Database
    if [ -f "${PROJECT_DIR}/database/leads.db" ]; then
        echo -e "${BLUE}=== Banco de Dados ===${NC}"
        local total_leads
        total_leads=$(sqlite3 "${PROJECT_DIR}/database/leads.db" "SELECT COUNT(*) FROM leads;" 2>/dev/null || echo "0")
        echo "  Total de leads: ${total_leads}"
        echo ""
    fi

    # Métricas
    if [ -f "${PROJECT_DIR}/database/metrics.json" ]; then
        echo -e "${BLUE}=== Últimas Métricas ===${NC}"
        python3 -c "
import json
with open('${PROJECT_DIR}/database/metrics.json') as f:
    m = json.load(f)
    c = m.get('current', {})
    leads = c.get('leads', {})
    print(f'  Leads total: {leads.get(\"total\", 0)}')
    print(f'  Novos hoje: {leads.get(\"novos_hoje\", 0)}')
    conv = c.get('conversao', {})
    print(f'  Taxa conversão: {conv.get(\"taxa_conversao_geral\", 0)}%')
" 2>/dev/null || echo "  (sem métricas)"
    fi
}

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
usage() {
    cat << EOF
Uso: $0 <comando>

Comandos:
  docker      Deploy via Docker Compose (produção)
  vercel      Deploy frontend no Vercel
  vps         Deploy backend na VPS
  full        Deploy completo (Docker + Vercel)
  rollback    Rollback para tag/commit anterior
  backup      Backup do banco de dados
  status      Mostra status atual

Variáveis de ambiente:
  PRODUCTION=true   Deploy em produção (Vercel)
  VPS_HOST          Endereço da VPS
  VPS_USER          Usuário SSH (default: root)
  VPS_PATH          Path remoto (default: /opt/maquina-vendas)

Exemplos:
  $0 docker                    # Deploy Docker local
  $0 full                      # Deploy completo
  PRODUCTION=true $0 vercel    # Deploy Vercel em produção
  $0 rollback v1.0.0           # Rollback para tag
  $0 backup                    # Backup do banco
  $0 status                    # Ver status
EOF
}

# Main
case "${1:-}" in
    docker)     check_deps; deploy_docker ;;
    vercel)     deploy_vercel ;;
    vps)        check_deps; deploy_vps ;;
    full)       check_deps; deploy_full ;;
    rollback)   check_deps; rollback "${2:-}" ;;
    backup)     backup_db ;;
    status)     status ;;
    -h|--help)  usage ;;
    *)          usage; exit 1 ;;
esac
