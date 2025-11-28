from django.db import models


class Todo(models.Model):
    """Simple TODO item with due date and resolved flag."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_resolved", "due_date", "created_at"]

    def __str__(self) -> str:
        status = "✓" if self.is_resolved else "✗"
        return f"{status} {self.title}"
