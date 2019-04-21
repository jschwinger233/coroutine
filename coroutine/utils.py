def singleton(klass):
    klass._instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    klass.get_instance = get_instance
    return klass
