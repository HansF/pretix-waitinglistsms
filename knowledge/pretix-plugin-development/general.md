---
title: "General APIs"
source: "https://docs.pretix.eu/dev/development/api/general.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/general.html](https://docs.pretix.eu/dev/development/api/general.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="general-apis" class="section">

# General APIs

This page lists some general signals and hooks which do not belong to a specific type of plugin but might come in handy for various plugins.

<div id="module-pretix.base.signals" class="section">

<span id="core"></span>

## Core

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">device_info_updated</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`old_device`</span>, <span class="pre">`new_device`</span>

This signal is sent out each time the information for a Device is modified. Both the original and updated versions of the Device are included to allow receivers to see what has been updated.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">email_filter</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`message`</span>, <span class="pre">`order`</span>, <span class="pre">`user`</span>, <span class="pre">`outgoing_mail`</span>

This signal allows you to implement a middleware-style filter on all outgoing emails. You are expected to return a (possibly modified) copy of the message object passed to you.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. The <span class="pre">`message`</span> argument will contain an <span class="pre">`EmailMultiAlternatives`</span> object. The <span class="pre">`outgoing_mail`</span> argument will contain the <span class="pre">`OutgoingMail`</span> model instance. Note that the <span class="pre">`message`</span> object might have newer information if a previous plugin already modified the email. If the email is associated with a specific order, the <span class="pre">`order`</span> argument will be passed as well, otherwise it will be <span class="pre">`None`</span>. If the email is associated with a specific user, e.g. a notification email, the <span class="pre">`user`</span> argument will be passed as well, otherwise it will be <span class="pre">`None`</span>.

You can raise <span class="pre">`WithholdMailException`</span> to prevent the email from being sent, e.g. when implementing rate limiting.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">event_copy_data</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: “other”, <span class="pre">`tax_map`</span>, <span class="pre">`category_map`</span>, <span class="pre">`item_map`</span>, <span class="pre">`question_map`</span>, <span class="pre">`variation_map`</span>, <span class="pre">`checkin_list_map`</span>, <span class="pre">`quota_map`</span>

This signal is sent out when a new event is created as a clone of an existing event, i.e. the settings from the older event are copied to the newer one. You can listen to this signal to copy data or configuration stored within your plugin’s models as well.

You don’t need to copy data inside the general settings storage which is cloned automatically, but you might need to modify that data.

The <span class="pre">`sender`</span> keyword argument will contain the event of the **new** event. The <span class="pre">`other`</span> keyword argument will contain the event to **copy from**. The keyword arguments <span class="pre">`tax_map`</span>, <span class="pre">`category_map`</span>, <span class="pre">`item_map`</span>, <span class="pre">`question_map`</span>, <span class="pre">`quota_map`</span>, <span class="pre">`variation_map`</span> and <span class="pre">`checkin_list_map`</span> contain mappings from object IDs in the original event to objects in the new event of the respective types.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">event_live_issues</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to determine whether an event can be taken live. If you want to prevent the event from going live, return a string that will be displayed to the user as the error message. If you don’t, your receiver should return <span class="pre">`None`</span>.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">gift_card_transaction_display</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`transaction`</span>, <span class="pre">`customer_facing`</span>

To display an instance of the <span class="pre">`GiftCardTransaction`</span> model to a human user, <span class="pre">`pretix.base.signals.gift_card_transaction_display`</span> will be sent out with a <span class="pre">`transaction`</span> argument. The <span class="pre">`customer_facing`</span> argument specifies whether the HTML will be shown to an end-user or if it is being used in the backend.

The first received response that is not <span class="pre">`None`</span> will be used to display the log entry to the user. The receivers are expected to return a string (that might be marked with <span class="pre">`mark_safe`</span> from Django if it contains HTML).

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">global_email_filter</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`message`</span>, <span class="pre">`order`</span>, <span class="pre">`user`</span>, <span class="pre">`customer`</span>, <span class="pre">`organizer`</span>, <span class="pre">`outgoing_mail`</span>

This signal allows you to implement a middleware-style filter on all outgoing emails. You are expected to return a (possibly modified) copy of the message object passed to you.

This signal is called on all events and even if there is no known event. <span class="pre">`sender`</span> is an event or None. The <span class="pre">`message`</span> argument will contain an <span class="pre">`EmailMultiAlternatives`</span> object. The <span class="pre">`outgoing_mail`</span> argument will contain the <span class="pre">`OutgoingMail`</span> model instance. Note that the <span class="pre">`message`</span> object might have newer information if a previous plugin already modified the email. If the email is associated with a specific order, the <span class="pre">`order`</span> argument will be passed as well, otherwise it will be <span class="pre">`None`</span>. If the email is associated with a specific user, e.g. a notification email, the <span class="pre">`user`</span> argument will be passed as well, otherwise it will be <span class="pre">`None`</span>.

You can raise <span class="pre">`WithholdMailException`</span> to prevent the email from being sent, e.g. when implementing rate limiting.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">item_copy_data</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`source`</span>, <span class="pre">`target`</span>

This signal is sent out when a new product is created as a clone of an existing product, i.e. the settings from the older product are copied to the newer one. You can listen to this signal to copy data or configuration stored within your plugin’s models as well.

The <span class="pre">`sender`</span> keyword argument will contain the event. The <span class="pre">`target`</span> will contain the item to copy to, the <span class="pre">`source`</span> keyword argument will contain the product to **copy from**.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">notification</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`logentry_id`</span>, <span class="pre">`notification_type`</span>

