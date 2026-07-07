---
title: "Plugin quality checklist"
source: "https://docs.pretix.eu/dev/development/api/quality.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/quality.html](https://docs.pretix.eu/dev/development/api/quality.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="plugin-quality-checklist" class="section">

<span id="pluginquality"></span>

# Plugin quality checklist

If you want to write a high-quality pretix plugin, this is a list of things you should check before you publish it. This is also a list of things that we check, if we consider installing an externally developed plugin on our hosted infrastructure.

<div id="a-meta" class="section">

## A. Meta

1.  The plugin is clearly licensed under an appropriate license.

2.  The plugin has an unambiguous name, description, and author metadata.

3.  The plugin has a clear versioning scheme and the latest version of the plugin is kept compatible to the latest stable version of pretix.

4.  The plugin is properly packaged using standard Python packaging tools.

5.  The plugin correctly declares its external dependencies.

6.  A contact address is provided in case of security issues.

</div>

<div id="b-isolation" class="section">

## B. Isolation

1.  If any signal receivers use the <a href="https://docs.djangoproject.com/en/2.0/topics/signals/#django.dispatch.Signal.connect" class="reference external">dispatch_uid</a> feature, the UIDs are prefixed by the plugin’s name and do not clash with other plugins.

2.  If any templates or static files are shipped, they are located in subdirectories with the name of the plugin and do not clash with other plugins or core files.

3.  Any keys stored to the settings store are prefixed with the plugin’s name and do not clash with other plugins or core.

4.  Any keys stored to the user session are prefixed with the plugin’s name and do not clash with other plugins or core.

5.  Any registered URLs are unlikely to clash with other plugins or future core URLs.

</div>

<div id="c-security" class="section">

## C. Security

1.  All important actions are logged to the <a href="logging.md#logging" class="reference internal"><span class="std std-ref">shared log storage</span></a> and a signal receiver is registered to provide a human-readable representation of the log entry.

2.  All views require appropriate permissions and use the <span class="pre">`event_urls`</span> mechanism if appropriate. <a href="customview.md#customview" class="reference internal"><span class="std std-ref">Read more</span></a>

3.  Any session data for customers is stored in the cart session system if appropriate.

4.  If the plugin is a payment provider:

> <div>
>
> 1.  No credit card numbers may be stored within pretix.
>
> 2.  A notification/webhook system is implemented to notify pretix of any refunds.
>
> 3.  If such a webhook system is implemented, contents of incoming webhooks are either verified using a cryptographic signature or are not being trusted and all data is fetched from an API instead.
>
> </div>

</div>

<div id="d-privacy" class="section">

## D. Privacy

1.  No personal data is stored that is not required for the plugin’s functionality.

2.  For any personal data that is saved to the database, an appropriate <a href="shredder.md#shredder" class="reference internal"><span class="std std-ref">data shredder</span></a> is provided that offers the data for download and then removes it from the database (including log entries).

</div>

<div id="e-internationalization" class="section">

## E. Internationalization

1.  All user-facing strings in templates, Python code, and templates are wrapped in <a href="https://docs.djangoproject.com/en/2.0/topics/i18n/translation/" class="reference external">gettext calls</a>.

2.  No languages, time zones, date formats, or time formats are hardcoded.

3.  Installing the plugin automatically compiles <span class="pre">`.po`</span> files to <span class="pre">`.mo`</span> files. This is fulfilled automatically if you use the <span class="pre">`setup.py`</span> file form our plugin cookiecutter.

</div>

<div id="f-functionality" class="section">

## F. Functionality

1.  If the plugin adds any database models or relationships from the settings storage to database models, it registers a receiver to the <a href="general.md#pretix.base.signals.event_copy_data" class="reference internal" title="pretix.base.signals.event_copy_data"><span class="pre"><code class="sourceCode python xref py py-attr docutils literal notranslate">pretix.base.signals.event_copy_data</code></span></a> or <a href="general.md#pretix.base.signals.item_copy_data" class="reference internal" title="pretix.base.signals.item_copy_data"><span class="pre"><code class="sourceCode python xref py py-attr docutils literal notranslate">pretix.base.signals.item_copy_data</code></span></a> signals.

2.  If the plugin is a payment provider:

    > <div>
    >
    > 1.  A webhook-like system is implemented if payment confirmations are not sent instantly.
    >
    > 2.  Refunds are implemented, if possible.
    >
    > 3.  In case of overpayment or external refunds, an external refund is properly created.
    >
    > </div>

3.  If the plugin adds steps to the checkout process, it has been tested in combination with the pretix widget.

</div>

<div id="g-code-quality" class="section">

## G. Code quality

1.  <a href="https://www.google.de/search?q=isort&amp;oq=isort&amp;aqs=chrome..69i57j0j69i59j69i60l2j69i59.599j0j4&amp;sourceid=chrome&amp;ie=UTF-8" class="reference external">isort</a> and <a href="http://flake8.pycqa.org/en/latest/" class="reference external">flake8</a> are used to ensure consistent code styling.

2.  Unit tests are provided for important pieces of business logic.

3.  Functional tests are provided for important interface parts.

4.  Tests are provided to check that permission checks are working.

5.  Continuous Integration is set up to check that tests are passing and styling is consistent.

</div>

<div id="h-specific-to-pretix-eu" class="section">

## H. Specific to pretix.eu

1.  pretix.eu integrates the data stored by this plugin with its data report features.

2.  pretix.eu integrates this plugin in its generated privacy statements, if necessary.

</div>

</div>

</div>

</div>
