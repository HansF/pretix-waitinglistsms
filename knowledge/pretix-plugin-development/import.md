---
title: "Extending the import process"
source: "https://docs.pretix.eu/dev/development/api/import.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/import.html](https://docs.pretix.eu/dev/development/api/import.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="extending-the-import-process" class="section">

<span id="importcol"></span>

# Extending the import process

It’s possible through the backend to import objects into pretix, for example orders from a legacy ticketing system. If your plugin defines additional data structures around those objects, it might be useful to make it possible to import them as well.

<div id="import-process" class="section">

## Import process

Here’s a short description of pretix’ import process to show you where the system will need to interact with your plugin. You can find more detailed descriptions of the attributes and methods further below.

1.  The user uploads a CSV file. The system tries to parse the CSV file and understand its column headers.

2.  A preview of the file is shown to the user and the user is asked to assign the various different input parameters to columns of the file or static values. For example, the user either needs to manually select a product or specify a column that contains a product. For this purpose, a select field is rendered for every possible input column, allowing the user to choose between a default/empty value (defined by your <span class="pre">`default_value`</span>/<span class="pre">`default_label`</span>) attributes, the columns of the uploaded file, or a static value (defined by your <span class="pre">`static_choices`</span> method).

3.  The user submits its assignment and the system uses the <span class="pre">`resolve`</span> method of all columns to get the raw value for all columns.

4.  The system uses the <span class="pre">`clean`</span> method of all columns to verify that all input fields are valid and transformed to the correct data type.

5.  The system prepares internal model objects (<span class="pre">`Order`</span> etc) and uses the <span class="pre">`assign`</span> method of all columns to assign these objects with actual values.

6.  The system saves all of these model objects to the database in a database transaction. Plugins can create additional objects in this stage through their <span class="pre">`save`</span> method.

</div>

<div id="column-registration" class="section">

## Column registration

The import API does not make a lot of usage from signals, however, it does use a signal to get a list of all available import columns. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.modelimport.ImportColumn`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

     1from django.dispatch import receiver
     2
     3from pretix.base.signals import order_import_columns
     4
     5
     6@receiver(order_import_columns, dispatch_uid="custom_columns")
     7def register_column(sender, **kwargs):
     8    return [
     9        EmailColumn(sender),
    10    ]

</div>

</div>

Similar signals exist for other objects:

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">voucher_import_columns</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out if the user performs an import of vouchers from an external source. You can use this to define additional columns that can be read during import. You are expected to return a list of instances of <span class="pre">`ImportColumn`</span> subclasses.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

</div>

<div id="the-column-class-api" class="section">

## The column class API

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.modelimport.</span></span><span class="sig-name descname"><span class="pre">ImportColumn</span></span>  
The central object of each import extension is the subclass of <span class="pre">`ImportColumn`</span>.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
Unique, internal name of the column.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
Human-readable description of the column

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">default_value</span></span>  
Internal default value for the assignment of this column. Defaults to <span class="pre">`empty`</span>. Return <span class="pre">`None`</span> to disable this option.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">default_label</span></span>  
Human-readable description of the default assignment of this column, defaults to “Keep empty”.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">initial</span></span>  
Initial value for the form component

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">static_choices</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span>  
This will be called when rendering the form component and allows you to return a list of values that can be selected by the user statically during import.

Returns<span class="colon">:</span>  
list of 2-tuples of strings

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">resolve</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">settings</span></span>*, *<span class="n"><span class="pre">record</span></span>*<span class="sig-paren">)</span>  
This method will be called to get the raw value for this field, usually by either using a static value or inspecting the CSV file for the assigned header. You usually do not need to implement this on your own, the default should be fine.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">clean</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">value</span></span>*, *<span class="n"><span class="pre">previous_values</span></span>*<span class="sig-paren">)</span>  
Allows you to validate the raw input value for your column. Raise <span class="pre">`ValidationError`</span> if the value is invalid. You do not need to include the column or row name or value in the error message as it will automatically be included.

Parameters<span class="colon">:</span>  
- **value** – Contains the raw value of your column as returned by <span class="pre">`resolve`</span>. This can usually be <span class="pre">`None`</span>, e.g. if the column is empty or does not exist in this row.

- **previous_values** – Dictionary containing the validated values of all columns that have already been validated.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">assign</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">value</span></span>*, *<span class="n"><span class="pre">obj</span></span>*, *<span class="o"><span class="pre">\*\*</span></span><span class="n"><span class="pre">kwargs</span></span>*<span class="sig-paren">)</span>  
This will be called to perform the actual import. You are supposed to set attributes on the <span class="pre">`obj`</span> or other related objects that get passed in based on the input <span class="pre">`value`</span>. This is called *before* the actual database transaction, so the input objects do not yet have a primary key. If you want to create related objects, you need to place them into some sort of internal queue and persist them when <span class="pre">`save`</span> is called.

<span class="sig-prename descclassname"><span class="pre">ImportColumn.</span></span><span class="sig-name descname"><span class="pre">save</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">obj</span></span>*<span class="sig-paren">)</span>  
This will be called to perform the actual import. This is called inside the actual database transaction and the input object <span class="pre">`obj`</span> has already been saved to the database.

</div>

<div id="example" class="section">

## Example

For example, the import column responsible for assigning email addresses looks like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1class EmailColumn(ImportColumn):
     2    identifier = 'email'
     3    verbose_name = _('E-mail address')
     4
     5    def clean(self, value, previous_values):
     6        if value:
     7            EmailValidator()(value)
     8        return value
     9
    10    def assign(self, value, order, position, invoice_address, **kwargs):
    11        order.email = value

</div>

</div>

</div>

</div>

</div>

</div>
