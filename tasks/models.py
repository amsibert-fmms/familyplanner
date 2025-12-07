import uuid

from django.conf import settings
from django.db import models

from visibility.models import OwnedVisibleModel


class RecurrenceRule(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    interval = models.PositiveIntegerField(default=1)
    by_weekday = models.JSONField(null=True, blank=True)
    by_monthday = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return f"Recurrence {self.frequency} every {self.interval}"


class Task(OwnedVisibleModel):
    class Category(models.TextChoices):
        HOUSEHOLD = "HOUSEHOLD", "Household"
        ELDER_CARE = "ELDER_CARE", "Elder care"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        PET = "PET", "Pet"
        BILL_REMINDER = "BILL_REMINDER", "Bill reminder"
        VEHICLE = "VEHICLE", "Vehicle"
        APPLIANCE = "APPLIANCE", "Appliance"

    class RecurrenceType(models.TextChoices):
        NONE = "none", "None"
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    household = models.ForeignKey(
        "accounts.Household", on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.HOUSEHOLD
    )
    location = models.ForeignKey(
        "locations.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    pet = models.ForeignKey(
        "accounts.Pet", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    related_maintenance_schedule = models.ForeignKey(
        "locations.MaintenanceSchedule",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_tasks",
    )
    due_date = models.DateField(null=True, blank=True)
    due_datetime = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    last_completed_at = models.DateTimeField(null=True, blank=True)
    assigned_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    assigned_to_group = models.ForeignKey(
        "visibility.VisibilityGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    recurrence_type = models.CharField(
        max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.NONE
    )
    recurrence_rule = models.ForeignKey(
        RecurrenceRule, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.title


class TaskCompletion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completions")
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="task_completions",
    )
    completed_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    source = models.CharField(max_length=50)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return f"Completion for {self.task}"


class BillReminderTemplate(OwnedVisibleModel):
    class RecurrenceType(models.TextChoices):
        MONTHLY = "monthly", "Monthly"

    household = models.ForeignKey(
        "accounts.Household", on_delete=models.CASCADE, related_name="bill_reminder_templates"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    day_of_month_due = models.PositiveSmallIntegerField()
    recurrence_type = models.CharField(
        max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.MONTHLY
    )
    active = models.BooleanField(default=True)
    last_generated = models.DateField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        return self.name