This signal is sent out when a notification is sent.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">periodic_task</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
This is a regular django signal (no pretix event signal) that we send out every time the periodic task cronjob runs. This interval is not sharply defined, it can be everything between a minute and a day. The actions you perform should be idempotent, i.e. it should not make a difference if this is sent out more often than expected.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">quota_availability</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`quota`</span>, <span class="pre">`result`</span>, <span class="pre">`count_waitinglist`</span>

This signal allows you to modify the availability of a quota. You are passed the <span class="pre">`quota`</span> and an <span class="pre">`availability`</span> result calculated by pretix code or other plugins. <span class="pre">`availability`</span> is a tuple with the first entry being one of the <span class="pre">`Quota.AVAILABILITY_*`</span> constants and the second entry being the number of available tickets (or <span class="pre">`None`</span> for unlimited). You are expected to return a value of the same type. The parameter <span class="pre">`count_waitinglists`</span> specifies whether waiting lists should be taken into account.

**Warning: Use this signal with great caution, it allows you to screw up the performance of the system really bad.** Also, keep in mind that your response is subject to caching and out-of-date quotas might be used for display (not for actual order processing).

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_event_permission_groups</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known permissions. Receivers should return an instance of pretix.base.permissions.PermissionGroup or a list of such instances.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_global_settings</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
All plugins that are installed may send fields for the global settings form, as an OrderedDict of (setting name, form field).

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_mail_placeholders</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
**DEPRECATED**: This signal has a new name, please use <span class="pre">`register_text_placeholders`</span> instead.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_notification_types</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known notification types. Receivers should return an instance of a subclass of pretix.base.notifications.NotificationType or a list of such instances.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event, however for this signal, the <span class="pre">`sender`</span> **may also be None** to allow creating the general notification settings!

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_organizer_permission_groups</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known permissions. Receivers should return an instance of pretix.base.permissions.PermissionGroup or a list of such instances.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_sales_channel_types</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known sales channels types. Receivers should return an instance of a subclass of <span class="pre">`pretix.base.channels.SalesChannelType`</span> or a list of such instances.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_text_placeholders</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known text placeholders. Receivers should return an instance of a subclass of pretix.base.services.placeholders.BaseTextPlaceholder or a list of these.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">register_ticket_secret_generators</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known ticket secret generators. Receivers should return a subclass of <span class="pre">`pretix.base.secrets.BaseTicketSecretGenerator`</span> or a list of these

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<div id="order-events" class="section">

### Order events

There are multiple signals that will be sent out in the ordering cycle:

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">allow_ticket_download</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out to check if tickets for an order can be downloaded. If any receiver returns false, a download will not be offered. If a receiver returns a list of OrderPositions, only those will be downloadable.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">build_invoice_data</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`invoice`</span>

This signal is sent out every time an invoice is built, after the invoice model was created and filled and before the PDF generation task is started. You can use this to make changes to the invoice, but we recommend to mostly use it to add content to <span class="pre">`Invoice.plugin_data`</span>. You are responsible for saving any changes to the database.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">invoice_line_text</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`position`</span>

This signal is sent out when an invoice is built for an order. You can return additional text that should be shown on the invoice for the given <span class="pre">`position`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_approved</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order is being approved. The order object is given as the first argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_canceled</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order is canceled. The order object is given as the first argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_changed</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order’s content is changed. The order object is given as the first argument. In contrast to <span class="pre">`modified`</span>, this signal is sent out if the order or any of its positions changes in a material way, such as changed products, prices, or tax rates, <span class="pre">`order_changed`</span> is used instead. If “only” user input is changed, such as attendee names, invoice addresses or question answers, <span class="pre">`order_modified`</span> is used instead.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_denied</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order is being denied. The order object is given as the first argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_expired</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order is marked as expired. The order object is given as the first argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_expiry_changed</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order expiry date is changed as an explicit operation (i.e. not if this is the result of an approval or order change). The order object is given as the first argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_fee_calculation</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`positions`</span>, <span class="pre">`invoice_address`</span>, <span class="pre">`meta_info`</span>, <span class="pre">`total`</span>, <span class="pre">`gift_cards`</span>, <span class="pre">`payment_requests`</span>

This signals allows you to add fees to an order while it is being created. You are expected to return a list of <span class="pre">`OrderFee`</span> objects that are not yet saved to the database (because there is no order yet).

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`positions`</span> argument will contain the cart positions and <span class="pre">`invoice_address`</span> the invoice address (useful for tax calculation). The argument <span class="pre">`meta_info`</span> contains the order’s meta dictionary. The <span class="pre">`total`</span> keyword argument will contain the total cart sum without any fees. You should not rely on this <span class="pre">`total`</span> value for fee calculations as other fees might interfere. The <span class="pre">`gift_cards`</span> argument lists the gift cards in use.

**DEPRECTATION:** Stop listening to the <span class="pre">`gift_cards`</span> attribute, it will be removed in the future.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_fee_type_name</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`fee`</span>

This signals allows you to return a human-readable description for a fee type based on the <span class="pre">`fee_type`</span> and <span class="pre">`internal_type`</span> attributes of the <span class="pre">`OrderFee`</span> model that you get as keyword arguments. You are expected to return a string or None, if you don’t know about this fee.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_gracefully_delete</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time a test-mode order is being deleted. The order object is given as the first argument.

Any plugin receiving this signals is supposed to perform any cleanup necessary at this point, so that the underlying order has no more external constraints that would inhibit the deletion of the order.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_modified</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order’s information is modified. The order object is given as the first argument. In contrast to <span class="pre">`order_changed`</span>, this signal is sent out if information of an order or any of it’s position is changed that concerns user input, such as attendee names, invoice addresses or question answers. If the order changes in a material way, such as changed products, prices, or tax rates, <span class="pre">`order_changed`</span> is used instead.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_paid</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time an order is paid. The order object is given as the first argument. This signal is *not* sent out if an order is marked as paid because an already-paid order has been split.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_placed</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`bulk`</span>

