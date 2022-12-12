from rest_framework import permissions


class SuperUserPermission(permissions.BasePermission):
    """
    Permission to allow superusers to use all of the methods.
    """
    
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class SubredditOwnerModeratorPostPermission(permissions.BasePermission):
    """
    Object-level permission to only allow related subreddit owner and moderators to edit the object.
    Assumes the model instance has an `subreddit` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user == obj.subreddit.owner:
            return True

        if request.user in obj.subreddit.moderator.all():
            return True
        
        return False
