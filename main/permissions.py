from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change this data."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Read: everyone. PUT/PATCH: owner or holder of `edit_permission`. POST/DELETE: owner only."""
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
    edit_permission = "main.change_achievement"


class ExperiencePermission(IsPortfolioOwnerOrEditorOrReadOnly):
    edit_permission = "main.change_experience"