---
title: "Writing a data shredder"
source: "https://docs.pretix.eu/dev/development/api/shredder.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/shredder.html](https://docs.pretix.eu/dev/development/api/shredder.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-a-data-shredder" class="section">

<span id="shredder"></span>

# Writing a data shredder

If your plugin adds the ability to store personal data within pretix, you should also implement a “data shredder” to anonymize or pseudonymize the data later.

<div id="shredder-registration" class="section">

## Shredder registration

The data shredder API does not make a lot of usage from signals, however, it does use a signal to get a list of all available data shredders. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.shredder.BaseDataShredder`</span> that we’ll provide in this plugin:

<div class="highlight-python notranslate">

<div class="highlight">

     1from django.dispatch import receiver
     2
     3from pretix.base.signals import register_data_shredders
     4
     5
     6@receiver(register_data_shredders, dispatch_uid="custom_data_shredders")
     7def register_shredder(sender, **kwargs):
     8    return [
     9        PluginDataShredder,
    10    ]

</div>

</div>

</div>

<div id="the-shredder-class" class="section">

## The shredder class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.shredder.</span></span><span class="sig-name descname"><span class="pre">BaseDataShredder</span></span>  
The central object of each data shredder is the subclass of <span class="pre">`BaseDataShredder`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseDataShredder.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for.

<span class="sig-prename descclassname"><span class="pre">BaseDataShredder.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this shredder. This should only contain lowercase letters and in most cases will be the same as your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseDataShredder.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for what this shredder removes. This should be short but self-explanatory. Good examples include ‘E-Mail addresses’ or ‘Invoices’.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseDataShredder.</span></span><span class="sig-name descname"><span class="pre">description</span></span>  
A more detailed description of what this shredder does. Can contain HTML.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseDataShredder.</span></span><span class="sig-name descname"><span class="pre">generate_files</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">List</span><span class="p"><span class="pre">\[</span></span><span class="pre">Tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>  
This method is called to export the data that is about to be shred and return a list of tuples consisting of a filename, a file type and file content.

You can also implement this as a generator and <span class="pre">`yield`</span> those tuples instead of returning a list of them.

<span class="sig-prename descclassname"><span class="pre">BaseDataShredder.</span></span><span class="sig-name descname"><span class="pre">shred_data</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">progress_callback</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span>  
This method is called to actually remove the data from the system. You should remove any database objects here.

You can call <span class="pre">`progress_callback`</span> with an integer value between 0 and 100 to communicate back your progress.

You should never delete <span class="pre">`LogEntry`</span> objects, but you might modify them to remove personal data. In this case, set the <span class="pre">`LogEntry.shredded`</span> attribute to <span class="pre">`True`</span> to show that this is no longer original log data.

</div>

<div id="example" class="section">

## Example

For example, the core data shredder responsible for removing invoice address information including their history looks like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1class InvoiceAddressShredder(BaseDataShredder):
     2    verbose_name = _('Invoice addresses')
     3    identifier = 'invoice_addresses'
     4    description = _('This will remove all invoice addresses from orders, '
     5                    'as well as logged changes to them.')
     6
     7    def generate_files(self) -> List[Tuple[str, str, str]]:
     8        yield 'invoice-addresses.json', 'application/json', json.dumps({
     9            ia.order.code: InvoiceAddressSerializer(ia).data
    10            for ia in InvoiceAddress.objects.filter(order__event=self.event)
    11        }, indent=4)
    12
    13    @transaction.atomic
    14    def shred_data(self):
    15        InvoiceAddress.objects.filter(order__event=self.event).delete()
    16
    17        for le in self.event.logentry_set.filter(action_type="pretix.event.order.modified"):
    18            d = le.parsed_data
    19            if 'invoice_data' in d and not isinstance(d['invoice_data'], bool):
    20                for field in d['invoice_data']:
    21                    if d['invoice_data'][field]:
    22                        d['invoice_data'][field] = '█'
    23                le.data = json.dumps(d)
    24                le.shredded = True
    25                le.save(update_fields=['data', 'shredded'])

</div>

</div>

</div>

</div>

</div>

</div>