This signal is sent out every time an order is placed. The order object is given as the first argument. The <span class="pre">`bulk`</span> argument specifies whether the order was placed as part of a bulk action, e.g. an import from a file. This signal is *not* sent out if an order is created through splitting an existing order, so you can not expect to see all orders by listening to this signal.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_reactivated</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out every time a canceled order is reactivated. The order object is given as the first argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_split</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`original`</span>, <span class="pre">`split_order`</span>

This signal is sent out when an order is split into two orders and allows you to copy related models to the new order. You will be passed the old order as <span class="pre">`original`</span> and the new order as <span class="pre">`split_order`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">order_valid_if_pending</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`payments`</span>, <span class="pre">`positions`</span>, <span class="pre">`email`</span>, <span class="pre">`locale`</span>, <span class="pre">`invoice_address`</span>, <span class="pre">`meta_info`</span>, <span class="pre">`customer`</span>

This signal is sent out when the user tries to confirm the order, before we actually create the order. It allows you to set the <span class="pre">`valid_if_pending`</span> of the order even before it is created. Whenever any plugin returns <span class="pre">`True`</span>, the order will be valid if pending.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">validate_cart</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`positions`</span>

This signal is sent out before the user starts checkout. It includes an iterable with the current CartPosition objects. The response of receivers will be ignored, but you can raise a CartError with an appropriate exception message.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">validate_cart_addons</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`addons`</span>, <span class="pre">`base_position`</span>, <span class="pre">`iao`</span>

This signal is sent when a user tries to select a combination of addons. In contrast to <span class="pre">`validate_cart`</span>, this is executed before the cart is actually modified. You are passed an argument <span class="pre">`addons`</span> containing a dict of <span class="pre">`(item,`</span>` `<span class="pre">`variation`</span>` `<span class="pre">`or`</span>` `<span class="pre">`None)`</span>` `<span class="pre">`→`</span>` `<span class="pre">`count`</span> tuples as well as the <span class="pre">`ItemAddOn`</span> object as the argument <span class="pre">`iao`</span> and the base cart position as <span class="pre">`base_position`</span>. The response of receivers will be ignored, but you can raise a CartError with an appropriate exception message.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">validate_order</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`payments`</span>, <span class="pre">`positions`</span>, <span class="pre">`email`</span>, <span class="pre">`locale`</span>, <span class="pre">`invoice_address`</span>, <span class="pre">`meta_info`</span>, <span class="pre">`customer`</span>

This signal is sent out when the user tries to confirm the order, before we actually create the order. It allows you to inspect the cart positions. Your return value will be ignored, but you can raise an OrderError with an appropriate exception message if you like to block the order. We strongly discourage making changes to the order here.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

**DEPRECTATION:** Stop listening to the <span class="pre">`payment_provider`</span> attribute, it will be removed in the future, as the <span class="pre">`payments`</span> attribute gives more information.

</div>

<div id="check-ins" class="section">

### Check-ins

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">checkin_annulled</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`checkin`</span>

This signal is sent out every time a check-in is annulled (i.e. changed to unsuccessful after it already was successful).

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">checkin_created</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`checkin`</span>

This signal is sent out every time a check-in is created (i.e. an order position is marked as checked in). It is not send if the position was already checked in and is force-checked-in a second time. The check-in object is given as the first argument.

For backwards compatibility reasons, this signal is only sent when a **successful** scan is saved.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

</div>

</div>

<div id="module-pretix.presale.signals" class="section">

<span id="frontend"></span>

## Frontend

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">checkout_all_optional</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’

If any receiver of this signal returns <span class="pre">`True`</span>, all input fields during checkout (contact data, invoice address, confirmations) will be optional, except for questions. Use with care!

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`request`</span> argument will contain the request object.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">checkout_confirm_messages</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to retrieve short messages that need to be acknowledged by the user before the order can be completed. This is typically used for something like “accept the terms and conditions”. Receivers are expected to return a dictionary where the keys are globally unique identifiers for the message and the values can be a SafeString containing arbitrary HTML, or a string that will be HTML-escaped.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">checkout_confirm_page_content</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signals allows you to add HTML content to the confirmation page that is presented at the end of the checkout process, just before the order is being created.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`request`</span> argument will contain the request object.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">checkout_flow_steps</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to retrieve pages for the checkout flow. Receivers are expected to return a subclass of <span class="pre">`pretix.presale.checkoutflow.BaseCheckoutFlowStep`</span>.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">contact_form_fields</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signals allows you to add form fields to the contact form that is presented during checkout and by default only asks for the email address. You are supposed to return a dictionary of form fields with globally unique keys. The validated form results will be saved into the <span class="pre">`contact_form_data`</span> entry of the order’s meta_info dictionary.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`request`</span> argument will contain the request object.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">contact_form_fields_overrides</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`order`</span>

This signal allows you to override fields of the contact form that is presented during checkout and by default only asks for the email address. It is also being used for the invoice address form. You are supposed to return a dictionary of dictionaries with globally unique keys. The value-dictionary should contain one or more of the following keys: <span class="pre">`initial`</span>, <span class="pre">`disabled`</span>, <span class="pre">`validators`</span>. The key of the dictionary should be the name of the form field.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`request`</span> argument will contain the request object. The <span class="pre">`order`</span> argument is <span class="pre">`None`</span> during the checkout process and contains an order if the customer is trying to change an existing order.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">fee_calculation_for_cart</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`invoice_address`</span>, <span class="pre">`total`</span>, <span class="pre">`positions`</span>, <span class="pre">`payment_requetss`</span>

