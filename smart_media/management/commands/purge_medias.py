from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Smart media purge command.
    """
    help = (
        "Explore defined model field data to search for stale medias to purge from "
        "storage."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--include",
            type=str,
            metavar="ITEM",
            action="append",
            dest="inclusions",
            default=[],
            help=(
                "This is a cumulative argument."
            )
        )
        parser.add_argument(
            "--exclude",
            type=str,
            metavar="ITEM",
            action="append",
            dest="exclusions",
            default=[],
            help=(
                "This is a cumulative argument."
            )
        )

    def handle(self, *args, **options):
        # self.logger = DjangoCommandOutput(
        #     command=self,
        #     verbosity=options["verbosity"]
        # )

        print("foo")
