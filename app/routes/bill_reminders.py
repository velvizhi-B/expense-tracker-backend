from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import get_current_user

router = APIRouter(prefix="/bill-reminders", tags=["Bill Reminders"])

# Create a bill reminder
@router.post("/", response_model=schemas.BillReminderResponse)
def create_bill_reminder(
    bill: schemas.BillReminderCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_bill = models.BillReminder(
        title=bill.title,
        amount=bill.amount,
        due_date=bill.due_date,
        repeat_cycle=bill.repeat_cycle,
        status=bill.status,
        notes=bill.notes,
        user_id=current_user.id
    )
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill


# Get all bill reminders
@router.get("/", response_model=list[schemas.BillReminderResponse])
def get_bills(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    bills = db.query(models.BillReminder).filter(models.BillReminder.user_id == current_user.id).all()
    return bills


# Get a bill reminder by ID
@router.get("/{bill_id}", response_model=schemas.BillReminderResponse)
def get_bill(bill_id: int,
             db: Session = Depends(database.get_db),
             current_user: models.User = Depends(get_current_user)):
    bill = db.query(models.BillReminder).filter(
        models.BillReminder.id == bill_id,
        models.BillReminder.user_id == current_user.id
    ).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill reminder not found")
    return bill


# Update a bill reminder
@router.put("/{bill_id}", response_model=schemas.BillReminderResponse)
def update_bill(bill_id: int,
                updated: schemas.BillReminderCreate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    bill = db.query(models.BillReminder).filter(
        models.BillReminder.id == bill_id,
        models.BillReminder.user_id == current_user.id
    ).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill reminder not found")

    bill.title = updated.title
    bill.amount = updated.amount
    bill.due_date = updated.due_date
    bill.repeat_cycle = updated.repeat_cycle
    bill.status = updated.status
    bill.notes = updated.notes

    db.commit()
    db.refresh(bill)
    return bill


# Delete a bill reminder
@router.delete("/{bill_id}", response_model=schemas.BillReminderResponse)
def delete_bill(bill_id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    bill = db.query(models.BillReminder).filter(
        models.BillReminder.id == bill_id,
        models.BillReminder.user_id == current_user.id
    ).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill reminder not found")

    db.delete(bill)
    db.commit()
    return bill
