# Authentication Strategy

เอกสารนี้อธิบายการออกแบบ Authentication Strategy สำหรับแยกการจัดการ Refresh Token ระหว่าง Web และ Mobile Platform

## Overview

ระบบรองรับ 2 Authentication Strategy:

### 1. Web Platform (SSR with BFF)

- **Refresh Token**: เก็บใน httpOnly Cookie
- **Access Token**: ส่งผ่าน Authorization Header
- **เหมาะสำหรับ**: SSR applications ที่มี Backend for Frontend (BFF)

### 2. Mobile Platform

- **Refresh Token**: ส่งใน JSON Response ให้ client จัดการเอง
- **Access Token**: ส่งผ่าน Authorization Header
- **เหมาะสำหรับ**: Mobile apps, SPAs ที่ไม่มี BFF

## Architecture

```
Web (SSR + BFF):
Browser → BFF → FastAPI (/login/web)
                ↓
        Response + Set-Cookie: refresh_token=xxx
                ↓
Browser ← Set-Cookie: refresh_token=xxx; HttpOnly

Mobile/SPA:
Client → FastAPI (/login)
         ↓
         Response: { access_token, refresh_token }
         ↓
Client ← เก็บ refresh_token ใน secure storage
```

## Implementation Details

### 1. Login Endpoints

#### Web Login

```python
@router.post("/login/web")
async def login_web(
    credentials: schemas.LoginRequest,
    response: Response,
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.WebTokenResponse:
    """Login สำหรับ Web - ตั้ง refresh token เป็น httpOnly cookie"""
    return await use_case.authenticate_web(credentials, response)
```

#### Mobile Login

```python
@router.post("/login")
async def login(
    credentials: schemas.LoginRequest,
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.Token:
    """Login สำหรับ Mobile - ส่ง refresh token ใน JSON"""
    return await use_case.authenticate(credentials)
```

### 2. Refresh Token Endpoints

#### Web Refresh

```python
@router.post("/refresh_token/web")
async def refresh_token_web(
    response: Response,
    refresh_token: str = Cookie(None, alias="refresh_token"),
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.GetAccessTokenResponse:
    """Refresh token สำหรับ Web - อ่านจาก Cookie"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    return await use_case.refresh_token_web(refresh_token, response)
```

#### Mobile Refresh

```python
@router.get("/refresh_token")
async def refresh_token(
    credentials: typing.Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.GetAccessTokenResponse:
    """Refresh token สำหรับ Mobile - อ่านจาก Authorization Header"""
    return await use_case.refresh_token(credentials)
```

### 3. Logout Endpoint

```python
@router.post("/logout")
async def logout(
    response: Response,
    platform: str = "mobile",
):
    if platform == "web":
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="lax"
        )
    return {"message": "Logged out successfully"}
```

### 4. Schemas

#### Login Request (JSON)

```python
class LoginRequest(BaseSchema):
    username: str
    password: str
    platform: str | None = "mobile"  # "web" or "mobile"
```

#### Web Token Response

```python
class WebTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    # ไม่มี refresh_token ใน response
```

#### Mobile Token Response

```python
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
```

### 5. Configuration

เพิ่ม Cookie settings ใน `core/config.py`:

```python
class Settings(BaseSettings):
    # Cookie settings
    COOKIE_SECURE: bool = True  # True in production (HTTPS)
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"  # "lax", "strict", or "none"
    COOKIE_DOMAIN: str | None = None  # e.g., ".yourdomain.com"
    COOKIE_PATH: str = "/"
```

### 6. Use Case Methods

เพิ่ม methods ใน `AuthUseCase`:

