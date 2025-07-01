#!/usr/bin/env python3
"""
Lusochat LiteLLM Cleanup Script

This script performs a comprehensive cleanup of the LiteLLM deployment, including:
- Docker containers (stopped and removed)
- Docker networks
- Docker images (built locally)
- Temporary files and caches

The script preserves:
- The cloned litellm-upstream repository (can be reused)
- Custom configuration files in .litellm-lusofona/
- Any persistent data volumes (if configured)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import json

# Configuration - matching the deployment script
LITELLM_DIR = "litellm-upstream"
CUSTOM_CONFIG_DIR = ".litellm-lusofona"
PROJECT_NAME = "lusochat-litellm"

def info(message):
    print(f"[INFO] {message}")

def success(message):
    print(f"[SUCCESS] {message}")

def error(message):
    print(f"[ERROR] {message}")

def warning(message):
    print(f"[WARNING] {message}")

def prompt_user(message, default="n"):
    """Prompt user for yes/no confirmation."""
    response = input(f"{message} [y/N]: ").strip().lower()
    response = response if response else default
    return response in ['y', 'yes']

def run_command(command, cwd=None, capture_output=True, check=False):
    """Run a command and handle errors gracefully."""
    if capture_output:
        info(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, cwd=cwd, check=check, capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        if check:
            error(f"Command failed with exit code {e.returncode}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
        return e
    except FileNotFoundError:
        if check:
            error(f"Command not found: {command[0]}")
        return None

def check_docker():
    """Check if Docker is available."""
    result = run_command(["docker", "--version"])
    if result is None or result.returncode != 0:
        error("Docker is not installed or not accessible")
    
    # Check if Docker daemon is running
    result = run_command(["docker", "info"])
    if result.returncode != 0:
        error("Docker daemon is not running")
    
    success("Docker is available and running")

def get_compose_cmd():
    """Get the appropriate docker compose command."""
    # Try docker compose first, then docker-compose
    result = run_command(["docker", "compose", "--version"])
    if result and result.returncode == 0:
        return ["docker", "compose"]
    
    result = run_command(["docker-compose", "--version"])
    if result and result.returncode == 0:
        return ["docker-compose"]
    
    error("Neither 'docker compose' nor 'docker-compose' is available")

def stop_services():
    """Stop all running services."""
    info("Stopping LiteLLM services...")
    
    compose_cmd = get_compose_cmd()
    litellm_dir = Path(LITELLM_DIR)
    
    if not litellm_dir.exists():
        warning(f"LiteLLM directory not found: {LITELLM_DIR}")
        return
    
    # Stop services
    result = run_command(
        compose_cmd + ["-p", PROJECT_NAME, "stop"],
        cwd=litellm_dir,
        capture_output=False
    )
    
    if result and result.returncode == 0:
        success("Services stopped successfully")
    else:
        warning("Some services may not have been running or failed to stop")

def remove_containers():
    """Remove all containers from the project."""
    info("Removing containers...")
    
    compose_cmd = get_compose_cmd()
    litellm_dir = Path(LITELLM_DIR)
    
    if not litellm_dir.exists():
        warning(f"LiteLLM directory not found: {LITELLM_DIR}")
        info("Attempting to remove containers by project name...")
        
        # Try to remove containers by project name even without compose file
        result = run_command(["docker", "ps", "-a", "--filter", f"label=com.docker.compose.project={PROJECT_NAME}", "-q"])
        if result and result.stdout.strip():
            container_ids = result.stdout.strip().split('\n')
            info(f"Found {len(container_ids)} containers to remove")
            
            for container_id in container_ids:
                run_command(["docker", "rm", "-f", container_id], capture_output=False)
            success("Containers removed by project label")
        else:
            info("No containers found with project label")
        return
    
    # Remove containers using docker-compose
    result = run_command(
        compose_cmd + ["-p", PROJECT_NAME, "rm", "-f"],
        cwd=litellm_dir,
        capture_output=False
    )
    
    if result and result.returncode == 0:
        success("Containers removed successfully")
    else:
        warning("Some containers may not exist or failed to remove")

def remove_networks():
    """Remove Docker networks created by the project."""
    info("Removing Docker networks...")
    
    # Get networks with the project name
    result = run_command(["docker", "network", "ls", "--filter", f"name={PROJECT_NAME}", "-q"])
    
    if result and result.stdout.strip():
        network_ids = result.stdout.strip().split('\n')
        info(f"Found {len(network_ids)} networks to remove")
        
        for network_id in network_ids:
            result = run_command(["docker", "network", "rm", network_id])
            if result and result.returncode == 0:
                info(f"Removed network: {network_id}")
            else:
                warning(f"Failed to remove network: {network_id} (may be in use)")
        
        success("Network cleanup completed")
    else:
        info("No project networks found to remove")

def remove_images():
    """Remove Docker images built by the project."""
    info("Checking for project-built images...")
    
    # Look for images with the project name or litellm tags
    patterns = [f"{PROJECT_NAME}", "litellm", "lusochat-litellm"]
    images_to_remove = set()
    
    for pattern in patterns:
        result = run_command(["docker", "images", "--filter", f"reference=*{pattern}*", "-q"])
        if result and result.stdout.strip():
            image_ids = result.stdout.strip().split('\n')
            images_to_remove.update(image_ids)
    
    if images_to_remove:
        info(f"Found {len(images_to_remove)} images to remove")
        
        if prompt_user("Do you want to remove locally built images? This will free up disk space"):
            for image_id in images_to_remove:
                result = run_command(["docker", "rmi", "-f", image_id])
                if result and result.returncode == 0:
                    info(f"Removed image: {image_id}")
                else:
                    warning(f"Failed to remove image: {image_id}")
            success("Image cleanup completed")
        else:
            info("Skipping image removal")
    else:
        info("No project-specific images found")

def cleanup_docker_system():
    """Clean up Docker system (dangling images, unused networks, etc.)."""
    if prompt_user("Do you want to run Docker system cleanup? This will remove dangling images and unused networks"):
        info("Running Docker system cleanup...")
        
        # Remove dangling images
        run_command(["docker", "image", "prune", "-f"], capture_output=False)
        
        # Remove unused networks
        run_command(["docker", "network", "prune", "-f"], capture_output=False)
        
        # Remove unused volumes (be careful with this one)
        if prompt_user("Do you want to remove unused Docker volumes? (This could remove data)"):
            run_command(["docker", "volume", "prune", "-f"], capture_output=False)
        
        success("Docker system cleanup completed")

def cleanup_temp_files():
    """Clean up temporary files and caches."""
    info("Cleaning up temporary files...")
    
    litellm_dir = Path(LITELLM_DIR)
    
    # Clean up files that might have been copied during deployment
    if litellm_dir.exists():
        temp_files = [
            litellm_dir / "config.yaml",
            litellm_dir / "docker-compose.yml", 
            litellm_dir / ".env"
        ]
        
        cleaned = 0
        for temp_file in temp_files:
            if temp_file.exists():
                info(f"Removing copied config: {temp_file.name}")
                temp_file.unlink()
                cleaned += 1
        
        if cleaned > 0:
            success(f"Cleaned up {cleaned} temporary config files")
        else:
            info("No temporary config files found")
    
    # Clean up any log files or caches in the custom config directory
    custom_dir = Path(CUSTOM_CONFIG_DIR)
    if custom_dir.exists():
        logs_dir = custom_dir / "logs"
        if logs_dir.exists() and logs_dir.is_dir():
            if prompt_user("Do you want to clean up log files?"):
                try:
                    shutil.rmtree(logs_dir)
                    logs_dir.mkdir(exist_ok=True)  # Recreate empty logs directory
                    success("Log files cleaned up")
                except Exception as e:
                    warning(f"Failed to clean logs: {e}")

def remove_repository():
    """Remove the cloned upstream repository."""
    litellm_dir = Path(LITELLM_DIR)
    
    if litellm_dir.exists():
        if prompt_user("Do you want to remove the cloned LiteLLM repository? (You can always re-clone it)"):
            info("Removing LiteLLM repository...")
            try:
                shutil.rmtree(litellm_dir)
                success("Repository removed successfully")
            except Exception as e:
                error(f"Failed to remove repository: {e}")
        else:
            info("Keeping LiteLLM repository")
    else:
        info("LiteLLM repository not found (already clean)")

def show_cleanup_summary():
    """Show summary of cleanup actions."""
    info("")
    info("=" * 60)
    info("LUSOCHAT LITELLM CLEANUP COMPLETE")
    info("=" * 60)
    info("Cleanup actions performed:")
    info("  🛑 Stopped all running services")
    info("  🗑️  Removed containers and networks")
    info("  🧹 Cleaned up temporary files")
    info("")
    info("Preserved:")
    info("  📁 Custom configurations in .litellm-lusofona/")
    info("  📁 LiteLLM repository (if you chose to keep it)")
    info("")
    info("To redeploy:")
    info("  python3 deploy_litellm.py")
    info("=" * 60)

def main():
    """Main cleanup function."""
    info("Starting Lusochat LiteLLM cleanup...")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Lusochat LiteLLM Cleanup Script")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")
    parser.add_argument("--keep-images", action="store_true", help="Keep Docker images")
    parser.add_argument("--keep-repo", action="store_true", help="Keep cloned repository")
    parser.add_argument("--deep-clean", action="store_true", help="Perform deep cleanup including Docker system")
    args = parser.parse_args()
    
    # Check Docker availability
    check_docker()
    
    if not args.force:
        if not prompt_user("This will stop and remove all LiteLLM Docker resources. Continue?"):
            info("Cleanup cancelled")
            return
    
    # Core cleanup steps
    stop_services()
    remove_containers()
    remove_networks()
    
    if not args.keep_images:
        remove_images()
    else:
        info("Skipping image removal (--keep-images)")
    
    cleanup_temp_files()
    
    if not args.keep_repo:
        remove_repository()
    else:
        info("Keeping repository (--keep-repo)")
    
    if args.deep_clean:
        cleanup_docker_system()
    
    show_cleanup_summary()
    success("Cleanup completed successfully!")

if __name__ == "__main__":
    main() 