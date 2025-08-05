# Project Lusochat: CI/CD Pipeline Architecture for Automated OpenWebUI Customization and Deployment

## 1\. Executive Summary

This document outlines a robust, automated Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Lusochat project. The primary goal is to replace the current manual process of customizing OpenWebUI, building a Docker image, and pushing it to Docker Hub.

The proposed solution will automate the entire workflow: fetching the latest OpenWebUI source code, applying Lusochat-specific customizations, building a new Docker image, performing critical validation tests, and securely pushing the verified image to Docker Hub. This architecture is designed to be resilient, maintainable, and self-aware, providing clear notifications on success or failure, thus ensuring that only stable, working images are published.

## 2\. Current State Analysis

The current workflow is split into two effective but disconnected processes:

1.  **Build & Customization (`lusochat-openwebui`):**

      * **Process:** A developer manually clones the `open-webui` repository and executes the `deploy_and_apply_lusochat_customizations.sh` script. This script patches the source code and then triggers a local `docker build`.
      * **Output:** A local Docker image tagged as `lusochat-openwebui:latest`.
      * **Gap:** This process is manual, time-consuming, and lacks automated validation. A successful Docker build does not guarantee a functional application.

2.  **Deployment (`lusochat-deploy`):**

      * **Process:** An administrator manually pushes the locally built image to Docker Hub. On a target server, they use the `lusochat-deploy` scripts (`deploy.sh`, `docker-compose.yml`) to pull this image and run the service.
      * **Output:** A running Lusochat instance.
      * **Gap:** The link between building the image and deploying it is a series of manual `docker tag` and `docker push` commands, which is inefficient and prone to error.

This proposal aims to connect these two phases with a professional, automated pipeline.

## 3\. Proposed CI/CD Pipeline Architecture

We will implement a multi-stage pipeline using a modern CI/CD platform like **GitHub Actions**, which is a natural fit as the source code resides on GitHub. The pipeline will be defined in a YAML file (e.g., `.github/workflows/build-lusochat.yml`) within your repository.

### Pipeline Flow Diagram

```
[Trigger] ---> [Stage 1: Setup] ---> [Stage 2: Build] ---> [Stage 3: Validate] ---> [Stage 4: Push] ---> [Stage 5: Notify]
(Weekly Cron | Manual)                                        |                      |                     (On Success)
                                                              |                      |
                                                              `-----> [Failure] ------> [Stage 5: Notify]
                                                                     (On Failure)
```

## 4\. Deep Dive into Pipeline Stages

### Stage 0: Trigger

The pipeline execution will be initiated by one of two events:

  * **Scheduled Trigger:** A cron job will run automatically on a defined schedule (e.g., every Sunday at 3:00 AM) to ensure the image is always up-to-date with the latest OpenWebUI changes.
  * **Manual Trigger (`workflow_dispatch`):** Allows a developer to manually run the pipeline from the GitHub Actions UI at any time, for on-demand builds or testing.

### Stage 1: Setup & Source Fetch

  * **Objective:** Prepare a clean and consistent build environment.
  * **Process Steps:**
    1.  Provision a fresh virtual runner (e.g., `ubuntu-latest`).
    2.  **Checkout Upstream Code:** Clone the latest version of the official `open-webui` repository at a specific depth (`--depth=1`) for efficiency.
          * `git clone --depth 1 https://github.com/open-webui/open-webui.git ./open-webui-src`
    3.  **Checkout Customization Code:** Checkout your own repository containing the customization scripts and assets (`lusochat-openwebui` folder).
          * This isolates your proprietary logic from the upstream code, a crucial best practice.

### Stage 2: Customization & Build

  * **Objective:** Apply your customizations and build the Docker image.
  * **Process Steps:**
    1.  **Execute Customization Script:** Run your `deploy_and_apply_lusochat_customizations.sh` script against the checked-out `open-webui-src` directory. The script's existing safety checks (backups, content validation) are valuable here.
    2.  **Build Docker Image:** Use the `docker build` command within the customized source directory to create the image.
          * **Tagging Strategy:** Tag the image with a unique identifier for this specific pipeline run (e.g., `lusochat-openwebui:ci-${{ github.run_id }}`). This temporary tag is used for validation in the next stage.
    3.  **Leverage Caching:** Utilize the CI/CD platform's Docker layer caching to significantly speed up subsequent builds.