This signals allows you to add fees to a cart. You are expected to return a list of <span class="pre">`OrderFee`</span> objects that are not yet saved to the database (because there is no order yet).

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`request`</span> argument will contain the request object and <span class="pre">`invoice_address`</span> the invoice address (useful for tax calculation). The <span class="pre">`total`</span> keyword argument will contain the total cart sum without any fees. You should not rely on this <span class="pre">`total`</span> value for fee calculations as other fees might interfere. The <span class="pre">`positions`</span> argument will contain a list or queryset of <span class="pre">`CartPosition`</span> objects.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">filter_subevents</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`subevents`</span>, <span class="pre">`sales_channel`</span>

This signal allows you to filter which subevents are publicly available. Receivers are passed a list of subevents that are about to be shown to the user and are expected to return a list of the same format, with all subevents removed that should not be available for sale.

<span class="pre">`sales_channels`</span> is a <span class="pre">`str`</span> with the sales channel identifier.

This is not an event-plugin signal as this will also be called on other levels when showing a list of subevents across events. Expect that the subevents in the input are mixed from different events **or even different organizers**. However, receivers will only receive subevents of events that the plugin is active for and can only filter out these. It is recommended that receivers return a subset of the same subevent instances that are passed in, not new instances, to ensure prefetch_related calls on the caller side are not pointless.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">footer_link</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

The signal <span class="pre">`pretix.presale.signals.footer_link`</span> allows you to add links to the footer of an event page. You are expected to return a dictionary containing the keys <span class="pre">`label`</span>, <span class="pre">`url`</span> and optionally <span class="pre">`cssclass`</span>.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">front_page_bottom</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`subevent`</span>

This signal is sent out to display additional information on the frontpage below the list of products.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. The receivers are expected to return HTML.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">front_page_bottom_widget</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`subevent`</span>

This signal is sent out to display additional information on the frontpage below the list of products if the front page is shown in the widget.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. The receivers are expected to return HTML.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">front_page_top</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`subevent`</span>

This signal is sent out to display additional information on the frontpage above the list of products and but below a custom frontpage text.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. The receivers are expected to return HTML.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">global_footer_link</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

The signal <span class="pre">`pretix.presale.signals.global_footer_link`</span> allows you to add links to the footer of any page. You are expected to return a dictionary containing the keys <span class="pre">`label`</span> and <span class="pre">`url`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">global_html_footer</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code before the end of the HTML <span class="pre">`<body>`</span> tag of every page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

This signal is called regardless of whether your plugin is active for all pages of the system.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">global_html_head</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code inside the HTML <span class="pre">`<head>`</span> tag of every page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

This signal is called regardless of whether your plugin is active for all pages of the system.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">global_html_page_header</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code right in the beginning of the HTML <span class="pre">`<body>`</span> tag of every page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

This signal is called regardless of whether your plugin is active for all pages of the system.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">html_footer</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code before the end of the HTML <span class="pre">`<body>`</span> tag of every page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

**Note:** If PCI DSS compliance is important to you and you keep an inventory according to rule 6.4.3 of PCI DSS, all plugins that are not required to load on a payment page should not return additional JavaScripts if <span class="pre">`getattr(request,`</span>` `<span class="pre">`'pci_dss_payment_page',`</span>` `<span class="pre">`False)`</span> is <span class="pre">`True`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">html_head</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code inside the HTML <span class="pre">`<head>`</span> tag of every page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

**Note:** If PCI DSS compliance is important to you and you keep an inventory according to rule 6.4.3 of PCI DSS, all plugins that are not required to load on a payment page should not return additional JavaScripts if <span class="pre">`getattr(request,`</span>` `<span class="pre">`'pci_dss_payment_page',`</span>` `<span class="pre">`False)`</span> is <span class="pre">`True`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">html_page_header</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code right in the beginning of the HTML <span class="pre">`<body>`</span> tag of every page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">item_description</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`item`</span>, <span class="pre">`variation`</span>, <span class="pre">`subevent`</span>

This signal is sent out when the description of an item or variation is rendered and allows you to append additional text to the description. You are passed the <span class="pre">`item`</span>, <span class="pre">`variation`</span> and <span class="pre">`subevent`</span>. You are expected to return HTML.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">position_info</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`position`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional information on the position detail page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">position_info_top</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`position`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional information on top of the position detail page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">question_form_fields</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`position`</span>

This signals allows you to add form fields to the questions form that is presented during checkout and by default asks for the questions configured in the backend. You are supposed to return a dictionary of form fields with globally unique keys. The validated form results will be saved into the <span class="pre">`question_form_data`</span> entry of the position’s meta_info dictionary.

The <span class="pre">`position`</span> keyword argument will contain either a <span class="pre">`CartPosition`</span> object or an <span class="pre">`OrderPosition`</span> object, depending on whether the form is called as part of the order checkout or for changing an order later.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">question_form_fields_overrides</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`position`</span>, <span class="pre">`request`</span>

This signal allows you to override fields of the questions form that is presented during checkout and by default only asks for the questions configured in the backend. You are supposed to return a dictionary of dictionaries with globally unique keys. The value-dictionary should contain one or more of the following keys: <span class="pre">`initial`</span>, <span class="pre">`disabled`</span>, <span class="pre">`validators`</span>. The key of the dictionary should be the form field name for system fields (e.g. <span class="pre">`company`</span>), or the question’s <span class="pre">`identifier`</span> for user-defined questions.

