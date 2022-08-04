from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Also allow authenticated users `custom_actions`
    Assumes the model instance has an `author` attribute.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        custom_actions = ['like', 'comment']
        print(f'{request.method} - checking object permissions')

        if view.action in custom_actions:
            return request.user.is_authenticated

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
