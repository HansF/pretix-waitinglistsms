---
title: "Data sync providers"
source: "https://docs.pretix.eu/dev/development/api/datasync.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/datasync.html](https://docs.pretix.eu/dev/development/api/datasync.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="data-sync-providers" class="section">

# Data sync providers

<div class="admonition warning">

Warning

This feature is considered **experimental**. It might change at any time without prior notice.

</div>

pretix provides connectivity to many external services through plugins. A common requirement is unidirectionally sending (order, customer, ticket, …) data into external systems. The transfer is usually triggered by signals provided by pretix core (e.g. <span class="pre">`order_placed`</span>), but performed asynchronously.

Such plugins should use the <span class="pre">`OutboundSyncProvider`</span> API to utilize the queueing, retry and mapping mechanisms as well as the user interface for configuration and monitoring. Sync providers are registered in the <span class="pre">`pretix.base.datasync.datasync.datasync_providers`</span> <a href="plugins.md#registries" class="reference internal"><span class="std std-ref">registry</span></a>.

An <span class="pre">`OutboundSyncProvider`</span> for subscribing event participants to a mailing list could start like this, for example:

<div class="highlight-python notranslate">

<div class="highlight">

    1from pretix.base.datasync.datasync import (OutboundSyncProvider, datasync_providers)
    2
    3@datasync_providers.register
    4class MyListSyncProvider(OutboundSyncProvider):
    5    identifier = "my_list"
    6    display_name = "My Mailing List Service"
    7    # ...

</div>

</div>

The plugin must register listeners in signals.py for all signals that should to trigger a sync and within it has to call <span class="pre">`MyListSyncProvider.enqueue_order()`</span> to enqueue the order for synchronization:

<div class="highlight-python notranslate">

<div class="highlight">

    @receiver(order_placed, dispatch_uid="mylist_order_placed")
    def on_order_placed(sender, order, **kwargs):
        MyListSyncProvider.enqueue_order(order, "order_placed")

</div>

</div>

<div id="property-mappings" class="section">

## Property mappings

Most of these plugins need to translate data from some pretix objects (e.g. orders) into an external system’s data structures. Sometimes, there is only one reasonable way or the plugin author makes an opinionated decision what information from which objects should be transferred into which data structures in the external system.

Otherwise, you can use a <span class="pre">`PropertyMappingFormSet`</span> to let the user set up a mapping from pretix model fields to external data fields. You could store the mapping information either in the event settings, or in a separate data model. Your implementation of <span class="pre">`OutboundSyncProvider.mappings`</span> needs to provide a list of mappings, which can be e.g. static objects or model instances, as long as they have at least the properties defined in <span class="pre">`pretix.base.datasync.datasync.StaticMapping`</span>.

<div class="highlight-python notranslate">

<div class="highlight">

    1# class MyListSyncProvider, contd.
    2    def mappings(self):
    3        return [
    4            StaticMapping(
    5                id=1, pretix_model='Order', external_object_type='Contact',
    6                pretix_id_field='email', external_id_field='email',
    7                property_mappings=self.event.settings.mylist_order_mapping,
    8            ))
    9        ]

</div>

</div>

Currently, we support orders and order positions as data sources, with the data fields defined in <span class="pre">`pretix.base.datasync.sourcefields.get_data_fields()`</span>.

To perform the actual sync, implement <span class="pre">`sync_object_with_properties()`</span> and optionally <span class="pre">`finalize_sync_order()`</span>. The former is called for each object to be created according to the <span class="pre">`mappings`</span>. For each order that was enqueued using <span class="pre">`enqueue_order()`</span>:

- each Mapping with <span class="pre">`pretix_model`</span>` `<span class="pre">`==`</span>` `<span class="pre">`"Order"`</span> results in one call to <span class="pre">`sync_object_with_properties()`</span>,

- each Mapping with <span class="pre">`pretix_model`</span>` `<span class="pre">`==`</span>` `<span class="pre">`"OrderPosition"`</span> results in one call to <span class="pre">`sync_object_with_properties()`</span> per order position,

- <span class="pre">`finalize_sync_order()`</span> is called one time after all calls to <span class="pre">`sync_object_with_properties()`</span>.

</div>

<div id="implementation-examples" class="section">

## Implementation examples

For example implementations, see the test cases in <span class="pre">`tests.base.test_datasync`</span>.

