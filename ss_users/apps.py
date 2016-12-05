from django.apps import AppConfig
from django.contrib.contenttypes.management import update_contenttypes
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate
from django.apps import apps as django_apps
from django.conf import settings

class SsUsersConfig(AppConfig):
    name = 'ss_users'
    ran = False

    def ready(self):
        if SsUsersConfig.ran:
            print("Got duplicate ready signal...")
        else:
            SsUsersConfig.ran = True
            print("registering post_migrate callback for permissions")
            if settings.DEBUG:
                post_migrate.connect(self.permissions_callback, sender=self)

    def permissions_callback(self, sender, **kwargs):
        from guardian.shortcuts import assign_perm
        from guardian.exceptions import NotUserNorGroup
        from ss_users.models import UserRoles
        permissions = {
        }
        saved_grps = {}
        grp_users = {
            'user': []
        }
        print("Loading groups into database...")
        group = django_apps.get_model('auth', 'Group')
        for role in UserRoles:
            grp = group.objects.get_or_create(name=role.value)
            saved_grps[role.value] = grp
        print("Loading groups completed...")
        print("Loading permission into database...")
        permission = django_apps.get_model('auth', 'Permission')
        for k, groups in permissions.items():
            app, perm = k.split(".")
            try:
                permission.objects.get(codename=perm)
            except permission.DoesNotExist:
                update_contenttypes(django_apps.get_app_config(app), django_apps.get_models())
                create_permissions(django_apps.get_app_config(app), django_apps.get_models(), 0)
            for grp in groups:
                try:
                    assign_perm(k, saved_grps[grp])
                except NotUserNorGroup as ex:
                    print("add permission: {}".format(ex))

        print("Loading permission completed...")
        print("Assigning users groups...")
        user = django_apps.get_model('ss_users', 'User')
        for k, users in grp_users.items():
            for user_id in users:
                usr = user.objects.get(pk=user_id)
                usr.groups.add(saved_grps[k])

        print("Assigning users groups completed...")
