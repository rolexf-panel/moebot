#!/bin/bash

# ============================================
# MoeBot Setup Script
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Bold colors
BOLD_RED='\033[1;31m'
BOLD_GREEN='\033[1;32m'
BOLD_YELLOW='\033[1;33m'
BOLD_BLUE='\033[1;34m'
BOLD_MAGENTA='\033[1;35m'
BOLD_CYAN='\033[1;36m'

# Box drawing characters
BOX_TOP="┌──────────────────────────────────────────┐"
BOX_BOTTOM="└──────────────────────────────────────────┘"
BOX_SIDE="│"

# Variables
BOT_DIR="/root/moebot"
VENV_DIR="/root/moebot_venv"

# ============================================
# Functions
# ============================================

print_banner() {
    clear
    echo -e "${BOLD_MAGENTA}"
    echo "╔═══════════════════════════════════════════════╗"
    echo "║                                               ║"
    echo "║   ${WHITE}██╗     ██╗   ██╗███╗   ███╗███╗   ███╗  ${MAGENTA}║"
    echo "║   ${WHITE}██║     ██╗   ██║████╗ ████║████╗ ████║  ${MAGENTA}║"
    echo "║   ${WHITE}██║     ██╗   ██║██╔████╔██║██╔████╔██║  ${MAGENTA}║"
    echo "║   ${WHITE}██║     ██╗   ██║██║╚██╔╝██║██║╚██╔╝██║  ${MAGENTA}║"
    echo "║   ${WHITE}███████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║  ${MAGENTA}║"
    echo "║   ${WHITE}╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ${MAGENTA}║"
    echo "║                                               ║"
    echo "║          ${WHITE}Multi-Feature Telegram Bot${MAGENTA}         ║"
    echo "║          ${WHITE}Powered by python-telegram-bot${MAGENTA}    ║"
    echo "║                                               ║"
    echo "╚═══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo ""
    echo -e "${BOLD_CYAN}➜ $1${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

box_message() {
    local msg="$1"
    local len=${#msg}
    local padding=$(( (50 - len) / 2 ))
    
    echo -e "${BOX_SIDE}$(printf '%*s' $((50 + ${#msg} - 2)) '' | tr ' ' ' ')${BOX_SIDE}"
    echo -e "${BOX_SIDE}$(printf '%*s' $padding)${msg}$(printf '%*s' $padding)${BOX_SIDE}"
    echo -e "${BOX_SIDE}$(printf '%*s' $((50 + ${#msg} - 2)) '' | tr ' ' ' ')${BOX_SIDE}"
}

yes_no_prompt() {
    local prompt="$1"
    local default="${2:-n}"
    
    while true; do
        if [ "$default" = "y" ]; then
            echo -ne "${CYAN}${prompt} [Y/n]: ${NC}"
        else
            echo -ne "${CYAN}${prompt} [y/N]: ${NC}"
        fi
        
        read -r response
        case "$response" in
            [yY][eE][sS]|[yY])
                return 0
                ;;
            [nN][oO]|[nN]|"")
                if [ "$default" = "y" ]; then
                    return 1
                else
                    return 1
                fi
                ;;
            *)
                print_warning "Masukkan 'y' atau 'n'"
                ;;
        esac
    done
}

input_prompt() {
    local prompt="$1"
    local default="$2"
    
    while true; do
        if [ -z "$default" ]; then
            echo -ne "${CYAN}${prompt}: ${NC}"
        else
            echo -ne "${CYAN}${prompt} [${default}]: ${NC}"
        fi
        
        read -r response
        
        if [ -n "$response" ]; then
            echo "$response"
            return 0
        elif [ -n "$default" ]; then
            echo "$default"
            return 0
        fi
    done
}

password_prompt() {
    local prompt="$1"
    
    echo -ne "${CYAN}${prompt}: ${NC}"
    read -rs password
    echo ""
    echo "$password"
}

progress_bar() {
    local duration=$1
    local description=$2
    
    echo -ne "${CYAN}${description}${NC} "
    
    for i in $(seq 1 20); do
        echo -ne "${GREEN}█${NC}"
        sleep "$duration"
    done
    
    echo ""
}

check_python() {
    print_step "1. Memeriksa Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python ditemukan: $PYTHON_VERSION"
        
        if [[ $(echo "$PYTHON_VERSION" | cut -d. -f1) -lt 3 ]]; then
            print_error "Python 3.x diperlukan!"
            exit 1
        fi
    else
        print_error "Python tidak ditemukan!"
        print_info "Install dengan: apt-get update && apt-get install -y python3 python3-pip python3-venv"
        exit 1
    fi
}

