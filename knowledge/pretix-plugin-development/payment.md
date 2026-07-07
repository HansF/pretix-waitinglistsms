---
title: "Writing a payment provider plugin"
source: "https://docs.pretix.eu/dev/development/api/payment.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/payment.html](https://docs.pretix.eu/dev/development/api/payment.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="writing-a-payment-provider-plugin" class="section">

# Writing a payment provider plugin

In this document, we will walk through the creation of a payment provider plugin. This is very similar to creating an export output.

Please read <a href="plugins.md#pluginsetup" class="reference internal"><span class="std std-ref">Creating a plugin</span></a> first, if you haven’t already.

<div class="admonition warning">

Warning

We changed our payment provider API a lot in pretix 2.x. Our documentation page on <span class="xref std std-ref">payment2.0</span> might be insightful even if you do not have a payment provider to port, as it outlines the rationale behind the current design.

</div>

<div id="provider-registration" class="section">

## Provider registration

The payment provider API does not make a lot of usage from signals, however, it does use a signal to get a list of all available payment providers. Your plugin should listen for this signal and return the subclass of <span class="pre">`pretix.base.payment.BasePaymentProvider`</span> that the plugin will provide:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.dispatch import receiver
    2
    3from pretix.base.signals import register_payment_providers
    4
    5
    6@receiver(register_payment_providers, dispatch_uid="payment_paypal")
    7def register_payment_provider(sender, **kwargs):
    8    from .payment import Paypal
    9    return Paypal

</div>

</div>

</div>

<div id="the-provider-class" class="section">

## The provider class

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.payment.</span></span><span class="sig-name descname"><span class="pre">BasePaymentProvider</span></span>  
The central object of each payment provider is the subclass of <span class="pre">`BasePaymentProvider`</span>.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">event</span></span>  
The default constructor sets this property to the event we are currently working for.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">settings</span></span>  
The default constructor sets this property to a <span class="pre">`SettingsSandbox`</span> object. You can use this object to store settings using its <span class="pre">`get`</span> and <span class="pre">`set`</span> methods. All settings you store are transparently prefixed, so you get your very own settings namespace.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this payment provider. This should only contain lowercase letters and in most cases will be the same as your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name for this payment provider. This should be short but self-explaining. Good examples include ‘Bank transfer’ and ‘Credit card via Stripe’.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">public_name</span></span>  
A human-readable name for this payment provider to be shown to the public. This should be short but self-explaining. Good examples include ‘Bank transfer’ and ‘Credit card’, but ‘Credit card via Stripe’ might be to explicit. By default, this is the same as <span class="pre">`verbose_name`</span>

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">confirm_button_name</span></span>  
A label for the “confirm” button on the last page before a payment is started. This is **not** used in the regular checkout flow, but only if the payment method is selected for an existing order later on.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">is_enabled</span></span>  
Returns whether or whether not this payment provider is enabled. By default, this is determined by the value of the <span class="pre">`_enabled`</span> setting.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">priority</span></span>  
Returns a priority that is used for sorting payment providers. Higher priority means higher up in the list. Default to 100. Providers with same priority are sorted alphabetically.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">settings_form_fields</span></span>  
When the event’s administrator visits the event configuration page, this method is called to return the configuration fields available.

It should therefore return a dictionary where the keys should be (unprefixed) settings keys and the values should be corresponding Django form fields.

The default implementation returns the appropriate fields for the <span class="pre">`_enabled`</span>, <span class="pre">`_fee_abs`</span>, <span class="pre">`_fee_percent`</span> and <span class="pre">`_availability_date`</span> settings mentioned above.

We suggest that you return an <span class="pre">`OrderedDict`</span> object instead of a dictionary and make use of the default implementation. Your implementation could look like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1@property
     2def settings_form_fields(self):
     3    return OrderedDict(
     4        list(super().settings_form_fields.items()) + [
     5            ('bank_details',
     6             forms.CharField(
     7                 widget=forms.Textarea,
     8                 label=_('Bank account details'),
     9                 required=False
    10             ))
    11        ]
    12    )

</div>

</div>

<div class="admonition warning">

Warning

It is highly discouraged to alter the <span class="pre">`_enabled`</span> field of the default implementation.

