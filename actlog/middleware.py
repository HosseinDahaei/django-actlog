"""Optional middleware placeholder for actlog context propagation."""


class ActLogRequestContextMiddleware:
    """No-op placeholder reserved for future request-scoped context."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
