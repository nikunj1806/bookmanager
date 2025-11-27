from django.utils import timezone
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "contact_number",
            "role",
            "is_active",
            "date_joined",
        ]


class MemberProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "contact_number", "password"]
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "contact_number": {"required": False},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if value and User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MemberRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "contact_number",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            **validated_data,
            password=password,
            role=User.ROLE_MEMBER,
        )
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    current_membership = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "contact_number",
            "role",
            "is_active",
            "date_joined",
            "current_membership",
        ]

    def get_current_membership(self, obj):
        from payments.models import UserMembership
        from payments.serializers import UserMembershipSerializer

        active_membership = obj.memberships.filter(
            status=UserMembership.STATUS_ACTIVE,
            end_date__gt=timezone.now()
        ).first()

        if active_membership:
            return UserMembershipSerializer(active_membership).data
        return None
