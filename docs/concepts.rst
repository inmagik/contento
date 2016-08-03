Concepts
========

Page
----

Content of a website is naturally structured into **pages**.

A **page** is a logical grouping of contents with the following traits:

- has a **title** that identifies the group of contents.
- has its own **slug** that specifies where the page is located within the pages
  tree and is used to build the page url.
- a page has one or more **regions** where pieces of content can be added.
  Available regions are defined by the **page template**


Content
-------

Pages define how content fits into the HTML markup of your site.
Actual pages contents are defined in another data structure, called **content**.

This additional data layer has been introduced for providing multiple "variations" of a single page,
that allows us to provide features such as i18n, flexibile publishing workflows and content versioning.

A content contains:

- a reference to a page, (by label)
- an optional language
- an optional key used for versioning and publishing workflows
- the actual data representing the content
