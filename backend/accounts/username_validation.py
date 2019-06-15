
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ConflictUsernameValidator:
    @staticmethod
    def validate(username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exisis')


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
    ConflictUsernameValidator,
    SpecialSymbolValidator,
    NoneTypeObjectValidator
]

username_validators_without_conflict_check = [
    SpecialSymbolValidator,
    NoneTypeObjectValidator
]


def validate_username(username, check_conflict):
    errors = []
    if check_conflict:
        validators = username_validators
    else:
        validators = username_validators_without_conflict_check
    for validator in validators:
        try:
            validator.validate(username)
        except ValidationError as error:
            errors.append(error)

    if errors:
        raise ValidationError(errors)
