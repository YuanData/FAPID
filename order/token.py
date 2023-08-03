import configparser
from datetime import datetime, timedelta

from jose import JWTError, jwt

from order import schemas

config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['JWT']['SECRET_KEY']
ALGORITHM = config['JWT']['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(config['JWT']['ACCESS_TOKEN_EXPIRE_MINUTES'])


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        acct: str = payload.get("acct")
        if acct is None:
            raise credentials_exception
        token_data = schemas.TokenData(account=acct)
        return token_data
    except JWTError:
        raise credentials_exception
