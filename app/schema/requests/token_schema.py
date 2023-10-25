from datetime import datetime, timedelta,timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
import pytz

class TokenRequest:
    def __init__(self, form_data: OAuth2PasswordRequestForm = Depends()):
        self.username = form_data.username
        self.password = form_data.password
        self.issued_time = datetime.now(timezone.utc)

        self.expiration_time = datetime.now(timezone.utc) + timedelta(hours=3)
        # utc_now = datetime.utcnow()
        # timezone = pytz.timezone("Asia/Calcutta")
        # self.issued_time = utc_now.replace(tzinfo=pytz.utc).astimezone(timezone)
        # self.expiration_time = self.issued_time + timedelta(hours=8)