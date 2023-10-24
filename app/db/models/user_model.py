from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True, generated=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    is_blocked = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)
    provider = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)

    class Meta:
        table = "users"
