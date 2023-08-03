from fastapi import APIRouter
from order import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from order.repository import account

router = APIRouter(
    prefix="/account",
    tags=['Accounts']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowAccount)
def create_account(request: schemas.Account, db: Session = Depends(get_db)):
    return account.create(request, db)


@router.get('/{id}', response_model=schemas.ShowAccount)
def get_account_display(id: int, db: Session = Depends(get_db)):
    return account.get_account(id, db)