The <span class="pre">`position`</span> keyword argument will contain a <span class="pre">`CartPosition`</span> or <span class="pre">`OrderPosition`</span> object.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A <span class="pre">`request`</span> argument will contain the request object.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">render_seating_plan</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`subevent`</span>, <span class="pre">`voucher`</span>

This signal is sent out to render a seating plan, if one is configured for the specific event. You will be passed the <span class="pre">`request`</span> as a keyword argument. If applicable, a <span class="pre">`subevent`</span> or <span class="pre">`voucher`</span> argument might be given.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. The receivers are expected to return HTML.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">seatingframe_html_head</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

**Temporary workaround, might be removed again later.** This signal allows you to put code inside the HTML <span class="pre">`<head>`</span> tag of the seatingframe page in the frontend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">order_api_meta_from_request</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal is sent before an order is created through the pretixpresale frontend. It allows you to return a dictionary that will be merged in the api_meta attribute of the order. You will receive the request triggering the order creation as the <span class="pre">`request`</span> keyword argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">order_info</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional information on the order detail page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">order_info_top</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional information on top of the order detail page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">order_meta_from_request</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal is sent before an order is created through the pretixpresale frontend. It allows you to return a dictionary that will be merged in the meta_info attribute of the order. You will receive the request triggering the order creation as the <span class="pre">`request`</span> keyword argument.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<div id="request-flow" class="section">

### Request flow

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">process_request</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal is sent out whenever a request is made to a event presale page. Most of the time, this will be called from the middleware layer (except on plugin-provided pages this will be called by the @event_view decorator). Similarly to Django’s process_request middleware method, if you return a Response, that response will be used and the request won’t be processed any further down the stack.

WARNING: Be very careful about using this signal as listening to it makes it really easy to cause serious performance problems.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">process_response</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>, <span class="pre">`response`</span>

This signal is sent out whenever a response is sent from a event presale page. Most of the time, this will be called from the middleware layer (except on plugin-provided pages this will be called by the @event_view decorator). Similarly to Django’s process_response middleware method you must return a response object, that will be passed further up the stack to other handlers of the signal. If you do not want to alter the response, just return the <span class="pre">`response`</span> parameter.

WARNING: Be very careful about using this signal as listening to it makes it really easy to cause serious performance problems.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

</div>

<div id="vouchers" class="section">

### Vouchers

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">voucher_redeem_info</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`voucher`</span>

This signal is sent out to display additional information on the “redeem a voucher” page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

</div>

</div>

<div id="module-pretix.control.signals" class="section">

<span id="backend"></span>

## Backend

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">event_settings_widget</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’

This signal is sent out to include template snippets on the settings page of an event that allows generating a pretix Widget code.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A second keyword argument <span class="pre">`request`</span> will contain the request object.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">html_head</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to put code inside the HTML <span class="pre">`<head>`</span> tag of every page in the backend. You will get the request as the keyword argument <span class="pre">`request`</span> and are expected to return plain HTML.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">html_page_start</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
This signal allows you to put code in the beginning of the main page for every page in the backend. You are expected to return HTML.

The <span class="pre">`sender`</span> keyword argument will contain the request.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">item_formsets</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’, ‘item’

This signal allows you to return additional formsets that should be rendered on the product modification page. You are passed <span class="pre">`request`</span> and <span class="pre">`item`</span> arguments and are expected to return an instance of a formset class that you bind yourself when appropriate. Your formset will be executed as part of the standard validation and rendering cycle and rendered using default bootstrap styles. It is advisable to set a prefix for your formset to avoid clashes with other plugins.

Your formset needs to have two special properties: <span class="pre">`template`</span> with a template that will be included to render the formset and <span class="pre">`title`</span> that will be used as a headline. Your template will be passed a <span class="pre">`formset`</span> variable with your formset.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">nav_event</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to add additional views to the admin panel navigation. You will get the request as a keyword argument <span class="pre">`request`</span>. Receivers are expected to return a list of dictionaries. The dictionaries should contain at least the keys <span class="pre">`label`</span> and <span class="pre">`url`</span>. You can also return a fontawesome icon name with the key <span class="pre">`icon`</span>, it will be respected depending on the type of navigation. You should also return an <span class="pre">`active`</span> key with a boolean set to <span class="pre">`True`</span>, when this item should be marked as active. The <span class="pre">`request`</span> object will have an attribute <span class="pre">`event`</span>.

You can optionally create sub-items to create hierarchical navigation. There are two ways to achieve this: Either you specify a key <span class="pre">`children`</span> on your top navigation item that contains a list of navigation items (as dictionaries), or you specify a <span class="pre">`parent`</span> key with the <span class="pre">`url`</span> value of the designated parent item. The latter method also allows you to register navigation items as a sub-item of existing ones.

If you use this, you should read the documentation on <a href="urlconfig.md#urlconf" class="reference internal"><span class="std std-ref">how to deal with URLs</span></a> in pretix.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">nav_event_settings</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’

This signal is sent out to include tab links on the settings page of an event. Receivers are expected to return a list of dictionaries. The dictionaries should contain at least the keys <span class="pre">`label`</span> and <span class="pre">`url`</span>. You should also return an <span class="pre">`active`</span> key with a boolean set to <span class="pre">`True`</span>, when this item should be marked as active.

If your linked view should stay in the tab-like context of this page, we recommend that you use <span class="pre">`pretix.control.views.event.EventSettingsViewMixin`</span> for your view and your template inherits from <span class="pre">`pretixcontrol/event/settings_base.html`</span>.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. A second keyword argument <span class="pre">`request`</span> will contain the request object.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">nav_global</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to add additional views to the navigation bar when no event is selected. You will get the request as a keyword argument <span class="pre">`request`</span>. Receivers are expected to return a list of dictionaries. The dictionaries should contain at least the keys <span class="pre">`label`</span> and <span class="pre">`url`</span>. You can also return a fontawesome icon name with the key <span class="pre">`icon`</span>, it will be respected depending on the type of navigation. You should also return an <span class="pre">`active`</span> key with a boolean set to <span class="pre">`True`</span>, when this item should be marked as active.

