#!/usr/bin/env python3
"""
Lusochat LiteLLM Deployment Script

Similar to the Open WebUI shell script, this automates deployment of 
LiteLLM with custom Lusófona configurations.

The approach:
1. Clone upstream LiteLLM repo (like the shell script clones Open WebUI)
2. Copy our custom configs from .litellm-lusofona/
3. Build and deploy with Docker
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse

# Configuration
LITELLM_GIT_URL = "https://github.com/BerriAI/litellm.git"
LITELLM_DIR = "litellm-upstream"
CUSTOM_CONFIG_DIR = ".litellm-lusofona"

def info(message):
    print(f"[INFO] {message}")

def success(message):
    print(f"[SUCCESS] {message}")

def error(message):
    print(f"[ERROR] {message}")
    sys.exit(1)

def warning(message):
    print(f"[WARNING] {message}")

def prompt_user(message, default="n"):
    """Prompt user for yes/no confirmation."""
    response = input(f"{message} [y/N]: ").strip().lower()
    response = response if response else default
    return response in ['y', 'yes']

def run_command(command, cwd=None):
    """Run a command and handle errors."""
    info(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        error(f"Command failed with exit code {e.returncode}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        sys.exit(1)

def check_tool(tool):
    """Check if a tool is available."""
    try:
        subprocess.run([tool, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def cleanup_and_clone():
    """Handle existing directory and clone fresh LiteLLM."""
    if Path(LITELLM_DIR).exists():
        warning(f"LiteLLM directory already exists: {LITELLM_DIR}")
        if prompt_user("Do you want to remove it and clone fresh?"):
            info("Removing existing LiteLLM directory...")
            shutil.rmtree(LITELLM_DIR)
            success("Cleanup complete.")
        else:
            info("Using existing LiteLLM directory...")
            return

    info("Cloning LiteLLM repository...")
    run_command(["git", "clone", "--depth", "1", LITELLM_GIT_URL, LITELLM_DIR])
    success("LiteLLM repository cloned successfully.")

def copy_custom_configs():
    """Copy our custom configurations to the LiteLLM directory."""
    info("Copying custom configurations...")
    
    custom_dir = Path(CUSTOM_CONFIG_DIR)
    litellm_dir = Path(LITELLM_DIR)
    
    if not custom_dir.exists():
        error(f"Custom config directory not found: {CUSTOM_CONFIG_DIR}")
    
    # Check if .env exists, if not, warn user to create from env.example
    env_file = custom_dir / ".env"
    if not env_file.exists():
        env_example = custom_dir / "env.example"
        if env_example.exists():
            warning(f".env file not found! Please copy {env_example} to {env_file} and configure it.")
            if not prompt_user("Continue without .env file? (Not recommended for production)"):
                error("Deployment cancelled. Please create .env file first.")
        else:
            warning(".env and env.example not found - deployment may fail")
    
    # Files to copy from custom config
    config_files = ["config.yaml", "docker-compose.yml", ".env"]
    
    copied = 0
    for file_name in config_files:
        source = custom_dir / file_name
        dest = litellm_dir / file_name
        
        if source.exists():
            shutil.copy2(source, dest)
            success(f"Copied {file_name}")
            copied += 1
        else:
            warning(f"File not found: {file_name} (skipping)")
    
    # Copy directory structures for modular configuration
    directories_to_copy = ["models", "settings"]
    
    for dir_name in directories_to_copy:
        source_dir = custom_dir / dir_name
        dest_dir = litellm_dir / dir_name
        
        if source_dir.exists() and source_dir.is_dir():
            # Remove destination directory if it exists
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            # Copy the entire directory
            shutil.copytree(source_dir, dest_dir)
            success(f"Copied {dir_name}/ directory")
            copied += 1
        else:
            warning(f"Directory not found: {dir_name}/ (skipping)")
    
    # Also copy prometheus.yml from upstream repo to the same directory as docker-compose.yml
    prometheus_source = litellm_dir / "prometheus.yml" 
    prometheus_dest = litellm_dir / "prometheus.yml"  # It's already there from clone
    if prometheus_source.exists():
        success("prometheus.yml already available from upstream")
        copied += 1
    else:
        warning("prometheus.yml not found in upstream repo")
    
    info(f"Configuration copying complete: {copied} files/directories copied")

def build_and_deploy():
    """Build Docker image and deploy services."""
    litellm_dir = Path(LITELLM_DIR)
    
    # Check if docker-compose.yml exists
    compose_file = litellm_dir / "docker-compose.yml"
    if not compose_file.exists():
        error("docker-compose.yml not found in LiteLLM directory")
    
    info("Building and deploying services...")
    
    # Try docker compose first, then docker-compose
    compose_cmd = ["docker", "compose"]
    try:
        subprocess.run(compose_cmd + ["--version"], cwd=litellm_dir, check=True, capture_output=True)
    except:
        compose_cmd = ["docker-compose"]
        subprocess.run(compose_cmd + ["--version"], cwd=litellm_dir, check=True, capture_output=True)
    
    # Deploy with project name - let output stream to console
    deploy_command = compose_cmd + ["-p", "lusochat-litellm", "up", "-d", "--build"]
    info(f"Running: {' '.join(deploy_command)}")
    
    result = subprocess.run(deploy_command, cwd=litellm_dir)
    if result.returncode != 0:
        error(f"Docker deployment failed with exit code {result.returncode}")
    
    success("Services deployed successfully!")

def show_deployment_info():
    """Show information about deployed services."""
    info("")
    info("=" * 60)
    info("LUSOCHAT LITELLM DEPLOYMENT COMPLETE")
    info("=" * 60)
    info("Services available:")
    info("  🤖 LiteLLM Proxy: http://localhost:4000")
    info("  📊 Grafana: http://localhost:3001 (admin/admin)")
    info("  📈 Prometheus: http://localhost:9090")
    info("")
    info("Useful commands:")
    info("  📋 Check status: docker compose -p lusochat-litellm ps")
    info("  📋 View logs: docker compose -p lusochat-litellm logs -f")
    info("  🛑 Stop: docker compose -p lusochat-litellm down")
    info("=" * 60)

def update_config():
    """Update configuration in running containers without full redeployment."""
    info("Updating LiteLLM configuration...")
    
    # Check if services are running
    try:
        result = subprocess.run(
            ["docker", "compose", "-p", "lusochat-litellm", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        if "litellm" not in result.stdout:
            error("LiteLLM service is not running. Please start it first.")
    except subprocess.CalledProcessError:
        error("Failed to check service status")

    try:
        # Stop the litellm service first
        info("Stopping LiteLLM service...")
        subprocess.run(
            ["docker", "compose", "-p", "lusochat-litellm", "stop", "litellm"],
            check=True
        )
        success("Service stopped")

        # Copy the config file and modular directories to the litellm-upstream directory
        info("Updating configuration files and directories...")
        
        # Copy main config file
        source_config = Path(CUSTOM_CONFIG_DIR) / "config.yaml"
        target_config = Path(LITELLM_DIR) / "config.yaml"
        shutil.copy2(source_config, target_config)
        success("Main configuration file updated")
        
        # Copy modular directories
        custom_dir = Path(CUSTOM_CONFIG_DIR)
        litellm_dir = Path(LITELLM_DIR)
        
        directories_to_copy = ["models", "settings"]
        for dir_name in directories_to_copy:
            source_dir = custom_dir / dir_name
            dest_dir = litellm_dir / dir_name
            
            if source_dir.exists() and source_dir.is_dir():
                # Remove destination directory if it exists
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                # Copy the entire directory
                shutil.copytree(source_dir, dest_dir)
                success(f"Updated {dir_name}/ directory")
            else:
                warning(f"Directory not found: {dir_name}/ (skipping)")

        # Start the litellm service again
        info("Starting LiteLLM service...")
        subprocess.run(
            ["docker", "compose", "-p", "lusochat-litellm", "start", "litellm"],
            check=True
        )
        success("Configuration update complete!")
    except subprocess.CalledProcessError as e:
        error(f"Failed to update configuration: {str(e)}")
        # Try to start the service again if it was stopped
        info("Attempting to restart service in case of failure...")
        subprocess.run(
            ["docker", "compose", "-p", "lusochat-litellm", "start", "litellm"],
            check=False
        )
    except Exception as e:
        error(f"Failed to update configuration: {str(e)}")
        # Try to start the service again if it was stopped
        info("Attempting to restart service in case of failure...")
        subprocess.run(
            ["docker", "compose", "-p", "lusochat-litellm", "start", "litellm"],
            check=False
        )

def main():
    """Main deployment function."""
    info("Starting Lusochat LiteLLM deployment...")
    
    # Check required tools
    info("Checking required tools...")
    required_tools = ["git", "docker"]
    for tool in required_tools:
        if not check_tool(tool):
            error(f"{tool} is not installed or not accessible")
    
    success("All required tools found")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Lusochat LiteLLM Deployment Script")
    parser.add_argument("--update-config", action="store_true", help="Only update configuration without full redeployment")
    args = parser.parse_args()
    
    if args.update_config:
        update_config()
        return
    
    # Main deployment steps
    cleanup_and_clone()
    copy_custom_configs()
    
    if prompt_user("Do you want to build and deploy now?", "y"):
        build_and_deploy()
        show_deployment_info()
    else:
        info("Skipping deployment. To deploy later, run:")
        info(f"  cd {LITELLM_DIR}")
        info("  docker compose -p lusochat-litellm up -d --build")

if __name__ == "__main__":
    main() 