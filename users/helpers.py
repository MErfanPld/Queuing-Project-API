from django.core.exceptions import ValidationError


def check_user_exist(user, new_phone):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    exists_user = User.objects.filter(phone=new_phone).first()
    if exists_user and exists_user.phone != user.phone:
        raise ValidationError([
            ValidationError(
                'کاربری با این موبایل قبلا ثبت شده است!', code='duplicate'),
        ])
