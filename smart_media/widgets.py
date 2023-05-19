from django.forms.widgets import FileInput, ClearableFileInput


class FileInputButtonBase(FileInput):
    """
    A simple FileInput override to use a custom template.

    The custom template is located at ``smart_image/fileinputbutton_basic.html``, you
    may override it in your project if needed, but mind it is global to all SmartMedia
    widgets.

    Default behavior if no ``class`` attribute is given is to apply the CSS
    classname ``fileinputbutton__input`` to the input.

    .. Note::
        When your input file enable the ``multiple`` attribute to accept more
        than one file, label input will be rendered to a default string like
        "4 files" which is not translatable (this is done in the Javascript
        source).

        If you want a translatable string just pass it to widget instance
        attribute ``data-multiple-caption`` like: ::

            FileInputButton(attrs={
                "data-multiple-caption": gettext_lazy("{count} files selected")
            })

        Pattern ``{count}`` will be replaced with the number of selected files.
    """
    template_name = "smart_image/fileinputbutton_basic.html"

    def __init__(self, attrs=None):
        default_attrs = {"class": "fileinputbutton__input"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ClearableFileInputButtonBase(ClearableFileInput):
    """
    Alike ``FileInputButtonBase`` but to extend with the additional clear checkbox.

    This won't support the "multiple" input file feature.
    """
    template_name = "smart_image/fileinputbutton_clearable.html"

    def __init__(self, attrs=None):
        default_attrs = {"class": "fileinputbutton__input"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class FileInputButton(FileInputButtonBase):
    """
    ``FileInputButtonBase`` version which includes the required assets to customize
    its layout and turn the file input as a button.

    This widget will define a stylesheet and a Javascript asset to load as
    `form medias <https://docs.djangoproject.com/en/4.2/topics/forms/media/>`_, this
    automatically done from admin but you will probably have to load them on your own
    in a custom form.

    * Stylesheet is located at ``smart_image/css/fileinputbutton.css`` (relative to
      static directory);
    * Javascript is located at ``smart_image/js/fileinputbutton.js`` (relative to
      static directory);

    You can retrieve these assets sources in repository, note than the CSS is built
    from a Sass source you may copy into your project Sass sources.
    """
    class Media:
        css = {
            "all": ("smart_image/css/fileinputbutton.css",),
        }
        js = ("smart_image/js/fileinputbutton.js",)


class ClearableFileInputButton(ClearableFileInputButtonBase):
    """
    ``ClearableFileInputButtonBase`` version which includes the required assets to
    customize its layout and turn the file input as a button.
    """
    class Media:
        css = {
            "all": ("smart_image/css/fileinputbutton.css",),
        }
        js = ("smart_image/js/fileinputbutton.js",)
