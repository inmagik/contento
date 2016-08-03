import os
import yaml
from contento.settings import CONTENTO_FLATFILES_BASE
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured

class FlatFilesBackend(object):

    """
    YAML based file backend.
    """

    def check_paths(self):
        if not CONTENTO_FLATFILES_BASE:
            raise FlatFilesBaseNotConfigured("CONTENTO_FLATFILES_BASE must be declared in order to use FlatFilesBackend")

    def get_path(self, slug, language=None, key=None ):
        if slug == "/" or slug == "":
            slug = "_root"
        if slug.endswith("/"):
            slug = slug[:-1]
        path = os.path.join(CONTENTO_FLATFILES_BASE, slug)
        return path

    def get_slug(self, path):
        slug = path.replace(CONTENTO_FLATFILES_BASE, "")
        if slug == "_root":
            return "/"
        return slug


    def get_page_path(self, slug, language=None, key=None ):
        path = self.get_path(slug, language=language, key=key)
        return path + ".yml"


    def get_page(self, slug, language=None, key=None ):
        self.check_paths()
        path = self.get_page_path(slug, language=language, key=key)
        print path
        #TODO:CHECK FILE VS DIR
        #if os.path.isfile(path)
        try:
            with open(path) as stream:
                data = yaml.load(stream)
        except IOError:
            raise CmsPageNotFound("Page %s not found" % slug)

        out = { "props" : data.get("page") }

        contents = data.get("contents", [])
        content = [x for x in contents if x["language"]==language and x["key"]==key]
        if len(content):
            out["content"] = content[0]
        else:
            out["content"] = None

        return out


    def get_tree(self, slug, language=None, key=None):
        out = {}
        self.check_paths()
        path = self.get_path(slug)
        print path
        for dirname, dirnames, filenames in os.walk(path):
            print "read", dirname
            nodeslug =  dirname.replace(path, "")
            nodeslug = nodeslug or "/"
            print "nodeslug", nodeslug

            #node = { "path" : nodename, "node" : [] }
            out[nodeslug] = { "children" : [], "page" : False }

            print "dirs:"
            for d in dirnames:
                dirnodeslug = self.get_slug(d)
                if dirnodeslug not in out:
                    out[dirnodeslug] = { "children" : [], "page" : False }

            print "files:"
            for f in filenames:
                filenodeslug = self.get_slug(f.replace(".yml", ""))
                print "f", filenodeslug
                out[nodeslug]["children"].append(filenodeslug)
                if filenodeslug not in out:
                    out[filenodeslug] = { "children" : []}
                out[filenodeslug]["page"] = True


            for k in out:
                print k, out[k]

            pass

        return out
