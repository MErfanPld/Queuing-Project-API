PERMISSIONS = []

USERS_PERMISSIONS = {
    'title': 'دسترسی کاربران',
    'permissions': [
        {'name': 'لیست کاربران', 'code': 'user_list',
            'description': 'دسترسی لیست کاربران'},
        {'name': 'افزودن کاربر', 'code': 'user_create',
            'description': 'دسترسی ساخت کاربر جدید'},
        {'name': 'ویرایش کاربر', 'code': 'user_edit',
            'description': 'دسترسی ویرایش کاربران'},
        {'name': 'حذف کاربر', 'code': 'user_delete',
            'description': 'دسترسی حذف کاربران'},
        {'name': 'تغییر رمز عبور کاربر', 'code': 'user_change_password',
         'description': 'دسترسی تغییر رمز عبور کاربران'},
    ]
}
PERMISSIONS.append(USERS_PERMISSIONS)

######################################################################

ROLES_PERMISSIONS = {
    'title': 'دسترسی نقش ها',
    'permissions': [
        {'name': 'لیست نقش ها', 'code': 'role_list',
            'description': 'دسترسی لیست نقش ها'},
        {'name': 'افزودن نقش', 'code': 'role_create',
            'description': 'دسترسی ساخت نقش جدید'},
        {'name': 'ویرایش نقش', 'code': 'role_edit',
            'description': 'دسترسی ویرایش نقش ها'},
        {'name': 'حذف نقش', 'code': 'role_delete',
            'description': 'دسترسی حذف نقش ها'},
    ]
}
PERMISSIONS.append(ROLES_PERMISSIONS)

######################################################################

RESERVATIONS_PERMISSIONS = {
    'title': 'دسترسی رزرو ها',
    'permissions': [
        {'name': 'لیست رزرو ها', 'code': 'reservations_list',
            'description': 'دسترسی لیست رزرو ها'},
        {'name': 'افزودن رزرو ها', 'code': 'reservations_create',
         'description': 'دسترسی ساخت رزرو ها جدید'},
        {'name': 'ویرایش رزرو ها', 'code': 'reservations_edit',
            'description': 'دسترسی ویرایش رزرو ها'},
        {'name': 'حذف رزرو ها', 'code': 'reservations_delete',
            'description': 'دسترسی حذف رزرو ها'},
    ]
}
PERMISSIONS.append(RESERVATIONS_PERMISSIONS)

######################################################################

REPORT_PERMISSIONS = {
    'title': 'دسترسی گزارش ها',
    'permissions': [
        {'name': 'لیست گزارش ها', 'code': 'report_list',
            'description': 'دسترسی لیست گزارش ها'},
        {'name': 'افزودن گزارش ها', 'code': 'report_create',
         'description': 'دسترسی ساخت گزارش ها جدید'},
        {'name': 'ویرایش گزارش ها', 'code': 'report_edit',
            'description': 'دسترسی ویرایش گزارش ها'},
        {'name': 'حذف گزارش ها', 'code': 'report_delete',
            'description': 'دسترسی حذف گزارش ها'},
    ]
}
PERMISSIONS.append(REPORT_PERMISSIONS)

TRANSACTION_REPORT_PERMISSIONS = {
    'title': 'دسترسی گزارش تراکنش ها',
    'permissions': [
        {'name': 'لیست گزارش تراکنش ها', 'code': 'transaction_report_list',
            'description': 'دسترسی لیست گزارش تراکنش ها'},
    ]
}
PERMISSIONS.append(TRANSACTION_REPORT_PERMISSIONS)

USERWITHDRAWAL_REPORT_PERMISSIONS = {
    'title': 'دسترسی گزارش درخواست‌های برداشت کاربر',
    'permissions': [
        {'name': 'لیست گزارش درخواست‌های برداشت کاربر', 'code': 'withdrawal_report_list',
            'description': 'دسترسی لیست گزارش درخواست‌های برداشت کاربر'},
    ]
}
PERMISSIONS.append(USERWITHDRAWAL_REPORT_PERMISSIONS)


######################################################################
WALLET_PERMISSIONS = {
    'title': 'دسترسی کیف پول ها',
    'permissions': [
        {'name': 'لیست کیف پول ها', 'code': 'wallet_list',
            'description': 'دسترسی لیست کیف پول ها'},
        {'name': 'افزودن کیف پول ها', 'code': 'wallet_create',
         'description': 'دسترسی ساخت کیف پول ها جدید'},
        {'name': 'ویرایش کیف پول ها', 'code': 'wallet_edit',
            'description': 'دسترسی ویرایش کیف پول ها'},
        {'name': 'حذف کیف پول ها', 'code': 'wallet_delete',
            'description': 'دسترسی حذف کیف پول ها'},
    ]
}
PERMISSIONS.append(WALLET_PERMISSIONS)