In <span class="pre">`SimpleOrderSync`</span>, a basic data transfer of order data only is shown. Therein, a <span class="pre">`sync_object_with_properties`</span> method is defined as follows:

<div class="highlight-python notranslate">

<div class="highlight">

     1from pretix.base.datasync.utils import assign_properties
     2
     3# class MyListSyncProvider, contd.
     4def sync_object_with_properties(
     5        self, external_id_field, id_value, properties: list, inputs: dict,
     6        mapping, mapped_objects: dict, **kwargs,
     7):
     8    # First, we query the external service if our object-to-sync already exists there.
     9    # This is necessary to make sure our method is idempotent, i.e. handles already synced
    10    # data gracefully.
    11    pre_existing_object = self.fake_api_client.retrieve_object(
    12        mapping.external_object_type,
    13        external_id_field,
    14        id_value
    15    )
    16
    17    # We use the helper function ``assign_properties`` to update a pre-existing object.
    18    update_values = assign_properties(
    19        new_values=properties,
    20        old_values=pre_existing_object or {},
    21        is_new=pre_existing_object is None,
    22        list_sep=";",
    23    )
    24
    25    # Then we can send our new data to the external service. The specifics of course depends
    26    # on your API, e.g. you may need to use different endpoints for creating or updating an
    27    # object, or pass the identifier separately instead of in the same dictionary as the
    28    # other properties.
    29    result = self.fake_api_client.create_or_update_object(mapping.external_object_type, {
    30        **update_values,
    31        external_id_field: id_value,
    32        "_id": pre_existing_object and pre_existing_object.get("_id"),
    33    })
    34
    35    # Finally, return a dictionary containing at least `object_type`, `external_id_field`,
    36    # `id_value`, `external_link_href`, and `external_link_display_name` keys.
    37    # Further keys may be provided for your internal use. This dictionary is provided
    38    # in following calls in the ``mapped_objects`` dict, to allow creating associations
    39    # to this object.
    40    return {
    41        "object_type": mapping.external_object_type,
    42        "external_id_field": external_id_field,
    43        "id_value": id_value,
    44        "external_link_href": f"https://example.org/external-system/{mapping.external_object_type}/{id_value}/",
    45        "external_link_display_name": f"Contact #{id_value} - Jane Doe",
    46        "my_result": result,
    47    }

</div>

</div>

<div class="admonition note">

Note

The result dictionaries of earlier invocations of <span class="pre">`sync_object_with_properties()`</span> are only provided in subsequent calls of the same sync run, such that a mapping can refer to e.g. the external id of an object created by a preceding mapping. However, the result dictionaries are currently not provided across runs. This will likely change in a future revision of this API, to allow easier integration of external systems that do not allow retrieving/updating data by a pretix-provided key.

</div>

<span class="pre">`mapped_objects`</span> is a dictionary of lists of dictionaries. The keys to the dictionary are the mapping identifiers (<span class="pre">`mapping.id`</span>), the lists contain the result dictionaries returned by <span class="pre">`sync_object_with_properties()`</span>.

In <span class="pre">`OrderAndTicketAssociationSync`</span>, an example is given where orders, order positions, and the association between them are transferred.

</div>

<div id="the-outboundsyncprovider-base-class" class="section">

## The OutboundSyncProvider base class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.datasync.datasync.</span></span><span class="sig-name descname"><span class="pre">OutboundSyncProvider</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">event</span></span>*<span class="sig-paren">)</span>  
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span>  
Called after all orders of an event have been synced. Can be used for clean-up tasks (e.g. closing a session).

<span class="property"><span class="k"><span class="pre">classmethod</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">enqueue_order</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span>*, *<span class="n"><span class="pre">triggered_by</span></span>*, *<span class="n"><span class="pre">not_before</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">immediate</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span>*<span class="sig-paren">)</span>  
Adds an order to the sync queue. May only be called on derived classes which define an <span class="pre">`identifier`</span> attribute.

Should be called in the appropriate signal receivers, e.g.:

<div class="highlight-python notranslate">

<div class="highlight">

    @receiver(order_placed, dispatch_uid="mysync_order_placed")
    def on_order_placed(sender, order, **kwargs):
        MySyncProvider.enqueue_order(order, "order_placed")

</div>

</div>

Parameters<span class="colon">:</span>  
- **order** – the Order that should be synced

- **triggered_by** – the reason why the order should be synced, e.g. name of the signal (currently only used internally for logging)

