"""DRF permission classes enforcing the portfolio's four roles."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change this data."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """DRF permission classes enforcing the portfolio's four roles."""
    message = "You do not have permission to perform this action."
    edit_permission = None

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return request.method in ("PUT", "PATCH") and user.has_perm(self.edit_permission)


class AchievementPermission(IsPortfolioOwnerOrEditorOrReadOnly):
    """Editors need main.change_achievement to PUT/PATCH achievements."""
    edit_permission = "main.change_achievement"


class ExperiencePermission(IsPortfolioOwnerOrEditorOrReadOnly):
    """Editors need main.change_experience to PUT/PATCH experiences."""
    edit_permission = "main.change_experience"