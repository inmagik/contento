from contento.models import Page
from contento.page_node import PageNode
from contento.exceptions import CmsPageNotFound, CmsPageAlreadyExisting
from django.core.cache import cache

class SQLBackend(object):
    """
    """
    def process_page_for_tree(self, page, language=None, key=None, parent_node=None):
        out = []
        if parent_node:
            level=parent_node.level+1
        else:
            level=0

        node = PageNode(
            page.label,
            page.url,
            page.data,
            parent=parent_node,
            language=language,
            order=page.order,
            key=key,
            level=level
        )

        node.children = []
        for child in page.children.filter(language=language, key=key).order_by('order'):
            child_nodes = self.process_page_for_tree(child, language=language, key=key, parent_node=node)
            node.children.extend(child_nodes)

        out.append(node)

        return out


    """
    READ API METHODS
    """

    def to_node(self, page, level=0):
        if page.parent:
            parent_node = self.to_node(page.parent)
        else:
            parent_node = None

        node = PageNode(
            page.label,
            page.url,
            page.data,
            content = page.content,
            template = page.template,
            parent=parent_node,
            language=page.language,
            order=page.order,
            key=page.key,
            level=level
        )
        return node

    def get_page(self, label, language=None, key=None):
        language = language or None
        try:
            page = Page.objects.get(
                label=label,
                language=language,
                key = key
            )
        except:
            raise CmsPageNotFound

        return self.to_node(page)



    def get_tree(self, base_path, language=None, key=None):
        cached_tree = cache.get("contento.pagetree-%s-%s-%s" % (base_path, language, key) )
        if cached_tree:
            out, root_node = cached_tree
        else:
            try:
                if base_path:
                    if not base_path.startswith("/"):
                        base_path = "/" + base_path
                    root_page = Page.objects.get(
                        fullpath=base_path, language=language, key=key
                    )
                    root_node = self.to_node(root_page)

                else:
                    root_node = None
                    root_page = None

                root_pages = Page.objects.filter(
                    parent=root_page, language=language, key=key
                ).order_by('order')
                out = []
                for p in root_pages:
                    out.extend(self.process_page_for_tree(p, parent_node=root_node))
                cache.set("contento.pagetree-%s-%s-%s" % (base_path, language, key), (out, root_node))

            except Page.DoesNotExist:
                return [], None


        return out, root_node




    """
    WRITE api methods
    """

    def add_page(self, label, template, url=None, parent_label=None,
        page_data={}, page_content={}, language=None, key=None):
        if url is None:
            url = label
        try:
            page = self.get_page(label, language=language, key=key)
            raise CmsPageAlreadyExisting

        except CmsPageNotFound:
            parent_page = None
            if parent_label:
                parent_page = Page.objects.get(label=parent_label, language=language, key=key)

            Page.objects.create(label=label, template=template, url=url,
                parent=parent_page,
                data=page_data, content=page_content,
                language=language, key=key)

            return self.get_page(label, language=language, key=key)


    def modify_page(self, label, template=None, url=None, page_data=None, page_content=None, language=None, key=None):

        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        if template:
            page.template = template

        if url:
            page.url = url

        if page_data:
            page.data = page_data

        if page_content:
            page.content = page_content

        page.save()


    def move_page(self, label, new_parent, language=None, key=None):
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        if new_parent:
            new_parent = Page.objects.get(
                label=new_parent,
                language=language,
                key = key
            )
        page.parent = new_parent
        page.save()

    def reorder_page(self, label, new_order, language=None, key=None):
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        page.order=new_order
        page.save()

    def drop_page(self, label, language=None, key=None):
        """
        removes a page from filesystem
        """
        try:
            page = Page.objects.get(
                label=label,
                language=language,
                key = key
            )
        except:
            raise CmsPageNotFound

        page.delete()


    def add_page_fragment(
            self, label,
            region, content_type, content_data,
            language=None, key=None,
            position=None
        ):
        """
        adds a fragment to a page, given a region
        """
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )

        if not page.content:
            page.content = {}
        if region not in page.content:
            page.content[region] = []

        fragment = {
            "type" : content_type,
            "data" : content_data
        }

        if not position:
            page.content[region].append(fragment)
        else:
            page.content[region].insert(position, fragment)

        page.save()


    def modify_page_fragment(
            self, label,
            region, position, content_data,
            language=None, key=None
        ):
        """
        This only changes the data of a fragment (fragment must exist)
        """
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        page.content[region][position]["data"] = content_data

        page.save()


    def move_page_fragment(
            self, label,
            region, position,
            new_region=None, new_position=None,
            language=None, key=None
        ):
        """
        """
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        old_fragment = page.content[region].pop(position)
        page.content[region].insert(new_position, old_fragment)
        page.save()


    def drop_page_fragment(
            self, label,
            region, position,
            language=None, key=None
        ):
        """
        """
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        page.content[region].pop(position)
        page.save()
