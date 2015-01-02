from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    file = models.CharField(max_length=200)

    def __str__(self):
        return "Name:{0} pub_date:{1} file:{2}".format(self.name, self.pub_date, self.file)