- **immediate** – whether a new sync task should run immediately for this order, instead of waiting for the next periodic_task interval

Returns<span class="colon">:</span>  
Return a tuple (queue_item, created), where created is a boolean specifying whether a new queue item was created.

<span class="sig-name descname"><span class="pre">filter_mapped_objects</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mapped_objects</span></span>*, *<span class="n"><span class="pre">inputs</span></span>*<span class="sig-paren">)</span>  
For order positions, only

<span class="sig-name descname"><span class="pre">finalize_sync_order</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span>*<span class="sig-paren">)</span>  
Called after <span class="pre">`sync_object`</span> has been called successfully for all objects of a specific order. Can be used for saving bulk information per order.

<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">mappings</span></span>  
Implementations must override this property to provide the data mappings as a list of objects.

They can return instances of the <span class="pre">`StaticMapping`</span> namedtuple defined above, or create their own class (e.g. a Django model).

Returns<span class="colon">:</span>  
The returned objects must have at least the following properties:

- id: Unique identifier for this mapping. If the mappings are Django models, the database primary key should be used. This may be referenced in other mappings, to establish relations between objects.

- pretix_model: Which pretix model to use as data source in this mapping. Possible values are the keys of <span class="pre">`sourcefields.AVAILABLE_MODELS`</span>

- external_object_type: Destination object type in the target system. opaque string of maximum 128 characters.

- pretix_id_field: Which pretix data field should be used to identify the mapped object. Any <span class="pre">`DataFieldInfo.key`</span> returned by <span class="pre">`sourcefields.get_data_fields()`</span> for the combination of <span class="pre">`Event`</span> and <span class="pre">`pretix_model`</span>.

- external_id_field: Destination identifier field in the target system.

- property_mappings: Mapping configuration as generated by <span class="pre">`PropertyMappingFormSet.to_property_mappings_list()`</span>.

<span class="sig-name descname"><span class="pre">next_retry_date</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">sq</span></span>*<span class="sig-paren">)</span>  
Optionally override to configure a different retry backoff behavior

<span class="sig-name descname"><span class="pre">should_sync_order</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span>*<span class="sig-paren">)</span>  
Optionally override this method to exclude certain orders from sync by returning <span class="pre">`False`</span>

<span class="sig-name descname"><span class="pre">sync_object_with_properties</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">external_id_field</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">id_value</span></span>*, *<span class="n"><span class="pre">properties</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span>*, *<span class="n"><span class="pre">inputs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span>*, *<span class="n"><span class="pre">mapping</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ObjectMapping</span></span>*, *<span class="n"><span class="pre">mapped_objects</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span>*, *<span class="o"><span class="pre">\*\*</span></span><span class="n"><span class="pre">kwargs</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span></span>  
This method is called for each object that needs to be created/updated in the external system – which these are is determined by the implementation of the mapping property.

Parameters<span class="colon">:</span>  
- **external_id_field** – Identifier field in the external system as provided in <span class="pre">`mapping.external_identifier`</span>

- **id_value** – Identifier contents as retrieved from the property specified by <span class="pre">`mapping.pretix_identifier`</span> of the model specified by <span class="pre">`mapping.pretix_model`</span>

- **properties** – All properties defined in <span class="pre">`mapping.property_mappings`</span>, as list of three-tuples <span class="pre">`(external_field,`</span>` `<span class="pre">`value,`</span>` `<span class="pre">`overwrite)`</span>

- **inputs** – All pretix model instances from which data can be retrieved for this mapping. Dictionary mapping from sourcefields.ORDER_POSITION, .ORDER, .EVENT, .EVENT_OR_SUBEVENT to the relevant Django model. Most providers don’t need to use this parameter directly, as properties and id_value already contain the values as evaluated from the available inputs.

- **mapping** – The mapping object as returned by <span class="pre">`self.mappings`</span>

- **mapped_objects** – Information about objects that were synced in the same sync run, by mapping definitions *before* the current one in order of <span class="pre">`self.mappings`</span>. Type is a dictionary <span class="pre">`{mapping.id:`</span>` `<span class="pre">`[list`</span>` `<span class="pre">`of`</span>` `<span class="pre">`OrderSyncResult`</span>` `<span class="pre">`objects]}`</span> Useful to create associations between objects in the target system.

Example code to create return value:

<div class="highlight-python notranslate">

