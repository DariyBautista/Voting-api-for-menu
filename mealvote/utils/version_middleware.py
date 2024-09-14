# from django.http import JsonResponse

# from django.utils.deprecation import MiddlewareMixin

# class VersioningMiddleware(MiddlewareMixin):
#     def process_request(self, request):

#         request.app_version = request.headers.get('X-App-Version', '1.0')

# class VersionMiddleware:
#     """
#     Middleware to add API version information from request headers to the request object.

#     Attributes:
#         get_response (callable): The next middleware or view in the processing chain.

#     Methods:
#         __call__(request): Processes the request to extract the API version from headers and attach it to the request object.
#     """
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         version = request.headers.get('App-Version')
#         if version:
#             request.version = version
#         else:
#             request.version = None
        
#         response = self.get_response(request)
#         return response
