from django.db import models


class Documents(models.Model):
    id_uniq = models.AutoField(primary_key=True, verbose_name='Идентификатор документа')
    title = models.CharField('Document_name', max_length=25)
    document = models.FileField('Document_file', upload_to='uploads/pdf')
    interpretation_pdf = models.FileField('Document_pdf', upload_to='predict/pdf', null=True)
    interpretation_html = models.FileField('Document_html', upload_to='predict/html', null=True)
    interpretation_confidence = models.FloatField('Confidence')
    interpretation_class = models.CharField('Class')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
