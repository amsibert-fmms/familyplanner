import uuid

from django.conf import settings
from django.db import models


class OwnedVisibleModel(models.Model):
    """Abstract base providing owner and visibility controls."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    private_to_owner = models.BooleanField(default=False)

    class VisibilityOverride(models.TextChoices):
        HOUSEHOLD_DEFAULT = "HOUSEHOLD_DEFAULT", "Household default"
        EXTENDED_FAMILY = "EXTENDED_FAMILY", "Extended family"
        CUSTOM_GROUPS_ONLY = "CUSTOM_GROUPS_ONLY", "Custom groups only"

    visibility_override = models.CharField(
        max_length=32,
        choices=VisibilityOverride.choices,
        default=VisibilityOverride.HOUSEHOLD_DEFAULT,
    )
    visibility_groups = models.ManyToManyField("visibility.VisibilityGroup", blank=True)

    class Meta:
        abstract = True


class VisibilityGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(
        "accounts.Household", on_delete=models.CASCADE, related_name="visibility_groups"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="visibility_group_memberships")

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.name
