from django.core.management.base import BaseCommand, CommandError
from contento.backends.files import FlatFilesBackend
from contento.backends.sql import SQLBackend
from contento.exceptions import CmsPageAlreadyExisting


sql_backend = SQLBackend()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('base_path', type=str)

    def process_node(self, node, parent_label=None):
        print node
        try:
            sql_backend.add_page(node.label, node.template,
                url=node.url, parent_label=parent_label,
                page_data=node.data,
                page_content=node.content,
                language=node.language,
                key=node.key)
        except CmsPageAlreadyExisting:
            print "cannot create", node.label

        for child in node.children:
            self.process_node(child, parent_label=node.label)


    def handle(self, *args, **options):
        base_path =  options['base_path']
        file_backend = FlatFilesBackend(FLATFILES_BASE=base_path)


        tree = file_backend.get_tree(None)
        for node in tree:
            self.process_node(node)
