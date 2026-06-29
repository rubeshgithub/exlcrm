# EXL-CRM — Multi-Tenant CRM Platform

## Multi-Industry · RCIC-Aligned · Healthcare-Ready

---

**Version:** 1.1  
**Date:** June 2026  
**Author:** EXL-CRM Team  
**Status:** Pre-Development (Concept Finalized)  
**Domain:** exlcrm.com

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Tech Stack](#3-tech-stack)
4. [Data Residency & Compliance](#4-data-residency--compliance)
5. [Cost Analysis](#5-cost-analysis)
6. [Pricing Strategy](#6-pricing-strategy)
7. [Core Concept: Shared Core + Industry Modules](#7-core-concept-shared-core--industry-modules)
8. [RBAC Permission Matrix](#8-rbac-permission-matrix)
9. [Form Builder + e-Signature Flow](#9-form-builder--e-signature-flow)
10. [3rd Party Integrations](#10-3rd-party-integrations)
11. [Development Phases](#11-development-phases)
12. [MongoDB Collections](#12-mongodb-collections)
13. [Project Structure](#13-project-structure)
14. [Python Dependencies](#14-python-dependencies)
15. [Environment Variables](#15-environment-variables)
16. [Docker Compose](#16-docker-compose)
17. [VPS Requirements](#17-vps-requirements)
18. [Competitive Landscape](#18-competitive-landscape)
19. [Open Questions (Resolved)](#19-open-questions-resolved)
20. [Next Steps](#20-next-steps)

---

## 1. Executive Summary

EXL-CRM is a unified multi-tenant CRM platform designed for Canadian professional services firms. Starting with **Immigration & Recruitment** (RCIC-compliant) and **Healthcare** (clinic management), the platform maximizes shared infrastructure while keeping industry-specific features modular.

The platform is deployed on a Canadian VPS (OVHcloud QC) with MongoDB Atlas (Toronto), AWS services (Montreal), and InfoBIP for SMS — ensuring all data resides in Canada.

---

## 2. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    NEXUS CRM ARCHITECTURE                          │
│                                                                    │
│   CANADA (AWS Montreal - ca-central-1)                            │
│   ┌───────────────────────────────────────────────────────────┐  │
│   │  AWS S3 (Documents)  │  AWS SES (Email)                    │  │
│   │  Encrypted AES-256    │  SPF/DKIM/DMARC                    │  │
│   └────────────────────────────┬──────────────────────────────┘  │
│                                │                                   │
│   MONGODB ATLAS (Toronto)      │                                   │
│   ┌────────────────────────────┼──────────────────────────────┐  │
│   │  MongoDB 7 (Database)      │                               │  │
│   │  Encrypted at rest         │                               │  │
│   └────────────────────────────┼──────────────────────────────┘  │
│                                │                                   │
│   OVHcloud VPS (Beauharnois QC)                                   │
│   ┌────────────────────────────┼──────────────────────────────┐  │
│   │  FastAPI (Backend)         │                               │  │
│   │  Next.js 15 (Frontend)     │                               │  │
│   │  DocuSeal (e-Sign)         │                               │  │
│   │  Celery + Redis (Queue)    │                               │  │
│   │  Nginx (Reverse Proxy)     │                               │  │
│   │  Uptime Kuma (Monitoring)  │                               │  │
│   └───────────────────────────────────────────────────────────┘  │
│                                                                    │
│   GLOBAL (API-only, no PII stored)                                │
│   ┌───────────────────────────────────────────────────────────┐  │
│   │  InfoBIP (SMS) — no PII stored                           │  │
│   └───────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Tech Stack

| Layer | Technology | Version | Hosting | Region |
|-------|-----------|---------|---------|--------|
| Backend | FastAPI + Python | 3.12+ | OVHcloud VPS | Beauharnois, QC |
| Frontend | Next.js + TypeScript | 15 | OVHcloud VPS | Beauharnois, QC |
| UI Framework | Tailwind CSS + shadcn/ui | 4+ | OVHcloud VPS | Beauharnois, QC |
| Database | MongoDB Atlas | 7.0 | MongoDB Cloud | Toronto, Canada |
| Document Storage | AWS S3 | — | AWS | Montreal (ca-central-1) |
| Email | AWS SES | — | AWS | Montreal (ca-central-1) |
| SMS | InfoBIP | — | Infobip Cloud | Global (API-only) |
| e-Signature | DocuSeal | Latest | OVHcloud VPS | Beauharnois, QC |
| Queue/Cache | Celery + Redis | 5.4 / 7 | OVHcloud VPS | Beauharnois, QC |
| Web Server | Nginx | Latest | OVHcloud VPS | Beauharnois, QC |
| Deployment | Docker + Compose | 24+ | OVHcloud VPS | Beauharnois, QC |
| Monitoring | Uptime Kuma | 1 | OVHcloud VPS | Beauharnois, QC |

---

## 4. Data Residency & Compliance

| Regulation | Requirement | Solution |
|------------|-------------|----------|
| PHIPA (Ontario) | Health info must be protected | All data in Canadian datacenters |
| PIPEDA | Personal info stored in Canada preferred | All servers in Canada |
| RCIC Code of Conduct | Client records must be safeguarded | Encrypted, auditable storage |
| Quebec Law 25 | Strict privacy for Quebec residents | Quebec-based VPS |
| US CLOUD Act avoidance | Avoid US jurisdiction | OVHcloud (French) + AWS Canada regions |

---

## 5. Cost Analysis (50 Tenants)

| Service | Monthly Cost (CAD) | Per-Tenant |
|---------|-------------------|------------|
| OVHcloud VPS (4vCPU/8GB) | $62 | $1.24 |
| MongoDB Atlas (M10, Toronto) | $77 | $1.54 |
| AWS S3 (100GB) | $3 | $0.06 |
| AWS SES (50K emails) | $2 | $0.04 |
| InfoBIP SMS (average) | $100 | $2.00 |
| Domain + SSL | $10 | $0.20 |
| **Total** | **~$254/month** | **~$5.08/tenant** |

**Revenue:** $149-499/mo per tenant × 50 tenants = **$7,450-$24,950/month**  
**Gross margin:** 95-97%

---

## 6. Pricing Strategy

**Model: Tiered Per-Tenant** (recommended over per-seat for professional services)

| Tier | Price | Target | Limits |
|------|-------|--------|--------|
| **Starter** | $149/mo | Solo practitioner | 2 users, 500 contacts, 100 SMS/mo |
| **Professional** | $299/mo | Small firm | 8 users, 5,000 contacts, 500 SMS/mo |
| **Enterprise** | $499/mo | Growing practice | Unlimited users/contacts, API access |

**Why tiered per-tenant:**
- Predictable MRR
- Easy to understand ("$299/month, period")
- Natural upsell path (Starter → Pro when they hire)
- No per-seat nickel-and-diming

---

## 7. Core Concept: Shared Core + Industry Modules

### 7.1 Shared Core (Both Industries)

| Module | Description |
|--------|-------------|
| Tenant Management | Multi-tenant onboarding, white-label, subdomain, billing, subscription plans |
| Admin Portal | Create/manage Admins, Supervisors, Users with RBAC |
| Contact Management | Unified "contacts" entity with industry-specific fields in embedded document |
| Communication Hub | Unified inbox: logs for all calls, SMS, emails with templates |
| Appointment/Scheduling | Calendar, booking, reminders — configurable per industry |
| Document Management | Upload to S3, organize, version control, templates |
| e-Signature Integration | DocuSeal: send & receive signed documents |
| Workflow Engine | Automated task sequences, status pipelines, triggers |
| Reporting & Analytics | Dashboards, exportable reports, KPI tracking |
| Notifications Engine | Push, in-app, SMS, email — configurable triggers |
| Compliance & Audit Log | Full action logging, data retention policies |
| Billing & Stripe | Subscription management, per-tenant invoicing |
| Client Portal | Self-service portal for applicants/patients |
| API Layer | RESTful API for 3rd party integrations |

### 7.2 Immigration Module (RCIC-Aligned)

| Feature | Details |
|---------|---------|
| Applicant Profile | Personal info, passport, education, work history, language scores, family composition |
| Case Management | Status pipeline: Intake → Doc Collection → Application → Submission → Decision |
| RCIC Credential Tracking | RCIC number, college membership, expiry dates, compliance reminders |
| Program Eligibility | Express Entry, PNP, LMIA, Study/Work Permit — configurable scoring |
| Document Checklist | Per-program checklist with mandatory/optional docs, expiry tracking |
| Consultation Notes | Session logging linked to applicant — RCIC-compliant record keeping |
| LOA/LOE Tracking | Letters of Acceptance, Letters of Explanation management |
| Submission Packaging | Auto-generate submission-ready PDF packages |
| Fee Tracking | Fee schedules, retainer tracking, payment milestones |

### 7.3 Healthcare Module (Clinic Management)

| Feature | Details |
|---------|---------|
| Patient Profile | Demographics, insurance, medical history, allergies, medications |
| Appointment Booking | Online self-booking, front-desk booking, recurring appointments, waitlist |
| Call/VoIP Management | Call logging, call recording (consent-based), call queue |
| SMS/Email Reminders | Appointment reminders, follow-ups, recall campaigns, bulk messaging |
| Form Templates Builder | Drag-and-drop form creator |
| e-Signature for Forms | Email form → Patient signs → Auto-attached to record |
| Clinical Notes | SOAP notes, progress notes, treatment plans |
| Recall & Follow-up | Automated recall campaigns for overdue patients |
| Provider Scheduling | Multi-provider calendars, breaks, availability rules |
| Inventory/Supplies | Basic clinic supply tracking |

---

## 8. RBAC Permission Matrix

| Action | Super Admin | Tenant Admin | Supervisor | User |
|--------|-------------|--------------|------------|------|
| Manage platform settings | ✅ | ❌ | ❌ | ❌ |
| Manage tenant users | ❌ | ✅ | ❌ | ❌ |
| Manage roles & permissions | ❌ | ✅ | ❌ | ❌ |
| View all tenant data | ❌ | ✅ | ✅ | Own records |
| Edit records | ❌ | ✅ | ✅ | Own records |
| Delete records | ❌ | ✅ | ✅ | ❌ |
| Send SMS/Email | ❌ | ✅ | ✅ | ✅ |
| Manage forms | ❌ | ✅ | ✅ | ❌ |
| Billing access | ❌ | ✅ | ❌ | ❌ |
| Export data | ❌ | ✅ | ✅ | ❌ |
| View audit logs | ❌ | ✅ | ✅ | ❌ |
| Manage workflows | ❌ | ✅ | ✅ | ❌ |

---

## 9. Form Builder + e-Signature Flow

```
1. Admin creates form template (drag & drop builder)
2. Template saved with field definitions to MongoDB
3. Admin sends form via email (AWS SES) to Applicant/Patient
4. Recipient clicks secure link → fills form → e-signs (DocuSeal embedded)
5. Form submitted → PDF generated → auto-attached to contact record
6. Notification sent to assigned user + audit log entry created
```

---

## 10. 3rd Party Integrations

| Service | Purpose | SDK/Library | Integration |
|---------|---------|-------------|-------------|
| AWS S3 | Document storage | boto3 | Async upload/download |
| AWS SES | Email delivery | boto3 | Raw emails + templates |
| InfoBIP | SMS messaging | httpx | Async REST API |
| DocuSeal | e-Signatures | httpx | Docker + REST API |
| Stripe | Billing/subscriptions | stripe-python | Webhooks + API |
| MongoDB Atlas | Database | Beanie (motor) | Async ODM |
| Twilio (backup) | Alternative SMS | httpx | REST API |

---

## 11. Development Phases

### Phase 0: Foundation (Week 1-2)
- [ ] Project scaffolding, config, environment setup
- [ ] MongoDB/Beanie async connection
- [ ] Docker Compose setup (backend, frontend, Redis, Nginx, DocuSeal)
- [ ] Tenant model + subdomain middleware
- [ ] User model + JWT auth (register, login, refresh)
- [ ] RBAC system (roles, permissions, decorators)
- [ ] Health check endpoints

### Phase 1: Core CRM (Week 3-5)
- [ ] Contact CRUD (base + flexible industry_fields)
- [ ] Search, filters, pagination
- [ ] Document upload to S3 (presigned URLs)
- [ ] AWS SES email service + templates
- [ ] InfoBIP SMS service
- [ ] Communication hub (unified log)
- [ ] Activity/notes timeline

### Phase 2: Immigration Module (Week 6-7)
- [ ] Case model with status pipeline
- [ ] RCIC credential tracking with expiry alerts
- [ ] Document checklist per program
- [ ] Program eligibility scoring (CRS calculator)
- [ ] IRCC processing time benchmarks
- [ ] Submission PDF packaging

### Phase 3: Healthcare Module (Week 8-9)
- [ ] Patient profile + health fields
- [ ] Appointment scheduling (both industries)
- [ ] SMS/Email reminders (InfoBIP + SES)
- [ ] Form template builder (drag & drop)
- [ ] Form submission flow + DocuSeal e-signature
- [ ] Clinical notes (SOAP format)

### Phase 4: Admin Portal + Client Portal (Week 10-11)
- [ ] User management (CRUD, invite, deactivate)
- [ ] Tenant settings + white-label (custom branding)
- [ ] Client portal (applicant/patient self-service)
- [ ] Stripe billing integration (subscriptions, invoices)
- [ ] Subscription plan enforcement

### Phase 5: Frontend + Polish (Week 12-13)
- [ ] Next.js dashboard layout + navigation
- [ ] Contact list/detail pages with data tables
- [ ] Dashboard with KPI widgets
- [ ] Reports + CSV/PDF export
- [ ] Responsive design verification (mobile + tablet)
- [ ] Error boundaries + loading states

---

## 12. MongoDB Collections

```
exlcrm (database)

├── tenants
│   { _id, name, industry, subdomain, plan, settings, created_at }
│
├── users
│   { _id, tenant_id, email, hashed_password, role, permissions, profile,
│     is_active, last_login, created_at }
│
├── contacts
│   { _id, tenant_id, industry, first_name, last_name, email, phone,
│     address, industry_fields{}, tags, assigned_to, created_by, created_at }
│
├── cases (Immigration)
│   { _id, tenant_id, contact_id, case_type, status, stage,
│     rcic_number, program, documents[], timeline[], notes[],
│     assigned_to, created_at }
│
├── encounters (Healthcare)
│   { _id, tenant_id, contact_id, provider_id, date, type,
│     soap_notes, diagnosis, treatment, status, created_at }
│
├── appointments (both industries)
│   { _id, tenant_id, contact_id, scheduled_at, duration,
│     type, status, reminders_sent[], notes, created_at }
│
├── communications
│   { _id, tenant_id, contact_id, type (call/sms/email), direction,
│     subject, content, attachments[], sent_at, sent_by, created_at }
│
├── documents
│   { _id, tenant_id, contact_id, filename, s3_key, mime_type,
│     size, signature_status, signers[], signed_at, uploaded_by, created_at }
│
├── form_templates
│   { _id, tenant_id, name, industry, fields[], is_active,
│     created_by, created_at }
│
├── form_submissions
│   { _id, tenant_id, template_id, contact_id, responses{},
│     signature_request_id (DocuSeal), signature_status,
│     submitted_pdf_s3_key, submitted_at, created_at }
│
├── workflows
│   { _id, tenant_id, name, trigger, actions[], is_active,
│     created_by, created_at }
│
├── invoices
│   { _id, tenant_id, contact_id, stripe_invoice_id, amount,
│     currency, status, due_date, paid_at, created_at }
│
└── audit_logs
    { _id, tenant_id, user_id, action, entity, entity_id,
      changes{}, ip_address, user_agent, timestamp }
```

**Key Design Decision:** `contacts` uses `industry_fields{}` as an embedded document for industry-specific data. This avoids ALTER TABLE migrations and keeps the flexible schema benefit of MongoDB.

---

## 13. Project Structure

```
exlcrm/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app factory + lifespan
│   │   ├── config.py                   # Settings (pydantic-settings)
│   │   ├── database.py                 # MongoDB/Beanie connection
│   │   │
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── tenant.py              # Tenant resolution from subdomain
│   │   │   └── auth.py                # JWT validation + current user
│   │   │
│   │   ├── models/                      # Beanie Document models
│   │   │   ├── __init__.py
│   │   │   ├── tenant.py
│   │   │   ├── user.py
│   │   │   ├── contact.py
│   │   │   ├── case.py
│   │   │   ├── encounter.py
│   │   │   ├── appointment.py
│   │   │   ├── communication.py
│   │   │   ├── document.py
│   │   │   ├── form_template.py
│   │   │   ├── form_submission.py
│   │   │   ├── workflow.py
│   │   │   ├── invoice.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/                     # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── tenant.py
│   │   │   ├── user.py
│   │   │   └── contact.py
│   │   │
│   │   ├── routers/                     # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                 # /api/v1/auth/*
│   │   │   ├── tenants.py              # /api/v1/tenants/*
│   │   │   ├── users.py                # /api/v1/users/*
│   │   │   ├── health.py               # /api/v1/health
│   │   │   └── __init__.py             # Router aggregator
│   │   │
│   │   ├── services/                    # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── tenant_service.py
│   │   │   ├── user_service.py
│   │   │   ├── contact_service.py
│   │   │   ├── storage_service.py     # AWS S3 wrapper
│   │   │   ├── email_service.py       # AWS SES wrapper
│   │   │   ├── sms_service.py         # InfoBIP wrapper
│   │   │   └── signature_service.py   # DocuSeal wrapper
│   │   │
│   │   └── utils/                       # Shared utilities
│   │       ├── __init__.py
│   │       ├── rbac.py                 # Permission checks
│   │       ├── pagination.py           # Cursor-based pagination
│   │       └── encryption.py           # Field-level encryption
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── forgot-password/page.tsx
│   │   │   │
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx         # Sidebar + Header + TenantProvider
│   │   │   │   ├── dashboard/page.tsx
│   │   │   │   ├── contacts/page.tsx
│   │   │   │   ├── cases/page.tsx
│   │   │   │   ├── encounters/page.tsx
│   │   │   │   ├── appointments/page.tsx
│   │   │   │   ├── communications/page.tsx
│   │   │   │   ├── documents/page.tsx
│   │   │   │   ├── forms/page.tsx
│   │   │   │   ├── workflows/page.tsx
│   │   │   │   ├── billing/page.tsx
│   │   │   │   ├── reports/page.tsx
│   │   │   │   └── settings/page.tsx
│   │   │   │
│   │   │   └── api/
│   │   │       └── auth/[...nextauth]/route.ts
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts                 # Axios instance + interceptors
│   │   │   ├── auth.ts                # NextAuth config
│   │   │   ├── tenant.ts              # TenantContext + hooks
│   │   │   └── rbac.ts                # usePermission hook
│   │   │
│   │   └── components/
│   │       ├── ui/                    # shadcn/ui components
│   │       ├── layout/                # AppShell, Sidebar, TopBar
│   │       ├── shared/                # DataTable, Modal, Form fields
│   │       └── industry/              # Industry-specific components
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.ts
│   └── Dockerfile
│
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
│
├── nginx/
│   └── exlcrm.conf
│
├── .env
├── .env.example
└── README.md
```

---

## 14. Python Dependencies (requirements.txt)

```txt
# === Web Framework ===
fastapi==0.115.*
uvicorn[standard]==0.32.*
python-multipart==0.0.*

# === Database ===
beanie==1.26.*
motor==3.5.*

# === Data Validation ===
pydantic[email]==2.9.*
pydantic-settings==2.6.*

# === Authentication ===
python-jose[cryptography]==3.3.*
passlib[bcrypt]==1.7.*
fastapi-users[beanie]==14.*

# === Async HTTP ===
httpx==0.27.*

# === AWS Services ===
boto3==1.35.*

# === Queue ===
celery[redis]==5.4.*

# === Email (optional fallback) ===
fastapi-mail==1.4.*

# === Billing ===
stripe==11.*

# === Utilities ===
structlog==24.*
tenacity==9.*
```

---

## 15. Environment Variables (.env.example)

```env
# === Application ===
APP_NAME=EXL-CRM
APP_ENV=production
APP_PORT=8000
APP_SECRET_KEY=generate-with-openssl-rand-hex-32
APP_URL=https://app.exlcrm.com

# === MongoDB Atlas (Toronto, CA-Central) ===
MONGODB_URL=mongodb+srv://username:***@cluster0.xxxxx.mongodb.net/exlcrm?retryWrites=true&w=majority

# === AWS (Montreal: ca-central-1) ===
AWS_REGION=ca-central-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=exlcrm-documents
SES_FROM_EMAIL=app@exlcrm.com

# === InfoBIP SMS ===
INFOBIP_API_KEY=...
INFOBIP_BASE_URL=https://api.infobip.com

# === Stripe (Billing) ===
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_STARTER=price_xxx
STRIPE_PRICE_PROFESSIONAL=price_xxx
STRIPE_PRICE_ENTERPRISE=price_xxx

# === Redis ===
REDIS_URL=redis://localhost:6379/0

# === DocuSeal (e-Signature) ===
DOCU_SEAL_URL=http://localhost:55017
DOCU_SEAL_SECRET=...
```

---

## 16. Docker Compose

```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - MONGODB_URL=mongodb+srv://...
      - AWS_REGION=ca-central-1
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - S3_BUCKET=exlcrm-documents
      - INFOBIP_API_KEY=${INFOBIP_API_KEY}
      - INFOBIP_BASE_URL=https://api.infobip.com
      - REDIS_URL=redis://redis:6379/0
      - APP_SECRET_KEY=${APP_SECRET_KEY}
      - DOCU_SEAL_URL=http://docuseal:55017
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      - redis
    restart: unless-stopped

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery worker -l info --concurrency=4
    environment:
      - MONGODB_URL=mongodb+srv://...
      - REDIS_URL=redis://redis:6379/0
      - AWS_REGION=ca-central-1
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - INFOBIP_API_KEY=${INFOBIP_API_KEY}
    depends_on:
      - redis
    restart: unless-stopped

  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery beat -l info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXTAUTH_SECRET=${APP_SECRET_KEY}
      - NEXTAUTH_URL=https://app.exlcrm.com
    depends_on:
      - backend
    restart: unless-stopped

  docuseal:
    image: docuseal/docuseal:latest
    environment:
      - DATABASE_URL=postgresql://docuseal:${DOCU_SEAL_DB_PASSWORD}@docuseal_db:5432/docuseal
      - SECRET_KEY_BASE=${DOCU_SEAL_SECRET}
      - DOCU_SEAL_URL_HOST=https://sign.exlcrm.com
    volumes:
      - docuseal_data:/app/storage
    depends_on:
      - docuseal_db
    restart: unless-stopped

  docuseal_db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=docuseal
      - POSTGRES_PASSWORD=${DOCU_SEAL_DB_PASSWORD}
      - POSTGRES_DB=docuseal
    volumes:
      - docuseal_pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/exlcrm.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - frontend
      - backend
      - docuseal
    restart: unless-stopped

  uptime-kuma:
    image: louislam/uptime-kuma:1
    volumes:
      - uptime_data:/app/data
    ports:
      - "3001:3001"
    restart: unless-stopped

volumes:
  redis_data:
  docuseal_data:
  docuseal_pgdata:
  uptime_data:
```

---

## 17. VPS Requirements

| Spec | Value |
|------|-------|
| Provider | OVHcloud |
| Plan | VPS Comfort (or equivalent) |
| Location | Beauharnois, Quebec, Canada |
| CPU | 4 vCPU |
| RAM | 8 GB DDR4 |
| Storage | 80 GB SSD (NVMe preferred) |
| OS | Ubuntu 22.04 LTS |
| Docker Engine | v24+ |
| Docker Compose | v2+ |
| Bandwidth | Unlimited |
| Monthly Cost | ~CA$62 |
| SSH | Yes (root access required) |

---

## 18. Competitive Landscape

| Competitor | Weakness | Our Edge |
|------------|----------|----------|
| Clio (Legal) | Legal-only, $99+/user | Multi-industry, flat per-tenant pricing |
| Pipedrive | Generic CRM, no industry features | RCIC + Healthcare specific workflows |
| Jane App (Healthcare) | Healthcare-only | Multi-industry platform |
| Salesforce | Complex, $75+/user/month | Simple, affordable, Canadian data residency |
| Zoho CRM | Generic, cluttered UI | Clean, focused, industry-specific |
| PracticePanther | Generic legal CRM | Multi-industry, Canadian compliance |
| HubSpot | Expensive at scale, US-based | Affordable, Canadian data residency |

**Our competitive moat:**
1. Industry-specific features at a fraction of Salesforce cost
2. Canadian data residency (PHIPA + RCIC compliance)
3. Modular architecture — add industries without rearchitecting
4. Flat per-tenant pricing (no per-seat nickel-and-diming)
5. Self-hosted e-signatures (DocuSeal) — unlimited, zero cost

---

## 19. Open Questions (Resolved)

| Question | Answer |
|----------|--------|
| Multi-tenant isolation | Single DB, tenant_id on all documents (cost-effective for 50 tenants) |
| Deployment | Cloud-only on Canadian VPS (OVHcloud QC) |
| Pricing model | Tiered per-tenant: $149 / $299 / $499 per month |
| Scale target | 50 tenants |
| Mobile app | Not now — responsive web is sufficient |
| e-Signature | DocuSeal (self-hosted, free, unlimited documents) |
| Document storage | AWS S3 Montreal (ca-central-1) |
| Email | AWS SES Montreal (ca-central-1) |
| SMS | InfoBIP (cheaper than Twilio, global coverage) |
| VPS Provider | OVHcloud QC (4vCPU/8GB/CA$62/mo, Linux Ubuntu 22.04) |
| Database | MongoDB Atlas Toronto |
| Data residency | All data stored in Canada (no US jurisdiction) |
| Auth | JWT + FastAPI-Users + custom RBAC |

---

## 20. Next Steps

| # | Action | Priority | Status |
|---|----------|----------|--------|
| 1 | Finalize concept document | 🔴 | ✅ Complete |
| 2 | Provision OVHcloud VPS (Ubuntu 22.04) | 🔴 | ⏳ In progress |
| 3 | Set up MongoDB Atlas (Toronto cluster) | 🔴 | Pending |
| 4 | Configure AWS S3 bucket + SES (Montreal) | 🔴 | Pending |
| 5 | Set up InfoBIP account + phone number | 🟡 | Pending |
| 6 | Set up domain + SSL (Cloudflare or Let's Encrypt) | 🟡 | Pending |
| 7 | Begin Phase 0: Backend foundation (FastAPI + auth) | 🔴 | Pending |
| 8 | Begin Phase 5: Frontend scaffold (Next.js) | 🔴 | Pending |
| 9 | Dockerize all services | 🔴 | Pending |
| 10 | Deploy to VPS + test | 🟡 | Pending |

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| RCIC | Regulated Canadian Immigration Consultant |
| IRCC | Immigration, Refugees and Citizenship Canada |
| PHIPA | Personal Health Information Protection Act (Ontario) |
| PIPEDA | Personal Information Protection and Electronic Documents Act (Canada) |
| TNW | True North (Express Entry, PNP, LMIA, Study/Work Permit, Provincial streams) |
| RBAC | Role-Based Access Control |
| ODM | Object-Document Mapper (Beanie for MongoDB) |
| JWT | JSON Web Token |
| TTL | Time to live |
| SLA | Service-level agreement |
| MRR | Monthly Recurring Revenue |
| eIDAS | EU electronic Identification, Authentication and Trust Services |
| CRS | Comprehensive Ranking System (Express Entry) |
| SOAP | Subjective, Objective, Assessment, Plan (clinical notes format) |

---

## Appendix B: Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-06-26 | EXL-CRM Team | Renamed from previous name to EXL-CRM (exlcrm.com) |
| 1.0 | 2026-06-26 | EXL-CRM Team | Initial concept document |

---

*This document serves as the single source of truth for the EXL-CRM project. All architectural decisions, tech choices, project structure, and development phases are defined here to ensure consistency across the team. Share this document with all developers and stakeholders for alignment.*
