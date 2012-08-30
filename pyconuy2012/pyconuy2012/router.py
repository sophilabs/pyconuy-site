class Router(object):
    pass
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'users'
        return None

    def allow_syncdb(self, db, model):
        if db == 'users':
            return False
        #contenttype fails if auth table does not exist
        elif model._meta.app_label == 'auth':
            return False
        return None


    def allow_relation(self, obj1, obj2, **hints):
        return True
        """
