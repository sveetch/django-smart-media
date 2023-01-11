from pathlib import Path

from django.core.exceptions import FieldDoesNotExist


def auto_purge_files_on_delete(fieldnames):
    """
    Return a callable to set as a signal receiver to purge related files from deleted
    object.

    When connected to your model, just before an object is deleted the signal check
    defined fields for their files and remove them from your Filesystem so you won't
    keep files from object that do not exists anymore.

    This is to be used with signal ``django.db.models.signals.post_delete`` and since
    this work with shallow function you will need to set ``weak=False`` on signal
    method ``connect``.

    Example:

        Commonly you connect signal in your models file and define a list of fields to
        watch for purge: ::

            from django.db import models
            from django.db.models.signals import post_delete
            from smart_media.signals import auto_purge_files_on_delete

            class MyModel(models.Model):
                cover = models.FileField(...)

            post_delete.connect(
                auto_purge_files_on_delete(["cover"]),
                dispatch_uid="mymodels_files_on_delete",
                sender=MyModel,
                weak=False,
            )

    Remember to set an unique key name to argument ``dispatch_uid``.

    Arguments:
        fieldnames (list): List of model field names to seek for file to remove. If
            a given field name does not exists for given model instance an exception
            is raised. It is important to keep this list up to date with your model.

    Returns
        callable: A callable function with expected signature from signal emitter.
    """
    def _receiver_func(sender, instance, **kwargs):
        unknow_fields = [
            fieldname
            for fieldname in fieldnames
            if not hasattr(instance, fieldname)
        ]

        if unknow_fields:
            raise FieldDoesNotExist((
                "Function 'auto_purge_files_on_delete' was given invalid field names"
                " for model '{model}': {fields}"
            ).format(
                fields=", ".join(unknow_fields),
                model=instance.__class__.__name__,
            ))

        for fieldname in fieldnames:
            field = getattr(instance, fieldname, None)
            if field and Path(field.path).is_file():
                field.storage.delete(field.path)

    return _receiver_func


def auto_purge_files_on_change(fieldnames):
    """
    Return a callable to set as a signal receiver to purge old related files for a
    modified object with new uploaded files.

    When connected to your model, just before an existing object is saved the signal
    check defined fields for their current files, if a current file is different than
    the one from the changes, it is removed from your Filesystem so you won't
    keep files that have been deleted or changed.

    It is safe if old file does not exists anymore.

    This is to be used with signal ``django.db.models.signals.pre_save`` and since
    this work with shallow function you will need to set ``weak=False`` on signal
    method ``connect``.

    This receiver perform an additional get queryset on object to get its previous
    value just before current save.

    Example:

        Commonly you connect signal in your models file and define a list of fields to
        watch for purge: ::

            from django.db import models
            from django.db.models.signals import pre_save
            from smart_media.signals import auto_purge_files_on_change

            class MyModel(models.Model):
                cover = models.FileField(...)

            pre_save.connect(
                auto_purge_files_on_change(["cover"]),
                dispatch_uid="mymodels_files_on_change",
                sender=MyModel,
                weak=False,
            )

    Remember to set an unique key name to argument ``dispatch_uid``.

    Arguments:
        fieldnames (list): List of model field names to seek for file to remove. If
            a given field name does not exists for given model instance an exception
            is raised. It is important to keep this list up to date with your model.

    Returns
        callable: A callable function with expected signature from signal emitter.
    """
    def _receiver_func(sender, instance, **kwargs):
        unknow_fields = [
            fieldname
            for fieldname in fieldnames
            if not hasattr(instance, fieldname)
        ]

        if unknow_fields:
            raise FieldDoesNotExist((
                "Function 'auto_purge_files_on_change' was given invalid field names"
                " for model '{model}': {fields}"
            ).format(
                fields=", ".join(unknow_fields),
                model=instance.__class__.__name__,
            ))

        # Only run for object which have already been saved
        if not instance.pk:
            return False

        # Get the old saved version object
        try:
            old_obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return False

        # Store old files
        old_fieldvalues = {
            fieldname: getattr(old_obj, fieldname, None)
            for fieldname in fieldnames
        }

        # Clean file when field value changed to a new file and if there was an old
        # existing file
        for fieldname in fieldnames:
            field = getattr(instance, fieldname, None)

            if (
                old_fieldvalues[fieldname] and
                old_fieldvalues[fieldname] != field and
                Path(old_fieldvalues[fieldname].path).is_file()
            ):
                field.storage.delete(old_fieldvalues[fieldname].path)

    return _receiver_func
