from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.utils.translation import gettext_lazy as _

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def __init__(self, user_attributes=None, max_similarity=0.7, message=None):
        self.user_attributes = user_attributes or ['username', 'first_name', 'last_name', 'email']
        self.max_similarity = max_similarity
        self.message = message or _('رمز عبور نباید مشابه اطلاعات شخصی شما باشد.')

    def validate(self, password, user=None):
        super().validate(password, user)

    def get_help_text(self):
        return self.message
