# Contento

**Contento** is an open source cms system for the web. It comes in two parts:

* a features specification 
* an implementation for the Django web framework

## Why another CMS
There are a lot of CMS systems around there, some with lots of feature and production-ready quality, being used on first-class websites.

We cannot say we're not happy with what's around, but our experience working with different CMS and our use cases led us to try and develop our solution to content editing for the web.

## Manifesto

These are the principles **contento** is being built on. They're all opinionable but we'll stick to them. 

1. Content should never break your website.
2. Content should be easy to serialize, store, and move around a website or even different websites. 
3. Editing content should be performed with an interface suitable both for the content and for the editor. Our editing paradigm is WYSIWIM (what you see is what you mean) and not WYSIWIG (what you see is what you get). We aim at building **responsive editing** vs. rich editing interfaces.
4. CMS should be just related to editing content on a website. It should not dictate the structure of the web site or become a constraint when it comes to adding other functionalities or keeping your web framework up to date.
5. CMS should be able to fit within any webpage design.
6. CMS should be extensible in order to handle different kind of content (think of texts, images, maps, image galleries). And it should be easy to implement such extensions.


## WYSIWIM and responsive editing

Working on digital content gives us the possibility to edit it in ways that are different from how it will be displayed to the public. We should leverage this freedom.

WYSIWYG (what you see is what you get) is for manifacturing the real world, but in the digital world it leads to complex and artificial interfaces that are normally very complex to build and to use, often leaving us with lack of control and a frustrated editors that cannot realize what they have in mind.

Our approach to content editing is WYSIWIM (what you see is what you mean): an editor should be provided with an interface that gives her a better control at her level of understanding of what she's working on. For example on a website we always display HTML but editing on a text could be performed in Markdown or other simplified markup formats for most of the cases.   

WYSIWIM, coupled with a real-time preview (... and possibly enough space on your screen) can lead to better control in content editing and makes easier to build and maintain editing interfaces for different kind of content.

WYSIWIM does not mean "raw" editing, it focus on using the right tool for tuning a precise aspect of your content, based on what you want to touch and possibily on who you are. This introduces the concept of **responsive editing**: providing the right editing interface for the right situation.

## Core concepts and features

TBW

### Fragments

### Pages

### Trees

### Progressive editing interfaces

### Content relations

### Versioning

### i18n

### Publishing workflows

##  Content representation

TBW. Will talk about:

1. JSON
2. YAML
3. ASSISTED INTERFACES

## Tech

Our implementation will be based on tools and technologies we believe in and work with, such as:

- Python programming language.
- Django, the python based web framework. 
- JSON for content storage and JSON schema for generating editing interfaces base. 
- PostgreSQL JSON data type for even querying our JSON content.
- Javascript for providing editing interfaces on web pages.


## Development

Development is lead by the [INMAGIK](https://www.inmagik.com) team.

## Contributors

* [Mauro Bianchi](https://github.com/bianchimro)

