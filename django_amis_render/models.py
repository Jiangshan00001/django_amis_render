from django.db import models


# Create your models here.

class AmisRenderList(models.Model):
    page_url = models.TextField(blank=True, null=True, help_text='')
    file_path = models.TextField(blank=True, null=True, help_text='')
    html_template = models.TextField(blank=True, null=True, help_text='')
    json_file_url = models.TextField(blank=True, null=True, help_text='')
    file_type = models.TextField(blank=True, null=True, help_text='supported file type: json or html')

    class Meta:
        managed = True
        verbose_name_plural = 'AMIS-PAGE'
        db_table = 'amis_render_list'
