# SIM-KKN Database Schema Guide

This document maps out the essential entities and relationships inside the SIM-KKN PostgreSQL 16 database. All ORM implementations (FastAPI SQLAlchemy) must reflect these constraints.

## Core Entities

### 1. User Model (`users`)
- Base entity representing an authenticated account.
- Fields: `id` (UUID), `email`, `hashed_password`, `role_id`, `created_at`, `updated_at`.
- Relationship: 1:1 with `Mahasiswa`, `Dosen`, or `Koordinator` profiles.

### 2. Mahasiswa (`mahasiswa`)
- Represents student participants.
- Fields: `nim` (PK), `user_id` (FK), `nama`, `fakultas`, `jurusan`, `kelompok_id` (FK).
- Business Rule: A student can only belong to one active `Kelompok` per semester.

### 3. Dosen Pembimbing Lapangan (`dosen_dpl`)
- Represents field advisors.
- Fields: `nidn` (PK), `user_id` (FK), `nama`, `departemen`.
- Relationship: 1:N with `Kelompok` (One DPL supervises multiple groups).

### 4. Kelompok (`kelompok`)
- The active KKN unit.
- Fields: `id`, `nama_desa`, `kecamatan`, `kabupaten`, `dpl_nidn` (FK).
- Relationship: 1:N with `Mahasiswa` and 1:N with `Logbook`.

### 5. Logbook & Kegiatan (`logbook`)
- Tracks daily activity of students or groups.
- Fields: `id`, `mahasiswa_nim` (FK), `kelompok_id` (FK), `tanggal`, `deskripsi_kegiatan`, `foto_url`, `status_approval`.
- Business Rule: `status_approval` is ENUM (`PENDING`, `APPROVED`, `REJECTED`) modified only by the assigned DPL.

## Schema Migrations
- Executed via Alembic.
- Command: `alembic upgrade head`.
- Never bypass the migration scripts by executing direct SQL `ALTER TABLE` commands.
