======================
django-representations
======================
A set of template tags that helps in displaying objects various ways.

About
-----
django-representations contains template tag that helps in representing
objects in several ways, dependent on the template selected and the object
type. It was forked from the original version by Eric Moritz.

For instance, for a list of blog entries: 

diario/entry_archive_day.html:: 

	... 
	{% represent entry as "summary.html" %}
	...

diario/entry_archive.html::

	...
	{% represent entry as "summary.html" %}
	...

diario/entry_detail.html::

	...
	{% represent entry as "detail.html" %}
	...

Each template is placed in `representations/diario/entry/`, for example. When
no template is found there, the tag looks for the named template in
`representations/diario/` and, lastly, `representations/` is tried. This
allows for easy overriding of templates for specific apps or object types
while maintaining generic representations for other objects.

The power of this convention is revealed when you do something like a search
engine that may be a list of different content types::

	{% for object in search_result_list %}
		{% represent object as "search_result.html" %} 
	{% endfor %}

Installation
------------
First make sure you install `django-representations` into you Python path::

	git clone git://github.com/dokterbob/django-representations.git
	cd django-representations
	python setup.py install

Next, add the application to your `INSTALLED_APPLICATIONS` in `settings.py`::

	INSTALLED_APPLICATIONS = (
	    ...
		representations,
		...
	)

Usage
-----
You can use the tag by loading the template library::

	...
	{% load representations %}
	...
	{% represent [model] as "[template]" %}

This tag takes a model and passes it and the context to
the named template, which will be looked for in the following locations (in order):

#) representations/app_label/object_name/[template]
#) representations/app_label/[template]
#) representations/[template]

The first one where the named template is found, will be used. This allows you
to have the same representation for the object in numerous templates.

This also allows you to have a list of mixed content types and if they all have
representation templates made, you display them all in the same list.

For instance you can have a list of videos, photes, blog entries and news stories
and if all of them has a representation of "summary.html" you could make a single
list of all the objects.
