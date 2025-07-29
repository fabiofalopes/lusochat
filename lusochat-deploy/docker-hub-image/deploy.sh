#!/bin/bash

# ===========================================
# LUSOCHAT DOCKER HUB IMAGE DEPLOYMENT SCRIPT
# ===========================================

set -e

# Configuration
DOCKER_IMAGE="fabiolx/lusochat-openwebui:latest"
CONTAINER_NAME="lusochat-openwebui"
ENV_FILE=".env"
ENV_EXAMPLE="env.example"
COMPOSE_FILE="docker-compose.yml"
SERVICE_NAME="lusochat-openwebui"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_banner() {
    echo -e "${PURPLE}"
    echo "=========================================="
    echo "   🚀 LUSOCHAT DOCKER HUB DEPLOYMENT"
    echo "=========================================="
    echo -e "${NC}"
}

echo_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

echo_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

echo_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

prompt_user() {
    local message="$1"
    local default="${2:-N}"
    echo -n -e "${BLUE}$message [y/N]: ${NC}"
    read -r response
    response=${response:-$default}
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Check requirements
check_requirements() {
    echo_step "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo_error "Docker is not installed or not in PATH"
        echo_info "Please install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        echo_error "Docker Compose is not available"
        echo_info "Please install Docker Compose or update Docker to a newer version"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        echo_error "Docker daemon is not running"
        echo_info "Please start Docker daemon"
        exit 1
    fi
    
    echo_success "All requirements met"
}

# Setup environment file
setup_environment() {
    echo_step "Setting up environment configuration..."
    
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f "$ENV_EXAMPLE" ]; then
            echo_warning "No .env file found"
            if prompt_user "Copy $ENV_EXAMPLE to .env?" "y"; then
                cp "$ENV_EXAMPLE" "$ENV_FILE"
                echo_success "Created .env file from $ENV_EXAMPLE"
                echo_warning "⚠️  IMPORTANT: Edit .env file with your actual configuration!"
                echo_info "Required variables to configure:"
                echo_info "  - WEBUI_SECRET_KEY (generate with: openssl rand -base64 32)"
                echo_info "  - OPENAI_API_KEY (if using OpenAI models)"
                echo_info "  - GROQ_API_KEY (if using Groq models)"
                echo_info "  - LDAP settings (if using LDAP authentication)"
                echo ""
                if prompt_user "Open .env file for editing now?" "y"; then
                    ${EDITOR:-nano} "$ENV_FILE"
                fi
            else
                echo_error "Cannot proceed without .env file"
                exit 1
            fi
        else
            echo_error "No .env or $ENV_EXAMPLE file found"
            exit 1
        fi
    else
        echo_success "Environment file exists"
        
        # Check for critical missing values
        if grep -q "your-very-strong-secret-key-here-replace-this" "$ENV_FILE"; then
            echo_warning "⚠️  Default secret key detected in .env file"
            echo_info "Please update WEBUI_SECRET_KEY with a secure value"
            if prompt_user "Generate a new secret key automatically?" "y"; then
                if command -v openssl &> /dev/null; then
                    NEW_KEY=$(openssl rand -base64 32)
                    sed -i "s/your-very-strong-secret-key-here-replace-this/$NEW_KEY/" "$ENV_FILE"
                    echo_success "Generated new secret key"
                else
                    echo_warning "OpenSSL not found. Please manually update WEBUI_SECRET_KEY"
                fi
            fi
        fi
    fi
}

# Pull latest image
pull_image() {
    echo_step "Pulling latest Lusochat image from Docker Hub..."
    echo_info "Image: $DOCKER_IMAGE"
    
    if docker pull "$DOCKER_IMAGE"; then
        echo_success "Successfully pulled latest image"
        
        # Show image info
        echo_info "Image details:"
        docker images "$DOCKER_IMAGE" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    else
        echo_error "Failed to pull image from Docker Hub"
        echo_info "Please check your internet connection and try again"
        exit 1
    fi
}

