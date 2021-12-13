from typing import Dict
from django.db import models
from django.db.models.signals import post_save
from datetime import datetime
import django_budget.utils as utils


class Budget(models.Model):
    """Monthly Budgets with linked expense instances"""
    timestamp_created_server = models.DateTimeField(auto_now_add=True)
    # Automatic create a timestamp when an expense instance is created

    timestamp_updated_server = models.DateTimeField(auto_now=True)
    # Automatic create a timestamp when an expense instance is updated

    timestamp = models.DateTimeField(null=True, blank=True)
    # User defined timestamp. Required

    expenses_list = models.JSONField(null=True, blank=True)
    # List of expenses linked to this budget

    income_in_cents = models.JSONField(null=True, blank=True)
    # User defined monthly income name and income value

    fixed_expenses = models.JSONField(null=True, blank=True)
    # User defined fixed monthly expenses (Name and value)

    variable_expenses = models.JSONField(null=True, blank=True)
    # User defined monthly budgeted expenses (category and value)

    total_remaining_in_cents = models.IntegerField(null=True, blank=True)
    # Automatically calculated total based on income, fixed and actual expenses

    remaining_by_category_in_cents = models.JSONField(null=True, blank=True)
    # Automatically calculated category totals based on budgeted and actual variable expenses

    remaining_this_week_in_cents = models.IntegerField(null=True, blank=True)
    # Automatically calculated total based on budgeted and actual variable expenses for curent week

    left_over_inbudget_in_cents = models.IntegerField(null=True, blank=True)
    # Automatically calculated total to help see if budgeted is not more than income - fixed expenses

    def save(self, *args, **kwargs):

        income_total = 0
        for person_income in self.income_in_cents:
            income_total += self.income_in_cents[person_income]

        fixed_expenses_total = 0
        for fixed_expense in self.fixed_expenses:
            fixed_expenses_total -= self.fixed_expenses[fixed_expense]

        # Get a list of all the expenses linked to this budget with certain fields
        expenses_for_budget_instance = {}
        if type(self.expenses_list) is list:
            try:
                expenses_for_budget_instance = Expense.objects.filter(
                    id__in=self.expenses_list).values("timestamp", "category", "value_in_cents")
            except:
                pass

        weeks_in_month = utils.week_in_month(self.timestamp, True)
        current_week = utils.week_in_month(datetime.now())

        self.total_remaining_in_cents = income_total + fixed_expenses_total
        self.remaining_by_category_in_cents = {}
        self.left_over_inbudget_in_cents = income_total + fixed_expenses_total
        self.remaining_this_week_in_cents = 0

        for variable_expense in self.variable_expenses:
            self.variable_expenses[variable_expense]["actual"] = 0
            self.remaining_this_week_in_cents += (
                self.variable_expenses[variable_expense]["budgeted"])/weeks_in_month
            try:
                for expense in expenses_for_budget_instance:
                    if expense["category"].casefold().strip() == variable_expense.casefold().strip():
                        self.variable_expenses[variable_expense]["actual"] += expense["value_in_cents"]

                    if current_week == utils.week_in_month(expense["timestamp"]):
                        self.remaining_this_week_in_cents -= expense["value_in_cents"]
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
    # User defined timestamp. Required

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
        except:
            pass


##### connect signal functions ################################################
post_save.connect(
    Expense.post_save,
    Expense,
    dispatch_uid="ek_hou_daarvan_om_budget_hier_te_skryf.models.Expense"
)
