from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permiso para que solo el usuario dueño de la cuenta pueda editarla.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Permisos de escritura solo están permitidos para el dueño de la cuenta.
        return obj.owner == request.user


class IsOwnerOfCuenta(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.cuenta.owner == request.user