# Deploy services
deploy_services() {
    echo_step "Deploying Lusochat services..."
    
    # Stop existing services if running
    if docker compose ps -q | grep -q .; then
        echo_info "Stopping existing services..."
        docker compose down
    fi
    
    # Start services
    echo_info "Starting services with Docker Compose..."
    if docker compose up -d; then
        echo_success "Services started successfully"
        
        # Wait for services to be ready
        echo_info "Waiting for services to initialize..."
        sleep 5
        
        # Check service health
        if docker compose ps --format json | grep -q '"Health":"healthy"\|"State":"running"'; then
            echo_success "✅ Lusochat is running and healthy!"
        else
            echo_warning "Services started but health status unknown"
            echo_info "Check logs with: ./deploy.sh logs"
        fi
    else
        echo_error "Failed to start services"
        echo_info "Check logs with: docker compose logs"
        exit 1
    fi
}

# Show deployment info
show_deployment_info() {
    local port=$(grep "OPEN_WEBUI_PORT" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 || echo "3000")
    
    echo ""
    echo_success "🎉 DEPLOYMENT COMPLETE!"
    echo ""
    echo -e "${GREEN}📱 Access Lusochat:${NC}"
    echo -e "   🌐 http://localhost:${port}"
    echo -e "   🌍 http://$(hostname -I | awk '{print $1}'):${port} (network access)"
    echo ""
    echo -e "${BLUE}🛠️  Management Commands:${NC}"
    echo -e "   📊 Status:   ${CYAN}./deploy.sh status${NC}"
    echo -e "   📋 Logs:     ${CYAN}./deploy.sh logs${NC}"
    echo -e "   🔄 Restart:  ${CYAN}./deploy.sh restart${NC}"
    echo -e "   🛑 Stop:     ${CYAN}./deploy.sh stop${NC}"
    echo -e "   ⬆️  Update:   ${CYAN}./deploy.sh update${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tips:${NC}"
    echo -e "   • First login: Create admin account at the web interface"
    echo -e "   • Configuration: Edit .env file and restart services"
    echo -e "   • Logs: Use './deploy.sh logs' to troubleshoot issues"
    echo ""
}

# Main deployment function
deploy_lusochat() {
    print_banner
    check_requirements
    setup_environment
    pull_image
    deploy_services
    show_deployment_info
}

# Update function
update_lusochat() {
    echo_step "Updating Lusochat to latest version..."
    
    pull_image
    
    echo_info "Restarting services with new image..."
    docker compose down
    docker compose up -d
    
    echo_success "✅ Lusochat updated successfully!"
    show_deployment_info
}

# Status function
show_status() {
    echo_step "Checking Lusochat status..."
    
    echo ""
    echo -e "${BLUE}🐳 Container Status:${NC}"
    docker compose ps
    
    echo ""
    echo -e "${BLUE}📊 Resource Usage:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    
    echo ""
    echo -e "${BLUE}💾 Volume Information:${NC}"
    docker volume ls --filter "name=lusochat"
    
    # Check if service is responding
    local port=$(grep "OPEN_WEBUI_PORT" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 || echo "3000")
    echo ""
    echo -e "${BLUE}🌐 Service Health:${NC}"
    if curl -s -f "http://localhost:${port}/health" >/dev/null 2>&1; then
        echo_success "✅ Service is responding on port $port"
    else
        echo_warning "⚠️  Service not responding on port $port"
        echo_info "Check logs with: ./deploy.sh logs"
    fi
}

# Backup function
backup_data() {
    echo_step "Creating backup of Lusochat data..."
    
    local backup_dir="backups"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_file="${backup_dir}/lusochat_backup_${timestamp}.tar.gz"
    
    mkdir -p "$backup_dir"
    
    echo_info "Creating backup: $backup_file"
    
    # Create backup of volumes
    docker run --rm \
        -v lusochat_data:/source:ro \
        -v "$(pwd)/$backup_dir":/backup \
        alpine tar czf "/backup/lusochat_backup_${timestamp}.tar.gz" -C /source .
    
    # Include environment file
    cp "$ENV_FILE" "${backup_dir}/.env_${timestamp}"
    
    echo_success "✅ Backup created: $backup_file"
    echo_info "Environment file backed up as: ${backup_dir}/.env_${timestamp}"
}

