from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from order import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from order.repository import order

router = APIRouter(
    prefix="/order",
    tags=['Orders']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowOrder])
def get_all(db: Session = Depends(get_db), current: schemas.Account = Depends(oauth2.get_current)):
    return order.get_orders(db, current.account)


@router.get('/{id}', status_code=200, response_model=schemas.ShowOrder)
def get_order_display(id: int, db: Session = Depends(get_db), current: schemas.Account = Depends(oauth2.get_current)):
    return order.get_order(id, db, current.account)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowOrder)
def create(request: schemas.Order, db: Session = Depends(get_db),
           current: schemas.Account = Depends(oauth2.get_current)):
    return order.create(request, db, current.account)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Order, db: Session = Depends(get_db),
           current: schemas.Account = Depends(oauth2.get_current)):
    return order.update(id, request, db, current.account)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def discard(id: int, db: Session = Depends(get_db), current: schemas.Account = Depends(oauth2.get_current)):
    return order.discard(id, db, current.account)
