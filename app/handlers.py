from app.models import User, MagicLinkAuth


class UserHandler:
    _user = None

    def __init__(self, email):
        self._user = self._create_or_get_by_email(email)

    def _create_or_get_by_email(self, email):
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist as e:
            user = User(email=email)
            user.save()

        return user

    def get_user(self):
        return self._user


class MagicLinkHandler:
    magic_link_auth = None

    def __init__(self, magic_link_auth):
        assert isinstance(magic_link_auth, MagicLinkAuth)

        self.magic_link_auth = magic_link_auth

    def generate_link(self):
        token = self.magic_link_auth.generate_token()
        self.magic_link_auth.save()

        return token

    def revoke_link(self):
        self.magic_link_auth.remove_access()
        self.magic_link_auth.save()

    def validate(self):
        return self.magic_link_auth.is_active

    def get_info(self):
        self.magic_link_auth.increase_counter()
        self.magic_link_auth.save()
        return {'count': self.magic_link_auth.get_counter()}
