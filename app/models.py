from sqlalchemy import Column, Integer, String, Numeric, Date, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    phonenumber = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    profileimage = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    incomes = relationship("Income", back_populates="user", cascade="all, delete")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")
    reminders = relationship("BillReminder", back_populates="user", cascade="all, delete")
    categories = relationship("Category", back_populates="user", cascade="all, delete")


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    source = Column(String(255))
    received_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="incomes")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100))
    expense_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")


class BillReminder(Base):
    __tablename__ = "bill_reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    repeat_cycle = Column(String(50))
    status = Column(String(20), default="pending")
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="reminders")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(20))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="categories")
