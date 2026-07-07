---
title: "Creating a plugin"
source: "https://docs.pretix.eu/dev/development/api/plugins.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/plugins.html](https://docs.pretix.eu/dev/development/api/plugins.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="creating-a-plugin" class="section">

<span id="pluginsetup"></span>

# Creating a plugin

It is possible to extend pretix with custom Python code using the official plugin API. Every plugin has to be implemented as an independent Django ‘app’ living in its own python package installed like any other python module. There are also some official plugins inside the <span class="pre">`pretix/plugins/`</span> directory of your pretix installation.

The communication between pretix and the plugins happens mostly using Django’s <a href="https://docs.djangoproject.com/en/3.0/topics/signals/" class="reference external">signal dispatcher</a> feature. The core modules of pretix, <span class="pre">`pretix.base`</span>, <span class="pre">`pretix.control`</span> and <span class="pre">`pretix.presale`</span> expose a number of signals which are documented on the next pages.

To create a new plugin, create a new python package which must be a valid <a href="https://docs.djangoproject.com/en/3.0/ref/applications/" class="reference external">Django app</a> and must contain plugin metadata, as described below. There is some boilerplate that you will need for every plugin to get started. To save your time, we created a <a href="https://cookiecutter.readthedocs.io/en/latest/" class="reference external">cookiecutter</a> template that you can use like this:

<div class="highlight-python notranslate">

<div class="highlight">

    $ pip install cookiecutter
    $ cookiecutter https://github.com/pretix/pretix-plugin-cookiecutter

</div>

</div>

This will ask you some questions and then create a project folder for your plugin.

The following pages go into detail about the several types of plugins currently supported. While these instructions don’t assume that you know a lot about pretix, they do assume that you have prior knowledge about Django (e.g. its view layer, how its ORM works, etc.).

<div id="plugin-metadata" class="section">

## Plugin metadata

The plugin metadata lives inside a <span class="pre">`PretixPluginMeta`</span> class inside your app’s configuration class. The metadata class must define the following attributes:

| Attribute | Type | Description |
|----|----|----|
| name | string | The human-readable name of your plugin |
| author | string | Your name |
| version | string | A human-readable version code of your plugin |
| description | string | A more verbose description of what your plugin does. May contain HTML. |
| category | string | Category of a plugin. Either one of <span class="pre">`"FEATURE"`</span>, <span class="pre">`"PAYMENT"`</span>, <span class="pre">`"INTEGRATION"`</span>, <span class="pre">`"CUSTOMIZATION"`</span>, <span class="pre">`"FORMAT"`</span>, or <span class="pre">`"API"`</span>, or any other string. |
| picture | string (optional) | Path to a picture resolvable through the static file system. |
| featured | boolean (optional) | <span class="pre">`False`</span> by default, can promote a plugin if it’s something many users will want, use carefully. |
| visible | boolean (optional) | <span class="pre">`True`</span> by default, can hide a plugin so it cannot be normally activated. |
| restricted | boolean (optional) | <span class="pre">`False`</span> by default, restricts a plugin such that it can only be enabled for an event by system administrators / superusers. |
| experimental | boolean (optional) | <span class="pre">`False`</span> by default, marks a plugin as an experimental feature in the plugins list. |
| compatibility | string | Specifier for compatible pretix versions. |
| level | string | System level the plugin can be activated at. Set to <span class="pre">`pretix.base.plugins.PLUGIN_LEVEL_EVENT`</span> for plugins that can be activated at event level and then be active for that event only. Set to <span class="pre">`pretix.base.plugins.PLUGIN_LEVEL_ORGANIZER`</span> for plugins that can be activated only for the organizer as a whole and are active for any event within that organizer. Set to <span class="pre">`pretix.base.plugins.PLUGIN_LEVEL_EVENT_ORGANIZER_HYBRID`</span> for plugins that can be activated at organizer level but are considered active only within events for which they have also been specifically activated. More levels, e.g. user-level plugins, might be invented in the future. |
| settings_links | list | List of <span class="pre">`((menu`</span>` `<span class="pre">`name,`</span>` `<span class="pre">`submenu`</span>` `<span class="pre">`name,`</span>` `<span class="pre">`…),`</span>` `<span class="pre">`urlname,`</span>` `<span class="pre">`url_kwargs)`</span> tuples that point to the plugin’s settings. |
| navigation_links | list | List of <span class="pre">`((menu`</span>` `<span class="pre">`name,`</span>` `<span class="pre">`submenu`</span>` `<span class="pre">`name,`</span>` `<span class="pre">`…),`</span>` `<span class="pre">`urlname,`</span>` `<span class="pre">`url_kwargs)`</span> tuples that point to the plugin’s system pages. |

