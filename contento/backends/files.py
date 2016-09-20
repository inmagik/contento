import os
import yaml
import re
import shutil

from contento import settings
from contento.page_node import PageNode
from django.conf import settings as django_settings
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured


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


    def get_tree(self, base_path, language=None, key=None, max_depth=None):
        """
        Gets a tree of pages, starting from a given PATH
        """
        self.check_paths()
        path = self.get_path(base_path, language=language, key=key)

        #out = PageTree(slug, page_path is not None)
        depth = 0
        nodes = []
        #topmost nodes will be the output.
        #the tree can be reconstructed by traversing these nodes via the .children attribute
        out = []
        nodes_dict = {}

        current_parent = None

        for dirname, dirnames, filenames in os.walk(path):
            depth += 1

            if max_depth and depth == max_depth:
                continue

            nodepath =  dirname.replace(path, "")
            if not nodepath.endswith("/"):
                nodepath += "/"

            for f in filenames:
                if not f.endswith(".yml"):
                    continue
                label, lang, key = self.get_meta_from_path(nodepath + f)
                page_data = self.get_page(label, lang, key)
                page = page_data["page"]
                #lang = page.get("language", lang)
                if lang != language:
                    continue

                node = PageNode(
                    label,
                    page.get('url'),
                    page.get("data", {}),
                    parent=current_parent
                )

                nodes_dict[node.get_path()] = node
                if depth == 1:
                    out.append(node)
        return out
        #return [out[x] for x in out]


    """
    WRITE api methods
    """

    def add_page(self, label, page_data, page_content={}, language=None, key=None):
        raise NotImplementedError


    def modify_page(self, label, page_data, page_content, language=None, key=None):
        raise NotImplementedError


    def move_page(self, label, new_parent, language=None, key=None):
        page = self.get_page(label, language=language, key=key)
        old_path = self.get_page_path(label, language=language, key=key)
        old_dir = self.get_path(label, language=language, key=key)
        clean_label = label.replace(old_dir, "")
        if clean_label.endswith("/"):
            clean_label = clean_label[:-1]

        if not new_parent.endswith("/"):
            new_parent = new_parent + "/"

        if not new_parent.startswith("/"):
            new_parent =  "/" + new_parent

        new_label = new_parent + clean_label
        new_path = self.get_page_path(new_label)

        shutil.move(old_path, new_path)



    def drop_page(self, label, language=None, key=None):
        raise NotImplementedError


    def add_page_fragment(
            self, label,
            region, content_type, content_data,
            language=None, key=None,
            position=None
        ):
        raise NotImplementedError

    def modify_page_fragment(
            self, label,
            region, position, content_data,
            language=None, key=None
        ):
        raise NotImplementedError

    def move_page_fragment(
            self, label,
            region, position,
            new_region=None, new_position=None,
            language=None, key=None
        ):
        raise NotImplementedError


    def drop_page_fragment(
            self, label,
            region, position,
            language=None, key=None
        ):
        raise NotImplementedError
