from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from order import models, schemas


def get_orders(db: Session, current_acct):
    account = db.query(models.Account).filter(and_(models.Account.account == current_acct)).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    orders = db.query(models.Order).filter(and_(models.Order.account_id == account.id))
    return orders


def get_order(id: int, db: Session, current_acct):
    account = db.query(models.Account).filter(and_(models.Account.account == current_acct)).first()
    order = db.query(models.Order).filter(and_(models.Order.id == id, models.Order.account_id == account.id)).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")
    return order


def create(request: schemas.Order, db: Session, current_acct):
    account = db.query(models.Account).filter(and_(models.Account.account == current_acct)).first()
    new_order = models.Order(
        order_type=request.order_type,
        symbol=request.symbol,
        volume=request.volume,
        account_id=account.id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def update(id: int, request: schemas.Order, db: Session, current_acct):
    account = db.query(models.Account).filter(and_(models.Account.account == current_acct)).first()
    order = db.query(models.Order).filter(and_(models.Order.id == id, models.Order.account_id == account.id))
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")

    update_dict = {
        "id": id,
        "account_id": account.id,
        "order_type": request.order_type,
        "symbol": request.symbol,
        "volume": request.volume
    }

    order.update(update_dict)
    db.commit()
    return 'updated'


def discard(id: int, db: Session, current_acct):
    account = db.query(models.Account).filter(and_(models.Account.account == current_acct)).first()
    order = db.query(models.Order).filter(and_(models.Order.id == id, models.Order.account_id == account.id))

    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")

    order.delete(synchronize_session=False)
    db.commit()
    return 'deleted'