```python
def set_refresh_token_cookie(self, response: Response, refresh_token: str):
    """Set refresh token as httpOnly cookie for web"""
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path=settings.COOKIE_PATH,
        domain=settings.COOKIE_DOMAIN,
    )

async def authenticate_web(
    self,
    credentials: schemas.LoginRequest,
    response: Response,
) -> schemas.WebTokenResponse:
    """Authentication สำหรับ Web platform"""
    # Validate credentials
    user = await self.validate_credentials(credentials.username, credentials.password)

    # Create tokens
    access_token = security.jwt_handler.create_access_token(user)
    refresh_token = security.jwt_handler.create_refresh_token(user)

    # Set refresh token cookie
    self.set_refresh_token_cookie(response, refresh_token)

    return schemas.WebTokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

async def refresh_token_web(
    self,
    refresh_token_str: str,
    response: Response,
) -> schemas.GetAccessTokenResponse:
    """Refresh token สำหรับ Web - อาจ rotate refresh token ใหม่"""
    new_access_token = security.jwt_handler.refresh_token(refresh_token_str)

    # Optional: Rotate refresh token
    # new_refresh_token = security.jwt_handler.create_refresh_token(...)
    # self.set_refresh_token_cookie(response, new_refresh_token)

    return schemas.GetAccessTokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )
```

## BFF Considerations

### สำหรับ SSR with BFF

1. **ใช้ Web Platform Strategy** (`/login/web`)
2. **BFF ต้อง forward `Set-Cookie` header** จาก FastAPI ไปยัง Browser
3. **FastAPI จัดการ Cookie attributes** (domain, path, secure, etc.)

### ตัวอย่าง BFF Implementation (Next.js)

```typescript
// pages/api/auth/login.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "POST") return res.status(405).end();

  try {
    const response = await fetch("http://fastapi/v1/auth/login/web", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();

    // Forward Set-Cookie header
    const setCookie = response.headers.get("set-cookie");
    if (setCookie) {
      res.setHeader("Set-Cookie", setCookie);
    }

    res.status(response.status).json(data);
  } catch (error) {
    res.status(500).json({ error: "Internal server error" });
  }
}
```

## Security Considerations

### Web Platform

- ✅ **httpOnly Cookie**: ป้องกัน XSS
- ✅ **Secure Flag**: ใช้ HTTPS เท่านั้น
- ✅ **SameSite**: ป้องกัน CSRF
- ⚠️ **Domain Setting**: ตั้งให้ตรงกับ domain ที่ต้องการ

### Mobile Platform

- ⚠️ **Secure Storage**: ใช้ Keychain (iOS) หรือ Keystore (Android)
- ⚠️ **Token Encryption**: เข้ารหัส refresh token ก่อนเก็บ
- ✅ **Certificate Pinning**: ป้องกัน MITM attacks

### General

- 🔄 **Token Rotation**: พิจารณา rotate refresh token ทุกครั้งที่ refresh
- 🕒 **Token Expiration**: ตั้งเวลาหมดอายุให้เหมาะสม
- 🔐 **JWT Security**: ใช้ strong secret และ algorithm ที่ปลอดภัย

## Migration Guide

### จาก Form Data เป็น JSON

1. **เปลี่ยน LoginRequest Schema**:

   ```python
   class LoginRequest(BaseSchema):
       username: str
       password: str
       platform: str | None = "mobile"
   ```

2. **อัปเดต Endpoints**:

   - เก็บ `/token` สำหรับ OAuth2 standard (Swagger UI)
   - เปลี่ยน `/login` และ `/login/web` เป็น JSON

3. **อัปเดต Use Cases**:
   - แยก `authenticate()` และ `authenticate_web()`

### เพิ่ม Web Strategy

1. **เพิ่ม Cookie Settings** ใน Config
2. **สร้าง Web-specific Schemas**
3. **เพิ่ม Cookie Methods** ใน Use Case
4. **สร้าง Web Endpoints** สำหรับ login และ refresh

## Checklist

- [ ] เพิ่ม Cookie settings ใน `core/config.py`
- [ ] สร้าง `LoginRequest` schema ใน `schemas.py`
- [ ] สร้าง `WebTokenResponse` schema
- [ ] เพิ่ม `set_refresh_token_cookie()` method ใน Use Case
- [ ] เพิ่ม `authenticate_web()` method
- [ ] เพิ่ม `refresh_token_web()` method
- [ ] สร้าง `/login/web` endpoint
- [ ] สร้าง `/refresh_token/web` endpoint
- [ ] สร้าง `/logout` endpoint
- [ ] อัปเดต CORS settings
- [ ] ทดสอบ Web flow
- [ ] ทดสอบ Mobile flow
- [ ] ทดสอบ BFF integration
