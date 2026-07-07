---
title: "Writing an invoice transmission plugin"
source: "https://docs.pretix.eu/dev/development/api/invoicetransmission.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/invoicetransmission.html](https://docs.pretix.eu/dev/development/api/invoicetransmission.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-an-invoice-transmission-plugin" class="section">

# Writing an invoice transmission plugin

An invoice transmission provider transports an invoice from the sender to the recipient. There are pre-defined types of invoice transmission in pretix, currently <span class="pre">`"email"`</span>, <span class="pre">`"peppol"`</span>, and <span class="pre">`"it_sdi"`</span>. You can find more information about them at <a href="invoices.md#rest-transmission-types" class="reference internal"><span class="std std-ref">Transmission types</span></a>.

New transmission types can not be added by plugins but need to be added to pretix itself. However, plugins can provide implementations for the actual transmission. Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div id="output-registration" class="section">

## Output registration

New invoice transmission providers can be registered through the <a href="plugins.md#registries" class="reference internal"><span class="std std-ref">registry</span></a> mechanism

<div class="highlight-python notranslate">

<div class="highlight">

    1from pretix.base.invoicing.transmission import transmission_providers, TransmissionProvider
    2
    3@transmission_providers.new()
    4class SdiTransmissionProvider(TransmissionProvider):
    5    identifier = "fatturapa_providerabc"
    6    type = "it_sdi"
    7    verbose_name = _("FatturaPA through provider ABC")
    8    ...

</div>

</div>

</div>

<div id="the-provider-class" class="section">

## The provider class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.invoicing.transmission.</span></span><span class="sig-name descname"><span class="pre">TransmissionProvider</span></span>  
<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this transmission provider. This should only contain lowercase letters and underscores.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">type</span></span>  
Identifier of the transmission type this provider provides.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for this transmission provider (can be localized).

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">priority</span></span>  
Returns a priority that is used for sorting transmission providers. Higher priority will be chosen over lower priority for transmission. Default to 100.

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">testmode_supported</span></span>  
Whether testmode invoices may be passed to this provider.

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">is_ready</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">event</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
Return whether this provider has all required configuration to be used in this event.

This is an abstract method, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">is_available</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">event</span></span>*, *<span class="n"><span class="pre">country</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Country</span></span>*, *<span class="n"><span class="pre">is_business</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
Return whether this provider may be used for an invoice for the given recipient country and address type.

This is an abstract method, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">transmit</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">invoice</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Invoice" class="reference internal" title="pretix.base.models.invoices.Invoice"><span class="pre">Invoice</span></a></span>*<span class="sig-paren">)</span>  
Transmit the invoice. The invoice passed as a parameter will be in status <span class="pre">`TRANSMISSION_STATUS_INFLIGHT`</span>. Invoices that stay in this state for more than 24h will be retried automatically. Implementations are expected to:

- Send the invoice.

- Update the <span class="pre">`transmission_status`</span> to TRANSMISSION_STATUS_COMPLETED or TRANSMISSION_STATUS_FAILED after sending, as well as <span class="pre">`transmission_info`</span> with provider-specific data, and <span class="pre">`transmission_date`</span> to the date and time of completion.

- Create a log entry of action type <span class="pre">`pretix.event.order.invoice.sent`</span> or <span class="pre">`pretix.event.order.invoice.sending_failed`</span> with the fields <span class="pre">`full_invoice_no`</span>, <span class="pre">`transmission_provider`</span>, <span class="pre">`transmission_type`</span> and a provider-specific <span class="pre">`data`</span> field.

Make sure to either handle <span class="pre">`invoice.order.testmode`</span> properly or set <span class="pre">`testmode_supported`</span> to <span class="pre">`False`</span>.

This is an abstract method, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">TransmissionProvider.</span></span><span class="sig-name descname"><span class="pre">settings_url</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">event</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span></span>  
Return a URL to the settings page of this provider (if any).

</div>

</div>

</div>

</div>
