from django.db import models


class User(models.Model):
    email = models.CharField(max_length=320, unique=True) #stated by rfc


class MagicLinkAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.BigIntegerField(default=0)
    token = models.CharField(max_length=36, unique=True)
    is_active = models.BooleanField(default=True)

    def increase_counter(self):
        self.counter += 1

    def get_counter(self):
        return self.counter

    def remove_access(self):
        self.is_active = False

    def grand_access(self):
        self.is_active = True

    def generate_token(self):
        import uuid

        self.token = uuid.uuid4()
        return self.token
