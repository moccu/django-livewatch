class Extension(object):
    name = None

    def check(self, request):
        raise NotImplementedError
