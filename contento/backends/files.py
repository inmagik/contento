import os
import yaml
import re
import shutil

from contento import settings
from contento.page_node import PageNode
from django.conf import settings as django_settings
from contento.exceptions import CmsPageNotFound, CmsPageAlreadyExisting, FlatFilesBaseNotConfigured



FILE_REGEX = "(?P<label>(_)?[^(__)^(---)]*)(__(?P<lang>\w+))?(---(?P<key>\w+))?\.yml"
file_regex = re.compile(FILE_REGEX)

class FlatFilesBackend(object):

    """
    YAML based file backend.
    It builds pages as follows:
    - label, language and key are inferred from filename
    - relations (parents) are inferred from filenames
    """

    def __init__(self, FLATFILES_BASE=None):
        if not FLATFILES_BASE:
            FLATFILES_BASE = getattr(django_settings, "CONTENTO_FLATFILES_BASE", getattr(settings, "CONTENTO_FLATFILES_BASE"))
        self.FLATFILES_BASE = FLATFILES_BASE

    def check_paths(self):
        """
        ensures that CONTENTO_FLATFILES_BASE is set
        """

        if not self.FLATFILES_BASE:
            raise FlatFilesBaseNotConfigured("CONTENTO_FLATFILES_BASE must be declared in order to use FlatFilesBackend")

    def ensure_directories(self, path):
        """
        ensures that container dirs exist for a file path
        """
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise  OSError

    def get_path(self, label, language=None, key=None, for_file=False ):
        """
        gets the file path for an url
        """
        if not label.startswith("/"):
            label = "/" + label
        if for_file and label == "/":
            label = "_root"
        if label.startswith("/"):
            label = label[1:]
        if label.endswith("/"):
            label = label[:-1]
        if language:
            label = label + "__%s" % language
        if key:
            label = label + "---%s" % key
        path = os.path.join(self.FLATFILES_BASE, label)
        return path

    def get_meta_from_path(self, path):
        """
        Reverse label, lang and key from path
        """
        path = path.replace(self.FLATFILES_BASE, "")

        search_result = file_regex.search(path)
        label = search_result.group('label')
        lang = search_result.group('lang')
        key = search_result.group('key')

        label = label.replace("_root", "")
        label = label or "/"

        return label, lang, key


    def get_path_from_meta(label, language="", key=""):
        return "%s__%s---%s" % (label, language, key)


    def get_page_path(self, label, language=None, key=None ):
        """
        """

        path = self.get_path(label, language=language, key=key, for_file=True)
        out = path + ".yml"
        return out


    """
    READ API METHODS
    """

    def get_page(self, label, language=None, key=None ):
        """
        Load a page data given a label, a language and a key.
        From the filesystem
        """
        self.check_paths()
        path = self.get_page_path(label, language=language, key=key)
        if path is None:
            raise CmsPageNotFound("Page %s not found" % label)
        try:
            with open(path) as stream:
                data = yaml.load(stream)
        except IOError:
            raise CmsPageNotFound("Page %s not found" % label)

        return data


    def process_folder(self, folder, parent_node, language=None, key=None):
        #TODO: !order
        out = []
        for f in os.listdir(folder):
            fullpath = os.path.join(folder, f)

            if os.path.isfile(fullpath):
                if not fullpath.endswith(".yml"):
                    continue

                label, lang, key = self.get_meta_from_path(fullpath)
                page_data = self.get_page(label, lang, key)
                #lang = page.get("language", lang)
                if lang != language:
                    continue


                node = PageNode(
                    label,
                    page_data.get('url'),
                    page_data.get("data", {}),
                    parent=parent_node,
                    language=lang,
                    key=key
                )

                nodedir = fullpath.replace(".yml", "")
                if os.path.isdir(nodedir):
                    nodes = self.process_folder(nodedir, node, language=language, key=key)
                    node.children = nodes

                out.append(node)

        return out


    def get_tree(self, base_path, language=None, key=None):
        """
        Gets a tree of pages, starting from a given PATH
        """
        self.check_paths()
        if base_path == "/" or base_path is None:
            base_path = ""
        path = self.get_path(base_path, language=language, key=key)
        out = self.process_folder(path, None, language=language, key=key)
        return out

    """
    WRITE api methods
    """


    def _write_page( self, label, template, url=None, parent_label=None,
                page_data={}, page_content={}, language=None, key=None
        ):
        """
        "private" method used to write a page to fs
        """
        if parent_label:
            label = "%s/%s" % (parent_label, label)
        path = self.get_page_path(label, language=language, key=key)
        self.ensure_directories(path)
        out_stream = {
            "url" : url,
            "template" : template,
            "data" : page_data,
            "content" : page_content
        }
        with open(path, "wb") as outfile:
            yaml.safe_dump(out_stream, outfile, encoding='utf-8', allow_unicode=True, default_style='"')

        return out_stream



    def add_page(self, label, template, url=None, page_data={}, page_content={}, language=None, key=None):
        if url is None:
            url = label
        try:
            page = self.get_page(label, language=language, key=key)
            raise CmsPageAlreadyExisting

        except CmsPageNotFound:
            return self._write_page(
                label, template, url=url, page_data=page_data, page_content=page_content,
                language=None, key=None
            )


    def modify_page(self, label, template=None, url=None, page_data=None, page_content=None, language=None, key=None):

        page = self.get_page(label, language=language, key=key)
        template = template or page.get("template")
        url = url or page.get("url")
        page_data = page_data or page.get("data")
        page_content = page_content or page.get("content")

        return self._write_page(
            label, template, url=url, parent_label=None,
            page_data=page_data, page_content=page_content,
            language=None, key=None
        )


    def move_page(self, label, new_parent, language=None, key=None):
        page = self.get_page(label, language=language, key=key)

        old_path = self.get_page_path(label, language=language, key=key)
        old_dir = self.get_path(label, language=language, key=key)

        if not new_parent.endswith("/"):
            new_parent = new_parent + "/"

        if not new_parent.startswith("/"):
            new_parent =  "/" + new_parent

        new_path = self.get_path(new_parent)

        container = self.get_path(new_parent)
        if not os.path.isdir(container):
            os.makedirs(container)

        shutil.move(old_path, new_path)



    def drop_page(self, label, language=None, key=None):
        """
        removes a page from filesystem
        """
        page = self.get_page(label, language=language, key=key)
        page_path = self.get_page_path(label, language=language, key=key)
        if os.path.exists(page_path):
            os.remove(page_path)


    def add_page_fragment(
            self, label,
            region, content_type, content_data,
            language=None, key=None,
            position=None
        ):
        """
        adds a fragment to a page, given a region
        """
        page = self.get_page(label, language=language, key=key)
        template = page.get("template")

        if region not in page["content"]:
            page["content"][region] = []

        fragment = {
            "type" : content_type,
            "data" : content_data
        }

        if not position:
            page["content"][region].append(fragment)
        else:
            page["content"][region].insert(position, fragment)

        return self._write_page(
            label,
            template,
            url=page.get("url", None), parent_label=None,
            page_data=page["data"],
            page_content=page["content"],
            language=language, key=key
        )



    def modify_page_fragment(
            self, label,
            region, position, content_data,
            language=None, key=None
        ):
        """
        This only changes the data of a fragment (fragment must exist)
        """
        page = self.get_page(label, language=language, key=key)
        page["content"][region][position]["data"] = content_data

        return self._write_page(
            label,
            url=page.get("url", None), parent_label=None,
            page_data=page["data"],
            page_content=page["content"],
            language=language, key=key
        )



    def move_page_fragment(
            self, label,
            region, position,
            new_region=None, new_position=None,
            language=None, key=None
        ):
        page = self.get_page(label, language=language, key=key)
        template = page.get("template")
        old_fragment = page["content"][region].pop(position)
        page["content"][region].insert(new_position, old_fragment)
        return self._write_page(
            label,
            template,
            url=page.get("url", None), parent_label=None,
            page_data=page["data"],
            page_content=page["content"],
            language=language, key=key
        )


    def drop_page_fragment(
            self, label,
            region, position,
            language=None, key=None
        ):
        page = self.get_page(label, language=language, key=key)
        template = page.get("template")
        page["content"][region].pop(position)

        return self._write_page(
            label,
            template,
            url=page.get("url", None), parent_label=None,
            page_data=page["data"],
            page_content=page["content"],
            language=language, key=key
        )
