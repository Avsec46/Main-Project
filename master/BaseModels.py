from django.db import models


class BaseModel(models.Model):
    code = models.CharField(max_length=50,null=True,blank=True)
    name_en = models.CharField(max_length=50)
    name_lc = models.CharField(max_length=50,null=True,blank=True)
    display_order = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['display_order']

    def __str__(self):
        return self.name_en