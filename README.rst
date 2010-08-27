======================
django-representations
======================
A set of template tags that helps in displaying objects various ways.
---------------------------------------------------------------------

django-representations is a set of template tags that helps in displaying
objects various ways. It was forked from the original version by Eric Moritz.


Tags
====

Represent
---------
This tag takes a model and passes it and the context to
a template in the following location:

representations/app_label/object_name/[template] or
representations/app_label/[template] or
representations/[template] (whichever comes first)
{% represent [model] as "[template]" %}

This allows you to have the same representation for the object in numerous
templates.

This also allows you to have a list of mixed content types and if they all have
representation templates made, you display them all in the same list.

For instance you can have a list of videos, photes, blog entries and news stories
and if all of them has a representation of "summary.html" you could make a single
list of all the objects.
