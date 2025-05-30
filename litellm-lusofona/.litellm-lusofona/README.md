# `.litellm-lusofona` Customization Layer for litellm-lusofona

This folder contains all custom configuration, Docker, and orchestration files for running your own fork of the `litellm-lusofona` project, without modifying the main repo code. It enables you to:

- Keep your custom configs, scripts, and compose files separate from upstream code
- Easily sync with the main repo without merge conflicts
- Overlay your own settings, secrets, and deployment logic

## How it works
- **Docker and Compose**: Custom `Dockerfile` and `docker-compose.yml` here use the parent repo as build context, but overlay configs/scripts from `.litellm-lusofona`.
- **Configs**: Place your `config.yaml`, `.env`, and any other custom files here. They will be used by the containers at runtime.
- **No upstream changes**: The main repo code stays untouched, making it easy to pull updates from upstream.

## Usage
1. Place your custom configs (e.g., `config.yaml`, `.env`, `prometheus.yml`) in `.litellm-lusofona`.
2. From inside `.litellm-lusofona`, run:
   ```bash
   docker compose up -d
   ```
   Or, to control resource naming, use:
   ```bash
   docker compose -p litellm-lusofona up -d
   ```
3. The services will build using the main repo code, but with your customizations applied.

## Troubleshooting & Lessons Learned

### License Verification
- The LiteLLM proxy requires a valid license for premium features (like Prometheus metrics).
- Set your license key in `.env` as `LITELLM_LICENSE=your_license_key`.
- The `.env` file must be present in `.litellm-lusofona` and referenced in `docker-compose.yml` via `env_file: - .env`.
- If you see license verification timeouts, check:
  - The license key is correct and present in the environment (use `docker compose exec litellm env | grep LITELLM_LICENSE`).
  - The container has internet access to reach the license server.

### Prometheus Metrics
- Prometheus metrics are only available with a valid LiteLLM Enterprise license.
- If you do not have a license, you will see warnings, but the service will still run.
- To suppress these warnings, remove Prometheus callbacks from your config and related environment variables.

### YAML Errors
- Invalid YAML in `config.yaml` will cause the container to crash with a parser error.
- Always validate your YAML (especially indentation and list syntax) before restarting the service.
- Example error: `expected <block end>, but found '<block sequence start>'` means you likely have a misplaced dash or indentation issue.

### Docker Compose Project Naming & Volumes
- By default, Docker Compose prefixes resources (volumes, networks) with the directory name you run from (e.g., `.litellm-lusofona_`).
- To control this, use the `-p` flag: `docker compose -p litellm-lusofona up -d`.
- Volumes are defined in the compose file, but their actual names are prefixed by the project name.

### File Mounting
- If you mount files from the parent directory (e.g., `../prometheus.yml`), ensure the path is correct relative to `.litellm-lusofona`.
- If a file is missing or the mount path is wrong, the container may fail to start or Prometheus may not load its config.

### General Debugging
- Use `docker logs <container>` to check why a service is failing.
- Use `docker compose exec <service> env` to check environment variables inside the container.
- Use `yamllint` or an online YAML validator to check your config files.

## Notes
- If you want to use the main repo's default setup, run Docker Compose from the repo root instead.
- To sync with upstream, just pull changes in the parent repo; your `.litellm-lusofona` folder is unaffected.
- For more details or to track changes, see `NOTE_MODIFICATIONS.md` (if present).

---

**This setup is ideal for maintaining a clean, up-to-date fork with your own deployment logic and secrets.** 