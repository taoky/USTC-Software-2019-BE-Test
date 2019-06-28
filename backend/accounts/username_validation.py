
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ConflictUsernameValidator:
    @staticmethod
    def validate(username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')


class SpecialSymbolValidator:
    @staticmethod
    def validate(username):
        if not re.search(u'^[_0-9a-zA-Z]+$', username):
            raise ValidationError('Username can not contain special symbol')


class NoneTypeObjectValidator:
    @staticmethod
    def validate(username):
        if (not username) or (username == ''):
            raise ValidationError('Please input the username')


username_validators = [
    NoneTypeObjectValidator,
    ConflictUsernameValidator,
    SpecialSymbolValidator
]


def validate_username(username, check_conflict):
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
