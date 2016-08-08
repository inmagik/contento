Concepts
========

Page
----

Content of a website is naturally structured into **pages**.

A **page** is a logical grouping of contents with the following traits:

- has an "label" used to identify the label
- an optional language
- an optional key used for versioning and publishing workflows
- has its own **slug** that contributes at building the page_url and for passing
  parameters to its own renderers
- a page has one or more **regions** where pieces of content can be added.
  Available regions are defined by the **page_template**
- the actual data representing the content, keyed by region. Data is represented as a dictionary
  and the actual meaning of its contents is deferred to the renderers.
- a page may have a "parent" field pointing to another page and an "order" field (integer)
that identifies the order within the parent.
- page also contains an optional data section useful for annotating the page.


Page backends
-------------

Pages can be stored with different backends

The following backends are provided:

- FlatFilesBackend (file system, yaml format)
- SQLBackend (django models)
