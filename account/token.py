
# - Import password reset token generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


# - Password reset token generator method

class UserVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user_id = six.text_type(user.pk)  # user pk
        ts = six.text_type(timestamp)   # timestemp

        # by deafult user is inactive one user verify account from the link, send to email then status changed to active
        is_active = six.text_type(user.is_active)  
        return f"{user_id}{ts}{is_active}"

user_tokenizer_generate = UserVerificationTokenGenerator()



