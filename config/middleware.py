class APICorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "OPTIONS":
            response = self._handle_preflight(request)
        else:
            response = self.get_response(request)

        response["Access-Control-Allow-Origin"] = "*"  # مبدا صحیح را وارد کنید
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH,DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    def _handle_preflight(self, request):
        response = HttpResponse(status=204)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Max-Age"] = "86400"
        return response