</div>

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">walletqueries</span></span>  
<div class="admonition warning">

Warning

This property is considered **experimental**. It might change or get removed at any time without prior notice.

</div>

A list of wallet payment methods that should be dynamically joined to the public name of the payment method, if they are available to the user. The detection is made on a best effort basis with no guarantees of correctness and actual availability. Wallets that pretix can check for are exposed through <span class="pre">`pretix.base.payment.WalletQueries`</span>.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">settings_form_clean</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">cleaned_data</span></span>*<span class="sig-paren">)</span>  
Overriding this method allows you to inject custom validation into the settings form.

Parameters<span class="colon">:</span>  
**cleaned_data** – Form data as per previous validations.

Returns<span class="colon">:</span>  
Please return the modified cleaned_data

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">settings_content_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
When the event’s administrator visits the event configuration page, this method is called. It may return HTML containing additional information that is displayed below the form fields configured in <span class="pre">`settings_form_fields`</span>.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">is_allowed</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">total</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Decimal</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
You can use this method to disable this payment provider for certain groups of users, products or other criteria. If this method returns <span class="pre">`False`</span>, the user will not be able to select this payment method. This will only be called during checkout, not on retrying.

The default implementation checks for the <span class="pre">`_availability_date`</span> setting to be either unset or in the future and for the <span class="pre">`_availability_from`</span>, <span class="pre">`_total_max`</span>, and <span class="pre">`_total_min`</span> requirements to be met. It also checks the <span class="pre">`_restrict_countries`</span> and <span class="pre">`_restrict_to_sales_channels`</span> setting.

Parameters<span class="colon">:</span>  
**total** – The total value without the payment method fee, after taxes.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_form_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">total</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Decimal</span></span>*, *<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
When the user selects this provider as their preferred payment method, they will be shown the HTML you return from this method.

The default implementation will call <span class="pre">`payment_form()`</span> and render the returned form. If your payment method doesn’t require the user to fill out form fields, you should just return a paragraph of explanatory text.

Parameters<span class="colon">:</span>  
**order** – Only set when this is a change to a new payment method for an existing order.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_form</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Form</span></span></span>  
This is called by the default implementation of <span class="pre">`payment_form_render()`</span> to obtain the form that is displayed to the user during the checkout process. The default implementation constructs the form using <span class="pre">`payment_form_fields`</span> and sets appropriate prefixes for the form and all fields and fills the form with data form the user’s session.

If you overwrite this, we strongly suggest that you inherit from <span class="pre">`PaymentProviderForm`</span> (from this module) that handles some nasty issues about required fields for you.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_form_fields</span></span>  
This is used by the default implementation of <span class="pre">`payment_form()`</span>. It should return an object similar to <span class="pre">`settings_form_fields`</span>.

The default implementation returns an empty dictionary.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_is_valid_session</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
This is called at the time the user tries to place the order. It should return <span class="pre">`True`</span> if the user’s session is valid and all data your payment provider requires in future steps is present.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">checkout_prepare</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">cart</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">str</span></span></span>  
Will be called after the user selects this provider as their payment method. If you provided a form to the user to enter payment data, this method should at least store the user’s input into their session.

This method should return <span class="pre">`False`</span> if the user’s input was invalid, <span class="pre">`True`</span> if the input was valid and the frontend should continue with default behavior or a string containing a URL if the user should be redirected somewhere else.

On errors, you should use Django’s message framework to display an error message to the user (or the normal form validation error messages).

The default implementation stores the input into the form returned by <span class="pre">`payment_form()`</span> in the user’s session.

If your payment method requires you to redirect the user to an external provider, this might be the place to do so.

<div class="admonition important">

Important

If this is called, the user has not yet confirmed their order. You may NOT do anything which actually moves money.

</div>

Note: The behavior of this method changes significantly when you set  
<span class="pre">`multi_use_supported`</span>. Please refer to the <span class="pre">`multi_use_supported`</span> documentation for more information.

Parameters<span class="colon">:</span>  
**cart** –

This dictionary contains at least the following keys:

positions:  
A list of <span class="pre">`CartPosition`</span> objects that are annotated with the special attributes <span class="pre">`count`</span> and <span class="pre">`total`</span> because multiple objects of the same content are grouped into one.

