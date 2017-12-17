class AppRouter(object):
    def db_for_read(self, model, **hints):
        "Point all operations on frontend models to 'primary'"
        if model._meta.app_label == 'frontend':
            return 'primary'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on frontend models to 'primary'"
        if model._meta.app_label == 'frontend':
            return 'primary'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in frontend app"
        if obj1._meta.app_label == 'frontend' and obj2._meta.app_label == 'frontend':
            return True
        # Allow if neither is frontend app
        elif 'frontend' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_syncdb(self, db, model):
        if db == 'primary' or model._meta.app_label == "frontend":
            return False  # we're not using syncdb on our legacy database
        else:  # but all other models/databases are fine
            return True
