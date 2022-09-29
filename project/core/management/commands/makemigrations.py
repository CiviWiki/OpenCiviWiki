from django.core.management.base import CommandError
from django.core.management.commands.makemigrations import (
    Command as BaseCommand,
)


class Command(BaseCommand):
    def handle(self, *app_labels, name, dry_run, merge, **options):
        if name is None and not dry_run and not merge:
            raise CommandError("-n/--name is required.")
        
        super().handle(
            *app_labels,
            name=name,
            dry_run=dry_run,
            merge=merge,
            **options,
        )