You can optionally create sub-items to create hierarchical navigation. There are two ways to achieve this: Either you specify a key <span class="pre">`children`</span> on your top navigation item that contains a list of navigation items (as dictionaries), or you specify a <span class="pre">`parent`</span> key with the <span class="pre">`url`</span> value of the designated parent item. The latter method also allows you to register navigation items as a sub-item of existing ones.

If you use this, you should read the documentation on <a href="urlconfig.md#urlconf" class="reference internal"><span class="std std-ref">how to deal with URLs</span></a> in pretix.

This is no <span class="pre">`EventPluginSignal`</span>, so you do not get the event in the <span class="pre">`sender`</span> argument and you may get the signal regardless of whether your plugin is active.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">nav_organizer</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.OrganizerPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘organizer’, ‘request’

This signal is sent out to include tab links on the detail page of an organizer. Receivers are expected to return a list of dictionaries. The dictionaries should contain at least the keys <span class="pre">`label`</span> and <span class="pre">`url`</span>. You should also return an <span class="pre">`active`</span> key with a boolean set to <span class="pre">`True`</span>, when this item should be marked as active.

You can optionally create sub-items to create hierarchical navigation. There are two ways to achieve this: Either you specify a key <span class="pre">`children`</span> on your top navigation item that contains a list of navigation items (as dictionaries), or you specify a <span class="pre">`parent`</span> key with the <span class="pre">`url`</span> value of the designated parent item. The latter method also allows you to register navigation items as a sub-item of existing ones.

If your linked view should stay in the tab-like context of this page, we recommend that you use <span class="pre">`pretix.control.views.organizer.OrganizerDetailViewMixin`</span> for your view and your template inherits from <span class="pre">`pretixcontrol/organizers/base.html`</span>.

This is an organizer plugin signal (not an event-level signal). Organizer and hybrid plugins, will receive it if they’re active for the current organizer.

**Deprecation Notice:** Currently, event plugins can always receive this signal, regardless of activation. In the future, event plugins will not be allowed to register to organizer-level signals.

Receivers will be passed the keyword arguments <span class="pre">`organizer`</span> and <span class="pre">`request`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">nav_topbar</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal allows you to add additional views to the top navigation bar. You will get the request as a keyword argument <span class="pre">`request`</span>. Receivers are expected to return a list of dictionaries. The dictionaries should contain at least the keys <span class="pre">`label`</span> and <span class="pre">`url`</span>. You can also return a fontawesome icon name with the key <span class="pre">`icon`</span>, it will be respected depending on the type of navigation. If set, on desktops only the <span class="pre">`icon`</span> will be shown. The <span class="pre">`title`</span> property can be used to set the alternative text.

If you use this, you should read the documentation on <a href="urlconfig.md#urlconf" class="reference internal"><span class="std std-ref">how to deal with URLs</span></a> in pretix.

This is no <span class="pre">`EventPluginSignal`</span>, so you do not get the event in the <span class="pre">`sender`</span> argument and you may get the signal regardless of whether your plugin is active.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">oauth_application_registered</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`user`</span>, <span class="pre">`application`</span>

This signal will be called whenever a user registers a new OAuth application.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">order_approve_info</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional information on the order approve page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. Additionally, the argument <span class="pre">`order`</span> and <span class="pre">`request`</span> are available.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">order_info</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional information on the order detail page

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. Additionally, the argument <span class="pre">`order`</span> and <span class="pre">`request`</span> are available.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">order_position_buttons</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>, <span class="pre">`position`</span>, <span class="pre">`request`</span>

This signal is sent out to display additional buttons for a single position of an order.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. Additionally, the argument <span class="pre">`order`</span> and <span class="pre">`request`</span> are available.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">order_search_filter_q</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`query`</span>

This signal will be called whenever a free-text order search is performed. You are expected to return one Q object that will be OR-ed with existing search queries. As order search exists on a global level as well, this is not an Event signal and will be called even if your plugin is not active. <span class="pre">`sender`</span> will contain the event if the search is performed within an event, and <span class="pre">`None`</span> otherwise. The search query will be passed as <span class="pre">`query`</span>.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">order_search_forms</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’

This signal allows you to return additional forms that should be rendered in the advanced order search. You are passed <span class="pre">`request`</span> argument and are expected to return an instance of a form class that you bind yourself when appropriate. Your form will be executed as part of the standard validation and rendering cycle and rendered using default bootstrap styles.

You are required to set <span class="pre">`prefix`</span> on your form instance. You are required to implement a <span class="pre">`filter_qs(queryset)`</span> method on your form that returns a new, filtered query set. You are required to implement a <span class="pre">`filter_to_strings()`</span> method on your form that returns a list of strings describing the currently active filters.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">quota_detail_html</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘quota’

This signal allows you to append HTML to a Quota’s detail view. You receive the quota as argument in the <span class="pre">`quota`</span> keyword argument.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">subevent_detail_html</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘subevent’

This signal allows you to append HTML to a SubEvent’s detail view. You receive the subevent as argument in the <span class="pre">`subevent`</span> keyword argument.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">subevent_forms</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’, ‘subevent’, ‘copy_from’

