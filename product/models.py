from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

class Product(models.Model):
    user = models.ForeignKey("users.Customuser", verbose_name=_(""), on_delete=models.CASCADE)
    tag = models.CharField(_("Tag"), max_length=50)

    def __str__(self):
        return str(self.user) +" ======> " + self.tag
