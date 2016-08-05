import os
import yaml
from contento.settings import CONTENTO_FLATFILES_BASE
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured
import re

FILE_REGEX = "(?P<slug>(_)?[^(__)^(---)]*)(__(?P<lang>\w+))?(---(?P<key>\w+))?\.yml"
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

    def get_path(self, slug, language=None, key=None, for_file=False ):
        """
        gets the file path for a slug
        """
        if for_file and slug == "/":
            slug = "_root"
        if slug.startswith("/"):
            slug = slug[1:]
        if slug.endswith("/"):
            slug = slug[:-1]
        if language:
            slug = slug + "__%s" % language
        if key:
            slug = slug + "---%s" % key
        path = os.path.join(CONTENTO_FLATFILES_BASE, slug)
        return path

    def get_slug(self, path):
        """
        Reverse slug from path
        """
        path = path.replace(CONTENTO_FLATFILES_BASE, "")

        search_result = file_regex.search(path)
        slug = search_result.group('slug')
        lang = search_result.group('lang')
        key = search_result.group('key')

        slug = slug.replace("_root", "")
        slug = slug or "/"

        return slug, lang, key


    def get_page_path(self, slug, language=None, key=None ):
        """
        """
        path = self.get_path(slug, language=language, key=key, for_file=True)
        out = path + ".yml"
        return out


    def get_page(self, slug, language=None, key=None ):
        """
        Load a page data given a slug, a language and a key.
        From the filesystem
        """
        self.check_paths()
        path = self.get_page_path(slug, language=language, key=key)
        if path is None:
            raise CmsPageNotFound("Page %s not found" % slug)
        try:
            with open(path) as stream:
                data = yaml.load(stream)
        except IOError:
            raise CmsPageNotFound("Page %s not found" % slug)

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
                slug, lang, key = self.get_slug(nodeslug + f)
                page_data = self.get_page(slug, lang, key)
                page = page_data["page"]

                lang = page.get("language", lang)
                if lang != language:
                    continue

                node = {
                    "slug" : slug[1:],
                    "url" : page.get("url", None),
                    "data" : page.get("data", {}),
                    "language" : lang,
                    "key" : page.get("key", key),
                    "parent" : page.get("parent", nodeslug[:-1] or None),
                    "children" : []
                }

                #nodes.append(node)
                if not node["parent"]:
                    out[node["slug"]] = node
                else:
                    nodes_dict[node["parent"]]["children"].append(node)

                nodes_dict[node["slug"]] = node

        return [out[x] for x in out]
