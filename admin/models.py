from django.db import models


class Page(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    title = models.TextField(db_column='Title')
    route = models.TextField(db_column='Route', unique=True)
    template = models.TextField(db_column='Template')

    class Meta:
        managed = True
        db_table = 'Page'
