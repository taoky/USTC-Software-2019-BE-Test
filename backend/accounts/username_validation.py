
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ConflictUsernameValidator:
    def validate(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exisis')


class SpecialSymbolValidator:
    def validate(self, username):
        if not re.search(u'^[_0-9a-zA-Z]+$', username):
            raise ValidationError('Username can not contain special symbol')


username_validators = [
    ConflictUsernameValidator,
    SpecialSymbolValidator
]

username_validators_no_conflict_check = [
    SpecialSymbolValidator
]


def validate_username(username, check_conflict):
    errors = []
    if check_conflict:
        validators = username_validators
    else:
        validators = username_validators_no_conflict_check
    for validator in validators:
        try:
            validator.validate(username)
        except ValidationError as error:
            errors.append(error)

    if errors:
        raise ValidationError(errors)
