from tortoise import fields, models


class DonationDistribution(models.Model):
    id                  = fields.BigIntField(pk=True)
    recipient_name      = fields.CharField(max_length=255)
    address             = fields.TextField()
    problem_description = fields.TextField()
    amount_received     = fields.DecimalField(max_digits=12, decimal_places=2)
    date_distributed    = fields.DateField()
    notes               = fields.TextField(null=True)
    created_at          = fields.DatetimeField(auto_now_add=True)
    updated_at          = fields.DatetimeField(auto_now=True)
    created_by          = fields.ForeignKeyField("user.User", null=True, on_delete=fields.SET_NULL)

    class Meta:
        table = "donation_distributions"
        ordering = ["-date_distributed"]

    def __str__(self):
        return f"Distribution({self.recipient_name}, {self.amount_received})"
