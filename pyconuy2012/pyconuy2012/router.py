
class Router(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'users'
        return None

    def allow_syncdb(self, db, model):
        if db == 'users':
            return False
        elif model._meta.app_label == 'auth':
            return False
        return None