A working example would be:

<div class="highlight-python notranslate">

<div class="highlight">

     1try:
     2    from pretix.base.plugins import PluginConfig, PLUGIN_LEVEL_EVENT
     3except ImportError:
     4    raise RuntimeError("Please use pretix 2025.7 or above to run this plugin!")
     5from django.utils.translation import gettext_lazy as _
     6
     7
     8class PaypalApp(PluginConfig):
     9    name = 'pretix_paypal'
    10    verbose_name = _("PayPal")
    11
    12    class PretixPluginMeta:
    13        name = _("PayPal")
    14        author = _("the pretix team")
    15        version = '1.0.0'
    16        category = 'PAYMENT'
    17        picture = 'pretix_paypal/paypal_logo.svg'
    18        level = PLUGIN_LEVEL_EVENT
    19        visible = True
    20        featured = False
    21        restricted = False
    22        description = _("This plugin allows you to receive payments via PayPal")
    23        compatibility = "pretix>=2.7.0"
    24        settings_links = []
    25        navigation_links = []
    26
    27
    28default_app_config = 'pretix_paypal.PaypalApp'

</div>

</div>

The <span class="pre">`AppConfig`</span> class may implement a property <span class="pre">`compatibility_errors`</span>, that checks whether the pretix installation meets all requirements of the plugin. If so, it should contain <span class="pre">`None`</span> or an empty list, otherwise a list of strings containing human-readable error messages. We recommend using the <span class="pre">`django.utils.functional.cached_property`</span> decorator, as it might get called a lot. You can also implement <span class="pre">`compatibility_warnings`</span>, those will be displayed but not block the plugin execution.

The <span class="pre">`AppConfig`</span> class may implement a method <span class="pre">`is_available(event)`</span> that checks if a plugin is available for a specific event. If not, it will not be shown in the plugin list of that event. You should not define <span class="pre">`is_available`</span> and <span class="pre">`restricted`</span> on the same plugin.

</div>

<div id="plugin-registration" class="section">

## Plugin registration

Somehow, pretix needs to know that your plugin exists at all. For this purpose, we make use of the <a href="pkg_resources.md#locating-plugins" class="reference external">entry point</a> feature of setuptools. To register a plugin that lives in a separate python package, your <span class="pre">`setup.py`</span> should contain something like this:

<div class="highlight-python notranslate">

<div class="highlight">

    1setup(
    2    args...,
    3    entry_points="""
    4[pretix.plugin]
    5pretix_paypal=pretix_paypal:PretixPluginMeta
    6"""
    7)

</div>

</div>

This will automatically make pretix discover this plugin as soon as it is installed e.g. through <span class="pre">`pip`</span>. During development, you can just run <span class="pre">`python`</span>` `<span class="pre">`setup.py`</span>` `<span class="pre">`develop`</span> inside your plugin source directory to make it discoverable.

</div>

<div id="signals" class="section">

<span id="id1"></span>

## Signals

The various components of pretix define a number of signals which your plugin can listen for. We will go into the details of the different signals in the following pages. We suggest that you put your signal receivers into a <span class="pre">`signals`</span> submodule of your plugin. You should extend your <span class="pre">`AppConfig`</span> (see above) by the following method to make your receivers available:

<div class="highlight-python notranslate">

<div class="highlight">

    1class PaypalApp(AppConfig):
    2    …
    3
    4    def ready(self):
    5        from . import signals  # NOQA

</div>

</div>

You can optionally specify code that is executed when your plugin is activated for an event or organizer in the <span class="pre">`installed`</span> method:

<div class="highlight-python notranslate">

<div class="highlight">

    1class PaypalApp(AppConfig):
    2    …
    3
    4    def installed(self, event_or_organizer):
    5        pass  # Your code here

</div>

</div>

Note that <span class="pre">`installed`</span> will *not* be called if the plugin is indirectly activated for an event because the event is created with settings copied from another event.

</div>

<div id="registries" class="section">

<span id="id2"></span>

## Registries

Many signals in pretix are used so that plugins can “register” a class, e.g. a payment provider or a ticket renderer.

