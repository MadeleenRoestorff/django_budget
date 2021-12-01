from django.db import models
from django.db.models.signals import post_save


class FuelLog(models.Model):
    timestamp_created_server = models.DateTimeField(auto_now_add=True)
    timestamp_updated_server = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    liters = models.IntegerField(null=True, blank=True)
    price_in_cent = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        print("we can process data here before saving")
        # Save self as the normal save method would
        super(FuelLog, self).save(*args, **kwargs)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        print("we can run side effects here after saving")


##### connect signal functions ################################################
post_save.connect(
    FuelLog.post_save,
    FuelLog,
    dispatch_uid="ek_hou_daarvan_om_logger_hier_te_skryf.models.FuelLog"
)
