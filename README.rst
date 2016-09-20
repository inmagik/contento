Contento
========

**Contento** is an open source cms system for the Django web framework.

Manifesto
---------

These are the principles **contento** is being built on.

1. Content should never break your website.
2. Content should be easy to serialize, store, and move around a website
   or even different websites.
3. Editing content should be performed with an interface suitable both
   for the content and for the editor. Our editing paradigm is WYSIWIM
   (what you see is what you mean) and not WYSIWIG (what you see is what
   you get). We aim at building **responsive editing** vs. rich editing
   interfaces.
4. A CMS should be just related to editing content on a website. It
   should not dictate the structure of the web site or become a
   constraint when it comes to adding other functionalities or keeping
   your web framework up to date.
5. A CMS should be able to fit within any webpage design.
6. A CMS should be extensible in order to handle different kind of
   content (think of texts, images, maps, image galleries). And it
   should be easy to implement such extensions.


Core concepts and features
--------------------------

Pages
~~~~~

A **page** is the unit of content that gets displayed given a **url** of the site.
Given a BASE_CMS_URL, a set of pages can be mounted on it, creating a **pages tree**.


- A page can have a **parent** and an **order** of displaying within its parent. If two pages have the same order within their parent, they will be sorted lexycographically using the label attribute.
- The **path** of a page is calculated by concatenating the path of the parent page, if any, and the **partial_url** of the page.
- The final url to which a page responds is calculated by concatenating the BASE_CMS_URL and the **path** of the page.
- A page has also a **label** that it's used to identify the page by a human. This field should be unique (#TODO:we could relax this by making unique the tuple (parent, label))


To recap:


- page.parial_url = f(page.url, page.key)
- page.path = page.parent.PATH + page.parial_url
- final_url = BASE_CMS_URL + page.path


A page may also have a **language** set.
The language should be determined by django itself via session/url prefix.
(see https://docs.djangoproject.com/en/1.10/topics/i18n/translation/#module-django.conf.urls.i18n)


Contents
~~~~~~~~

Fragments
~~~~~~~~~

Progressive editing interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Versioning
~~~~~~~~~~

i18n
~~~~

Publishing workflows
~~~~~~~~~~~~~~~~~~~~

Content representation
----------------------

TBW. Will talk about:

1. JSON
2. YAML
3. ASSISTED INTERFACES

Tech
----

Our implementation will be based on tools and technologies we believe in
and work with, such as:

-  Python programming language.
-  Django, the python based web framework.
-  JSON for content storage and JSON schema for generating editing
   interfaces base.
-  PostgreSQL JSON data type for even querying our JSON content.
-  Javascript for providing editing interfaces on web pages.


Contributors
------------

-  `Mauro Bianchi <https://github.com/bianchimro>`__
