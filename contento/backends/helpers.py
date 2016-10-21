import re

PATH_REGEX = "(?P<label>(_)?[^(__)^(---)]*)(__(?P<lang>\w+))?(---(?P<key>\w+))?"
path_regex = re.compile(PATH_REGEX)


def get_meta_from_path(path):
    """
    Reverse label, lang and key from path
    """
    search_result = path_regex.search(path)
    label = search_result.group('label')
    lang = search_result.group('lang')
    key = search_result.group('key')

    label = label.replace("_root", "")
    label = label or "/"

    return label, lang, key


def get_path_from_meta(label, language="", key=""):
    language = language or ""
    key = key or ""
    return "%s__%s---%s" % (label, language, key)
