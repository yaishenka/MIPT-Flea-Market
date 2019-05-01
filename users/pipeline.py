from django.contrib.auth import logout
USER_FIELDS = ['username']

def create_user_by_social(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    fields['is_verified'] = True
    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }

def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(kwargs['request'])
        user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': social is None}

def save_user(backend, user, response, *args, **kwargs):
    if (not user.is_verified):
        user.is_verified = True
        user.save()
    return