This signal allows you to return additional forms that should be rendered on the subevent creation or modification page. You are passed <span class="pre">`request`</span> and <span class="pre">`subevent`</span> arguments and are expected to return an instance of a form class that you bind yourself when appropriate. Your form will be executed as part of the standard validation and rendering cycle and rendered using default bootstrap styles. It is advisable to set a prefix for your form to avoid clashes with other plugins.

<span class="pre">`subevent`</span> can be <span class="pre">`None`</span> during creation. Before <span class="pre">`save()`</span> is called, a <span class="pre">`subevent`</span> property of your form instance will automatically being set to the subevent that has just been created. During creation, <span class="pre">`copy_from`</span> can be a subevent that is being copied from.

Your forms may also have two special properties: <span class="pre">`template`</span> with a template that will be included to render the form, and <span class="pre">`title`</span>, which will be used as a headline. Your template will be passed a <span class="pre">`form`</span> variable with your form.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">customer_created</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.OrganizerPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`customer`</span>

This signal is sent out every time a customer account is created. The <span class="pre">`customer`</span> object is given as the first argument.

The <span class="pre">`sender`</span> keyword argument will contain the organizer.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">customer_signed_in</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.OrganizerPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`customer`</span>

This signal is sent out every time a customer signs in. The <span class="pre">`customer`</span> object is given as the first argument.

The <span class="pre">`sender`</span> keyword argument will contain the organizer.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">logentry_display</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`logentry`</span>

**DEPRECTATION:** Please do not use this signal for new LogEntry types. Use the log_entry_types registry instead, as described in <a href="logging.md" class="reference external">https://docs.pretix.eu/en/latest/development/implementation/logging.html</a>

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">logentry_object_link</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`logentry`</span>

**DEPRECTATION:** Please do not use this signal for new LogEntry types. Use the log_entry_types registry instead, as described in <a href="logging.md" class="reference external">https://docs.pretix.eu/en/latest/development/implementation/logging.html</a>

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">orderposition_blocked_display</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`orderposition`</span>, <span class="pre">`block_name`</span>

To display the reason for a blocked ticket to a backend user, <span class="pre">`pretix.base.signals.orderposition_block_display`</span> will be sent out.

The first received response that is not <span class="pre">`None`</span> will be used to display the block to the user. The receivers are expected to return plain text.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">requiredaction_display</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
**DEPRECATED**, will no longer be called.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">timeline_events</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to collect events for the time line shown on event dashboards. You are passed a <span class="pre">`subevent`</span> argument which might be none and you are expected to return a list of instances of <span class="pre">`pretix.base.timeline.TimelineEvent`</span>, which is a <span class="pre">`namedtuple`</span> with the fields <span class="pre">`event`</span>, <span class="pre">`subevent`</span>, <span class="pre">`datetime`</span>, <span class="pre">`description`</span> and <span class="pre">`edit_url`</span>.

<div id="id1" class="section">

### Vouchers

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">item_forms</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’, ‘item’

This signal allows you to return additional forms that should be rendered on the product modification page. You are passed <span class="pre">`request`</span> and <span class="pre">`item`</span> arguments and are expected to return an instance of a form class that you bind yourself when appropriate. Your form will be executed as part of the standard validation and rendering cycle and rendered using default bootstrap styles. It is advisable to set a prefix for your form to avoid clashes with other plugins.

Your forms may also have special properties:

- <span class="pre">`template`</span> with a template that will be included to render the form. Your template will be passed a <span class="pre">`form`</span> variable with your form.

- <span class="pre">`title`</span>, which will be used as a headline.

- <span class="pre">`ìs_layouts`</span>` `<span class="pre">`=`</span>` `<span class="pre">`True`</span>, if your form should be grouped with the ticket layout settings (mutually exclusive with setting <span class="pre">`title`</span>).

- <span class="pre">`group_with_formset`</span>` `<span class="pre">`=`</span>` `<span class="pre">`True`</span>, if your form should be grouped with a formset of the same <span class="pre">`title`</span>

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">voucher_form_class</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`cls`</span>

This signal allows you to replace the form class that is used for modifying vouchers. You will receive the default form class (or the class set by a previous plugin) in the <span class="pre">`cls`</span> argument so that you can inherit from it.

Note that this is also called for the voucher bulk creation form, which is executed in an asynchronous context. For the bulk creation form, <span class="pre">`save()`</span> is not called. Instead, you can implement <span class="pre">`post_bulk_save(saved_vouchers)`</span> which may be called multiple times for every batch persisted to the database.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">voucher_form_html</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘form’

This signal allows you to add additional HTML to the form that is used for modifying vouchers. You receive the form object in the <span class="pre">`form`</span> keyword argument.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">voucher_form_validation</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘form’

This signal allows you to add additional validation to the form that is used for creating and modifying vouchers. You will receive the form instance in the <span class="pre">`form`</span> argument and the current data state in the <span class="pre">`data`</span> argument.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

</div>

<div id="dashboards" class="section">

### Dashboards

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">event_dashboard_top</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘request’

This signal is sent out to include custom HTML in the top part of the the event dashboard. Receivers should return HTML.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. An additional keyword argument <span class="pre">`subevent`</span> *can* contain a sub-event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">event_dashboard_widgets</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to include widgets in the event dashboard. Receivers should return a list of dictionaries, where each dictionary can have the keys:

- content (str, containing HTML)

- display_size (str, one of “full” (whole row), “big” (half a row) or “small” (quarter of a row). May be ignored on small displays, default is “small”)

- priority (int, used for ordering, higher comes first, default is 1)

- url (str, optional, if the full widget should be a link)

As with all event plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event. An additional keyword argument <span class="pre">`subevent`</span> *can* contain a sub-event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.control.signals.</span></span><span class="sig-name descname"><span class="pre">user_dashboard_widgets</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
Arguments: ‘user’

