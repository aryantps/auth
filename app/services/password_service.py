import bcrypt


class PasswordService:
    @staticmethod
    def get_hashed_password(plain_text_password):
        hashed_password = bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))