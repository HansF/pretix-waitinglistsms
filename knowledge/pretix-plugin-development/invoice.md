---
title: "Writing an invoice renderer plugin"
source: "https://docs.pretix.eu/dev/development/api/invoice.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/invoice.html](https://docs.pretix.eu/dev/development/api/invoice.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-an-invoice-renderer-plugin" class="section">

# Writing an invoice renderer plugin

An invoice renderer controls how invoice files are built. The creation of such a plugin is very similar to creating an export output.

Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div id="output-registration" class="section">

## Output registration

The invoice renderer API does not make a lot of usage from signals, however, it does use a signal to get a list of all available invoice renderers. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.invoice.BaseInvoiceRenderer`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_invoice_renderers
    4
    5
    6@receiver(register_invoice_renderers, dispatch_uid="output_custom")
    7def register_invoice_renderers(sender, **kwargs):
    8    from .invoice import MyInvoiceRenderer
    9    return MyInvoiceRenderer

</div>

</div>

</div>

<div id="the-renderer-class" class="section">

## The renderer class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.invoice.</span></span><span class="sig-name descname"><span class="pre">BaseInvoiceRenderer</span></span>  
The central object of each invoice renderer is the subclass of <span class="pre">`BaseInvoiceRenderer`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for.

<span class="sig-prename descclassname"><span class="pre">BaseInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this renderer. This should only contain lowercase letters and in most cases will be the same as your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for this renderer. This should be short but self-explanatory. Good examples include ‘German DIN 5008’ or ‘Italian invoice’.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">generate</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">invoice</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Invoice" class="reference internal" title="pretix.base.models.invoices.Invoice"><span class="pre">Invoice</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>  
This method should generate the invoice file and return a tuple consisting of a filename, a file type and file content. The extension will be taken from the filename which is otherwise ignored.

</div>

<div id="helper-class-for-reportlab-base-renderers" class="section">

## Helper class for reportlab-base renderers

All PDF rendering that ships with pretix is based on reportlab. We recommend to read the <a href="https://www.reportlab.com/docs/reportlab-userguide.pdf" class="reference external">reportlab User Guide</a> to understand all the concepts used here.

If you want to implement a renderer that also uses report lab, this helper class might be convenient to you:

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.invoice.</span></span><span class="sig-name descname"><span class="pre">BaseReportlabInvoiceRenderer</span></span>  
<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">pagesize</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">left_margin</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">right_margin</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">top_margin</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">bottom_margin</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">doc_template_class</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">invoice</span></span>  

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_init</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span>  
Initialize the renderer. By default, this registers fonts and sets <span class="pre">`self.stylesheet`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_get_stylesheet</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span>  
Get a stylesheet. By default, this contains the “Normal” and “Heading1” styles.

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_register_fonts</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span>  
Register fonts with reportlab. By default, this registers the OpenSans font family

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_on_first_page</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">canvas</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Canvas</span></span>*, *<span class="n"><span class="pre">doc</span></span>*<span class="sig-paren">)</span>  
Called when a new page is rendered that is the first page.

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_on_other_page</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">canvas</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Canvas</span></span>*, *<span class="n"><span class="pre">doc</span></span>*<span class="sig-paren">)</span>  
Called when a new page is rendered that is *not* the first page.

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_get_first_page_frames</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">doc</span></span>*<span class="sig-paren">)</span>  
Called to create a list of frames for the first page.

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_get_other_page_frames</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">doc</span></span>*<span class="sig-paren">)</span>  
Called to create a list of frames for the other pages.

<span class="sig-prename descclassname"><span class="pre">BaseReportlabInvoiceRenderer.</span></span><span class="sig-name descname"><span class="pre">\_build_doc</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">fhandle</span></span>*<span class="sig-paren">)</span>  
Build a PDF document in a given file handle

</div>

</div>

</div>

</div>
