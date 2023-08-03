
from sqlalchemy.orm import Session
from order import models, schemas
from fastapi import HTTPException, status
from order.hashing import Hash


def create(request: schemas.Account, db: Session):
    new_account = models.Account(account=request.account, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def get_account(id: int, db: Session):
    account = db.query(models.Account).filter(models.Account.id == id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Account with the id {id} is not available")
    return account
