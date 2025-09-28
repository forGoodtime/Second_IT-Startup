from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from typing import Optional, List
import logging
import requests
import json

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bvckz:your_password_here@localhost:5432/bvckz_mvp")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
MEDIA_SERVICE_URL = os.getenv("MEDIA_SERVICE_URL", "http://media:8001")

# Database setup (synchronous for simplicity)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()

# FastAPI app
app = FastAPI(
    title="BvckZ MVP API",
    description="MVP API for BvckZ clothing upcycling service",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    role = Column(String, default="user")  # user, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class DonationBatch(Base):
    __tablename__ = "donation_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    items_count = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending, collected, processing, completed
    pickup_address = Column(Text, nullable=True)
    pickup_method = Column(String, nullable=True)  # courier, drop_point
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="donation_batches")

# Alias for admin compatibility
Donation = DonationBatch

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    donation_batch_id = Column(Integer, ForeignKey("donation_batches.id"), nullable=True)
    status = Column(String, default="pending")  # pending, paid, production, shipped, completed
    total_price = Column(Integer, default=0)  # in cents
    design_metadata = Column(Text, nullable=True)  # JSON
    preview_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")

# Add relationships
User.donation_batches = relationship("DonationBatch", back_populates="user")
User.orders = relationship("Order", back_populates="user")

# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DonationRequest(BaseModel):
    items_count: int
    pickup_method: str
    pickup_address: Optional[str] = None
    notes: Optional[str] = None

# Alias for compatibility
DonationCreate = DonationRequest

class DonationResponse(BaseModel):
    id: int
    user_id: int
    item_count: int
    pickup_method: Optional[str]
    address: Optional[str]
    phone: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, donation):
        return cls(
            id=donation.id,
            user_id=donation.user_id,
            item_count=donation.items_count,
            pickup_method=donation.pickup_method,
            address=donation.pickup_address,
            status=donation.status,
            created_at=donation.created_at
        )

class OrderCreate(BaseModel):
    donation_batch_id: Optional[int] = None
    design_metadata: Optional[str] = None

# Utility functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user

# API Routes
@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "created_at": current_user.created_at
    }