check_dependencies() {
    print_step "2. Memeriksa dependencies..."
    
    MISSING_DEPS=()
    
    if ! command -v git &> /dev/null; then
        MISSING_DEPS+=("git")
    fi
    
    if ! command -v curl &> /dev/null; then
        MISSING_DEPS+=("curl")
    fi
    
    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        print_warning "Menginstall dependencies yang kurang..."
        apt-get update -qq
        apt-get install -y -qq "${MISSING_DEPS[@]}" 2>/dev/null || true
    fi
    
    print_success "Semua dependencies tersedia"
}

create_directory() {
    print_step "3. Membuat direktori bot..."
    
    if [ -d "$BOT_DIR" ]; then
        if yes_no_prompt "Direktori sudah ada. Hapus dan buat ulang?" "n"; then
            rm -rf "$BOT_DIR"
            mkdir -p "$BOT_DIR"
            print_success "Direktori dibuat"
        else
            print_info "Menggunakan direktori yang ada"
        fi
    else
        mkdir -p "$BOT_DIR"
        print_success "Direktori dibuat: $BOT_DIR"
    fi
}

setup_env() {
    print_step "4. Mengkonfigurasi environment..."
    
    if [ -f "$BOT_DIR/.env" ]; then
        if yes_no_prompt "File .env sudah ada. Timpa?" "n"; then
            :
        else
            print_info "Menggunakan .env yang ada"
            return 0
        fi
    fi
    
    echo ""
    echo -e "${BOLD_YELLOW}📝 Konfigurasi Bot${NC}"
    echo ""
    
    # Bot Token
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    BOT_TOKEN=$(input_prompt "Masukkan BOT TOKEN" "")
    while [ -z "$BOT_TOKEN" ]; do
        print_error "BOT TOKEN tidak boleh kosong!"
        BOT_TOKEN=$(input_prompt "Masukkan BOT TOKEN" "")
    done
    
    # Owner ID
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    OWNER_ID=$(input_prompt "Masukkan OWNER ID (angka)" "")
    while [ -z "$OWNER_ID" ] || ! [[ "$OWNER_ID" =~ ^[0-9]+$ ]]; do
        print_error "OWNER ID harus angka!"
        OWNER_ID=$(input_prompt "Masukkan OWNER ID (angka)" "")
    done
    
    # Ollama (optional)
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    print_info "Konfigurasi Ollama (opsional - tekan Enter untuk skip)"
    OLLAMA_BASE_URL=$(input_prompt "Ollama URL" "http://localhost:11434")
    OLLAMA_MODEL=$(input_prompt "Ollama Model" "qwen2.5-coder:14b")
    
    if [ -z "$OLLAMA_BASE_URL" ]; then
        OLLAMA_BASE_URL="http://localhost:11434"
    fi
    if [ -z "$OLLAMA_MODEL" ]; then
        OLLAMA_MODEL="qwen2.5-coder:14b"
    fi
    
    # Database path
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    DB_PATH=$(input_prompt "Database Path" "moebot.db")
    
    # Log Level
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    LOG_LEVEL=$(input_prompt "Log Level (DEBUG/INFO/WARNING/ERROR)" "INFO")
    
    # Flood settings
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    FLOOD_THRESHOLD=$(input_prompt "Flood Threshold (default: 5)" "5")
    FLOOD_COOLDOWN=$(input_prompt "Flood Cooldown dalam detik (default: 300)" "300")
    
    # Create .env file
    cat > "$BOT_DIR/.env" << EOF
BOT_TOKEN=$BOT_TOKEN
OWNER_ID=$OWNER_ID
OLLAMA_BASE_URL=$OLLAMA_BASE_URL
OLLAMA_MODEL=$OLLAMA_MODEL
DB_PATH=$DB_PATH
LOG_LEVEL=$LOG_LEVEL
FLOOD_THRESHOLD=$FLOOD_THRESHOLD
FLOOD_COOLDOWN=$FLOOD_COOLDOWN
EOF
    
    print_success "File .env dibuat"
}

install_requirements() {
    print_step "5. Menginstall Python packages..."
    
    # Create venv
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        print_success "Virtual environment dibuat"
    fi
    
    # Activate venv
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip -q
    print_success "Pip diupgrade"
    
    # Install requirements
    if [ -f "$BOT_DIR/requirements.txt" ]; then
        pip install -r "$BOT_DIR/requirements.txt" -q
    else
        pip install python-telegram-bot[job-queue]==21.* aiosqlite yt-dlp httpx python-dotenv psutil -q
    fi
    
    print_success "Packages terinstall"
    
    # Deactivate
    deactivate
}