raw:  
The raw list of <span class="pre">`CartPosition`</span> objects in the users cart

total:  
The overall total *including* the fee for the payment method.

payment_fee:  
The fee for the payment method.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">checkout_confirm_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span>*, *<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">info_data</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
If the user has successfully filled in their payment data, they will be redirected to a confirmation page which lists all details of their order for a final review. This method should return the HTML which should be displayed inside the ‘Payment’ box on this page.

In most cases, this should include a short summary of the user’s input and a short explanation on how the payment process will continue.

Parameters<span class="colon">:</span>  
- **request** – The current HTTP request.

- **order** – Only set when this is a change to a new payment method for an existing order.

- **info_data** – The <span class="pre">`info_data`</span> dictionary you set during <span class="pre">`add_payment_to_cart`</span> (only filled if <span class="pre">`multi_use_supported`</span> is set)

This is an abstract method, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">execute_payment</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">None</span></span></span>  
After the user has confirmed their purchase, this method will be called to complete the payment process. This is the place to actually move the money if applicable. You will be passed an <a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.OrderPayment"><span class="pre"><code class="sourceCode python xref py py-class docutils literal notranslate">pretix.base.models.OrderPayment</code></span></a> object that contains the amount of money that should be paid.

If you need any special behavior, you can return a string containing the URL the user will be redirected to. If you are done with your process you should return the user to the order’s detail page. Redirection is only allowed if you set <span class="pre">`execute_payment_needs_user`</span> to <span class="pre">`True`</span>.

If the payment is completed, you should call <span class="pre">`payment.confirm()`</span>. Please note that this might raise a <span class="pre">`Quota.QuotaExceededException`</span> if (and only if) the payment term of this order is over and some of the items are sold out. You should use the exception message to display a meaningful error to the user.

The default implementation just returns <span class="pre">`None`</span> and therefore leaves the order unpaid. The user will be redirected to the order’s detail page by default.

On errors, you should raise a <span class="pre">`PaymentException`</span>.

Parameters<span class="colon">:</span>  
- **request** – A HTTP request, except if <span class="pre">`execute_payment_needs_user`</span> is <span class="pre">`False`</span>

- **payment** – An <span class="pre">`OrderPayment`</span> instance

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">calculate_fee</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">price</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Decimal</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Decimal</span></span></span>  
Calculate the fee for this payment provider which will be added to final price before fees (but after taxes). It should include any taxes. The default implementation makes use of the setting <span class="pre">`_fee_abs`</span> for an absolute fee and <span class="pre">`_fee_percent`</span> for a percentage.

Parameters<span class="colon">:</span>  
**price** – The total value without the payment method fee, after taxes.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">order_pending_mail_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
After the user has submitted their order, they will receive a confirmation email. You can return a string from this method if you want to add additional information to this email.

Parameters<span class="colon">:</span>  
- **order** – The order object

- **payment** – The payment object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_pending_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Render customer-facing instructions on how to proceed with a pending payment

Returns<span class="colon">:</span>  
HTML

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">abort_pending_allowed</span></span>  
Whether or not a user can abort a payment in pending state to switch to another payment method. This returns <span class="pre">`False`</span> by default which is no guarantee that aborting a pending payment can never happen, it just hides the frontend button to avoid users accidentally committing double payments.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">render_invoice_text</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
This is called when an invoice for an order with this payment provider is generated. The default implementation returns the content of the \_invoice_text configuration variable (an I18nString), or an empty string if unconfigured. For paid orders, the default implementation always renders a string stating that the invoice is already paid.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">render_invoice_stamp</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
This is called when an invoice for an order with this payment provider is generated. The default implementation returns “paid” if the order was already paid, and <span class="pre">`None`</span> otherwise. You can override this with a string, but it should be *really* short to make the invoice look pretty.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">order_change_allowed</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*, *<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
Will be called to check whether it is allowed to change the payment method of an order to this one.

The default implementation checks for the <span class="pre">`_availability_date`</span> setting to be either unset or in the future, as well as for the <span class="pre">`_availability_from`</span>, <span class="pre">`_total_max`</span>, <span class="pre">`_total_min`</span>, and <span class="pre">`_restricted_countries`</span> settings.

