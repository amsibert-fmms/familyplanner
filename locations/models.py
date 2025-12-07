from django.db import models

from visibility.models import OwnedVisibleModel


class Location(OwnedVisibleModel):
    class LocationType(models.TextChoices):
        PRIMARY_HOME = "PRIMARY_HOME", "Primary home"
        ELDER_HOME = "ELDER_HOME", "Elder home"
        OTHER = "OTHER", "Other"

    household = models.ForeignKey(
        "accounts.Household", on_delete=models.CASCADE, related_name="locations"
    )
    name = models.CharField(max_length=255)
    location_type = models.CharField(
        max_length=20, choices=LocationType.choices, default=LocationType.PRIMARY_HOME
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.name


class PropertyNote(OwnedVisibleModel):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="property_notes"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.CharField(max_length=255, blank=True)
    pinned = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.title


class MaintenanceSchedule(OwnedVisibleModel):
    class RecurrenceType(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        CUSTOM = "custom", "Custom"

    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="maintenance_schedules"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    recurrence_type = models.CharField(
        max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.MONTHLY
    )
    interval = models.PositiveIntegerField(default=1)
    day_of_week = models.PositiveSmallIntegerField(null=True, blank=True)
    day_of_month = models.PositiveSmallIntegerField(null=True, blank=True)
    next_due = models.DateField()
    last_completed = models.DateField(null=True, blank=True)
    auto_create_task = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.name
