from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsOwner(BasePermission):
    message = "You must be the owner"
    print("1111111111111111111111111111100000000000000000000000000000gsh")
    def has_permission(self, request, view):
        print("sagagagasg11111111111111111111")
        print(request.user)
        return True

    def has_object_permission(self, request, view, obj):
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        return request.user == obj.owner