### Stage 3: Validation & Smoke Testing (Critical Stage)

  * **Objective:** Verify that the newly built image is not just buildable, but **functional**. This prevents pushing broken images.
  * **Process Steps:**
    1.  **Run Container in CI:** In the pipeline runner, start a container from the newly built image (`lusochat-openwebui:ci-${{ github.run_id }}`). Expose its port internally (e.g., map container port 8080 to host port 8080 on the runner).
    2.  **Health Check:** Wait for the application to become healthy. Poll the health check endpoint defined in your `docker-compose.yml` (e.g., `curl --fail http://localhost:8080/healthz`) until it returns a success code (HTTP 200). Implement a timeout to prevent infinite loops.
    3.  **Functional Verification:** Once healthy, perform a series of automated "smoke tests":
          * **Branding Check:** `curl http://localhost:8080 | grep "Lusochat"`. This simple command checks if your custom branding was correctly injected into the main page's HTML.
          * **Asset Check:** Attempt to `curl` the path to a critical custom asset, like the favicon (e.g., `http://localhost:8080/favicon.ico`), and verify the response is HTTP 200.
          * **Login Page Check:** `curl` the login page and `grep` for a custom string you've injected (e.g., a custom placeholder for the Lusófona email).
    4.  **Teardown:** Stop and remove the temporary container regardless of the test outcome.
  * **Outcome:** If any of these validation steps fail, the entire pipeline fails immediately. It will **not** proceed to the push stage.

### Stage 4: Tagging & Push to Docker Hub

  * **Objective:** Tag the validated image correctly and publish it.
  * **Process Steps:**
    1.  **Login to Docker Hub:** Use encrypted secrets stored in the CI/CD platform (e.g., GitHub Secrets) to securely log in to your Docker Hub account (`fabiolx`).
          * `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
    2.  **Re-tag the Validated Image:** If Stage 3 passed, re-tag the temporary image (`lusochat-openwebui:ci-${{ github.run_id }}`) with the final tags:
          * **Latest Tag:** `fabiolx/lusochat-openwebui:latest`
          * **Version Tag (Recommended):** `fabiolx/lusochat-openwebui:v$(date +%Y.%m.%d)-${{ github.run_id }}`. This creates a versioned, immutable tag (e.g., `v2025.08.05-12345`) which is invaluable for rollbacks and debugging.
    3.  **Push Images:** Push both the `latest` and the versioned tags to Docker Hub.

### Stage 5: Notification & Reporting

  * **Objective:** Inform stakeholders about the outcome of the pipeline.
  * **Process Steps:**
    1.  **On Success:** Send a notification to a designated channel (e.g., email, Slack, Discord webhook) with a message like:
        > ✅ **SUCCESS:** Lusochat image `v2025.08.05-12345` built and pushed successfully to `fabiolx/lusochat-openwebui`.
    2.  **On Failure:** Send a more urgent notification with details about the failure.
        > ❌ **FAILURE:** Lusochat build failed at stage: **[Validation]**. Please review the pipeline logs: [Link to GitHub Actions Run]

## 5\. Recommended Technology Stack (GitHub Actions)

  * **CI/CD Platform:** **GitHub Actions**
  * **Workflow File:** `.github/workflows/build-lusochat.yml`
  * **Key Actions:**
      * `actions/checkout@v4`: To check out your repositories.
      * `docker/login-action@v3`: To securely log in to Docker Hub.
      * `docker/build-push-action@v5`: A powerful action that can handle building, tagging, caching, and pushing in one step.
      * **Custom Scripts:** Your existing bash scripts will be called directly using `run` steps.
  * **Secrets Management:** **GitHub Encrypted Secrets** for storing your Docker Hub token.

## 6\. Closing the Loop: Automating Deployment

The pipeline above automates the **build** process. The next logical step is to automate the **deployment** on your servers.

  * **Recommendation: Use Watchtower**
      * **Watchtower** is a lightweight container that runs on your server and monitors your running Docker containers.
      * When it detects that the `fabiolx/lusochat-openwebui:latest` image has been updated on Docker Hub, it will automatically pull the new image and gracefully restart your `lusochat-openwebui` service with the new version.
      * This creates a true end-to-end, "Git-to-Production" pipeline with minimal manual intervention.

## 7\. Summary & Next Steps

By adopting this CI/CD architecture, you will transform your current manual process into a professional, resilient, and efficient automation system.

1.  **Create a dedicated repository** for your customization scripts (`lusochat-openwebui`) and deployment configurations (`lusochat-deploy`).
2.  **Implement the GitHub Actions workflow** (`.github/workflows/build-lusochat.yml`) within that repository.
3.  **Configure GitHub Secrets** with your Docker Hub credentials.
4.  **Start by implementing Stages 1 and 2.** Ensure the image builds correctly in the CI environment.
5.  **Incrementally add Stage 3 (Validation).** This is the most critical step for ensuring stability.
6.  **Finally, add Stages 4 and 5** to push the image and send notifications.
7.  **Consider deploying Watchtower** on your servers for a fully automated deployment cycle.