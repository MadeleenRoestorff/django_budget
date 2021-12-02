from django.db import models
from django.db.models.signals import post_save


class Budget(models.Model):
    """Monthly Budgets"""
    timestamp_created_server = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    timestamp_updated_server = models.DateTimeField(
        auto_now=True, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    expenses_list = models.JSONField(null=True, blank=True)
    income_in_cents = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        print("we can process data here before saving")
        # Save self as the normal save method would
        super(Budget, self).save(*args, **kwargs)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        print("we can run side effects here after saving")


##### connect signal functions ################################################
post_save.connect(
    Budget.post_save,
    Budget,
    dispatch_uid="ek_hou_daarvan_om_budget_hier_te_skryf.models.Budget"
)


class Expense(models.Model):
    """Monthly expenses"""
    timestamp_created_server = models.DateTimeField(auto_now_add=True)
    timestamp_updated_server = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    linked_budget_id = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=60, null=True, blank=True)
    description = models.CharField(max_length=60, null=True, blank=True)
    value_in_cents = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.description:
            self.description = self.category

        if self.id:
            prev_version = Expense.objects.get(id=self.id)
            if self.linked_budget_id != prev_version.linked_budget_id:
                budget_instance = Budget.objects.get(
                    id=prev_version.linked_budget_id
                )
                list_of_expense_ids = budget_instance.expenses_list

                if type(list_of_expense_ids) is list:
                    try:
                        while True:
                            list_of_expense_ids.remove(self.id)
                    except:
                        pass
                    budget_instance.expenses_list = sorted(
                        set(list_of_expense_ids)
                    )
                    budget_instance.save()

        # Save self as the normal save method would
        super(Expense, self).save(*args, **kwargs)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):

        budget_instance = Budget.objects.get(id=instance.linked_budget_id)
        list_of_expense_ids = budget_instance.expenses_list

        if type(list_of_expense_ids) is not list:
            list_of_expense_ids = []

        if instance.id not in list_of_expense_ids:
            list_of_expense_ids.append(instance.id)
            budget_instance.expenses_list = sorted(
                set(list_of_expense_ids)
            )
            budget_instance.save()


##### connect signal functions ################################################
post_save.connect(
    Expense.post_save,
    Expense,
    dispatch_uid="ek_hou_daarvan_om_budget_hier_te_skryf.models.Expense"
)