# Restore function
restore_data() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        echo_error "Please specify backup file"
        echo_info "Usage: ./deploy.sh restore <backup_file>"
        echo_info "Available backups:"
        ls -la backups/*.tar.gz 2>/dev/null || echo_info "No backups found"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        echo_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    echo_step "Restoring Lusochat data from: $backup_file"
    
    if prompt_user "This will overwrite current data. Continue?" "N"; then
        # Stop services
        docker compose down
        
        # Restore data
        docker run --rm \
            -v lusochat_data:/target \
            -v "$(pwd)/$(dirname "$backup_file")":/backup \
            alpine sh -c "cd /target && tar xzf /backup/$(basename "$backup_file")"
        
        # Start services
        docker compose up -d
        
        echo_success "✅ Data restored successfully"
    else
        echo_info "Restore cancelled"
    fi
}

# Main script logic
case "${1:-deploy}" in
    "deploy"|"start")
        deploy_lusochat
        ;;
    "update")
        update_lusochat
        ;;
    "stop")
        echo_step "Stopping Lusochat services..."
        docker compose down
        echo_success "✅ Services stopped"
        ;;
    "restart")
        echo_step "Restarting Lusochat services..."
        docker compose restart
        echo_success "✅ Services restarted"
        show_deployment_info
        ;;
    "status")
        show_status
        ;;
    "logs")
        echo_step "Showing service logs (Ctrl+C to exit)..."
        docker compose logs -f
        ;;
    "shell")
        echo_step "Opening shell in Lusochat container..."
        docker compose exec "$SERVICE_NAME" /bin/bash
        ;;
    "backup")
        backup_data
        ;;
    "restore")
        restore_data "$2"
        ;;
    "clean")
        echo_step "Cleaning up Lusochat deployment..."
        if prompt_user "This will remove all containers, volumes, and data. Continue?" "N"; then
            docker compose down -v
            docker image rm "$DOCKER_IMAGE" 2>/dev/null || true
            echo_success "✅ Cleanup complete"
        else
            echo_info "Cleanup cancelled"
        fi
        ;;
    "help"|"--help"|"-h")
        print_banner
        echo -e "${BLUE}Usage:${NC} $0 [COMMAND]"
        echo ""
        echo -e "${BLUE}Commands:${NC}"
        echo -e "  ${CYAN}deploy${NC}   Deploy Lusochat (default command)"
        echo -e "  ${CYAN}start${NC}    Alias for deploy"
        echo -e "  ${CYAN}update${NC}   Update to latest Docker Hub image"
        echo -e "  ${CYAN}stop${NC}     Stop all services"
        echo -e "  ${CYAN}restart${NC}  Restart all services"
        echo -e "  ${CYAN}status${NC}   Show service status and health"
        echo -e "  ${CYAN}logs${NC}     Show and follow service logs"
        echo -e "  ${CYAN}shell${NC}    Open shell in Lusochat container"
        echo -e "  ${CYAN}backup${NC}   Create backup of data"
        echo -e "  ${CYAN}restore${NC}  Restore from backup file"
        echo -e "  ${CYAN}clean${NC}    Remove all containers and data"
        echo -e "  ${CYAN}help${NC}     Show this help message"
        echo ""
        echo -e "${BLUE}Examples:${NC}"
        echo -e "  $0 deploy           # Deploy Lusochat"
        echo -e "  $0 update           # Update to latest version"
        echo -e "  $0 logs             # View logs"
        echo -e "  $0 backup           # Create backup"
        echo -e "  $0 restore backup.tar.gz  # Restore from backup"
        echo ""
        ;;
    *)
        echo_error "Unknown command: $1"
        echo_info "Use '$0 help' to see available commands"
        exit 1
        ;;
esac