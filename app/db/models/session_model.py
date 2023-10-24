from tortoise import fields, models


class Session(models.Model):
    session_id = fields.IntField(pk=True, generated=True)
    user_scope = fields.CharField(max_length=255,default='')
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    expiring_at = fields.DatetimeField(auto_now_add=True)
    token = fields.CharField(max_length=1000)
    user_id = fields.IntField()

    class Meta:
        table = "sessions"
