Concepts
========

Page
----

Content of a website is naturally structured into **pages**.

A **page** is a logical grouping of contents with the following traits:

- has its own **slug** that specifies where the page is located within the pages
  tree and is used to build the page url.
- an optional language
- an optional key used for versioning and publishing workflows
- a page has one or more **regions** where pieces of content can be added.
  Available regions are defined by the **page template**
- the actual data representing the content, keyed by region

A page may have a "parent" field pointing to another page and an "order" field (integer)
that identifies the order within the parent

A page also contains an optional data section useful for annotating the page.


Page backends
-------------

Pages can be stored with different backends

The following backends are provided:

- FlatFilesBackend (file system, yaml format)
- SQLBackend (django models)
