---
title: "Writing an exporter plugin"
source: "https://docs.pretix.eu/dev/development/api/exporter.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/exporter.html](https://docs.pretix.eu/dev/development/api/exporter.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-an-exporter-plugin" class="section">

# Writing an exporter plugin

An Exporter is a method to export the product and order data in pretix for later use in another program.

In this document, we will walk through the creation of an exporter output plugin step by step.

Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div id="exporter-registration" class="section">

## Exporter registration

The exporter API does not make a lot of usage from signals, however, it does use a signal to get a list of all available exporters. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.exporter.BaseExporter`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_data_exporters
    4
    5
    6@receiver(register_data_exporters, dispatch_uid="exporter_myexporter")
    7def register_data_exporter(sender, **kwargs):
    8    from .exporter import MyExporter
    9    return MyExporter

</div>

</div>

Some exporters might also prove to be useful, when provided on an organizer-level. In order to declare your exporter as capable of providing exports spanning multiple events, your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.exporter.BaseExporter`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_multievent_data_exporters
    4
    5
    6@receiver(register_multievent_data_exporters, dispatch_uid="multieventexporter_myexporter")
    7def register_multievent_data_exporter(sender, **kwargs):
    8    from .exporter import MyExporter
    9    return MyExporter

</div>

</div>

If your exporter supports both event-level and multi-event level exports, you will need to listen for both signals.

</div>

<div id="the-exporter-class" class="section">

## The exporter class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.exporter.</span></span><span class="sig-name descname"><span class="pre">BaseExporter</span></span>  
The central object of each exporter is the subclass of <span class="pre">`BaseExporter`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for. This will be <span class="pre">`None`</span> if the exporter is run for multiple events.

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">events</span></span>  
The default constructor sets this property to the list of events to work on, regardless of whether the exporter is called for one or multiple events.

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this exporter. This should only contain lowercase letters and in most cases will be the same as your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for this exporter. This should be short but self-explaining. Good examples include ‘Orders as JSON’ or ‘Orders as Microsoft Excel’.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">description</span></span>  
A description for this exporter.

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">category</span></span>  
A category name for this exporter, or <span class="pre">`None`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">export_form_fields</span></span>  
When the event’s administrator visits the export page, this method is called to return the configuration fields available.

It should therefore return a dictionary where the keys should be field names and the values should be corresponding Django form fields.

We suggest that you return an <span class="pre">`OrderedDict`</span> object instead of a dictionary. Your implementation could look like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1@property
     2def export_form_fields(self):
     3    return OrderedDict(
     4        [
     5            ('tab_width',
     6             forms.IntegerField(
     7                 label=_('Tab width'),
     8                 default=4
     9             ))
    10        ]
    11    )

</div>

</div>

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">repeatable_read</span></span>  
If <span class="pre">`True`</span>, this exporter will be run in a REPEATABLE READ transaction. This ensures consistent results for all queries performed by the exporter, but creates a performance burden on the database server. We recommend to disable this for exporters that take very long to run and do not rely on this behavior, such as export of lists to CSV files.

Defaults to <span class="pre">`True`</span> for now, but default may change in future versions.

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">form_data</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">bytes</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span><span class="p"><span class="pre">\]</span></span></span></span>  
Render the exported file and return a tuple consisting of a filename, a file type and file content.

Parameters<span class="colon">:</span>  
- **form_data** (*dict*) – The form data of the export details form

- **output_file** – You can optionally accept a parameter that will be given a file handle to write the output to. In this case, you can return None instead of the file content.

Note: If you use a <span class="pre">`ModelChoiceField`</span> (or a <span class="pre">`ModelMultipleChoiceField`</span>), the <span class="pre">`form_data`</span> will not contain the model instance but only it’s primary key (or a list of primary keys) for reasons of internal serialization when using background tasks.

This is an abstract method, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">available_for_user</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">user</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
Allows to do additional checks whether an exporter is available based on the user who calls it. Note that <span class="pre">`user`</span> may be <span class="pre">`None`</span> e.g. during API usage.

<span class="property"><span class="k"><span class="pre">classmethod</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">BaseExporter.</span></span><span class="sig-name descname"><span class="pre">get_required_event_permission</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span></span>  
The permission level required to use this exporter for events. For multi-event-exports, this will be used to limit the selection of events. Will be ignored if the <span class="pre">`OrganizerLevelExportMixin`</span> mixin is used. The default implementation returns <span class="pre">`"event.orders:read"`</span>.

On organizer level, by default exporters are expected to handle on a *set of events* and the system will automatically add a form field that allows the selection of events, limited to events the user has correct permissions for. If this does not fit your organizer, because it is not related to events, you should **also** inherit from the following class:

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.exporter.</span></span><span class="sig-name descname"><span class="pre">OrganizerLevelExportMixin</span></span>  
<span class="property"><span class="k"><span class="pre">classmethod</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">OrganizerLevelExportMixin.</span></span><span class="sig-name descname"><span class="pre">get_required_organizer_permission</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span></span>  
The permission level required to use this exporter. Must be set for organizer-level exports. Set to None to allow everyone with any access to the organizer.

<span class="pre">`get_required_event_permission`</span> will be ignored on this class.

</div>

</div>

</div>

</div>
