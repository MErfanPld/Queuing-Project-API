class APICorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    
from business.models import Business

class BusinessContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.business = None

        business_code = request.headers.get('X-Business-Code')

        if business_code:
            try:
                request.business = Business.objects.get(
                    random_code=business_code,
                    is_active=True
                )
            except Business.DoesNotExist:
                request.business = None

        return self.get_response(request)


# middleware.py
from django.utils.deprecation import MiddlewareMixin
from business.models import Business

class ResolveBusinessMiddleware(MiddlewareMixin):
    """
    اگر درخواست مشتری شامل query param ?business_code=XYZ باشد،
    این middleware کسب‌وکار را بارگذاری کرده و به request اضافه می‌کند.
    """
    def process_request(self, request):
        code = request.GET.get('business_code')
        if code:
            try:
                business = Business.objects.get(random_code=code, is_active=True)
                request.business = business
            except Business.DoesNotExist:
                request.business = None
        else:
            request.business = None