verify_installation() {
    print_step "6. Memverifikasi instalasi..."
    
    source "$VENV_DIR/bin/activate"
    
    # Check packages
    MISSING=()
    
    if ! python -c "import telegram" 2>/dev/null; then
        MISSING+=("python-telegram-bot")
    fi
    
    if ! python -c "import aiosqlite" 2>/dev/null; then
        MISSING+=("aiosqlite")
    fi
    
    if ! python -c "import yt_dlp" 2>/dev/null; then
        MISSING+=("yt-dlp")
    fi
    
    if ! python -c "import httpx" 2>/dev/null; then
        MISSING+=("httpx")
    fi
    
    if ! python -c "import dotenv" 2>/dev/null; then
        MISSING+=("python-dotenv")
    fi
    
    if ! python -c "import psutil" 2>/dev/null; then
        MISSING+=("psutil")
    fi
    
    deactivate
    
    if [ ${#MISSING[@]} -eq 0 ]; then
        print_success "Semua packages terinstall dengan benar"
        return 0
    else
        print_error "Packages yang kurang: ${MISSING[*]}"
        return 1
    fi
}

print_summary() {
    print_step "Selesai!"
    
    echo ""
    echo -e "${BOLD_GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD_GREEN}  🎉 Setup MoeBot Selesai! 🎉${NC}"
    echo -e "${BOLD_GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${WHITE}📁 Lokasi bot:${NC} ${CYAN}$BOT_DIR${NC}"
    echo -e "${WHITE}🐍 Virtual env:${NC} ${CYAN}$VENV_DIR${NC}"
    echo ""
    echo -e "${WHITE}📝 Untuk menjalankan bot:${NC}"
    echo ""
    echo -e "${YELLOW}   # Activate virtual environment${NC}"
    echo -e "${CYAN}   source $VENV_DIR/bin/activate${NC}"
    echo ""
    echo -e "${YELLOW}   # Jalankan bot${NC}"
    echo -e "${CYAN}   cd $BOT_DIR && python main.py${NC}"
    echo ""
    echo -e "${YELLOW}   # Atau gunakan script helper${NC}"
    echo -e "${CYAN}   $BOT_DIR/start.sh${NC}"
    echo ""
    echo -e "${BOLD_MAGENTA}━━━${NC} ${WHITE}Bot Commands:${NC} ${BOLD_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${WHITE}   /start   - Mulai bot${NC}"
    echo -e "${WHITE}   /help    - Lihat bantuan${NC}"
    echo -e "${WHITE}   /plugins - Lihat plugin${NC}"
    echo -e "${WHITE}   /stats   - Statistik${NC}"
    echo ""
}

create_start_script() {
    print_step "Membuat script helper..."
    
    cat > "$BOT_DIR/start.sh" << 'STARTEOF'
#!/bin/bash

BOT_DIR="/root/moebot"
VENV_DIR="/root/moebot_venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment tidak ditemukan. Jalankan setup.sh dulu!"
    exit 1
fi

source "$VENV_DIR/bin/activate"
cd "$BOT_DIR"
python main.py
STARTEOF

    chmod +x "$BOT_DIR/start.sh"
    print_success "Script start.sh dibuat"
}

create_stop_script() {
    cat > "$BOT_DIR/stop.sh" << 'STOPEOF'
#!/bin/bash

BOT_DIR="/root/moebot"

echo "Menghentikan MoeBot..."

# Find and kill bot process
pkill -f "python.*main.py" 2>/dev/null || true

echo "MoeBot dihentikan!"
STOPEOF

    chmod +x "$BOT_DIR/stop.sh"
}

create_service() {
    if yes_no_prompt "Buat systemd service untuk auto-start?" "y"; then
        SERVICE_FILE="/etc/systemd/system/moebot.service"
        
        cat > "$SERVICE_FILE" << SERVICEEOF
[Unit]
Description=MoeBot Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$BOT_DIR
Environment=PATH=$VENV_DIR/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$VENV_DIR/bin/python $BOT_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF
        
        systemctl daemon-reload
        print_success "Systemd service dibuat"
        print_info "Gunakan: systemctl start moebot"
    fi
}

main() {
    print_banner
    
    echo -e "${WHITE}Selamat datang di MoeBot Setup!${NC}"
    echo ""
    echo "Script ini akan:"
    echo "  • Memeriksa Python dan dependencies"
    echo "  • Membuat direktori bot"
    echo "  • Mengkonfigurasi bot"
    echo "  • Menginstall packages"
    echo ""
    
    if ! yes_no_prompt "Lanjutkan setup?" "y"; then
        print_warning "Setup dibatalkan"
        exit 0
    fi
    
    check_python
    check_dependencies
    create_directory
    setup_env
    install_requirements
    
    if ! verify_installation; then
        print_error "Verifikasi gagal. Coba install manual:"
        print_info "source $VENV_DIR/bin/activate"
        print_info "pip install -r $BOT_DIR/requirements.txt"
    fi
    
    create_start_script
    create_stop_script
    
    if [ "$(uname -m)" = "x86_64" ] || [ "$(uname -m)" = "aarch64" ]; then
        create_service
    fi
    
    print_summary
    
    if yes_no_prompt "Jalankan bot sekarang?" "n"; then
        print_info "Menjalankan bot..."
        source "$VENV_DIR/bin/activate"
        cd "$BOT_DIR"
        python main.py
    fi
}

# Run main
main "$@"
