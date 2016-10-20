from contento.models import Page
from contento.page_node import PageNode
from contento.exceptions import CmsPageNotFound, CmsPageAlreadyExisting

class SQLBackend(object):
    """
    """
    def process_page(self, page, language=None, key=None, parent_node=None):
        out = []
        node = PageNode(
            page.label,
            page.url,
            page.data,
            parent=parent_node,
            language=language,
            key=key
        )

        #TODO: !order
        node.children = []
        for child in page.children.filter(language=language, key=key):
            child_nodes = self.process_page(child, language, key, parent_node=node)
            node.children.extend(child_nodes)

        out.append(node)

        return out
    

    """
    READ API METHODS
    """
    def get_page(self, label, language=None, key=None):
        try:
            page = Page.objects.get(
                label=label,
                language=language,
                key = key
            )
        except:
            raise CmsPageNotFound

        out = {
            "label" : page.label,
            "url" : page.url,
            "template" : page.template,
            "data" : page.data,
            "content" : page.content
        }
        return out



    def get_tree(self, base_path, language=None, key=None):
        try:
            if base_path:
                root_page = Page.objects.get(
                    fullpath=base_path,language=language, key=key
                )
                return self.process_page(root_page)
            else:
                root_pages = Page.objects.filter(
                    parent=None,language=language, key=key
                )
                out = []
                for p in root_pages:
                    out.extend(self.process_page(p))
                return out


        except Page.DoesNotExist:
            return []

    """
    WRITE api methods
    """

    def add_page(self, label, template, url=None, page_data={}, page_content={}, language=None, key=None):
        if url is None:
            url = label
        try:
            page = self.get_page(label, language=language, key=key)
            raise CmsPageAlreadyExisting

        except CmsPageNotFound:
            Page.objects.create(label=label, template=template, url=url,
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
