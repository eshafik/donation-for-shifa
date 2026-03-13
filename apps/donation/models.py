from tortoise import fields, models


class Donation(models.Model):
    id                 = fields.BigIntField(pk=True)
    donor_name         = fields.CharField(max_length=255)
    transaction_number = fields.CharField(max_length=100, unique=True)
    amount             = fields.DecimalField(max_digits=12, decimal_places=2)
    date_received      = fields.DateField()
    notes              = fields.TextField(null=True)
    created_at         = fields.DatetimeField(auto_now_add=True)
    updated_at         = fields.DatetimeField(auto_now=True)
    created_by         = fields.ForeignKeyField("user.User", null=True, on_delete=fields.SET_NULL)

    class Meta:
        table = "donations"
        ordering = ["-date_received"]

    def __str__(self):
        return f"Donation({self.donor_name}, {self.amount})"
