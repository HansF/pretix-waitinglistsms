---
title: "Writing a ticket output plugin"
source: "https://docs.pretix.eu/dev/development/api/ticketoutput.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/ticketoutput.html](https://docs.pretix.eu/dev/development/api/ticketoutput.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-a-ticket-output-plugin" class="section">

# Writing a ticket output plugin

A ticket output is a method to offer a ticket (an order) for the user to download.

In this document, we will walk through the creation of a ticket output plugin. This is very similar to creating an export output.

Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div id="output-registration" class="section">

## Output registration

The ticket output API does not make a lot of usage from signals, however, it does use a signal to get a list of all available ticket outputs. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.ticketoutput.BaseTicketOutput`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_ticket_outputs
    4
    5
    6@receiver(register_ticket_outputs, dispatch_uid="output_pdf")
    7def register_ticket_output(sender, **kwargs):
    8    from .ticketoutput import PdfTicketOutput
    9    return PdfTicketOutput

</div>

</div>

</div>

<div id="the-output-class" class="section">

## The output class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.ticketoutput.</span></span><span class="sig-name descname"><span class="pre">BaseTicketOutput</span></span>  
The central object of each ticket output is the subclass of <span class="pre">`BaseTicketOutput`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">settings</span></span>  
The default constructor sets this property to a <span class="pre">`SettingsSandbox`</span> object. You can use this object to store settings using its <span class="pre">`get`</span> and <span class="pre">`set`</span> methods. All settings you store are transparently prefixed, so you get your very own settings namespace.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this ticket output. This should only contain lowercase letters and in most cases will be the same as your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for this ticket output. This should be short but self-explanatory. Good examples include ‘PDF tickets’ and ‘Passbook’.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">is_enabled</span></span>  
Returns whether or whether not this output is enabled. By default, this is determined by the value of the <span class="pre">`_enabled`</span> setting.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">multi_download_enabled</span></span>  
Returns whether or not the <span class="pre">`generate_order`</span> method may be called. Returns <span class="pre">`True`</span> by default.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">settings_form_fields</span></span>  
When the event’s administrator visits the event configuration page, this method is called to return the configuration fields available.

It should therefore return a dictionary where the keys should be (unprefixed) settings keys and the values should be corresponding Django form fields.

The default implementation returns the appropriate fields for the <span class="pre">`_enabled`</span> setting mentioned above.

We suggest that you return an <span class="pre">`OrderedDict`</span> object instead of a dictionary and make use of the default implementation. Your implementation could look like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1@property
     2def settings_form_fields(self):
     3    return OrderedDict(
     4        list(super().settings_form_fields.items()) + [
     5            ('paper_size',
     6             forms.CharField(
     7                 label=_('Paper size'),
     8                 required=False
     9             ))
    10        ]
    11    )

</div>

</div>

<div class="admonition warning">

Warning

It is highly discouraged to alter the <span class="pre">`_enabled`</span> field of the default implementation.

</div>

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">settings_content_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
When the event’s administrator visits the event configuration page, this method is called. It may return HTML containing additional information that is displayed below the form fields configured in <span class="pre">`settings_form_fields`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">generate</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">position</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPosition" class="reference internal" title="pretix.base.models.orders.OrderPosition"><span class="pre">OrderPosition</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>  
This method should generate the download file and return a tuple consisting of a filename, a file type and file content. The extension will be taken from the filename which is otherwise ignored.

Alternatively, you can pass a tuple consisting of an arbitrary string, <span class="pre">`text/uri-list`</span> and a single URL. In this case, the user will be redirected to this link instead of being asked to download a generated file.

<div class="admonition note">

Note

If the event uses the event series feature (internally called subevents) and your generated ticket contains information like the event name or date, you probably want to display the properties of the subevent. A common pattern to do this would be a declaration <span class="pre">`ev`</span>` `<span class="pre">`=`</span>` `<span class="pre">`position.subevent`</span>` `<span class="pre">`or`</span>` `<span class="pre">`position.order.event`</span> and then access properties that are present on both classes like <span class="pre">`ev.name`</span> or <span class="pre">`ev.date_from`</span>.

</div>

<div class="admonition note">

Note

Should you elect to use the URI redirection feature instead of offering downloads, you should also set the <span class="pre">`multi_download_enabled`</span>-property to <span class="pre">`False`</span>.

</div>

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">generate_order</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>  
This method is the same as order() but should not generate one file per order position but instead one file for the full order.

This method is optional to implement. If you don’t implement it, the default implementation will offer a zip file of the generate() results for the order positions.

This method should generate a download file and return a tuple consisting of a filename, a file type and file content. The extension will be taken from the filename which is otherwise ignored.

If you override this method, make sure that positions that are addons (i.e. <span class="pre">`addon_to`</span> is set) are only outputted if the event setting <span class="pre">`ticket_download_addons`</span> is active. Do the same for positions that are non-admission without <span class="pre">`ticket_download_nonadm`</span> active. If you want, you can just iterate over <span class="pre">`order.positions_with_tickets`</span> which applies the appropriate filters for you.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">download_button_text</span></span>  
The text on the download button in the frontend.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">download_button_icon</span></span>  
The Font Awesome icon on the download button in the frontend.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">multi_download_button_text</span></span>  
The text on the multi download button in the frontend.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">long_download_button_text</span></span>  
The text on the large download button in the frontend.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">preview_allowed</span></span>  
By default, the <span class="pre">`generate()`</span> method is called for generating a preview in the pretix backend. In case your plugin cannot generate previews for any reason, you can manually disable it here.

<span class="sig-prename descclassname"><span class="pre">BaseTicketOutput.</span></span><span class="sig-name descname"><span class="pre">javascript_required</span></span>  
If this property is set to true, the download-button for this ticket-type will not be displayed when the user’s browser has JavaScript disabled.

Defaults to <span class="pre">`False`</span>

</div>

</div>

</div>

</div>
