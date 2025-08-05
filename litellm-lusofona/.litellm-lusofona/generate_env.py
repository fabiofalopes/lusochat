#!/usr/bin/env python3
"""
LiteLLM Environment Configuration Generator

This script generates a secure .env file from .env.example with proper API keys.
Supports both development and production environments with appropriate security levels.

Usage:
    python generate_env.py --dev     # Generate development keys (simple)
    python generate_env.py --prod    # Generate production keys (secure)
    python generate_env.py           # Interactive mode (asks for environment)

Requirements:
    - .env.example must exist in the current directory
    - .env must NOT exist (will prompt for deletion if it does)
"""

import os
import sys
import secrets
import base64
import argparse
from pathlib import Path


class EnvironmentGenerator:
    def __init__(self):
        self.env_example_path = Path('.env.example')
        self.env_path = Path('.env')
        
    def generate_dev_key(self, key_type: str) -> str:
        """Generate simple development keys."""
        dev_keys = {
            'LITELLM_MASTER_KEY': 'sk-dev-master-1234567890abcdef',
            'LITELLM_SALT_KEY': 'sk-dev-salt-abcdef1234567890'
        }
        return dev_keys.get(key_type, 'sk-dev-default-1234567890')
    
    def generate_prod_key(self) -> str:
        """Generate cryptographically secure production key."""
        # Generate 32 random bytes and encode as base64 (URL-safe)
        random_bytes = secrets.token_bytes(32)
        key_suffix = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
        return f"sk-{key_suffix}"
    
    def check_prerequisites(self) -> bool:
        """Check if .env.example exists and handle existing .env file."""
        # Check if .env.example exists
        if not self.env_example_path.exists():
            print("❌ ERROR: .env.example file not found in current directory!")
            print("   Make sure you're running this script from the app directory.")
            return False
        
        # Check if .env already exists
        if self.env_path.exists():
            print("\n⚠️  WARNING: .env file already exists!")
            print("   This script will overwrite the existing .env file.")
            print("   Please backup any important configuration before proceeding.")
            
            while True:
                response = input("\n   Delete existing .env and continue? (y/N): ").strip().lower()
                if response in ['y', 'yes']:
                    try:
                        self.env_path.unlink()
                        print("   ✅ Existing .env file deleted.")
                        break
                    except Exception as e:
                        print(f"   ❌ ERROR: Could not delete .env file: {e}")
                        return False
                elif response in ['n', 'no', '']:
                    print("   ❌ Operation cancelled. Please manually delete .env file to proceed.")
                    return False
                else:
                    print("   Please enter 'y' for yes or 'n' for no.")
        
        return True
    
    def copy_example_file(self) -> bool:
        """Copy .env.example to .env."""
        try:
            with open(self.env_example_path, 'r', encoding='utf-8') as source:
                content = source.read()
            
            with open(self.env_path, 'w', encoding='utf-8') as target:
                target.write(content)
            
            print("✅ Copied .env.example to .env")
            return True
        except Exception as e:
            print(f"❌ ERROR: Could not copy .env.example to .env: {e}")
            return False
    
    def update_env_keys(self, is_production: bool) -> bool:
        """Update the .env file with generated keys."""
        try:
            with open(self.env_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Generate keys based on environment
            if is_production:
                master_key = self.generate_prod_key()
                salt_key = self.generate_prod_key()
                env_type = "PRODUCTION"
            else:
                master_key = self.generate_dev_key('LITELLM_MASTER_KEY')
                salt_key = self.generate_dev_key('LITELLM_SALT_KEY')
                env_type = "DEVELOPMENT"
            
            # Replace the placeholder values
            content = content.replace(
                'LITELLM_MASTER_KEY=sk-your-master-key-here',
                f'LITELLM_MASTER_KEY={master_key}'
            )
            content = content.replace(
                'LITELLM_SALT_KEY=sk-your-salt-key-here',
                f'LITELLM_SALT_KEY={salt_key}'
            )
            
            # Write updated content back to file
            with open(self.env_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f"✅ Generated {env_type} keys:")
            print(f"   🔑 LITELLM_MASTER_KEY: {master_key[:20]}...")
            print(f"   🧂 LITELLM_SALT_KEY: {salt_key[:20]}...")
            
            if is_production:
                print("\n⚠️  IMPORTANT SECURITY NOTES:")
                print("   • Keep these keys secure and never share them")
                print("   • The SALT_KEY cannot be changed once set!")
                print("   • Backup these keys in a secure location")
                print("   • Add .env to your .gitignore file")
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR: Could not update .env file: {e}")
            return False
    
    def get_environment_choice(self) -> bool:
        """Interactive prompt to choose environment type."""
        print("\n🔧 Environment Configuration")
        print("   Choose the environment type:")
        print("   1. Development (simple keys for local testing)")
        print("   2. Production  (cryptographically secure keys)")
        
        while True:
            choice = input("\n   Enter choice (1 for dev, 2 for prod): ").strip()
            if choice == '1':
                return False  # Development
            elif choice == '2':
                return True   # Production
            else:
                print("   Please enter '1' for development or '2' for production.")
    
    def run(self, args) -> bool:
        """Main execution flow."""
        print("🚀 LiteLLM Environment Generator")
        print("=" * 40)
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Determine environment type
        if args.dev:
            is_production = False
            print("\n📦 Generating DEVELOPMENT environment...")
        elif args.prod:
            is_production = True
            print("\n🏭 Generating PRODUCTION environment...")
        else:
            is_production = self.get_environment_choice()
        
        # Copy example file
        if not self.copy_example_file():
            return False
        
        # Generate and update keys
        if not self.update_env_keys(is_production):
            return False
        
        print("\n🎉 SUCCESS! Your .env file has been generated.")
        print("   You can now start your LiteLLM application.")
        print("\n📝 Next steps:")
        print("   1. Review the .env file and update any other required values")
        print("   2. Add your API provider keys (GROQ_API_KEY, etc.)")
        print("   3. Update DATABASE_URL if needed")
        print("   4. Make sure .env is in your .gitignore file")
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate secure .env file for LiteLLM application'
    )
    parser.add_argument(
        '--dev', 
        action='store_true', 
        help='Generate development keys (simple, not secure)'
    )
    parser.add_argument(
        '--prod', 
        action='store_true', 
        help='Generate production keys (cryptographically secure)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.dev and args.prod:
        print("❌ ERROR: Cannot specify both --dev and --prod flags")
        sys.exit(1)
    
    # Create and run generator
    generator = EnvironmentGenerator()
    success = generator.run(args)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()