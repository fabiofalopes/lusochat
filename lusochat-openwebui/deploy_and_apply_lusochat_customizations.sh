#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e
# Treat unset variables as an error when substituting.
set -u
# Prevent errors in a pipeline from being masked.
set -o pipefail

# --- Configuration ---
OPENWEBUI_GIT_URL="https://github.com/open-webui/open-webui.git"
OPENWEBUI_DIR="open-webui"
CUSTOM_DOCKER_IMAGE_NAME="lusochat-openwebui"
CUSTOM_DOCKER_IMAGE_TAG="latest"
CUSTOM_ICONS_DIR="../.lusochat-ldap/edited-files"

# --- Helper Functions ---
echo_info() {
  echo "[INFO] $1"
}

echo_error() {
  echo "[ERROR] $1" >&2
  exit 1
}

echo_success() {
  echo "[SUCCESS] $1"
}

echo_warning() {
  echo "[WARNING] $1"
}

echo_critical() {
  echo "[CRITICAL] $1" >&2
}

check_tool() {
  if ! command -v "$1" &> /dev/null; then
    echo_error "$1 is not installed. Please install it and try again."
  fi
}

prompt_user() {
    local message="$1"
    local default="$2"
    echo -n "$message [y/N]: "
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

cleanup_openwebui() {
    if [ -d "$OPENWEBUI_DIR" ]; then
        echo_warning "Open WebUI directory already exists: $OPENWEBUI_DIR"
        if prompt_user "Do you want to remove it and clone fresh?" "n"; then
            echo_info "Removing existing Open WebUI directory..."
            rm -rf "$OPENWEBUI_DIR"
            echo_success "Cleanup complete."
            return 0
        else
            echo_info "Using existing Open WebUI directory..."
            return 1
        fi
    fi
    return 0
}

clone_openwebui() {
    echo_info "Cloning Open WebUI..."
    git clone --depth 1 "$OPENWEBUI_GIT_URL" "$OPENWEBUI_DIR"
    echo_success "Open WebUI cloned successfully."
}

# Function to safely replace text in a file
safe_replace() {
    local file="$1"
    local search="$2"
    local replace="$3"
    local description="$4"
    
    if [ ! -f "$file" ]; then
        echo_error "File not found: $file"
        return 1
    fi
    
    # Check if the search string exists
    if ! grep -F "$search" "$file" > /dev/null; then
        echo_error "Search string not found in $file: $search"
        echo_error "Skipping: $description"
        return 1
    fi
    
    # Escape special characters for sed - use a different delimiter
    local delimiter='|'
    # Make sure our delimiter doesn't appear in the strings
    while [[ "$search" == *"$delimiter"* ]] || [[ "$replace" == *"$delimiter"* ]]; do
        delimiter="${delimiter}${delimiter}"
    done
    
    # Perform the replacement
    sed -i "s${delimiter}${search}${delimiter}${replace}${delimiter}g" "$file"
    
    # Verify the replacement was successful by checking that old content is gone
    if ! grep -F "$search" "$file" > /dev/null; then
        echo_success "$description"
    else
        echo_error "Failed to apply: $description"
        return 1
    fi
}

# Function to safely replace text in a file (with confirmation)
safe_replace_with_backup() {
    local file="$1"
    local search="$2"
    local replace="$3"
    local description="$4"
    
    # Create backup
    cp "$file" "$file.backup"
    
    if safe_replace "$file" "$search" "$replace" "$description"; then
        rm "$file.backup"
        return 0
    else
        # Restore backup on failure but continue
        mv "$file.backup" "$file"
        echo_warning "Skipping failed replacement: $description"
        return 1
    fi
}

# Function to check if custom icons directory exists and has the expected structure
check_custom_icons() {
    local icons_available=0
    local missing_icons=()
    
    echo_info "Checking for custom icons in $CUSTOM_ICONS_DIR..."
    
    if [ ! -d "$CUSTOM_ICONS_DIR" ]; then
        echo_warning "Custom icons directory not found: $CUSTOM_ICONS_DIR"
        return 1
    fi
    
    # Define expected icon files and their sources
    local icon_mappings=(
        # Format: "source_path:relative_destination"
        "app/build/favicon.png:static/favicon.png"
        "app/build/static/favicon.png:static/static/favicon.png"
        "app/build/static/splash.png:static/static/splash.png"
        "app/build/static/splash-dark.png:static/static/splash-dark.png"
        "app/backend/static/favicon.png:static/static/favicon-96x96.png"
        "app/backend/static/logo.png:static/static/apple-touch-icon.png"
        "app/backend/static/splash.png:static/static/web-app-manifest-192x192.png"
    )
    
    for mapping in "${icon_mappings[@]}"; do
        local source_path="${mapping%%:*}"
        local full_source_path="$CUSTOM_ICONS_DIR/$source_path"
        
        if [ -f "$full_source_path" ]; then
            icons_available=$((icons_available + 1))
        else
            missing_icons+=("$source_path")
        fi
    done
    
    if [ $icons_available -gt 0 ]; then
        echo_success "Found $icons_available custom icon files"
        if [ ${#missing_icons[@]} -gt 0 ]; then
            echo_warning "Missing icon files:"
            for missing in "${missing_icons[@]}"; do
                echo_warning "  - $missing"
            done
        fi
        return 0
    else
        echo_warning "No custom icon files found"
        return 1
    fi
}

# Function to detect Open WebUI icon structure changes
verify_openwebui_icon_structure() {
    local structure_ok=true
    local expected_paths=(
        "static/favicon.png"
        "static/static/favicon.png"
        "static/static/favicon.ico"
        "static/static/favicon-96x96.png"
        "static/static/apple-touch-icon.png"
        "static/static/splash.png"
        "static/static/web-app-manifest-192x192.png"
        "static/static/web-app-manifest-512x512.png"
        "static/static/site.webmanifest"
        "src/app.html"
    )
    
    echo_info "Verifying Open WebUI icon structure..."
    
    for path in "${expected_paths[@]}"; do
        if [ ! -f "$path" ]; then
            echo_warning "Expected file not found: $path"
            structure_ok=false
        fi
    done
    
    # Check if favicon references in app.html are still the same
    if [ -f "src/app.html" ]; then
        local expected_refs=(
            "/static/favicon.png"
            "/static/favicon-96x96.png"
            "/static/apple-touch-icon.png"
            "/static/splash.png"
        )
        
        for ref in "${expected_refs[@]}"; do
            if ! grep -q "$ref" "src/app.html"; then
                echo_warning "Icon reference not found in app.html: $ref"
                structure_ok=false
            fi
        done
    fi
    
    if [ "$structure_ok" = true ]; then
        echo_success "Open WebUI icon structure verified"
        return 0
    else
        echo_warning "Open WebUI icon structure has changed - icon replacement may not work as expected"
        return 1
    fi
}

# Function to copy custom icons with verification
copy_custom_icons() {
    local icons_copied=0
    local failed_copies=0
    
    echo_info "Copying custom icons..."
    
    # Define icon mappings: source_path:destination_path:description
    local icon_mappings=(
        "app/build/favicon.png:static/favicon.png:Root favicon"
        "app/build/static/favicon.png:static/static/favicon.png:Static favicon"
        "app/build/static/splash.png:static/static/splash.png:Splash screen image"
        "app/build/static/splash-dark.png:static/static/splash-dark.png:Dark mode splash screen"
        "app/backend/static/favicon.png:static/static/favicon-96x96.png:96x96 favicon"
        "app/backend/static/logo.png:static/static/apple-touch-icon.png:Apple touch icon"
        "app/backend/static/splash.png:static/static/web-app-manifest-192x192.png:Web app manifest 192x192"
    )
    
    # Additional mappings for comprehensive coverage
    local additional_mappings=(
        "app/backend/static/favicon.png:static/static/favicon.ico:Favicon ICO (fallback)"
        "app/backend/static/logo.png:static/static/web-app-manifest-512x512.png:Web app manifest 512x512"
        "app/backend/static/favicon.png:static/static/favicon-dark.png:Dark mode favicon"
    )
    
    # Combine all mappings
    local all_mappings=("${icon_mappings[@]}" "${additional_mappings[@]}")
    
    for mapping in "${all_mappings[@]}"; do
        IFS=':' read -r source_path dest_path description <<< "$mapping"
        local full_source_path="$CUSTOM_ICONS_DIR/$source_path"
        
        if [ -f "$full_source_path" ]; then
            # Create destination directory if it doesn't exist
            mkdir -p "$(dirname "$dest_path")"
            
            # Copy the file
            if cp "$full_source_path" "$dest_path"; then
                echo_success "Copied $description: $source_path → $dest_path"
                icons_copied=$((icons_copied + 1))
            else
                echo_warning "Failed to copy $description: $source_path → $dest_path"
                failed_copies=$((failed_copies + 1))
            fi
        else
            echo_warning "Source icon not found: $source_path (skipping $description)"
        fi
    done
    
    # CRITICAL FIX: Update SVG favicon with our custom icon
    echo_info "Updating SVG favicon with custom icon (browsers prioritize SVG)..."
    if [ -f "static/favicon.png" ]; then
        # Convert PNG to base64 and embed in SVG
        local base64_content=$(base64 "static/favicon.png" | tr -d '\n')
        cat > "static/static/favicon.svg" << EOF
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs" width="500" height="500" viewBox="0 0 500 500"><image width="500" height="500" xlink:href="data:image/png;base64,${base64_content}"></image><style>
@media (prefers-color-scheme: light) { :root { filter: none; } }
@media (prefers-color-scheme: dark) { :root { filter: none; } }
</style></svg>
EOF
        echo_success "Updated SVG favicon with custom Lusochat icon (fixes browser tab icon)"
        icons_copied=$((icons_copied + 1))
    else
        echo_warning "Could not update SVG favicon - static/favicon.png not found"
        failed_copies=$((failed_copies + 1))
    fi
    
    echo_info "Icon copying complete: $icons_copied copied, $failed_copies failed"
    
    if [ $icons_copied -gt 0 ]; then
        return 0
    else
        return 1
    fi
}

# Function to update manifest files with new app name
update_manifest_files() {
    echo_info "Updating manifest files..."
    
    # Update site.webmanifest
    if [ -f "static/static/site.webmanifest" ]; then
        safe_replace_with_backup \
            "static/static/site.webmanifest" \
            '"name": "Open WebUI"' \
            '"name": "Lusochat"' \
            "Updated app name in site.webmanifest" || true
            
        safe_replace_with_backup \
            "static/static/site.webmanifest" \
            '"short_name": "WebUI"' \
            '"short_name": "Lusochat"' \
            "Updated short name in site.webmanifest" || true
    fi
    
    # Update opensearch.xml if it exists
    if [ -f "static/opensearch.xml" ]; then
        safe_replace_with_backup \
            "static/opensearch.xml" \
            "Open WebUI" \
            "Lusochat" \
            "Updated opensearch.xml app name" || true
    fi
}

# Function to customize login form placeholders across all languages
customize_login_placeholders() {
    echo_info "Customizing login form placeholders for Lusófona University..."
    
    local updated_files=0
    local failed_files=0
    
    # Language-specific username placeholders
    declare -A username_placeholders=(
        ["pt-PT"]="Nº aluno/professor/funcionário (aXXXXXX, pXXXX, fXXXX)"
        ["pt-BR"]="Nº aluno/professor/funcionário (aXXXXXX, pXXXX, fXXXX)"
        ["en-US"]="Student/teacher/staff number (aXXXXXX, pXXXX, fXXXX)"
        ["en-GB"]="Student/teacher/staff number (aXXXXXX, pXXXX, fXXXX)"
        ["es-ES"]="Nº estudiante/profesor/personal (aXXXXXX, pXXXX, fXXXX)"
        ["fr-FR"]="Nº étudiant/professeur/personnel (aXXXXXX, pXXXX, fXXXX)"
        ["de-DE"]="Student/Lehrer/Personal-Nr. (aXXXXXX, pXXXX, fXXXX)"
        ["it-IT"]="Nº studente/professore/personale (aXXXXXX, pXXXX, fXXXX)"
    )
    
    # Language-specific sign-in titles (without "with LDAP")
    declare -A signin_titles=(
        ["pt-PT"]="Iniciar sessão em {{WEBUI_NAME}}"
        ["pt-BR"]="Faça login em {{WEBUI_NAME}}"
        ["en-US"]="Sign in to {{WEBUI_NAME}}"
        ["en-GB"]="Sign in to {{WEBUI_NAME}}"
        ["es-ES"]="Iniciar sesión en {{WEBUI_NAME}}"
        ["fr-FR"]="Se connecter à {{WEBUI_NAME}}"
        ["de-DE"]="Bei {{WEBUI_NAME}} anmelden"
        ["it-IT"]="Accedi a {{WEBUI_NAME}}"
    )
    
    # Default fallback for other languages
    local default_placeholder="Student/staff number (aXXXXXX, pXXXX, fXXXX)"
    local default_signin_title="Sign in to {{WEBUI_NAME}}"
    
    # Process all translation files
    for locale_dir in src/lib/i18n/locales/*/; do
        if [ -d "$locale_dir" ]; then
            local locale=$(basename "$locale_dir")
            local translation_file="$locale_dir/translation.json"
            
            if [ -f "$translation_file" ]; then
                local placeholder="${username_placeholders[$locale]:-$default_placeholder}"
                local signin_title="${signin_titles[$locale]:-$default_signin_title}"
                
                # Update empty username placeholders
                if grep -q '"Enter Your Username": ""' "$translation_file"; then
                    if safe_replace_with_backup \
                        "$translation_file" \
                        '"Enter Your Username": ""' \
                        "\"Enter Your Username\": \"$placeholder\"" \
                        "Updated $locale username placeholder"; then
                        updated_files=$((updated_files + 1))
                    else
                        failed_files=$((failed_files + 1))
                    fi
                elif grep -q '"Enter Your Username":' "$translation_file"; then
                    # Update existing non-empty placeholders
                    local current_line=$(grep '"Enter Your Username":' "$translation_file")
                    if safe_replace_with_backup \
                        "$translation_file" \
                        "$current_line" \
                        "    \"Enter Your Username\": \"$placeholder\"," \
                        "Updated $locale username placeholder (replaced existing)"; then
                        updated_files=$((updated_files + 1))
                    else
                        failed_files=$((failed_files + 1))
                    fi
                fi
                
                # Remove "with LDAP" from sign-in titles
                if grep -q '"Sign in to {{WEBUI_NAME}} with LDAP":' "$translation_file"; then
                    local current_signin_line=$(grep '"Sign in to {{WEBUI_NAME}} with LDAP":' "$translation_file")
                    if safe_replace_with_backup \
                        "$translation_file" \
                        "$current_signin_line" \
                        "    \"Sign in to {{WEBUI_NAME}} with LDAP\": \"$signin_title\"," \
                        "Updated $locale sign-in title (removed 'with LDAP')"; then
                        echo_success "Removed 'with LDAP' from $locale sign-in title"
                    fi
                fi
            fi
        fi
    done
    
    echo_info "Login placeholder customization complete: $updated_files updated, $failed_files failed"
    
    if [ $updated_files -gt 0 ]; then
        echo_success "Login form placeholders customized for Lusófona University context"
    fi
}

# --- VALIDATION SYSTEM ---

# Validation result tracking
VALIDATION_ERRORS=0
VALIDATION_WARNINGS=0
VALIDATION_CRITICAL=0

log_validation_result() {
    local severity="$1"
    local message="$2"
    local impact="$3"
    
    case "$severity" in
        "CRITICAL")
            echo_critical "$message"
            echo_critical "Impact: $impact"
            VALIDATION_CRITICAL=$((VALIDATION_CRITICAL + 1))
            ;;
        "WARNING")
            echo_warning "$message"
            echo_warning "Impact: $impact"
            VALIDATION_WARNINGS=$((VALIDATION_WARNINGS + 1))
            ;;
        "ERROR")
            echo_error "$message"
            echo_error "Impact: $impact"
            VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
            ;;
        "INFO")
            echo_info "$message"
            ;;
    esac
}

# Phase 1: File Structure Validation
validate_file_structure() {
    echo_info "=== PHASE 1: FILE STRUCTURE VALIDATION ==="
    
    local critical_files=(
        "src/lib/constants.ts:Frontend APP_NAME customization"
        "backend/open_webui/env.py:Backend WEBUI_NAME logic fix"
        "static/favicon.png:Root favicon replacement"
        "static/static/site.webmanifest:App manifest updates"
        "src/app.html:Icon reference verification"
    )
    
    local optional_files=(
        "static/static/favicon.png:Static favicon replacement"
        "static/static/favicon.ico:ICO favicon replacement"
        "static/static/apple-touch-icon.png:Apple touch icon replacement"
        "static/opensearch.xml:OpenSearch name updates"
        "src/lib/i18n/locales/pt-PT/translation.json:Login form placeholder customization"
    )
    
    echo_info "Checking critical files..."
    for file_info in "${critical_files[@]}"; do
        local file_path="${file_info%%:*}"
        local purpose="${file_info##*:}"
        
        if [ ! -f "$file_path" ]; then
            log_validation_result "CRITICAL" "Missing critical file: $file_path" "Cannot perform: $purpose"
        else
            echo_success "Found: $file_path"
        fi
    done
    
    echo_info "Checking optional files..."
    for file_info in "${optional_files[@]}"; do
        local file_path="${file_info%%:*}"
        local purpose="${file_info##*:}"
        
        if [ ! -f "$file_path" ]; then
            log_validation_result "WARNING" "Missing optional file: $file_path" "Will skip: $purpose"
        else
            echo_success "Found: $file_path"
        fi
    done
}

# Phase 2: Content Pattern Validation
validate_customization_targets() {
    echo_info "=== PHASE 2: CONTENT PATTERN VALIDATION ==="
    
    # Frontend constants.ts validation
    if [ -f "src/lib/constants.ts" ]; then
        echo_info "Validating constants.ts patterns..."
        if grep -q "export const APP_NAME = 'Open WebUI';" "src/lib/constants.ts"; then
            echo_success "Found expected APP_NAME pattern in constants.ts"
        else
            # Check for variations
            if grep -q "APP_NAME.*Open WebUI" "src/lib/constants.ts"; then
                log_validation_result "WARNING" "APP_NAME pattern in constants.ts has changed format" "Frontend customization may fail - manual review needed"
                echo_info "Current APP_NAME line:"
                grep "APP_NAME.*Open WebUI" "src/lib/constants.ts" || echo "  (not found)"
            else
                log_validation_result "ERROR" "No APP_NAME with 'Open WebUI' found in constants.ts" "Frontend customization will fail"
            fi
        fi
    fi
    
    # Backend env.py validation
    if [ -f "backend/open_webui/env.py" ]; then
        echo_info "Validating env.py patterns..."
        if grep -q 'WEBUI_NAME += " (Open WebUI)"' "backend/open_webui/env.py"; then
            echo_success "Found expected WEBUI_NAME appending pattern in env.py"
            
            # Validate surrounding context for safety
            local context_lines=$(grep -A2 -B2 'WEBUI_NAME += " (Open WebUI)"' "backend/open_webui/env.py")
            if echo "$context_lines" | grep -q "if WEBUI_NAME"; then
                echo_success "WEBUI_NAME pattern has safe context (if block)"
            else
                log_validation_result "WARNING" "WEBUI_NAME pattern context has changed" "Backend fix may cause syntax errors"
            fi
        else
            # Check for variations
            if grep -q "WEBUI_NAME.*Open WebUI" "backend/open_webui/env.py"; then
                log_validation_result "WARNING" "WEBUI_NAME pattern in env.py has changed format" "Backend customization may fail - manual review needed"
                echo_info "Current WEBUI_NAME lines:"
                grep -n "WEBUI_NAME.*Open WebUI" "backend/open_webui/env.py" || echo "  (not found)"
            else
                log_validation_result "ERROR" "No WEBUI_NAME with 'Open WebUI' found in env.py" "Backend customization will fail"
            fi
        fi
    fi
    
    # Icon system validation
    echo_info "Validating icon system integrity..."
    local icon_references_ok=true
    
    if [ -f "src/app.html" ]; then
        local expected_icon_refs=(
            "/static/favicon.png"
            "/static/favicon-96x96.png"
            "/static/apple-touch-icon.png"
            "/static/splash.png"
        )
        
        for ref in "${expected_icon_refs[@]}"; do
            if ! grep -q "$ref" "src/app.html"; then
                log_validation_result "WARNING" "Icon reference missing in app.html: $ref" "Icon replacement may be incomplete"
                icon_references_ok=false
            fi
        done
        
        if [ "$icon_references_ok" = true ]; then
            echo_success "All expected icon references found in app.html"
        fi
    fi
    
    # Manifest validation
    if [ -f "static/static/site.webmanifest" ]; then
        if grep -q '"name": "Open WebUI"' "static/static/site.webmanifest"; then
            echo_success "Found expected app name pattern in site.webmanifest"
        else
            log_validation_result "WARNING" "App name pattern in site.webmanifest has changed" "Manifest customization may fail"
        fi
    fi
}

# Phase 3: Python Syntax Safety Validation
validate_python_syntax() {
    echo_info "=== PHASE 3: PYTHON SYNTAX VALIDATION ==="
    
    if [ -f "backend/open_webui/env.py" ]; then
        echo_info "Checking Python syntax safety..."
        
        # Test if Python can parse the file
        if python3 -m py_compile "backend/open_webui/env.py" 2>/dev/null; then
            echo_success "env.py has valid Python syntax"
        else
            log_validation_result "CRITICAL" "env.py has Python syntax errors" "Cannot safely modify backend code"
        fi
        
        # Check for import dependencies we might affect
        echo_info "Checking for potential import conflicts..."
        if grep -q "from.*env.*import" backend/open_webui/*.py 2>/dev/null; then
            local import_count=$(grep -c "from.*env.*import" backend/open_webui/*.py 2>/dev/null || echo "0")
            echo_info "Found $import_count files importing from env.py - changes should be safe"
        fi
    fi
}

# Main validation orchestrator
run_validation_suite() {
    echo_info ""
    echo_info "################################################################"
    echo_info "# LUSOCHAT CUSTOMIZATION VALIDATION SUITE"
    echo_info "################################################################"
    echo_info "Validating Open WebUI compatibility before applying customizations..."
    echo_info ""
    
    # Reset counters
    VALIDATION_ERRORS=0
    VALIDATION_WARNINGS=0
    VALIDATION_CRITICAL=0
    
    # Run validation phases
    validate_file_structure
    echo_info ""
    validate_customization_targets
    echo_info ""
    validate_python_syntax
    echo_info ""
    
    # Generate validation report
    echo_info "################################################################"
    echo_info "# VALIDATION REPORT"
    echo_info "################################################################"
    
    if [ $VALIDATION_CRITICAL -gt 0 ]; then
        echo_critical "VALIDATION FAILED: $VALIDATION_CRITICAL critical issue(s) found"
        echo_critical "Cannot proceed with customizations. Open WebUI version may be incompatible."
        echo_critical ""
        echo_critical "Recommended actions:"
        echo_critical "1. Check Open WebUI release notes for breaking changes"
        echo_critical "2. Consider using a known compatible version"
        echo_critical "3. Manual customization may be required"
        return 1
    elif [ $VALIDATION_ERRORS -gt 0 ]; then
        echo_error "VALIDATION FAILED: $VALIDATION_ERRORS error(s) found"
        echo_error "Customizations will likely fail. Aborting for safety."
        return 1
    elif [ $VALIDATION_WARNINGS -gt 0 ]; then
        echo_warning "VALIDATION PASSED WITH WARNINGS: $VALIDATION_WARNINGS warning(s) found"
        echo_warning "Some customizations may not work as expected."
        echo_warning ""
        
        if prompt_user "Do you want to proceed despite warnings? (Recommended: No)" "n"; then
            echo_info "Proceeding with customizations (warnings acknowledged)..."
            return 0
        else
            echo_info "Aborting customizations for safety."
            return 1
        fi
    else
        echo_success "VALIDATION PASSED: No issues found"
        echo_success "Open WebUI version appears compatible with customizations"
        return 0
    fi
}

# --- Main Script ---

echo_info "Starting Lusochat Open WebUI Customization..."

# 1. Check required tools
echo_info "Checking required tools..."
check_tool "git"
check_tool "docker"

# 2. Handle existing open-webui directory
if cleanup_openwebui; then
    # Directory was removed or didn't exist, so clone fresh
    clone_openwebui
fi

# 3. Verify we have the directory
if [ ! -d "$OPENWEBUI_DIR" ]; then
    echo_error "Open WebUI directory not found: $OPENWEBUI_DIR"
fi

cd "$OPENWEBUI_DIR"

# 4. RUN VALIDATION SUITE BEFORE ANY CUSTOMIZATIONS
if ! run_validation_suite; then
    echo_error "Validation failed. Aborting customizations for safety."
fi

echo_info "Applying customizations..."

# 1. Update app title in constants.ts (if it exists)
echo_info "Checking for constants.ts customizations..."
if [ -f "src/lib/constants.ts" ]; then
    echo_info "Updating APP_NAME in constants.ts..."
    safe_replace_with_backup \
        "src/lib/constants.ts" \
        "export const APP_NAME = 'Open WebUI';" \
        "export const APP_NAME = 'Lusochat';" \
        "Updated APP_NAME to Lusochat" || true
else
    echo_info "constants.ts not found - skipping frontend title updates"
fi

# 2. Fix backend WEBUI_NAME logic in env.py
echo_info "Updating WEBUI_NAME logic in backend env.py..."
if [ -f "backend/open_webui/env.py" ]; then
    # Comment out the line that appends "(Open WebUI)" to custom names
    safe_replace_with_backup \
        "backend/open_webui/env.py" \
        '    WEBUI_NAME += " (Open WebUI)"' \
        '    # WEBUI_NAME += " (Open WebUI)"  # Commented out to prevent appending' \
        "Commented out WEBUI_NAME appending logic" || true
    
    # Add pass statement after the if block to prevent Python syntax error
    if grep -q "# WEBUI_NAME.*Commented out" backend/open_webui/env.py; then
        # Find the line number and add pass after it
        line_num=$(grep -n "# WEBUI_NAME.*Commented out" backend/open_webui/env.py | cut -d: -f1)
        sed -i "${line_num}a\\    pass" backend/open_webui/env.py
        echo_success "Added pass statement to fix Python syntax"
    fi
else
    echo_info "backend/open_webui/env.py not found - skipping backend WEBUI_NAME fix"
fi

# 3. Icon replacement system
echo_info ""
echo_info "===== ICON REPLACEMENT SYSTEM ====="

# Check if custom icons are available
if check_custom_icons; then
    # Verify Open WebUI structure
    if verify_openwebui_icon_structure; then
        # Copy custom icons
        if copy_custom_icons; then
            echo_success "Custom icons applied successfully!"
            
            # Update manifest files
            update_manifest_files
        else
            echo_warning "Some icon copying failed, but continuing..."
        fi
    else
        echo_warning "Open WebUI icon structure has changed!"
        echo_warning "Icon replacement may not work correctly."
        echo_warning "Manual verification recommended after deployment."
        
        if prompt_user "Do you want to attempt icon copying anyway?" "n"; then
            copy_custom_icons || true
            update_manifest_files || true
        else
            echo_info "Skipping icon replacement."
        fi
    fi
else
    echo_info "No custom icons found - skipping icon replacement."
fi

echo_info "====================================="
echo_info ""

# 3.5. Complete app.html metadata customization for browser tab and PWA
echo_info "===== COMPLETE METADATA CUSTOMIZATION ====="
if [ -f "src/app.html" ]; then
    echo_info "Updating remaining Open WebUI references in app.html..."
    
    # Update apple-mobile-web-app-title
    safe_replace_with_backup \
        "src/app.html" \
        '<meta name="apple-mobile-web-app-title" content="Open WebUI" />' \
        '<meta name="apple-mobile-web-app-title" content="Lusochat" />' \
        "Updated apple-mobile-web-app-title to Lusochat" || true
    
    # Update meta description
    safe_replace_with_backup \
        "src/app.html" \
        '<meta name="description" content="Open WebUI" />' \
        '<meta name="description" content="Lusochat - Lusófona University AI Chat Interface" />' \
        "Updated meta description to Lusochat" || true
    
    # Update opensearch title
    safe_replace_with_backup \
        "src/app.html" \
        'title="Open WebUI"' \
        'title="Lusochat"' \
        "Updated opensearch title to Lusochat" || true
    
    # Update page title (most important for browser tab)
    safe_replace_with_backup \
        "src/app.html" \
        '<title>Open WebUI</title>' \
        '<title>Lusochat</title>' \
        "Updated page title to Lusochat (fixes browser tab title)" || true
    
    echo_success "App.html metadata customization complete!"
else
    echo_warning "src/app.html not found - skipping metadata updates"
fi

# Update manifest.json to ensure it's not empty and has correct app info
echo_info "Updating manifest.json..."
if [ -f "static/manifest.json" ]; then
    # Check if manifest.json is empty or minimal
    if [ ! -s "static/manifest.json" ] || [ "$(cat static/manifest.json | tr -d ' \n\t')" = "{}" ]; then
        echo_info "Creating comprehensive manifest.json..."
        cat > "static/manifest.json" << 'EOF'
{
  "name": "Lusochat",
  "short_name": "Lusochat",
  "description": "Lusófona University AI Chat Interface",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#171717",
  "background_color": "#ffffff",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/static/favicon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/static/web-app-manifest-192x192.png", 
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/web-app-manifest-512x512.png",
      "sizes": "512x512", 
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    }
  ]
}
EOF
        echo_success "Created comprehensive manifest.json with Lusochat branding"
    else
        echo_info "manifest.json already has content - updating names only"
        safe_replace_with_backup \
            "static/manifest.json" \
            '"name": "Open WebUI"' \
            '"name": "Lusochat"' \
            "Updated manifest.json name" || true
        safe_replace_with_backup \
            "static/manifest.json" \
            '"short_name": "WebUI"' \
            '"short_name": "Lusochat"' \
            "Updated manifest.json short_name" || true
        safe_replace_with_backup \
            "static/manifest.json" \
            '"short_name": "Open WebUI"' \
            '"short_name": "Lusochat"' \
            "Updated manifest.json short_name (alternative pattern)" || true
    fi
else
    echo_warning "static/manifest.json not found - creating new one"
    mkdir -p static
    cat > "static/manifest.json" << 'EOF'
{
  "name": "Lusochat",
  "short_name": "Lusochat",
  "description": "Lusófona University AI Chat Interface",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#171717",
  "background_color": "#ffffff",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/static/favicon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/static/web-app-manifest-192x192.png", 
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/web-app-manifest-512x512.png",
      "sizes": "512x512", 
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    }
  ]
}
EOF
    echo_success "Created new manifest.json with Lusochat branding"
fi

echo_info "================================================"
echo_info ""

# 4. Customize login form placeholders for all languages
customize_login_placeholders

# 5. Copy custom .env file if it exists
if [ -f "../.lusochat-ldap/.env" ]; then
    echo_info "Copying custom .env file..."
    cp "../.lusochat-ldap/.env" ".env"
    echo_success "Custom .env file applied"
else
    echo_info "No custom .env file found - skipping"
fi

# 6. Copy custom docker-compose.yaml if it exists
if [ -f "../.lusochat-ldap/docker-compose.yaml" ]; then
    echo_info "Copying custom docker-compose.yaml..."
    cp "../.lusochat-ldap/docker-compose.yaml" "docker-compose.yaml"
    echo_success "Custom docker-compose.yaml applied"
else
    echo_info "No custom docker-compose.yaml found - skipping"
fi

cd ..

echo_info ""
echo_info "====================================================================="
echo_info " CUSTOMIZATION COMPLETE"
echo_info "====================================================================="
echo_info "Lusochat customizations have been applied to Open WebUI!"
echo_info ""
echo_info "Changes applied:"
echo_info "  ✓ Updated APP_NAME in constants.ts"
echo_info "  ✓ Updated WEBUI_NAME logic in backend env.py"
echo_info "  ✓ Applied custom .env file (if available)"
echo_info "  ✓ Applied custom docker-compose.yaml (if available)"
echo_info "  ✓ Replaced custom icons (if available and structure verified)"
echo_info "  ✓ Updated login form placeholders for all languages"
echo_info "  ✓ Updated app.html metadata (browser tab, PWA, OpenSearch)"
echo_info "  ✓ Updated manifest.json with comprehensive branding"
echo_info ""
echo_info "🎯 BROWSER TAB ISSUES SHOULD NOW BE FIXED:"
echo_info "  • Browser tab title will show 'Lusochat' instead of 'Open WebUI'"
echo_info "  • Custom favicon should appear in browser tab"
echo_info "  • PWA installation will use Lusochat branding"
echo_info "  • All metadata now references Lusófona University"
echo_info ""

# Ask if user wants to build and deploy
if prompt_user "Do you want to build the Docker image now?" "y"; then
    echo_info "Building Docker image..."
    cd "$OPENWEBUI_DIR"
    docker build -t "$CUSTOM_DOCKER_IMAGE_NAME:$CUSTOM_DOCKER_IMAGE_TAG" .
    
    # Update docker-compose to use our custom image
    echo_info "Updating docker-compose to use custom image..."
    sed -i '/build:/,/dockerfile: Dockerfile/d' docker-compose.yaml
    sed -i "s|image: ghcr.io/open-webui/open-webui:.*|image: $CUSTOM_DOCKER_IMAGE_NAME:$CUSTOM_DOCKER_IMAGE_TAG|g" docker-compose.yaml
    
    echo_success "Docker image built successfully!"
    
    if prompt_user "Do you want to start the services now?" "y"; then
        echo_info "Starting services..."
        docker compose up -d
        echo_success "Services started successfully!"
        echo_info ""
        echo_info "Open WebUI should be available at: http://localhost:3000"
        echo_info "Check logs with: docker compose logs -f open-webui"
    else
        echo_info "To start services later, run:"
        echo_info "  cd $OPENWEBUI_DIR"
        echo_info "  docker compose up -d"
    fi
    cd ..
else
    echo_info "To build and deploy later:"
    echo_info "  cd $OPENWEBUI_DIR"
    echo_info "  docker build -t $CUSTOM_DOCKER_IMAGE_NAME:$CUSTOM_DOCKER_IMAGE_TAG ."
    echo_info "  docker compose up -d"
fi

echo_info "=====================================================================" 