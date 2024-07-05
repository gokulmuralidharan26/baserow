from baserow.core.user_files.handler import UserFileHandler

from .models import (
    ButtonThemeConfigBlock,
    ColorThemeConfigBlock,
    ImageThemeConfigBlock,
    LinkThemeConfigBlock,
    PageThemeConfigBlock,
    ThemeConfigBlock,
    TypographyThemeConfigBlock,
)
from .registries import ThemeConfigBlockType


class ColorThemeConfigBlockType(ThemeConfigBlockType):
    type = "color"
    model_class = ColorThemeConfigBlock


class TypographyThemeConfigBlockType(ThemeConfigBlockType):
    type = "typography"
    model_class = TypographyThemeConfigBlock

    def import_serialized(self, parent, serialized_values, id_mapping):
        # Translate from old color property names to new names for compat with templates
        for level in range(3):
            if f"heading_{level+1}_color" in serialized_values:
                serialized_values[
                    f"heading_{level+1}_text_color"
                ] = serialized_values.pop(f"heading_{level+1}_color")

        return super().import_serialized(parent, serialized_values, id_mapping)


class ButtonThemeConfigBlockType(ThemeConfigBlockType):
    type = "button"
    model_class = ButtonThemeConfigBlock


class LinkThemeConfigBlockType(ThemeConfigBlockType):
    type = "link"
    model_class = LinkThemeConfigBlock


class ImageThemeConfigBlockType(ThemeConfigBlockType):
    type = "image"
    model_class = ImageThemeConfigBlock


class PageThemeConfigBlockType(ThemeConfigBlockType):
    type = "page"
    model_class = PageThemeConfigBlock

    def get_property_names(self):
        """
        Let's replace the page_background_file property with page_background_file_id.
        """

        return [
            n if n != "page_background_file" else "page_background_file_id"
            for n in super().get_property_names()
        ]

    @property
    def serializer_field_overrides(self):
        from baserow.api.user_files.serializers import UserFileField
        from baserow.contrib.builder.api.validators import image_file_validation

        return {
            "page_background_file": UserFileField(
                allow_null=True,
                required=False,
                help_text="The image file",
                validators=[image_file_validation],
            ),
        }

    def serialize_property(
        self,
        theme_config_block: ThemeConfigBlock,
        prop_name: str,
        files_zip=None,
        storage=None,
        cache=None,
    ):
        """
        You can customize the behavior of the serialization of a property with this
        hook.
        """

        if prop_name == "page_background_file_id":
            return UserFileHandler().export_user_file(
                theme_config_block.page_background_file,
                files_zip=files_zip,
                storage=storage,
                cache=cache,
            )

        return super().serialize_property(
            theme_config_block,
            prop_name,
            files_zip=files_zip,
            storage=storage,
            cache=cache,
        )

    def deserialize_property(
        self,
        prop_name: str,
        value,
        id_mapping,
        files_zip=None,
        storage=None,
        cache=None,
        **kwargs,
    ):
        if prop_name == "page_background_file_id":
            user_file = UserFileHandler().import_user_file(
                value, files_zip=files_zip, storage=storage
            )
            if user_file:
                return user_file.id
            return None

        return value
