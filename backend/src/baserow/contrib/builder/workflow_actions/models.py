from django.contrib.contenttypes.models import ContentType
from django.db import models

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.pages.models import Page
from baserow.core.formula.field import FormulaField
from baserow.core.mixins import OrderableMixin
from baserow.core.registry import ModelRegistryMixin
from baserow.core.workflow_actions.models import WorkflowAction


class EventTypes(models.TextChoices):
    CLICK = "click"
    SUBMIT = "submit"


class BuilderWorkflowAction(
    WorkflowAction,
    OrderableMixin,
):
    order = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="builder_workflow_actions",
        on_delete=models.CASCADE,
    )
    event = models.CharField(
        max_length=30,
        choices=EventTypes.choices,
        help_text="The event that triggers the execution",
    )
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    element = models.ForeignKey(
        Element, on_delete=models.CASCADE, null=True, default=None
    )

    @staticmethod
    def get_type_registry() -> ModelRegistryMixin:
        from baserow.contrib.builder.workflow_actions.registries import (
            builder_workflow_action_type_registry,
        )

        return builder_workflow_action_type_registry

    def get_parent(self):
        return self.page

    @classmethod
    def get_last_order_element_scope(cls, element: Element):
        queryset = BuilderWorkflowAction.objects.filter(element=element)
        return cls.get_highest_order_of_queryset(queryset) + 1

    @classmethod
    def get_last_order_page_scope(cls, page: Page):
        queryset = BuilderWorkflowAction.objects.filter(page=page, element=None)
        return cls.get_highest_order_of_queryset(queryset) + 1


class NotificationWorkflowAction(BuilderWorkflowAction):
    title = FormulaField(default="")
    description = FormulaField(default="")


class OpenPageWorkflowAction(BuilderWorkflowAction):
    url = FormulaField(default="")