######################################################################
EMPLOYEE_PERMISSIONS = {
    'title': 'دسترسی کارمند ها',
    'permissions': [
        {'name': 'لیست کارمند ها', 'code': 'employee_list',
            'description': 'دسترسی لیست کارمند ها'},
        {'name': 'افزودن کارمند ها', 'code': 'employee_create',
         'description': 'دسترسی ساخت کارمند ها جدید'},
        {'name': 'ویرایش کارمند ها', 'code': 'employee_edit',
            'description': 'دسترسی ویرایش کارمند ها'},
        {'name': 'حذف کارمند ها', 'code': 'employee_delete',
            'description': 'دسترسی حذف کارمند ها'},
    ]
}
PERMISSIONS.append(EMPLOYEE_PERMISSIONS)

######################################################################
SERVICE_PERMISSIONS = {
    'title': 'دسترسی سرویس ها',
    'permissions': [
        {'name': 'لیست سرویس ها', 'code': 'service_list',
            'description': 'دسترسی لیست سرویس ها'},
        {'name': 'افزودن سرویس ها', 'code': 'service_create',
         'description': 'دسترسی ساخت سرویس ها جدید'},
        {'name': 'ویرایش سرویس ها', 'code': 'service_edit',
            'description': 'دسترسی ویرایش سرویس ها'},
        {'name': 'حذف سرویس ها', 'code': 'service_delete',
            'description': 'دسترسی حذف سرویس ها'},
    ]
}
PERMISSIONS.append(SERVICE_PERMISSIONS)

######################################################################
BUSINESS_PERMISSIONS = {
    'title': 'دسترسی کسب و کار ها',
    'permissions': [
        {'name': 'لیست کسب و کار ها', 'code': 'business_list',
            'description': 'دسترسی لیست کسب و کار ها'},
        {'name': 'افزودن کسب و کار ها', 'code': 'business_create',
         'description': 'دسترسی ساخت کسب و کار ها جدید'},
        {'name': 'ویرایش کسب و کار ها', 'code': 'business_edit',
            'description': 'دسترسی ویرایش کسب و کار ها'},
        {'name': 'حذف کسب و کار ها', 'code': 'business_delete',
            'description': 'دسترسی حذف کسب و کار ها'},
    ]
}
PERMISSIONS.append(BUSINESS_PERMISSIONS)

######################################################################
# GET_AVAILABLE_PERMISSIONS = {
#     'title': 'دسترسی ساعت‌های در دسترس ها',
#     'permissions': [
#         {'name': 'لیست ساعت‌های در دسترس ها', 'code': 'get_available_list',
#             'description': 'دسترسی لیست ساعت‌های در دسترس ها'},
#         {'name': 'افزودن ساعت‌های در دسترس ها', 'code': 'get_available_create',
#          'description': 'دسترسی ساخت ساعت‌های در دسترس ها جدید'},
#         {'name': 'ویرایش ساعت‌های در دسترس ها', 'code': 'get_available_edit',
#             'description': 'دسترسی ویرایش ساعت‌های در دسترس ها'},
#         {'name': 'حذف ساعت‌های در دسترس ها', 'code': 'get_available_delete',
#             'description': 'دسترسی حذف ساعت‌های در دسترس ها'},
#     ]
# }
# PERMISSIONS.append(GET_AVAILABLE_PERMISSIONS)

######################################################################
WORKINGHOURS_PERMISSIONS = {
    'title': 'دسترسی ساعت کاری ها',
    'permissions': [
        {'name': 'لیست ساعت کاری ها', 'code': 'working_hours_list',
            'description': 'دسترسی لیست ساعت کاری ها'},
        {'name': 'افزودن ساعت کاری ها', 'code': 'working_hours_create',
         'description': 'دسترسی ساخت ساعت کاری ها جدید'},
        {'name': 'ویرایش ساعت کاری ها', 'code': 'working_hours_edit',
            'description': 'دسترسی ویرایش ساعت کاری ها'},
        {'name': 'حذف ساعت کاری ها', 'code': 'working_hours_delete',
            'description': 'دسترسی حذف ساعت کاری ها'},
    ]
}
PERMISSIONS.append(WORKINGHOURS_PERMISSIONS)


