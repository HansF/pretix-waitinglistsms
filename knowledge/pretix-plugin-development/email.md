---
title: "Writing an HTML e-mail renderer plugin"
source: "https://docs.pretix.eu/dev/development/api/email.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/email.html](https://docs.pretix.eu/dev/development/api/email.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-an-html-e-mail-renderer-plugin" class="section">

# Writing an HTML e-mail renderer plugin

An email renderer class controls how the HTML part of e-mails sent by pretix is built. The creation of such a plugin is very similar to creating an export output.

Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div id="output-registration" class="section">

## Output registration

The email HTML renderer API does not make a lot of usage from signals, however, it does use a signal to get a list of all available email renderers. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.email.BaseHTMLMailRenderer`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_html_mail_renderers
    4
    5
    6@receiver(register_html_mail_renderers, dispatch_uid="renderer_custom")
    7def register_mail_renderers(sender, **kwargs):
    8    from .email import MyMailRenderer
    9    return MyMailRenderer

</div>

</div>

</div>

<div id="the-renderer-class" class="section">

## The renderer class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.email.</span></span><span class="sig-name descname"><span class="pre">BaseHTMLMailRenderer</span></span>  
The central object of each email renderer is the subclass of <span class="pre">`BaseHTMLMailRenderer`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseHTMLMailRenderer.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for.

<span class="sig-prename descclassname"><span class="pre">BaseHTMLMailRenderer.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this renderer. This should only contain lowercase letters and in most cases will be the same as your package name or prefixed with your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseHTMLMailRenderer.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for this renderer. This should be short but self-explanatory.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseHTMLMailRenderer.</span></span><span class="sig-name descname"><span class="pre">thumbnail_filename</span></span>  
A file name discoverable in the static file storage that contains a preview of your renderer. This should be with aspect resolution 4:3.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseHTMLMailRenderer.</span></span><span class="sig-name descname"><span class="pre">is_available</span></span>  
This renderer will only be available if this returns <span class="pre">`True`</span>. You can use this to limit this renderer to certain events. Defaults to <span class="pre">`True`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseHTMLMailRenderer.</span></span><span class="sig-name descname"><span class="pre">render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">plain_body</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">plain_signature</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">subject</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">order</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">position</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">context</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
This method should generate the HTML part of the email.

Parameters<span class="colon">:</span>  
- **plain_body** – The body of the email in plain text.

- **plain_signature** – The signature with event organizer contact details in plain text.

- **subject** – The email subject.

- **order** – The order if this email is connected to one, otherwise <span class="pre">`None`</span>.

- **position** – The order position if this email is connected to one, otherwise <span class="pre">`None`</span>.

- **context** – Context to use to render placeholders in the plain body

Returns<span class="colon">:</span>  
An HTML string

This is an abstract method, you **must** implement this!

</div>

<div id="helper-class-for-template-base-renderers" class="section">

## Helper class for template-base renderers

The email renderer that ships with pretix is based on Django templates to generate HTML. In case you also want to render emails based on a template, we provided a ready-made base class <span class="pre">`TemplateBasedMailRenderer`</span> that you can re-use to perform the following steps:

- Convert the body text and the signature to HTML using our markdown renderer

- Render the template

- Call <a href="https://pypi.org/project/inlinestyler/" class="reference external">inlinestyler</a> to convert all <span class="pre">`<style>`</span> style sheets to inline <span class="pre">`style=""`</span> attributes for better compatibility

To use it, you just need to implement some variables:

<div class="highlight-python notranslate">

<div class="highlight">

    1class ClassicMailRenderer(TemplateBasedMailRenderer):
    2    verbose_name = _('pretix default')
    3    identifier = 'classic'
    4    thumbnail_filename = 'pretixbase/email/thumb.png'
    5    template_name = 'pretixbase/email/plainwrapper.html'

</div>

</div>

The template is passed the following context variables:

<span class="pre">`site`</span>  
Name of the pretix installation (<span class="pre">`settings.PRETIX_INSTANCE_NAME`</span>)

<span class="pre">`site_url`</span>  
Root URL of the pretix installation (<span class="pre">`settings.SITE_URL`</span>)

<span class="pre">`body`</span>  
The body as markdown (render with <span class="pre">`{{`</span>` `<span class="pre">`body|safe`</span>` `<span class="pre">`}}`</span>)

<span class="pre">`subject`</span>  
The email subject

<span class="pre">`color`</span>  
The primary color of the event

<span class="pre">`event`</span>  
The <span class="pre">`Event`</span> object

<span class="pre">`signature`</span> (optional, only if configured)  
The signature with event organizer contact details as markdown (render with <span class="pre">`{{`</span>` `<span class="pre">`signature|safe`</span>` `<span class="pre">`}}`</span>)

<span class="pre">`order`</span> (optional, only if applicable)  
The <span class="pre">`Order`</span> object

<span class="pre">`position`</span> (optional, only if applicable)  
The <span class="pre">`OrderPosition`</span> object

</div>

</div>

</div>

</div>
