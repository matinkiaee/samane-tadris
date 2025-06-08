


def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

def is_group_manager(user):
    return user.is_authenticated and user.role == 'group_manager'

def is_security(user):
    return user.is_authenticated and user.role == 'security'

def is_province_admin(user):
    return user.is_authenticated and user.role == 'province_admin'