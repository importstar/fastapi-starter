# 📁 โครงสร้างโปรเจกต์

```
project/
├── .env                    # เก็บ Environment Variables (เช่น DATABASE_URL)
├── .gitignore
├── main.py                 # จุดเริ่มต้นแอปพลิเคชัน, รวม Router และ init ระบบ
├── pyproject.toml
└── api_app/
    ├── __init__.py
    │
    ├── core/
    │   └── security.py       # (ตัวอย่าง) สำหรับจัดการ Password Hashing, JWT
    │
    ├── infrastructure/
    │   └── database.py       # สำหรับเชื่อมต่อและ Initialize Beanie กับ MongoDB
    │
    ├── models/
    │   ├── __init__.py
    │   ├── product_model.py  # Beanie Document สำหรับ Product
    │   └── user_model.py     # Beanie Document สำหรับ User
    │
    ├── utils/
    │   └── openapi.py        # เก็บฟังก์ชัน generate_operation_id
    │
    └── modules/              # <-- Modules
        ├── users/            # <-- User Management
        │   ├── __init__.py
        │   ├── repository.py
        │   ├── router.py
        │   ├── schemas.py
        │   └── use_case.py
        ├── auth/             # <-- Authentication
        │   ├── __init__.py
        │   ├── repository.py
        │   ├── router.py
        │   ├── schemas.py
        │   └── use_case.py
        └── products/         # <-- Product Management
            ├── __init__.py
            ├── repository.py
            ├── router.py
            ├── schemas.py
            └── use_case.py
```
