from django.db import models

class PageActiveTime(models.Model):
    class Meta:
        unique_together = (("user_id","page_id","last_updated_timestamp"),)
        ordering = ["last_updated_timestamp"]
        index_together = [   ["user_id", "page_id","page_title","last_updated_timestamp"], ]

    user_id = models.CharField(max_length=500)
    page_id = models.CharField(max_length=500)
    page_title = models.CharField(max_length=500)
    base_url = models.CharField(max_length=500)
    cumulative_time = models.IntegerField(default =0)
    icon_url = models.CharField(max_length=500)
    last_updated_timestamp = models.DateTimeField(auto_now=True)
    page_content = models.TextField(default="")
    is_active = models.IntegerField(default =1)
    is_deleted = models.IntegerField(default =0)

    def __str__(self):
        return self.page_id

class BlackListedPages(models.Model):
    class Meta:
        index_together = [   ["user_id", "base_url"], ]
        unique_together = (("user_id","base_url"),)

    user_id = models.CharField(max_length=500)
    base_url = models.CharField(max_length=500)

class UserDetails(models.Model):
    class Meta:
        unique_together = (("user_id","password","email"),)
        index_together = [["email","password"]]

    user_id = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default =1)
    is_deleted = models.IntegerField(default =0)