<div class="highlight">

     1return {
     2   # optional:
     3   "action": "nothing_to_do",  # to inform that no action was taken, because the data was already up-to-date.
     4                               # other values for action (e.g. create, update) currently have no special
     5                               # meaning, but are visible for debugging purposes to admins.
     6
     7   # optional:
     8   "external_link_href": "https://external-system.example.com/backend/link/to/contact/123/",
     9   "external_link_display_name": "Contact #123 - Jane Doe",
    10   "...optionally further values you need in mapped_objects for association": 123456789,
    11}

</div>

</div>

The return value needs to be a JSON serializable dict, or None.

Return None only in case you decide this object should not be synced at all in this mapping. Do not return None in case the object is already up-to-date in the target system (return “action”: “nothing_to_do” instead).

This method needs to be idempotent, i.e. calling it multiple times with the same input values should create only a single object in the target system.

Subsequent calls with the same mapping and id_value should update the existing object, instead of creating a new one. In a SQL database, you might use an INSERT OR UPDATE or UPSERT statement; many REST APIs provide an equivalent API call.

<span class="sig-name descname"><span class="pre">sync_queued_orders</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">queued_orders</span></span>*<span class="sig-paren">)</span>  
This method should catch all Exceptions and handle them appropriately. It should never throw an Exception, as that may block the entire queue.

</div>

<div id="property-mapping-format" class="section">

## Property mapping format

To allow the user to configure property mappings, you can use the PropertyMappingFormSet, which will generate the required <span class="pre">`property_mappings`</span> value automatically. If you need to specify the property mappings programmatically, you can refer to the description below on their format.

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.control.forms.mapping.</span></span><span class="sig-name descname"><span class="pre">PropertyMappingFormSet</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">pretix_fields</span></span>*, *<span class="n"><span class="pre">external_fields</span></span>*, *<span class="n"><span class="pre">available_modes</span></span>*, *<span class="n"><span class="pre">prefix</span></span>*, *<span class="o"><span class="pre">\*</span></span><span class="n"><span class="pre">args</span></span>*, *<span class="o"><span class="pre">\*\*</span></span><span class="n"><span class="pre">kwargs</span></span>*<span class="sig-paren">)</span>  

A simple JSON-serialized <span class="pre">`property_mappings`</span> list for mapping some order information can look like this:

<div class="highlight-json notranslate">

<div class="highlight">

     1[
     2  {
     3      "pretix_field": "email",
     4      "external_field": "orderemail",
     5      "value_map": "",
     6      "overwrite": "overwrite",
     7  },
     8  {
     9      "pretix_field": "order_status",
    10      "external_field": "status",
    11      "value_map": "{\"n\": \"pending\", \"p\": \"paid\", \"e\": \"expired\", \"c\": \"canceled\", \"r\": \"refunded\"}",
    12      "overwrite": "overwrite",
    13  },
    14  {
    15      "pretix_field": "order_total",
    16      "external_field": "total",
    17      "value_map": "",
    18      "overwrite": "overwrite",
    19  }
    20]

</div>

</div>

</div>

<div id="translating-mappings-on-event-copy" class="section">

## Translating mappings on Event copy

Property mappings can contain references to event-specific primary keys. Therefore, plugins must register to the event_copy_data signal and call translate_property_mappings on all property mappings they store.

<span class="sig-prename descclassname"><span class="pre">pretix.base.datasync.utils.</span></span><span class="sig-name descname"><span class="pre">translate_property_mappings</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">property_mappings</span></span>*, *<span class="n"><span class="pre">checkin_list_map</span></span>*<span class="sig-paren">)</span>  
To properly handle copied events, users of data fields as provided by get_data_fields need to register to the event_copy_data signal and translate all stored references to those fields using this method.

For example, if you store your mappings in a custom Django model with a ForeignKey to Event:

<div class="highlight-python notranslate">

<div class="highlight">

     1@receiver(signal=event_copy_data, dispatch_uid="my_sync_event_copy_data")
     2def event_copy_data_receiver(sender, other, checkin_list_map, **kwargs):
     3    object_mappings = other.my_object_mappings.all()
     4    object_mapping_map = {}
     5    for om in object_mappings:
     6        om = copy.copy(om)
     7        object_mapping_map[om.pk] = om
     8        om.pk = None
     9        om.event = sender
    10        om.property_mappings = translate_property_mappings(om.property_mappings, checkin_list_map)
    11        om.save()

</div>

</div>

</div>

</div>

</div>

</div>
