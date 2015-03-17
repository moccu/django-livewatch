class Extension(object):
    name = None

    def check_service(self, request):
        raise NotImplementedError
