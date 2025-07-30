#!/usr/bin/env python3
"""
Apply local enterprise unlock modifications to LiteLLM
This script directly modifies the license check file instead of using git patches

Robust validation and modification of LiteLLM license checking to enable
enterprise features locally without external validation.
"""

import os
import re
import hashlib
import shutil
from datetime import datetime

# Global variable to store the base path to litellm-upstream
LITELLM_BASE_PATH = None

def validate_file_structure():
    """Validate that all required files and structures exist"""
    # Try both relative paths - when run from deploy script vs manually
    base_paths = ["litellm-upstream", "../litellm-upstream", "./litellm-upstream"]
    
    # Find the correct base path
    litellm_base = None
    for base in base_paths:
        if os.path.exists(os.path.join(base, "pyproject.toml")):
            litellm_base = base
            break
    
    if not litellm_base:
        print("ERROR: Could not find litellm-upstream directory")
        return False
    
    required_files = [
        f"{litellm_base}/litellm/proxy/auth/litellm_license.py",
        f"{litellm_base}/litellm/proxy/_types.py",
        f"{litellm_base}/pyproject.toml",
        f"{litellm_base}/docker-compose.yml"
    ]
    
    # Store the base path globally for other functions
    global LITELLM_BASE_PATH
    LITELLM_BASE_PATH = litellm_base
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"ERROR: Missing required files: {', '.join(missing_files)}")
        return False
    
    return True

def backup_original_file(file_path):
    """Create a backup of the original file before modification"""
    backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        print(f"WARNING: Could not create backup: {e}")
        return False

def get_file_hash(file_path):
    """Get SHA256 hash of file content for validation"""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def validate_modification_feasibility(content):
    """Check if the file structure allows our modification"""
    required_patterns = [
        r'class LicenseCheck:',
        r'def is_premium\(self\)',
        r'if self\.license_str is None:\s+return False',
        r'from litellm\.proxy\._types import'
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if not re.search(pattern, content):
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"ERROR: Cannot apply modification - missing required code patterns:")
        for pattern in missing_patterns:
            print(f"  - {pattern}")
        return False
    
    return True

def modify_license_file():
    """Modify the license file to include local enterprise unlock logic"""
    
    # Validate file structure first
    if not validate_file_structure():
        return False
    
    # Use the base path found in validation
    global LITELLM_BASE_PATH
    license_file_path = f"{LITELLM_BASE_PATH}/litellm/proxy/auth/litellm_license.py"
    
    # Read the current file
    with open(license_file_path, 'r') as f:
        content = f.read()
    
    # Check if our modification is already present
    if 'LOCAL_ENTERPRISE_UNLOCK' in content:
        print("✅ Local enterprise unlock already applied")
        return True
    
    # Validate that modification is feasible
    if not validate_modification_feasibility(content):
        return False
    
    # Create backup before modification
    backup_original_file(license_file_path)
    
    # Define the modification to insert
    local_unlock_code = '''            
            if self.license_str == "LOCAL_ENTERPRISE_UNLOCK":
                from litellm.proxy._types import EnterpriseLicenseData
                expiration_date = "9999-12-31"
                license_data = {
                    "expiration_date": expiration_date,
                    "max_users": 100000,
                    "max_teams": 100000,
                }
                self.airgapped_license_data = EnterpriseLicenseData(**license_data)
                return True'''
    
    # Find the insertion point: after "if self.license_str is None: return False"
    pattern = r'(\s+if self\.license_str is None:\s+return False)'
    
    if re.search(pattern, content):
        # Insert our code after the None check
        modified_content = re.sub(
            pattern,
            r'\1' + local_unlock_code,
            content
        )
        
        # Also modify the final return statement to use else for better structure
        modified_content = re.sub(
            r'(\s+elif self\._verify\(license_str=self\.license_str\) is True:\s+return True)\s+return False',
            r'\1\n            else:\n                return False',
            modified_content
        )
        
        # Write the modified content back
        with open(license_file_path, 'w') as f:
            f.write(modified_content)
        
        print("✅ Successfully applied local enterprise unlock modification")
        
        # Validate the modification was applied correctly
        with open(license_file_path, 'r') as f:
            new_content = f.read()
        
        if 'LOCAL_ENTERPRISE_UNLOCK' in new_content and 'EnterpriseLicenseData' in new_content:
            print("✅ Modification validation successful")
            return True
        else:
            print("❌ ERROR: Modification validation failed")
            return False
    else:
        print("❌ ERROR: Could not find insertion point in license file")
        print("The file structure may have changed. Manual review required.")
        return False

def verify_enterprise_features():
    """Verify that enterprise features can be accessed"""
    try:
        global LITELLM_BASE_PATH
        
        # Check if config files support enterprise features
        config_file = f"{LITELLM_BASE_PATH}/config.yaml"
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_content = f.read()
                if 'prometheus' in config_content.lower():
                    print("✅ Enterprise monitoring configuration detected")
                else:
                    print("⚠️  WARNING: No enterprise monitoring configuration found")
        
        # Check docker-compose for enterprise services
        compose_file = f"{LITELLM_BASE_PATH}/docker-compose.yml"
        if os.path.exists(compose_file):
            with open(compose_file, 'r') as f:
                compose_content = f.read()
                services = ['prometheus', 'grafana']
                for service in services:
                    if service in compose_content:
                        print(f"✅ {service.title()} service configured")
                    else:
                        print(f"⚠️  WARNING: {service.title()} service not found")
        
        return True
    except Exception as e:
        print(f"⚠️  WARNING: Could not verify enterprise features: {e}")
        return False

if __name__ == "__main__":
    print("🔧 LiteLLM Local Enterprise Unlock Script")
    print("=" * 50)
    
    success = modify_license_file()
    
    if success:
        print("\n🔍 Verifying enterprise features...")
        verify_enterprise_features()
        
        print("\n✅ LOCAL ENTERPRISE UNLOCK COMPLETE")
        print("Set LITELLM_LICENSE=LOCAL_ENTERPRISE_UNLOCK in your .env file")
    else:
        print("\n❌ MODIFICATION FAILED")
        print("Manual intervention may be required")
    
    exit(0 if success else 1)