Parameters<span class="colon">:</span>  
**order** – The order object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_prepare</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><span class="pre">str</span></span></span>  
Will be called if the user retries to pay an unpaid order (after the user filled in e.g. the form returned by <span class="pre">`payment_form()`</span>) or if the user changes the payment method.

It should return and report errors the same way as <span class="pre">`checkout_prepare()`</span>, but receives an <span class="pre">`Order`</span> object instead of a cart object.

Note: The <span class="pre">`Order`</span> object given to this method might be different from the version stored in the database as it’s total will already contain the payment fee for the new payment method.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_control_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Will be called if the *event administrator* views the details of a payment.

It should return HTML code containing information regarding the current payment status and, if applicable, next steps.

The default implementation returns an empty string.

Parameters<span class="colon">:</span>  
**order** – The order object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_control_render_short</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Will be called if the *event administrator* performs an action on the payment. Should return a very short version of the payment method. Usually, this should return e.g. an account identifier of the payee, but no information on status, dates, etc.

The default implementation falls back to <span class="pre">`payment_presale_render`</span>.

Parameters<span class="colon">:</span>  
**payment** – The payment object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_refund_supported</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
Will be called to check if the provider supports automatic refunding for this payment.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_partial_refund_supported</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>  
Will be called to check if the provider supports automatic partial refunding for this payment.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">payment_presale_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Will be called if the *ticket customer* views the details of a payment. This is currently used e.g. when the customer requests a refund to show which payment method is used for the refund. This should only include very basic information about the payment, such as “VISA card …9999”, and never raw payment information.

The default implementation returns the public name of the payment provider.

Parameters<span class="colon">:</span>  
**order** – The order object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">execute_refund</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">refund</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span>*<span class="sig-paren">)</span>  
Will be called to execute an refund. Note that refunds have an amount property and can be partial.

This should transfer the money back (if possible). On success, you should call <span class="pre">`refund.done()`</span>. On failure, you should raise a PaymentException.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">refund_control_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">refund</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Will be called if the *event administrator* views the details of a refund.

It should return HTML code containing information regarding the current refund status and, if applicable, next steps.

The default implementation returns an empty string.

Parameters<span class="colon">:</span>  
**refund** – The refund object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">refund_control_render_short</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">refund</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Will be called if the *event administrator* performs an action on the refund. Should return a very short description of the refund method. Usually, this should return e.g. an account identifier of the refund recipient, but no information on status, dates, etc.

The default implementation returns an empty string.

Parameters<span class="colon">:</span>  
**refund** – The refund object

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">new_refund_control_form_render</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>  
Render a form that will be shown to backend users when trying to create a new refund.

Usually, refunds are created from an existing payment object, e.g. if there is a credit card payment and the credit card provider returns <span class="pre">`True`</span> from <span class="pre">`payment_refund_supported`</span>, the system will automatically create an <span class="pre">`OrderRefund`</span> and call <span class="pre">`execute_refund`</span> on that payment. This method can and should not be used in that situation! Instead, by implementing this method you can add a refund flow for this payment provider that starts without an existing payment. For example, even though an order was paid by credit card, it could easily be refunded by SEPA bank transfer. In that case, the SEPA bank transfer provider would implement this method and return a form that asks for the IBAN.

This method should return HTML or <span class="pre">`None`</span>. All form fields should have a globally unique name.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">new_refund_control_form_process</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">HttpRequest</span></span>*, *<span class="n"><span class="pre">amount</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Decimal</span></span>*, *<span class="n"><span class="pre">order</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.Order" class="reference internal" title="pretix.base.models.orders.Order"><span class="pre">Order</span></a></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span></span>  
Process a backend user’s request to initiate a new refund with an amount of <span class="pre">`amount`</span> for <span class="pre">`order`</span>.

This method should parse the input provided to the form created and either raise <span class="pre">`ValidationError`</span> or return an <span class="pre">`OrderRefund`</span> object in <span class="pre">`created`</span> state that has not yet been saved to the database. The system will then call <span class="pre">`execute_refund`</span> on that object.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">api_payment_details</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span>  
Will be called to populate the <span class="pre">`details`</span> parameter of the payment in the REST API.