This signal is sent out to include widgets in the personal user dashboard. Receivers should return a list of dictionaries, where each dictionary can have the keys:

- content (str, containing HTML)

- display_size (str, one of “full” (whole row), “big” (half a row) or “small” (quarter of a row). May be ignored on small displays, default is “small”)

- priority (int, used for ordering, higher comes first, default is 1)

- url (str, optional, if the full widget should be a link)

This is a regular django signal (no pretix event signal).

</div>

<div id="ticket-designs" class="section">

### Ticket designs

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">layout_image_variables</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to collect variables that can be used to display dynamic images in ticket-related PDF layouts. Receivers are expected to return a dictionary with globally unique identifiers as keys and more dictionaries as values that contain keys like in the following example:

<div class="highlight-python notranslate">

<div class="highlight">

    1return {
    2    "profile": {
    3        "label": _("Profile picture"),
    4        "evaluate": lambda orderposition, order, event: ContentFile(b"some-image-data"),
    5        "etag": lambda orderposition, order, event: hash(b"some-image-data")
    6    }
    7}

</div>

</div>

The <span class="pre">`evaluate`</span> member will be called with the order position, order and event as arguments. The event might also be a subevent, if applicable. The return value of <span class="pre">`evaluate`</span> should be an instance of Django’s <span class="pre">`File`</span> class and point to a valid JPEG or PNG file. If no image is available, <span class="pre">`evaluate`</span> should return <span class="pre">`None`</span>.

The <span class="pre">`etag`</span> member will be called with the same arguments as <span class="pre">`evaluate`</span> but should return a <span class="pre">`str`</span> value uniquely identifying the version of the file. This can be a hash of the file, but can also be something else. If no image is available, <span class="pre">`etag`</span> should return <span class="pre">`None`</span>. In some cases, this can speed up the implementation.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">layout_text_variables</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to collect variables that can be used to display text in ticket-related PDF layouts. Receivers are expected to return a dictionary with globally unique identifiers as keys and more dictionaries as values that contain keys like in the following example:

<div class="highlight-python notranslate">

<div class="highlight">

    1return {
    2    "product": {
    3        "label": _("Product name"),
    4        "editor_sample": _("Sample product"),
    5        "evaluate": lambda orderposition, order, event: str(orderposition.item),
    6        "evaluate_bulk": lambda orderpositions: [str(op.item) for op in orderpositions],
    7    }
    8}

</div>

</div>

The <span class="pre">`evaluate`</span> member will be called with the order position, order and event as arguments. The event might also be a subevent, if applicable.

The <span class="pre">`evaluate_bulk`</span> member is optional but can significantly improve performance in some situations because you can perform database fetches in bulk instead of single queries for every position.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.plugins.ticketoutputpdf.signals.</span></span><span class="sig-name descname"><span class="pre">override_layout</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`layout`</span>, <span class="pre">`orderposition`</span>

This signal allows you to forcefully override the ticket layout that is being used to create the ticket PDF. Use with care, as this will render any specifically by the organizer selected templates useless.

The <span class="pre">`layout`</span> keyword argument will contain the layout which has been originally selected by the system, the <span class="pre">`orderposition`</span> keyword argument will contain the <span class="pre">`OrderPosition`</span> which is being generated.

If you implement this signal and do not want to override the layout, make sure to return the <span class="pre">`layout`</span> keyword argument which you have been passed.

As with all event plugin signals, the <span class="pre">`sender`</span> keyword will contain the event.

</div>

</div>

<div id="api" class="section">

## API

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">api_event_settings_fields</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to collect serializable settings fields for the API. You are expected to return a dictionary mapping names of attributes in the settings store to DRF serializer field instances.

These are readable for all users with access to the events, therefore secrets stored in the settings store should not be included!

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.base.signals.</span></span><span class="sig-name descname"><span class="pre">validate_event_settings</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`settings_dict`</span>

This signal is sent out if the user performs an update of event settings through the API or web interface. You are passed a <span class="pre">`settings_dict`</span> dictionary with the new state of the event settings object and are expected to raise a <span class="pre">`django.core.exceptions.ValidationError`</span> if the new state is not valid. You can not modify the dictionary. This is only recommended to use if you have multiple settings that can only be validated together. To validate individual settings, pass a validator to the serializer field instead.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.api.signals.</span></span><span class="sig-name descname"><span class="pre">order_api_details</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`order`</span>

This signal is sent out to fill the <span class="pre">`plugin_details`</span> field of the order API. Receivers should return a dictionary that is combined with the dictionaries of all other plugins. Note that doing database or network queries in receivers to this signal is discouraged and could cause serious performance issues. The main purpose is to provide information from e.g. <span class="pre">`meta_info`</span> to the API consumer,

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.api.signals.</span></span><span class="sig-name descname"><span class="pre">orderposition_api_details</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`orderposition`</span>

This signal is sent out to fill the <span class="pre">`plugin_details`</span> field of the order API. Receivers should return a dictionary that is combined with the dictionaries of all other plugins. Note that doing database or network queries in receivers to this signal is discouraged and could cause serious performance issues. The main purpose is to provide information from e.g. <span class="pre">`meta_info`</span> to the API consumer,

<!-- -->

<span class="sig-prename descclassname"><span class="pre">pretix.api.signals.</span></span><span class="sig-name descname"><span class="pre">register_device_security_profile</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.GlobalSignal</span> <span class="pre">object\></span></span>  
This signal is sent out to get all known device security_profiles. Receivers should return an instance of a subclass of <span class="pre">`pretix.api.auth.devicesecurity.BaseSecurityProfile`</span> or a list of such instances.

</div>

</div>

</div>

</div>
