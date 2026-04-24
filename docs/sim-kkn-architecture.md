# SIM-KKN Enterprise Architecture Guide

This document outlines the high-level architecture of the SIM-KKN (Sistem Informasi Manajemen Kuliah Kerja Nyata) ecosystem. It serves as the primary technical context for AI and developer onboarding.

## 1. System Overview
SIM-KKN is a containerized microservices platform designed to orchestrate the lifecycle of university community service programs.

- **Frontend:** SvelteKit + Tailwind CSS (SSR & Client Hydration).
- **Backend:** FastAPI (Python 3.11) following MVC + Service/Repository patterns.
- **Database:** PostgreSQL 16.
- **Authentication:** Keycloak (OIDC/OAuth 2.0).
- **Caching:** Redis 7.
- **Storage:** MinIO (S3-Compatible Object Storage).

## 2. Microservices Interconnectivity
- The **Frontend** accesses the **FastAPI Backend** exclusively via REST endpoints.
- Authentication flows are handled by **Keycloak**. Tokens are verified by the FastAPI middleware using public keys.
- **Redis** is utilized for session management, API rate limiting, and background task queuing (via Celery/RQ).
- **MinIO** is used for uploading and serving Logbook attachments, student profile pictures, and PDF reports.

## 3. Docker Compose Orchestration
The entire stack is orchestrated using `docker-compose.yaml`.
**Key constraints:**
- Keycloak runs on port `8080` (or `8081` to avoid conflicts).
- PostgreSQL runs on `5432` with mapped volumes to prevent data loss.
- Antigravity IDE (Open WebUI) maps to `3013`.

## 4. Operational Boundaries
- The `/legacy` and `/config` directories are highly restricted and must not be modified without explicit lead architect approval.
- All database migrations must be performed using Alembic. Direct SQL injections to production schemas are strictly forbidden.