######################################################################
PACKAGE_PERMISSIONS = {
    'title': 'دسترسی پکیچ ها',
    'permissions': [
        {'name': 'لیست پکیچ ها', 'code': 'packages_list',
            'description': 'دسترسی لیست پکیچ ها'},
        {'name': 'افزودن پکیچ ها', 'code': 'packages_create',
         'description': 'دسترسی ساخت پکیچ ها جدید'},
        {'name': 'ویرایش پکیچ ها', 'code': 'packages_edit',
            'description': 'دسترسی ویرایش پکیچ ها'},
        {'name': 'حذف پکیچ ها', 'code': 'packages_delete',
            'description': 'دسترسی حذف پکیچ ها'},
    ]
}
PERMISSIONS.append(PACKAGE_PERMISSIONS)

######################################################################
TIME_SLOT_PERMISSIONS = {
    'title': 'دسترسی ساعت رزرو ها',
    'permissions': [
        {'name': 'لیست ساعت رزرو ها', 'code': 'time_slot_list',
            'description': 'دسترسی لیست ساعت رزرو ها'},
        {'name': 'افزودن ساعت رزرو ها', 'code': 'time_slot_create',
         'description': 'دسترسی ساخت ساعت رزرو ها جدید'},
        {'name': 'ویرایش ساعت رزرو ها', 'code': 'time_slot_edit',
            'description': 'دسترسی ویرایش ساعت رزرو ها'},
        {'name': 'حذف ساعت رزرو ها', 'code': 'time_slot_delete',
            'description': 'دسترسی حذف ساعت رزرو ها'},
    ]
}
PERMISSIONS.append(TIME_SLOT_PERMISSIONS)

######################################################################
SLIDER_PERMISSIONS = {
    'title': 'دسترسی اسلایدر ها',
    'permissions': [
        {'name': 'لیست اسلایدر ها', 'code': 'slider_list',
            'description': 'دسترسی لیست اسلایدر ها'},
        {'name': 'افزودن اسلایدر ها', 'code': 'slider_create',
         'description': 'دسترسی ساخت اسلایدر ها جدید'},
        {'name': 'ویرایش اسلایدر ها', 'code': 'slider_edit',
            'description': 'دسترسی ویرایش اسلایدر ها'},
        {'name': 'حذف اسلایدر ها', 'code': 'slider_delete',
            'description': 'دسترسی حذف اسلایدر ها'},
    ]
}
PERMISSIONS.append(SLIDER_PERMISSIONS)

######################################################################
NUM_CARD_PERMISSIONS = {
    'title': 'دسترسی شماره کارت ها',
    'permissions': [
        {'name': 'لیست شماره کارت ها', 'code': 'num_card_list',
            'description': 'دسترسی لیست شماره کارت ها'},
        {'name': 'افزودن شماره کارت ها', 'code': 'num_card_create',
         'description': 'دسترسی ساخت شماره کارت ها جدید'},
        {'name': 'ویرایش شماره کارت ها', 'code': 'num_card_edit',
            'description': 'دسترسی ویرایش شماره کارت ها'},
        {'name': 'حذف شماره کارت ها', 'code': 'num_card_delete',
            'description': 'دسترسی حذف شماره کارت ها'},
    ]
}
PERMISSIONS.append(SLIDER_PERMISSIONS)

######################################################################

USER_PERMISSIONS_PERMISSIONS = {
    'title': 'دسترسی دسترسی کاربر ها',
    'permissions': [
        {'name': 'لیست دسترسی کاربر ها', 'code': 'user_permissions_list',
            'description': 'دسترسی لیست دسترسی کاربر ها'},
        {'name': 'افزودن دسترسی کاربر ها', 'code': 'user_permissions_create',
         'description': 'دسترسی ساخت دسترسی کاربر ها جدید'},
        {'name': 'ویرایش دسترسی کاربر ها', 'code': 'user_permissions_edit',
         'description': 'دسترسی ویرایش دسترسی کاربر ها'},
        {'name': 'حذف دسترسی کاربر ها', 'code': 'user_permissions_delete',
            'description': 'دسترسی حذف دسترسی کاربر ها'},
    ]
}
PERMISSIONS.append(USER_PERMISSIONS_PERMISSIONS)


######################################################################


def filter_permissions(permissions, codes):
    filtered_permissions = []
    for permission_category in permissions:
        filtered_category = {
            'title': permission_category['title'],
            'permissions': [p for p in permission_category['permissions'] if p['code'] in codes]
        }
        if filtered_category['permissions']:
            filtered_permissions.append(filtered_category)
    return filtered_permissions


######################################################################


class ROLE_CODES:
    ALL_ADMIN = "all_admin"
    BUSINESS_MANAGER = "business_manager"
    CUSTOMER = "customer"
