import os
import yaml
from contento.settings import CONTENTO_FLATFILES_BASE
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured
import re
import shutil

FILE_REGEX = "(?P<label>(_)?[^(__)^(---)]*)(__(?P<lang>\w+))?(---(?P<key>\w+))?\.yml"
file_regex = re.compile(FILE_REGEX)

class FlatFilesBackend(object):

    """
    YAML based file backend.
    It builds pages as follows:
    - slug, language and key are inferred from filename
    - relations (parents) are inferred from filenames
    """

    def check_paths(self):
        """
        ensures that CONTENTO_FLATFILES_BASE is set
        """
        if not CONTENTO_FLATFILES_BASE:
            raise FlatFilesBaseNotConfigured("CONTENTO_FLATFILES_BASE must be declared in order to use FlatFilesBackend")

    def get_path(self, label, language=None, key=None, for_file=False ):
        """
        gets the file path for a slug
        """
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
        path = os.path.join(CONTENTO_FLATFILES_BASE, label)
        return path

    def get_meta_from_path(self, path):
        """
        Reverse label, lang and key from path
        """
        path = path.replace(CONTENTO_FLATFILES_BASE, "")

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


    #TODO: probaby keys should not influence trees
    def get_tree(self, slug, language=None, key=None, max_depth=None):
        self.check_paths()
        path = self.get_path(slug, language=language, key=key)

        #out = PageTree(slug, page_path is not None)
        depth = 0
        nodes = []
        out = {}
        nodes_dict = {}

        for dirname, dirnames, filenames in os.walk(path):
            depth += 1

            if max_depth and depth == max_depth:
                continue

            nodeslug =  dirname.replace(path, "")
            if not nodeslug.endswith("/"):
                nodeslug += "/"

            for f in filenames:
                label, lang, key = self.get_meta_from_path(nodeslug + f)
                page_data = self.get_page(label, lang, key)
                page = page_data["page"]
                #lang = page.get("language", lang)
                if lang != language:
                    continue

                node = {
                    "label" : label,
                    "slug" : page.get("slug"),
                    "data" : page.get("data", {}),
                    "language" : lang,
                    "key" : page.get("key", key),
                    "parent" : page.get("parent", nodeslug[:-1] or None),
                    "children" : []
                }

                if not node["parent"]:
                    node["page_url"] = node["slug"]
                    out[node["slug"]] = node
                else:
                    node["page_url"] = nodes_dict[node["parent"]]["page_url"] + "/" + node["slug"]
                    nodes_dict[node["parent"]]["children"].append(node)

                nodes_dict[node["slug"]] = node

        return [out[x] for x in out]



    # write api methods

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
