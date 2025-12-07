import uuid

from django.conf import settings
from django.db import models


class Household(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="member_households"
    )
    extended_family_members = models.ManyToManyField(
        "accounts.FamilyMember", blank=True, related_name="extended_households"
    )

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    default_household = models.ForeignKey(
        Household, on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles"
    )
    timezone = models.CharField(max_length=64, default="UTC")

    class PreferredUnits(models.TextChoices):
        METRIC = "metric", "Metric"
        US = "us", "US"

    preferred_units = models.CharField(
        max_length=10, choices=PreferredUnits.choices, default=PreferredUnits.US
    )
    notification_preferences = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return f"Profile for {self.user}"


class FamilyMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="family_members"
    )
    linked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="family_member_links",
    )
    full_name = models.CharField(max_length=255)
    relationship_to_household = models.CharField(max_length=255)
    is_elder = models.BooleanField(default=False)
    primary_location = models.ForeignKey(
        "locations.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_family_members",
    )

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.full_name


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    primary_location = models.ForeignKey(
        "locations.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pets",
    )
    primary_caregiver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_caregiver_pets",
    )
    primary_caregiver_family_member = models.ForeignKey(
        FamilyMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="caregiver_pets",
    )

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.name
