# Generated by Django 3.2.21 on 2023-12-14 14:19

import django.db.models.deletion
from django.db import migrations, models

import baserow.core.formula.field


class Migration(migrations.Migration):
    dependencies = [
        ("builder", "0033_auto_20231215_1041"),
    ]

    operations = [
        migrations.CreateModel(
            name="DropdownElement",
            fields=[
                (
                    "element_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="builder.element",
                    ),
                ),
                (
                    "label",
                    baserow.core.formula.field.FormulaField(
                        default="", help_text="The text label for this dropdown"
                    ),
                ),
                (
                    "default_value",
                    baserow.core.formula.field.FormulaField(
                        default="", help_text="This dropdowns input's default value."
                    ),
                ),
                (
                    "required",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this drodpown is a required field.",
                    ),
                ),
                (
                    "placeholder",
                    baserow.core.formula.field.FormulaField(
                        default="",
                        help_text="The placeholder text which should be applied to the element.",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("builder.element",),
        ),
        migrations.CreateModel(
            name="DropdownElementOption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    models.TextField(
                        blank=True, default="", help_text="The value of the option"
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="The display name of the option",
                    ),
                ),
                (
                    "dropdown",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="builder.dropdownelement",
                    ),
                ),
            ],
        ),
    ]
