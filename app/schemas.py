from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# ==== USER ====
class UserBase(BaseModel):
    name: str
    phonenumber: str
    email: EmailStr
    address: Optional[str] = None
    profileimage: Optional[str] = None

class UserCreate(UserBase):
    password: str

# class UserResponse(UserBase):
#     id: int
#     created_at: datetime

#     class Config:
#         from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    phonenumber: str
    email: EmailStr
    profileimage: str | None = None
    address: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
        
class UserUpdate(BaseModel):
    name: Optional[str]
    phonenumber: Optional[str]
    email: Optional[EmailStr]
    profileimage: Optional[str]
    address: Optional[str]


# ==== EXPENSE ====
class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: Optional[str]
    expense_date: date


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    expense_date: date

class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True



# ==== CATEGORY ====
class CategoryBase(BaseModel):
    name: str
    color: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# === AUTH ===


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None

# login


class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# ==== INCOME ====
class IncomeBase(BaseModel):
    amount: float
    source: Optional[str]
    received_date: date

class IncomeCreate(IncomeBase):
    pass

class IncomeResponse(IncomeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==== BILL REMINDER ====
class BillReminderBase(BaseModel):
    title: str
    amount: float
    due_date: date
    repeat_cycle: Optional[str]
    status: Optional[str] = "pending"
    notes: Optional[str]

class BillReminderCreate(BillReminderBase):
    pass

class BillReminderResponse(BillReminderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# summary

class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    remaining_balance: float

    class Config:
        from_attributes = True


