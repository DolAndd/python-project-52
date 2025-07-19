def get_username(strategy, details, user=None, *args, **kwargs):
    if not user:
        email = details.get('email', '')
        if email:
            return {'username': email.split('@')[0]}
        else:
            return {'username': f"yandex_{kwargs['uid']}"}