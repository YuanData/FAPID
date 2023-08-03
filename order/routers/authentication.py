from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from order import schemas, database, models, token
from order.hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    account = db.query(models.Account).filter(
        models.Account.account == request.username).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(account.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"acct": account.account})
    return {"access_token": access_token, "token_type": "bearer"}
