from django.db import models
from django.utils.translation import gettext_lazy as _

class Fan_speed(models.Model):
    ID = models.BigAutoField(_("ID"), primary_key=True)
    time = models.CharField(_("time"), max_length=50)
    value = models.CharField(_("value"), max_length=50)
    serverroom_temperature = models.CharField(_("serverroom_temperature"), max_length=50)
    softwareroom_temperature = models.CharField(_("softwareroom_temperature"), max_length=50)
    serverroom_humidity = models.CharField(_("serverroom_humidity"), max_length=50)

    def save(self, *args, **kwargs):
        import time
        unix_time = str(round(time.time()))
        self.time = unix_time
        return super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.value} at {self.time}'