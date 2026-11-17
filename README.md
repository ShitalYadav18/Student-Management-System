# Student Management System – Docker & CI/CD

A small Flask + MySQL application demonstrating:
- Experiment 14: multi-container application using Docker Compose.
- Experiment 15: GitHub Actions CI/CD pipeline with test, Docker build and SSH deployment.

## Requirements

- Docker Desktop (Windows/macOS) or Docker Engine + Compose plugin (Linux)
- Git
- GitHub account

## Run locally (Experiment 14)

1. Open a terminal in this project directory.
2. Start both containers:

   ```bash
   docker compose up -d --build
   ```

3. Open http://localhost:5000
4. Add student records and verify they appear in the table.
5. Check running containers:

   ```bash
   docker compose ps
   ```

6. View logs:

   ```bash
   docker compose logs -f
   ```

7. Stop containers:

   ```bash
   docker compose down
   ```

The MySQL data is stored in the named volume `mysql_data`, so normal container recreation does not remove it. To delete the database volume too, use `docker compose down -v`.

## Experiment 15: GitHub Actions CI/CD

1. Create a GitHub repository named `Student-Management-System`.
2. Push this project to the repository's `main` branch.
3. Open the repository's **Actions** tab.
4. The workflow `.github/workflows/ci-cd.yml` runs:
   - Checkout source code
   - Install Python dependencies
   - Run pytest
   - Validate Docker Compose configuration
   - Build the Docker image
   - Deploy on an Ubuntu server after a push to `main`

### Configure deployment (optional, for a real server)

The CI and Docker build stages work without deployment secrets. To enable the deploy job:

1. Arrange an Ubuntu VPS/server with Docker Engine and the Docker Compose plugin.
2. Clone this repository on the server, for example in `/home/ubuntu/Student-Management-System`.
3. Ensure the SSH user can run Docker commands and pull the repository.
4. In GitHub, open **Settings → Secrets and variables → Actions → New repository secret**.
5. Add these secrets:
   - `DEPLOY_HOST`: server IP or hostname
   - `DEPLOY_USER`: SSH username
   - `DEPLOY_SSH_KEY`: private SSH key for that user
   - `DEPLOY_PATH`: absolute path of the cloned repository on the server
6. Push a new commit to `main`. GitHub Actions will test, build and then run `git pull` and `docker compose up -d --build` on the server.

If deployment secrets are not configured, the deployment step is skipped; the test-and-build job still runs successfully. For a classroom demo, you can demonstrate the complete local Docker Compose experiment and the GitHub Actions test/build stages without a VPS.

## Useful commands

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f web
docker compose logs -f db
docker compose down
```

## Notes

- The default database passwords in `docker-compose.yml` are for local demonstration only. Change them before any public deployment; use GitHub secrets and a server-side environment file for production.
- Do not commit real passwords or private SSH keys to GitHub.
- The `/health` endpoint is used by the CI test and returns `{"status":"ok"}`.
