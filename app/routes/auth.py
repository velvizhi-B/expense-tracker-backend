from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, database
from app.auth_utils import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        phonenumber=user.phonenumber,
        email=user.email,
        password_hash=hashed_pw,
        profileimage=user.profileimage,
        address=user.address,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/update-profile", response_model=schemas.UserResponse)
def update_profile(
    updates: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if updates.email:
        # Check if email is already taken by someone else
        email_user = db.query(models.User).filter(models.User.email == updates.email).first()
        if email_user and email_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already in use")

    # Update fields only if values are provided
    if updates.name is not None:
        current_user.name = updates.name
    if updates.phonenumber is not None:
        current_user.phonenumber = updates.phonenumber
    if updates.email is not None:
        current_user.email = updates.email
    if updates.profileimage is not None:
        current_user.profileimage = updates.profileimage
    if updates.address is not None:
        current_user.address = updates.address

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/login", response_model=schemas.Token)
def login_user(login_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"email": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/user-name")
def get_user_name(current_user: models.User = Depends(get_current_user)):
    return {"name": current_user.name}

@router.get("/profile", response_model=schemas.UserResponse)
def get_user_profile(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return current_user


@router.post("/change-password")
def change_password(
    payload: schemas.ChangePasswordRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Step 1: Verify old password
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Step 2: Hash and update new password
    new_hashed_pw = hash_password(payload.new_password)
    current_user.password_hash = new_hashed_pw
    db.commit()

    return {"message": "Password updated successfully"}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: models.User = Depends(get_current_user)):
    """
    Dummy logout endpoint. Simply instruct client to delete JWT token.
    """
    return {"message": "Logout successful. Please delete the token on the client side."}

@router.delete("/delete-account")
def delete_account(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Delete user record
    db.delete(current_user)
    db.commit()
    return {"message": "Your account has been deleted successfully"}
