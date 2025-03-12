import jdatetime
from django import template
from acl.models import Permission

register = template.Library()


@register.simple_tag
def get_permission_id(value, arg=None):
    try:
        pk = Permission.objects.get(code=value).pk
    except:
        pk = None
    return pk


@register.simple_tag
def parse_permission(value, arg=None):
    if type(value) == list:
        value = [item.id for item in value]
    else:
        if not value:
            value = ''
        value = value.split(',')
    return value


@register.simple_tag
def parse_permission_str_list(value, arg=None):
    if type(value) == list:
        perms = [item.id for item in value]
        value = ','.join(map(str, perms))
    return value


@register.filter
def check_perm_selected(value, perm_list):
    if value in perm_list:
        return True
    return False


@register.filter(name='has_perm')
def has_permission(user, args):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True

    for permission in args.split(","):
        try:
            if user.check_has_permission(permission):
                return True
        except:
            return False
    return False