Parameters<span class="colon">:</span>  
**payment** – The payment in question.

Returns<span class="colon">:</span>  
A serializable dictionary

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">api_refund_details</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">refund</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span>*<span class="sig-paren">)</span>  
Will be called to populate the <span class="pre">`details`</span> parameter of the refund in the REST API.

Parameters<span class="colon">:</span>  
**refund** – The refund in question.

Returns<span class="colon">:</span>  
A serializable dictionary

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">matching_id</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span>  
Will be called to get an ID for matching this payment when comparing pretix records with records of an external source. This should return the main transaction ID for your API.

Parameters<span class="colon">:</span>  
**payment** – The payment in question.

Returns<span class="colon">:</span>  
A string or None

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">refund_matching_id</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">refund</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span>*<span class="sig-paren">)</span>  
Will be called to get an ID for matching this refund when comparing pretix records with records of an external source. This should return the main transaction ID for your API.

Parameters<span class="colon">:</span>  
**refund** – The refund in question.

Returns<span class="colon">:</span>  
A string or None

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">shred_payment_info</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">obj</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a><span class="w"> </span><span class="p"><span class="pre">\|</span></span><span class="w"> </span><a href="models.md#pretix.base.models.OrderRefund" class="reference internal" title="pretix.base.models.orders.OrderRefund"><span class="pre">OrderRefund</span></a></span>*<span class="sig-paren">)</span>  
When personal data is removed from an event, this method is called to scrub payment-related data from a payment or refund. By default, it removes all info from the <span class="pre">`info`</span> attribute. You can override this behavior if you want to retain attributes that are not personal data on their own, i.e. a reference to a transaction in an external system. You can also override this to scrub more data, e.g. data from external sources that is saved in LogEntry objects or other places.

Parameters<span class="colon">:</span>  
**order** – An order

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">cancel_payment</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">payment</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a href="models.md#pretix.base.models.OrderPayment" class="reference internal" title="pretix.base.models.orders.OrderPayment"><span class="pre">OrderPayment</span></a></span>*<span class="sig-paren">)</span>  
Will be called to cancel a payment. The default implementation fails if the payment is <span class="pre">`OrderPayment.PAYMENT_STATE_PENDING`</span> and <span class="pre">`abort_pending_allowed`</span> is false. Otherwise, it just sets the payment state to canceled. In some cases you might want to modify this behaviour to notify the external provider of the cancellation.

On success, you should set <span class="pre">`payment.state`</span>` `<span class="pre">`=`</span>` `<span class="pre">`OrderPayment.PAYMENT_STATE_CANCELED`</span> (or call the super method). On failure, you should raise a PaymentException.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">is_implicit</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<function</span> <span class="pre">BasePaymentProvider.is_implicit\></span></span>  

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">is_meta</span></span>  
Returns whether or whether not this payment provider is a “meta” payment provider that only works as a settings holder for other payment providers and should never be used directly. This is a trick to implement payment gateways with multiple payment methods but unified payment settings. Take a look at the built-in stripe provider to see how this might be used. By default, this returns <span class="pre">`False`</span>.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">execute_payment_needs_user</span></span>  
Set this to <span class="pre">`True`</span> if your <span class="pre">`execute_payment`</span> function needs to be triggered by a user request, i.e. either needs the <span class="pre">`request`</span> object or might require a browser redirect. If this is <span class="pre">`False`</span>, you will not receive a <span class="pre">`request`</span> and may not redirect since execute_payment might be called server-side. You should ensure that your <span class="pre">`execute_payment`</span> method has a limited execution time (i.e. by using <span class="pre">`timeout`</span> for all external calls) and handles all error cases appropriately.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">multi_use_supported</span></span>  
Returns whether or whether not this payment provider supports being used multiple times in the same checkout, or in addition to a different payment provider. This is usually only useful for payment providers that represent gift cards, i.e. payment methods with an upper limit per payment instrument that can usually be combined with other instruments.

If you set this property to <span class="pre">`True`</span>, the behavior of how pretix interacts with your payment provider changes and you will need to respect the following rules:

- <span class="pre">`payment_form_render`</span> must not depend on session state, it must always allow a user to add a new payment.  
  Editing a payment is not possible, but pretix will give users an option to delete it.

- Returning <span class="pre">`True`</span> from <span class="pre">`checkout_prepare`</span> is no longer enough. Instead, you must *also* call <span class="pre">`pretix.base.services.cart.add_payment_to_cart(request,`</span>` `<span class="pre">`provider,`</span>` `<span class="pre">`min_value,`</span>` `<span class="pre">`max_value,`</span>` `<span class="pre">`info_data)`</span> to add the payment to the session. You are still allowed to do a redirect from <span class="pre">`checkout_prepare`</span> and then call this function upon return.

- Unlike in the general case, when <span class="pre">`checkout_prepare`</span> is called, the <span class="pre">`cart['total']`</span> parameter will **not yet** include payment fees charged by your provider as we don’t yet know the amount of the charge, so you need to take care of that yourself when setting your maximum amount.

- <span class="pre">`payment_is_valid_session`</span> will not be called during checkout, don’t rely on it. If you called <span class="pre">`add_payment_to_cart`</span>, we’ll trust the payment is okay and your next chance to change that will be <span class="pre">`execute_payment`</span>.

The changed behavior currently only affects the behavior during initial checkout (i.e. <span class="pre">`checkout_prepare`</span>), for <span class="pre">`payment_prepare`</span> the regular behavior applies and you are expected to just modify the amount of the <span class="pre">`OrderPayment`</span> object if you need to.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">test_mode_message</span></span>  
If this property is set to a string, this will be displayed when this payment provider is selected while the event is in test mode. You should use it to explain to your user how your plugin behaves, e.g. if it falls back to a test mode automatically as well or if actual payments will be performed.

If you do not set this (or, return <span class="pre">`None`</span>), pretix will show a default message warning the user that this plugin does not support test mode payments.

<span class="sig-prename descclassname"><span class="pre">BasePaymentProvider.</span></span><span class="sig-name descname"><span class="pre">requires_invoice_immediately</span></span>  
Return whether this payment method requires an invoice to exist for an order, even though the event is configured to only create invoices for paid orders. By default this is False, but it might be overwritten for e.g. bank transfer. execute_payment is called after the invoice is created.

</div>

<div id="additional-views" class="section">

## Additional views

See also: <a href="customview.md#customview" class="reference internal"><span class="std std-ref">Creating custom views</span></a>.

For most simple payment providers it is more than sufficient to implement some of the <span class="pre">`BasePaymentProvider`</span> methods. However, in some cases it is necessary to introduce additional views. One example is the PayPal provider. It redirects the user to a PayPal website in the <span class="pre">`BasePaymentProvider.checkout_prepare()`</span> step of the checkout process and provides PayPal with a URL to redirect back to. This URL points to a view which looks roughly like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1@login_required
     2def success(request):
     3    pid = request.GET.get('paymentId')
     4    payer = request.GET.get('PayerID')
     5    # We stored some information in the session in checkout_prepare(),
     6    # let's compare the new information to double-check that this is about
     7    # the same payment
     8    if pid == request.session['payment_paypal_id']:
     9        # Save the new information to the user's session
    10        request.session['payment_paypal_payer'] = payer
    11        try:
    12            # Redirect back to the confirm page. We chose to save the
    13            # event ID in the user's session. We could also put this
    14            # information into a URL parameter.
    15            event = Event.objects.current.get(identity=request.session['payment_paypal_event'])
    16            return redirect(reverse('presale:event.checkout.confirm', kwargs={
    17                'event': event.slug,
    18                'organizer': event.organizer.slug,
    19            }))
    20        except Event.DoesNotExist:
    21            pass  # TODO: Display error message
    22    else:
    23        pass  # TODO: Display error message

</div>

</div>

If you do not want to provide a view of your own, you could even let PayPal redirect directly back to the confirm page and handle the query parameters inside <span class="pre">`BasePaymentProvider.checkout_is_valid_session()`</span>. However, because some external providers (not PayPal) force you to have a *constant* redirect URL, it might be necessary to define custom views.

</div>

</div>

</div>

</div>
