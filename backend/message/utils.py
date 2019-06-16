from django.core.exceptions import ValidationError


class MessageInfoClean():
    def content_clean(self, content):
        if len(content) > 255:
            raise ValidationError({
                'error_code': '211',
                'message': 'too long content'
            })
        if len(content) <= 0:
            raise ValidationError({
                'error_code': '212',
                'message': 'content can not be blank'
            })

    def hidden_seconds_clean(self, hidden_seconds):
        if hidden_seconds < 0:
            raise ValidationError({
                'error_code': '221',
                'message': 'hidden secoonds can not be minus'
            })

    def message_send_clean(self, message_info):
        cleaned_attr = ('hidden_seconds', 'content')
        for attr in cleaned_attr:
            try:
                getattr(self, attr + '_clean')(message_info[attr])
            except AttributeError:
                raise ValidationError({
                    'error_code': '001',
                    'message': 'except attribute: %s' % attr
                })
