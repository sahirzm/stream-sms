from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, mobile, password=None):

        if not email:
            raise ValueError('Email is required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, mobile, password=None):

        if not email:
            raise ValueError('Email is required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile
            )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user
