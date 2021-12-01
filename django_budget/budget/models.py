from django.db import models
from django.db.models.signals import post_save


class FixedExpenses(models.Model):
    timestamp_created_server = models.DateTimeField(auto_now_add=True)
    timestamp_updated_server = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    expense_name = models.CharField(max_length=60, null=True, blank=True)
    expence_in_cents = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        print("we can process data here before saving")
        # Save self as the normal save method would
        super(FixedExpenses, self).save(*args, **kwargs)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        print("we can run side effects here after saving")


##### connect signal functions ################################################
post_save.connect(
    FixedExpenses.post_save,
    FixedExpenses,
    dispatch_uid="ek_hou_daarvan_om_budget_hier_te_skryf.models.FixedExpenses"
)


class Necessities(models.Model):
    timestamp_created_server = models.DateTimeField(auto_now_add=True)
    timestamp_updated_server = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    expense_name = models.CharField(max_length=60, null=True, blank=True)
    budgeted_expense_in_cents = models.IntegerField(null=True, blank=True)
    actual_expense_in_cents = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        print("we can process data here before saving")
        # Save self as the normal save method would
        super(Necessities, self).save(*args, **kwargs)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        print("we can run side effects here after saving")


##### connect signal functions ################################################
post_save.connect(
    Necessities.post_save,
    Necessities,
    dispatch_uid="ek_hou_daarvan_om_budget_hier_te_skryf.models.Necessities"
)