However, for some of them (types of <a href="logging.md#logging" class="reference internal"><span class="std std-ref">Log Entries</span></a>) we use a different method to keep track of them: In a <span class="pre">`Registry`</span>, classes are collected at application startup, along with a unique key (in case of LogEntryType, the <span class="pre">`action_type`</span>) as well as which plugin registered them.

To register a class, you can use one of several decorators provided by the Registry object:

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.logentrytypes.</span></span><span class="sig-name descname"><span class="pre">LogEntryTypeRegistry</span></span>  
<span class="sig-name descname"><span class="pre">new</span></span><span class="sig-paren">(</span>*<span class="o"><span class="pre">\*</span></span><span class="n"><span class="pre">args</span></span>*, *<span class="o"><span class="pre">\*\*</span></span><span class="n"><span class="pre">kwargs</span></span>*<span class="sig-paren">)</span>  
Instantiate the decorated class with the given \*args and \*\*kwargs, and register the instance in this registry. May be used multiple times.

<div class="highlight-python notranslate">

<div class="highlight">

    1@animal_sound_registry.new("meow")
    2@animal_sound_registry.new("woof")
    3class AnimalSound:
    4  def __init__(self, sound):
    5    # ...

</div>

</div>

<span class="sig-name descname"><span class="pre">new_from_dict</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">data</span></span>*<span class="sig-paren">)</span>  
Register multiple instance of a LogEntryType class with different action_type and plain text strings, as given by the items of the specified data dictionary.

This method is designed to be used as a decorator as follows:

<div class="highlight-python notranslate">

<div class="highlight">

    1@log_entry_types.new_from_dict({
    2    'pretix.event.item.added': _('The product has been created.'),
    3    'pretix.event.item.changed': _('The product has been changed.'),
    4    # ...
    5})
    6class CoreItemLogEntryType(ItemLogEntryType):
    7    # ...

</div>

</div>

Parameters<span class="colon">:</span>  
**data** – action types and descriptions <span class="pre">`{"some_action_type":`</span>` `<span class="pre">`"Plain`</span>` `<span class="pre">`text`</span>` `<span class="pre">`description",`</span>` `<span class="pre">`...}`</span>

<span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span>*<span class="o"><span class="pre">\*</span></span><span class="n"><span class="pre">objs</span></span>*<span class="sig-paren">)</span>  
Register one or more entries in this registry.

Usable as a regular method or as decorator on a class or function. If used on a class, the class type object itself is registered, not an instance of the class. To register an instance, use the <span class="pre">`new`</span> method.

<div class="highlight-python notranslate">

<div class="highlight">

    @some_registry.register
    def my_new_entry(foo):
      # ...

</div>

</div>

All files in which classes are registered need to be imported in the <span class="pre">`AppConfig.ready`</span> as explained in <a href="https://docs.pretix.eu/dev/development/api/signals" class="reference external">Signals</a> above.

</div>

<div id="views" class="section">

## Views

Your plugin may define custom views. If you put an <span class="pre">`urls`</span> submodule into your plugin module, pretix will automatically import it and include it into the root URL configuration with the namespace <span class="pre">`plugins:<label>:`</span>, where <span class="pre">`<label>`</span> is your Django app label.

<div class="admonition warning">

Warning

If you define custom URLs and views, you are currently on your own with checking that the calling user is logged in, has appropriate permissions, etc. We plan on providing native support for this in a later version.

</div>

To make your plugin views easily discoverable, you can specify links for “Go to” and “Settings” buttons next to your entry on the plugin page. These links should be added to the <span class="pre">`navigation_links`</span> and <span class="pre">`settings_links`</span>, respectively, in the <span class="pre">`PretixPluginMeta`</span> class.

Each array entry consists of a tuple <span class="pre">`(label,`</span>` `<span class="pre">`urlname,`</span>` `<span class="pre">`kwargs)`</span>. For the label, either a string or a tuple of strings can be specified. In the latter case, the provided strings will be merged with a separator indicating they are successive navigation steps the user would need to take to reach the page via the regular menu (e.g. “Payment \> Bank transfer” as below).

<div class="highlight-python notranslate">

<div class="highlight">

    1settings_links = [
    2    ((_("Payment"), _("Bank transfer")), "control:event.settings.payment.provider", {"provider": "banktransfer"}),
    3]
    4navigation_links = [
    5    ((_("Bank transfer"), _("Import bank data")), "plugins:banktransfer:import", {}),
    6    ((_("Bank transfer"), _("Export refunds")), "plugins:banktransfer:refunds.list", {}),
    7]

</div>

</div>

</div>

</div>

</div>

</div>
