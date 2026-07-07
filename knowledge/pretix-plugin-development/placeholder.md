---
title: "Writing a template placeholder plugin"
source: "https://docs.pretix.eu/dev/development/api/placeholder.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/placeholder.html](https://docs.pretix.eu/dev/development/api/placeholder.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-a-template-placeholder-plugin" class="section">

# Writing a template placeholder plugin

A template placeholder is a dynamic value that pretix users can use in their email templates and in other configurable texts.

Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div id="placeholder-registration" class="section">

## Placeholder registration

The placeholder API does not make a lot of usage from signals, however, it does use a signal to get a list of all available placeholders. Your plugin should listen for this signal and return an instance of a subclass of <span class="pre">`pretix.base.services.placeholders.BaseTextPlaceholder`</span>:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_text_placeholders
    4
    5
    6@receiver(register_text_placeholders, dispatch_uid="placeholder_custom")
    7def register_placeholder_renderers(sender, **kwargs):
    8    from .placeholders import MyPlaceholderClass
    9    return MyPlaceholder()

</div>

</div>

</div>

<div id="context-mechanism" class="section">

## Context mechanism

Templates are used in different “contexts” within pretix. For example, many emails are rendered from templates in the context of an order, but some are not, such as the notification of a waiting list voucher.

Not all placeholders make sense everywhere, and placeholders usually depend on some parameters themselves, such as the <span class="pre">`Order`</span> object. Therefore, placeholders are expected to explicitly declare what values they depend on and they will only be available in a context where all those dependencies are met. Currently, placeholders can depend on the following context parameters:

- <span class="pre">`event`</span>

- <span class="pre">`order`</span>

- <span class="pre">`position`</span>

- <span class="pre">`waiting_list_entry`</span>

- <span class="pre">`invoice_address`</span>

- <span class="pre">`payment`</span>

There are a few more that are only to be used internally but not by plugins.

</div>

<div id="the-placeholder-class" class="section">

## The placeholder class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.services.placeholders.</span></span><span class="sig-name descname"><span class="pre">BaseTextPlaceholder</span></span>  
<span class="sig-prename descclassname"><span class="pre">BaseTextPlaceholder.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
This should return the identifier of this placeholder in the email.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseTextPlaceholder.</span></span><span class="sig-name descname"><span class="pre">required_context</span></span>  
This property should return a list of all attribute names that need to be contained in the base context so that this placeholder is available. By default, it returns a list containing the string “event”.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseTextPlaceholder.</span></span><span class="sig-name descname"><span class="pre">render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">context</span></span>*<span class="sig-paren">)</span>  
This method is called to generate the actual text that is being used in the email. You will be passed a context dictionary with the base context attributes specified in <span class="pre">`required_context`</span>. You are expected to return a plain-text string.

This is an abstract method, you **must** implement this!

<span class="sig-prename descclassname"><span class="pre">BaseTextPlaceholder.</span></span><span class="sig-name descname"><span class="pre">render_sample</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">event</span></span>*<span class="sig-paren">)</span>  
This method is called to generate a text to be used in email previews. This may only depend on the event.

This is an abstract method, you **must** implement this!

</div>

<div id="helper-class-for-simple-placeholders" class="section">

## Helper class for simple placeholders

pretix ships with a helper class that makes it easy to provide placeholders based on simple functions:

<div class="highlight-python notranslate">

<div class="highlight">

    placeholder = SimpleFunctionalTextPlaceholder(
        'code', ['order'], lambda order: order.code, sample='F8VVL'
    )

</div>

</div>

</div>

<div id="signals" class="section">

## Signals

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_text_placeholders</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known text placeholders. Receivers should return an instance of a subclass of pretix.base.services.placeholders.BaseTextPlaceholder or a list of these.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_mail_placeholders</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
**DEPRECATED**: This signal has a new name, please use <span class="pre">`register_text_placeholders`</span> instead.

</div>

</div>

</div>

</div>
