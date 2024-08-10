from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from db_lib import MongoDBClient
from models.models import PhoneNumberVerification, BusinessSelection
from .security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from db_lib import db_client

router = APIRouter()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    client = db_client
    user = await client.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверить, к каким бизнесам принадлежит пользователь
    businesses = await client.get_businesses_for_user(user["_id"])
    if len(businesses) > 1:
        return {"businesses": businesses}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["phone_number"], "business_id": str(businesses[0]["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/select_business")
async def select_business(selection: BusinessSelection):
    client = db_client
    user = await client.get_user_by_phone_number(selection.phone_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["phone_number"], "business_id": selection.business_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify_phone")
async def verify_phone(phone_verification: PhoneNumberVerification):
    if phone_verification.code == "0000":
        return {"message": "Phone number verified"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid verification code")
