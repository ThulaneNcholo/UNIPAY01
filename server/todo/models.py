from django.db import models

# Create your models here.


class TodoModel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    todo = models.TextField(blank=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, default='Pending')
    dueDate = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
