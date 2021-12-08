from typing import Dict
from django.db import models
from django.db.models.signals import post_save
from math import ceil
from datetime import datetime, date


class Budget(models.Model):
    """Monthly Budgets with linked expense instances"""
    timestamp_created_server = models.DateTimeField(auto_now_add=True)
    timestamp_updated_server = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    expenses_list = models.JSONField(null=True, blank=True)
    income_in_cents = models.JSONField(null=True, blank=True)
    fixed_expenses = models.JSONField(null=True, blank=True)
    variable_expenses = models.JSONField(null=True, blank=True)
    total_remaining_in_cents = models.IntegerField(null=True, blank=True)
    remaining_by_category_in_cents = models.JSONField(null=True, blank=True)
    remaining_this_week_in_cents = models.IntegerField(null=True, blank=True)
    left_over_inbudget_in_cents = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):

        # Week begins on monday isoweekday vs weekday
        days_in_month = 31
        try:
            days_in_month = date(self.timestamp.year, self.timestamp.month, 1) - \
                date(self.timestamp.year, self.timestamp.month + 1, 1)
        except:
            pass
        weeks_in_month = ceil(
            (date(datetime.now().year, datetime.now().month,
                  1).weekday()+days_in_month)/7
        )

        current_week = ceil(
            (date(datetime.now().year, datetime.now().month,
                  1).weekday()+datetime.now().day)/7
        )

        income_total = 0
        for person_income in self.income_in_cents:
            income_total += self.income_in_cents[person_income]

        fixed_expenses_total = 0
        for fixed_expense in self.fixed_expenses:
            fixed_expenses_total -= self.fixed_expenses[fixed_expense]

        expenses_for_budget_instance = {}
        if type(self.expenses_list) is list:
            expenses_for_budget_instance = Expense.objects.filter(
                id__in=self.expenses_list).values("timestamp", "category", "value_in_cents")

        self.remaining_by_category_in_cents = {}
        self.left_over_inbudget_in_cents = income_total + fixed_expenses_total
        self.remaining_this_week_in_cents = 0
        self.total_remaining_in_cents = income_total + fixed_expenses_total

        for variable_expense in self.variable_expenses:
            self.variable_expenses[variable_expense]["actual"] = 0
            self.remaining_this_week_in_cents += (
                self.variable_expenses[variable_expense]["budgeted"])/weeks_in_month
            try:
                for expense in expenses_for_budget_instance:
                    expense_timestamp = expense["timestamp"]
                    expense_category = expense["category"]
                    expense_value_in_cents = expense["value_in_cents"]
                    if expense_category.casefold().strip() == variable_expense.casefold().strip():
                        self.variable_expenses[variable_expense]["actual"] += expense_value_in_cents

                    expense_week = ceil(
                        (date(expense_timestamp.year, expense_timestamp.month,
                         1).weekday()+expense_timestamp.day)/7
                    )

                    if current_week == expense_week:
                        self.remaining_this_week_in_cents -= expense_value_in_cents

            except:
                pass

            self.total_remaining_in_cents -= self.variable_expenses[variable_expense]["actual"]
            self.left_over_inbudget_in_cents -= self.variable_expenses[variable_expense]["budgeted"]
            self.remaining_by_category_in_cents[variable_expense] = self.variable_expenses[
                variable_expense]["budgeted"] - self.variable_expenses[variable_expense]["actual"]

        # Save self as the normal save method would
        super(Budget, self).save(*args, **kwargs)

    @ staticmethod
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
    # Automatic create a timestamp when an expense instance is created

    timestamp_updated_server = models.DateTimeField(auto_now=True)
    # Automatic create a timestamp when an expense instance is updated

    timestamp = models.DateTimeField(null=True, blank=True)
    # User defined timestamp

    linked_budget_id = models.IntegerField(null=True, blank=True)
    # User selected monthly budget instance to link to this expense

    category = models.CharField(max_length=60, null=True, blank=True)
    # User defined expense category

    description = models.CharField(max_length=60, null=True, blank=True)
    # User defined expense description

    value_in_cents = models.IntegerField(null=True, blank=True)
    # User defined expense value

    def save(self, *args, **kwargs):

        # If now description is given use the category as the description
        if not self.description:
            self.description = self.category

        # Remove links to previous linked budget
        # get the previous id of the linked budget in the database
        # remove the current instanse expense id
        if self.id:
            prev_ver = Expense.objects.get(id=self.id)
            try:

                # check that current instance linked budget id is not equal to previous expense linked budget id
                if self.linked_budget_id != prev_ver.linked_budget_id:
                    prev_budget_instance = Budget.objects.get(
                        id=prev_ver.linked_budget_id
                    )

                    list_of_expense_ids = prev_budget_instance.expenses_list

                    if type(list_of_expense_ids) is list:
                        try:
                            while True:
                                list_of_expense_ids.remove(self.id)
                        except:
                            pass
                        prev_budget_instance.expenses_list = sorted(
                            set(list_of_expense_ids)
                        )
                        prev_budget_instance.save()

                # if type(prev_budget_instance.variable_expenses) is dict and prev_ver.category in prev_budget_instance.variable_expenses:
                #     dict_of_prev_budget_category = prev_budget_instance.variable_expenses[
                #         prev_ver.category]
                #     if type(dict_of_prev_budget_category) is dict:
                #         dict_of_prev_budget_category["actual"] -= prev_ver.value_in_cents
                #         prev_budget_instance.save()

            except:
                pass

        # Save self as the normal save method would
        super(Expense, self).save(*args, **kwargs)

    @ staticmethod
    def post_save(sender, instance, created, **kwargs):

        try:
            # Use linked_budget_id to link expense to a budget
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

            # if type(budget_instance.variable_expenses) is dict and instance.category in budget_instance.variable_expenses:
            #     dict_of_instance_budget_category = budget_instance.variable_expenses[
            #         instance.category]
            #     if type(dict_of_instance_budget_category) is dict:
            #         dict_of_instance_budget_category["actual"] += instance.value_in_cents
            #         budget_instance.save()

        except:
            pass


##### connect signal functions ################################################
post_save.connect(
    Expense.post_save,
    Expense,
    dispatch_uid="ek_hou_daarvan_om_budget_hier_te_skryf.models.Expense"
)
