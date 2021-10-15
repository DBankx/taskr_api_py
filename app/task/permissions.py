from rest_framework import permissions

class UpdateOwnTask(permissions.BasePermission):
	"""Allow users to edit their own tasks"""

	def has_object_permission(self, request, view, obj):
		"""Check user has permission to edit their task"""

		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.creator.id == request.user.id	