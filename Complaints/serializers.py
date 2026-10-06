from rest_framework import serializers
from .models import Complaint

CITIZEN_FIELDS = ["issue_type", "description", "image", "location"]
OFFICER_FIELDS = ["status", "admin_update", "resolved_image"]


class ComplaintSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "id", "username", "issue_type", "description", "image",
            "location", "status", "admin_update", "resolved_image",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        is_staff = bool(request and request.user.is_staff)

        if not is_staff:
            for name in OFFICER_FIELDS:      # citizens can't set these
                fields[name].read_only = True

        return fields