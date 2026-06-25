from rest_framework.permissions import BasePermission, SAFE_METHODS


# Задание 2: кастомный пермишен
# Логика простая: читать могут все авторизованные,
# а изменять/удалять — только владелец объекта
class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS — пускаем всех авторизованных
        if request.method in SAFE_METHODS:
            return True

        # для изменения/удаления проверяем что текущий юзер = owner
        return obj.owner == request.user
