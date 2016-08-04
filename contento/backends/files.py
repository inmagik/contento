import os
import yaml
from contento.settings import CONTENTO_FLATFILES_BASE
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured
import re

class PageNode(object):
    def __init__(self, slug, has_page=False):
        self.slug = slug
        self.has_page = has_page
        self.children = []

    def add_children(self, node):
        if node not in self.children:
            self.children.append(node)

    def to_dict(self):
        return {
            "slug" : self.slug,
            "has_page" : self.has_page,
            "children" : [x.to_dict() for x in self.children ]
        }


class PageTree(object):
    def __init__(self, root_path, is_page=False):
        self.refs = {}
        self.root = PageNode(root_path, is_page)
        self.refs[root_path] = self.root

    def add_page(self, slug):
        if slug not in self.refs:
            node = PageNode(slug, True)
            self.refs[slug] = node
        else:
            self.refs[slug].has_page = True

    def to_dict(self):
        return self.root.to_dict()

    def add_children(self, slug, child_slug, has_page):
        if slug not in self.refs:
            node = PageNode(slug)
            self.refs[slug] = node
        else:
            node = self.refs[slug]

        if child_slug not in self.refs:
            child_node = PageNode(child_slug)
            self.refs[child_slug] = child_node
        else:
            child_node = self.refs[child_slug]


        node.add_children(child_node)



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

        if slug.startswith("/"):
            slug = slug[1:]

        return slug, lang, key


    def get_page_path(self, slug, language=None, key=None ):
        """
        """
        path = self.get_path(slug, language=language, key=key, for_file=True)
        out = path + ".yml"
        if os.path.isfile(out):
            return out
        return None


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
        print 1234, path


        #out = PageTree(slug, page_path is not None)
        depth = 0
        for dirname, dirnames, filenames in os.walk(path):
            depth += 1
            if max_depth and depth == max_depth:
                continue

            nodeslug =  dirname.replace(path, "")
            if not nodeslug.endswith("/"):
                nodeslug += "/"

            for f in filenames:
                slug, lang, key = self.get_slug(nodeslug + f)
                print slug, lang, key
                #filenodeslug = self.get_slug(f.replace(".yml", ""))
                #if nodeslug != filenodeslug:
                    #out.add_children(nodeslug, filenodeslug, True)
                #out.add_page(filenodeslug)


        return {}
        #return out.to_dict()
