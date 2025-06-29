# 📁 โครงสร้างโปรเจกต์หลัง Refactor

## โครงสร้างปัจจุบัน vs โครงสร้างใหม่

### 🔄 การ Refactor

```
project/
├── .env                      # เก็บ Environment Variables (เช่น DATABASE_URL)
├── .gitignore
├── main.py                   # จุดเริ่มต้นแอปพลิเคชัน, รวม Router และ init ระบบ
├── pyproject.toml
├── poetry.lock
├── poetry.toml
├── scripts/                  # Scripts สำหรับ deployment และ development
│   ├── init-admin
│   ├── run-dev
│   └── run-prod
└── api_app/
    ├── __init__.py
    │
    ├── core/                 # 🆕 Core business logic และ shared components
    │   ├── __init__.py
    │   ├── security.py       # Password Hashing, JWT (ย้ายมาจาก api/core/)
    │   ├── config.py         # Configuration settings (ย้ายมาจาก api/core/)
    │   ├── dependencies.py   # Shared dependencies (ย้ายมาจาก api/core/)
    │   ├── exceptions.py     # Custom exceptions (ย้ายมาจาก api/core/)
    │   ├── schemas.py        # 🆕 Base schemas ที่แชร์ใช้กัน (จาก schemas/base_schema.py)
    │   └── base_repository.py # 🆕 Base repository pattern (จาก repositories/base_repo.py)
    │
    ├── infrastructure/       # 🆕 Infrastructure layer
    │   ├── __init__.py
    │   └── database.py       # Database connection และ Beanie initialization
    │
    ├── models/               # Beanie Document models (เก็บไว้เหมือนเดิม)
    │   ├── __init__.py
    │   ├── user_model.py     # Beanie Document สำหรับ User
    │   ├── token_model.py    # Beanie Document สำหรับ Token
    │   └── image_model.py    # Beanie Document สำหรับ Image
    │
    ├── utils/                # 🆕 Utility functions
    │   ├── __init__.py
    │   ├── openapi.py        # OpenAPI utilities
    │   ├── logging.py        # Logging utilities (ย้ายมาจาก utils/)
    │   └── request_logs.py   # Request logging (ย้ายมาจาก utils/)
    │
    │
    ├── middlewares/          # 🆕 FastAPI middlewares
    │   ├── __init__.py       # Clean exports only
    │   ├── base.py           # init_all_middlewares function
    │   ├── cors.py           # CORS middleware (ย้ายมาจาก api/middlewares/)
    │   ├── security.py       # Security middleware (User agent filtering)
    │   └── timing.py         # Performance timing middleware
    │
    └── modules/              # 🆕 Feature modules
        ├── __init__.py
        │
        ├── auth/             # 🔄 Authentication module
        │   ├── __init__.py
        │   ├── schemas.py    # Auth schemas (จาก schemas/auth_schema.py)
        │   ├── repository.py # Auth repository (สร้างใหม่)
        │   ├── use_case.py   # Auth business logic (จาก services/auth_service.py)
        │   └── router.py     # Auth endpoints (จาก api/routers/v1/auth.py)
        │
        └── users/            # 🔄 User management module
            ├── __init__.py
            ├── schemas.py    # User schemas (จาก schemas/user_schema.py)
            ├── repository.py # User repository (จาก repositories/user_repo.py)
            ├── use_case.py   # User business logic (จาก services/user_service.py)
            └── router.py     # User endpoints (จาก api/routers/v1/user.py)
```

## 📋 การแปลงไฟล์

### 1. **Core Layer** (ย้ายและรวม)

- `api/core/security.py` → `core/security.py`
- `api/core/config.py` → `core/config.py`
- `api/core/dependencies.py` → `core/dependencies.py`
- `api/core/exceptions.py` → `core/exceptions.py`
- `schemas/base_schema.py` → `core/schemas.py`
- `repositories/base_repo.py` → `core/base_repository.py`

### 2. **Infrastructure Layer** (สร้างใหม่)

- `infrastructure/database.py` (สร้างใหม่จาก database connection logic)

### 3. **Utils Layer** (ย้ายและรวม)

- `utils/logging.py` → `utils/logging.py`
- `utils/request_logs.py` → `utils/request_logs.py`
- `utils/schema.py` → `utils/schema.py`
- สร้าง `utils/openapi.py` ใหม่

### 4. **Middlewares** (ย้าย)

- `api/middlewares/` → `middlewares/`

### 5. **Modules** (แปลงจาก services + repositories + routers + schemas)

#### Auth Module:

- `schemas/auth_schema.py` → `modules/auth/schemas.py`
- `services/auth_service.py` → `modules/auth/use_case.py`
- `api/routers/v1/auth.py` → `modules/auth/router.py`
- สร้าง `modules/auth/repository.py` ใหม่

#### Users Module:

- `schemas/user_schema.py` → `modules/users/schemas.py`
- `repositories/user_repo.py` → `modules/users/repository.py`
- `services/user_service.py` → `modules/users/use_case.py`
- `api/routers/v1/user.py` → `modules/users/router.py`

## 🎯 ประโยชน์ของการ Refactor

1. **Modular Architecture**: แต่ละ module เป็นอิสระและจัดการ feature เฉพาะตัว
2. **Clean Architecture**: แยก layer ตาม responsibility ชัดเจน
3. **Scalability**: ง่ายต่อการเพิ่ม module ใหม่
4. **Maintainability**: โค้ดจัดระเบียบดีขึ้น หาและแก้ไขง่าย
5. **Testability**: แต่ละส่วนทดสอบแยกกันได้
6. **Reusability**: Base classes และ utilities ใช้ร่วมกันได้

## 📝 ขั้นตอนการ Refactor

1. สร้าง folder structure ใหม่
2. ย้าย core components ไป `core/`
3. สร้าง `infrastructure/` layer
4. ย้าย utilities ไป `utils/`
5. แปลง services + repositories + routers เป็น modules
6. อัพเดต imports ทั้งหมด
7. ทดสอบว่าทุกอย่างทำงานถูกต้อง
