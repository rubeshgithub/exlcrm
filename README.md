# EXL-CRM

Multi-tenant CRM platform for Canadian professional services firms.

## Quick Start

```bash
# 1. Clone and configure
cp backend/.env.example backend/.env
# Edit .env with your credentials

# 2. Start with Docker
cd docker
docker-compose up -d

# 3. Access
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Health: http://localhost:8000/api/v1/health
```

## Tech Stack

- **Backend:** FastAPI + Python 3.12
- **Database:** MongoDB Atlas (Beanie ODM)
- **Cache/Queue:** Redis
- **Storage:** AWS S3 (Montreal)
- **Email:** AWS SES (Montreal)
- **SMS:** InfoBIP
- **e-Signature:** DocuSeal (self-hosted)
- **Deployment:** Docker on OVHcloud QC

## Project Structure

```
exlcrm/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py   # App factory
│   │   ├── config.py # Settings
│   │   ├── database.py
│   │   ├── middleware/
│   │   ├── models/   # Beanie documents
│   │   ├── schemas/  # Pydantic models
│   │   ├── routers/  # API endpoints
│   │   ├── services/ # Business logic
│   │   └── utils/    # Helpers
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Next.js 15 (Phase 5)
├── docker/
│   └── docker-compose.yml
├── nginx/
│   └── exlcrm.conf
└── CONCEPT.md        # Full project documentation
```

## Phase 0 Status

- [x] Project structure
- [x] Config (pydantic-settings)
- [x] MongoDB/Beanie connection
- [x] All 13 models (Tenant, User, Contact, Case, Encounter, Appointment, Communication, Document, FormTemplate, FormSubmission, Workflow, Invoice, AuditLog)
- [x] Schemas (Auth, Tenant, Contact)
- [x] Auth middleware (JWT)
- [x] Tenant middleware (subdomain resolution)
- [x] RBAC system
- [x] Health check endpoints
- [x] Auth routes (register, login, refresh, me, logout)
- [x] Tenant routes
- [x] User routes
- [x] Docker setup
- [x] Nginx config

## Next: Phase 1 — Core CRM

- Contact CRUD with industry-specific fields
- Search, filters, pagination
- Document upload to S3
- AWS SES email service
- InfoBIP SMS service
- Communication hub
