# from django.http import JsonResponse
# from functools import wraps

# def check_version(min_version):
#     """
#     Decorator to enforce a minimum API version requirement.

#     Args:
#         min_version (str): The minimum version required for the view to be accessible.

#     Returns:
#         function: The decorator function that wraps the original view function.
#     """
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             version = request.headers.get('X-App-Version', '0.0')
#             if version < min_version:
#                 return JsonResponse({'error': 'Update required'}, status=400)
#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator