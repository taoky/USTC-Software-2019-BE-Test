
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

User = get_user_model()


class ConflictUsernameValidator:
    '''
    检查用户名是否已经存在
    '''
    @staticmethod
    def validate(username):
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('Username already exists'))


class SpecialSymbolValidator:
    '''
    检查用户名中是否包含除了字母、数字、下划线以外的字符
    '''
    @staticmethod
    def validate(username):
        if not re.search(u'^[_0-9a-zA-Z]+$', username):
            raise ValidationError(_('Username can not contain special symbol'))


class NoneTypeObjectValidator:
    '''
    检查用户提交的数据中是否包含用户名
    '''
    @staticmethod
    def validate(username):
        if (not username) or (username == ''):
            raise ValidationError(_('Please input the username'))


username_validators = [
    ConflictUsernameValidator,
    SpecialSymbolValidator
]


def validate_username(username, check_conflict):
    '''
    检查用户名是否合法
    @param:
        username<str>:  用户提交的数据中的用户名
        check_conflict<bool>:   是否检查用户名已存在，在注册账户时请打开此开关
    '''
    try:
        NoneTypeObjectValidator.validate(username)
    except ValidationError as e:
        raise ValidationError([e])
    errors = []
    validators = username_validators.copy()
    if not check_conflict:
        validators.remove(ConflictUsernameValidator)
    for validator in validators:
        try:
            validator.validate(username)
        except ValidationError as error:
            errors.append(error)

    if errors:
        raise ValidationError(errors)