# Donation management
@app.post("/api/donations", response_model=DonationResponse)
async def create_donation(
    donation: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new donation request"""
    db_donation = Donation(**donation.dict(), user_id=current_user.id)
    db.add(db_donation)
    await db.commit()
    await db.refresh(db_donation)
    
    logger.info(f"User {current_user.email} created donation request for {donation.item_count} items")
    return DonationResponse.from_orm(db_donation)

@app.get("/api/donations", response_model=List[DonationResponse])
async def get_user_donations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's donations"""
    result = await db.execute(
        select(Donation).where(Donation.user_id == current_user.id)
    )
    donations = result.scalars().all()
    return [DonationResponse.from_orm(d) for d in donations]

# Admin endpoints
def is_admin(current_user: User = Depends(get_current_user)):
    """Check if user is admin"""
    if current_user.email == "admin@bvckz.com" or current_user.email == "test@bvckz.com":
        return current_user
    raise HTTPException(status_code=403, detail="Admin access required")

@app.get("/api/admin/stats")
async def get_admin_stats(
    admin_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """Get admin statistics"""
    # Count donations
    total_donations = db.query(Donation).count()
    
    # Count orders
    total_orders = db.query(Order).count()
    
    # Count users
    total_users = db.query(User).count()
    
    # Count pending donations
    pending_donations = db.query(Donation).filter(Donation.status == "pending").count()
    
    return {
        "total_donations": total_donations,
        "total_orders": total_orders,
        "total_users": total_users,
        "pending_donations": pending_donations
    }

@app.get("/api/admin/donations")
async def get_all_donations(
    admin_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """Get all donations for admin"""
    donations = db.query(Donation, User.email).join(User, Donation.user_id == User.id).order_by(Donation.created_at.desc()).all()
    
    return [
        {
            "id": donation.id,
            "user_email": user_email,
            "item_count": donation.items_count,
            "pickup_method": donation.pickup_method,
            "status": donation.status,
            "created_at": donation.created_at.isoformat(),
            "address": donation.pickup_address,
            "phone": donation.notes  # Using notes as phone for now
        }
        for donation, user_email in donations
    ]

@app.get("/api/admin/orders")
async def get_all_orders(
    admin_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """Get all orders for admin"""
    orders = db.query(Order, User.email).join(User, Order.user_id == User.id).order_by(Order.created_at.desc()).all()
    
    return [
        {
            "id": order.id,
            "user_email": user_email,
            "design": f"{order.design_metadata[:50] if order.design_metadata else 'Дизайн не указан'}",
            "status": order.status,
            "price": order.total_price or 0,
            "created_at": order.created_at.isoformat()
        }
        for order, user_email in orders
    ]

@app.get("/api/admin/users")
async def get_all_users(
    admin_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """Get all users for admin"""
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": "admin" if user.email in ["admin@bvckz.com", "test@bvckz.com"] else "user",
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]

@app.patch("/api/admin/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    status_data: dict,
    admin_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status_data.get("status", order.status)
    db.commit()
    
    logger.info(f"Admin {admin_user.email} updated order {order_id} status to {order.status}")
    return {"message": "Order status updated successfully"}

@app.patch("/api/admin/donations/{donation_id}/status")
async def update_donation_status(
    donation_id: int,
    status_data: dict,
    admin_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """Update donation status"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    donation.status = status_data.get("status", donation.status)
    db.commit()
    
    logger.info(f"Admin {admin_user.email} updated donation {donation_id} status to {donation.status}")
    return {"message": "Donation status updated successfully"}

@app.get("/api/donations")
async def get_donations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    donations = db.query(DonationBatch).filter(DonationBatch.user_id == current_user.id).all()
    return [
        {
            "id": d.id,
            "status": d.status,
            "items_count": d.items_count,
            "pickup_method": d.pickup_method,
            "created_at": d.created_at
        } for d in donations
    ]

@app.post("/api/orders")
async def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_order = Order(
        user_id=current_user.id,
        donation_batch_id=order.donation_batch_id,
        design_metadata=order.design_metadata
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return {
        "id": db_order.id,
        "status": db_order.status,
        "created_at": db_order.created_at
    }

@app.get("/api/orders")
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return [
        {
            "id": o.id,
            "status": o.status,
            "total_price": o.total_price,
            "preview_url": o.preview_url,
            "created_at": o.created_at
        } for o in orders
    ]

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/demo", response_class=FileResponse)
async def serve_demo():
    """Serve the demo HTML page"""
    demo_path = os.path.join(os.path.dirname(__file__), "demo.html")
    return FileResponse(demo_path, media_type="text/html")

@app.post("/api/media/render")
async def render_design_preview(
    design_metadata: str,
    current_user: User = Depends(get_current_user)
):
    """Generate design preview via media service"""
    try:
        # Parse design metadata
        design_data = json.loads(design_metadata) if isinstance(design_metadata, str) else design_metadata
        
        # Prepare request for media service
        media_request = {
            "left_design": design_data.get("left"),
            "center_color": design_data.get("center", {}).get("color", "blue"),
            "right_pattern": design_data.get("right"),
            "width": 900,
            "height": 300
        }
        
        # Call media service
        response = requests.post(
            f"{MEDIA_SERVICE_URL}/render",
            json=media_request,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Media service error")
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Media service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

@app.get("/api/media/templates")
async def get_design_templates():
    """Get available design templates from media service"""
    try:
        response = requests.get(f"{MEDIA_SERVICE_URL}/templates", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback templates if media service is unavailable
            return {
                "left_designs": [
                    {"id": "", "name": "Без дизайна"},
                    {"id": "logo", "name": "Логотип"},
                    {"id": "pattern", "name": "Узор"}
                ],
                "colors": [
                    {"id": "blue", "name": "Синий"},
                    {"id": "green", "name": "Зелёный"},
                    {"id": "red", "name": "Красный"},
                    {"id": "black", "name": "Чёрный"}
                ],
                "patterns": [
                    {"id": "", "name": "Без орнамента"},
                    {"id": "kazakh", "name": "Казахский орнамент"},
                    {"id": "uzbek", "name": "Узбекский орнамент"},
                    {"id": "kyrgyz", "name": "Киргизский орнамент"}
                ]
            }
    except Exception:
        # Return fallback templates
        return {
            "left_designs": [{"id": "", "name": "Без дизайна"}, {"id": "logo", "name": "Логотип"}],
            "colors": [{"id": "blue", "name": "Синий"}, {"id": "green", "name": "Зелёный"}],
            "patterns": [{"id": "", "name": "Без орнамента"}, {"id": "kazakh", "name": "Казахский"}]
        }

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
