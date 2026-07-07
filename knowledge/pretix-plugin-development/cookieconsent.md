---
title: "Handling cookie consent"
source: "https://docs.pretix.eu/dev/development/api/cookieconsent.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/cookieconsent.html](https://docs.pretix.eu/dev/development/api/cookieconsent.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="handling-cookie-consent" class="section">

<span id="cookieconsent"></span>

# Handling cookie consent

pretix includes an optional feature to handle cookie consent explicitly to comply with EU regulations. If your plugin sets non-essential cookies or includes a third-party service that does so, you should integrate with this feature.

<div id="server-side-integration" class="section">

## Server-side integration

First, you need to declare that you are using non-essential cookies by responding to the following signal:

<span class="sig-prename descclassname"><span class="pre">pretix.presale.signals.</span></span><span class="sig-name descname"><span class="pre">register_cookie_providers</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">\<pretix.base.signals.EventPluginSignal</span> <span class="pre">object\></span></span>  
Arguments: <span class="pre">`request`</span>

This signal is sent out to get all cookie providers that could set a cookie on this page, regardless of consent state. Receivers should return a list of <span class="pre">`pretix.presale.cookies.CookieProvider`</span> objects.

As with all event-plugin signals, the <span class="pre">`sender`</span> keyword argument will contain the event.

You are expected to return a list of <span class="pre">`CookieProvider`</span> objects instantiated from the following class:

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.presale.cookies.</span></span><span class="sig-name descname"><span class="pre">CookieProvider</span></span>  
<span class="sig-prename descclassname"><span class="pre">CookieProvider.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier used to distinguish this cookie provider form others (required).

<span class="sig-prename descclassname"><span class="pre">CookieProvider.</span></span><span class="sig-name descname"><span class="pre">provider_name</span></span>  
A human-readable name of the entity of feature responsible for setting the cookie (required).

<span class="sig-prename descclassname"><span class="pre">CookieProvider.</span></span><span class="sig-name descname"><span class="pre">usage_classes</span></span>  
A list of enum values from the <span class="pre">`pretix.presale.cookies.UsageClass`</span> enumeration class, such as <span class="pre">`UsageClass.ANALYTICS`</span>, <span class="pre">`UsageClass.MARKETING`</span>, or <span class="pre">`UsageClass.SOCIAL`</span> (required).

<span class="sig-prename descclassname"><span class="pre">CookieProvider.</span></span><span class="sig-name descname"><span class="pre">privacy_url</span></span>  
A link to a privacy policy (optional).

Here is an example of such a receiver:

<div class="highlight-python notranslate">

<div class="highlight">

    1@receiver(register_cookie_providers)
    2def recv_cookie_providers(sender, request, **kwargs):
    3    return [
    4        CookieProvider(
    5            identifier='google_analytics',
    6            provider_name='Google Analytics',
    7            usage_classes=[UsageClass.ANALYTICS],
    8        )
    9    ]

</div>

</div>

</div>

<div id="javascript-side-integration" class="section">

## JavaScript-side integration

The server-side integration only causes the cookie provider to show up in the cookie dialog. You still need to care about actually enforcing the consent state.

You can access the consent state through the <span class="pre">`window.pretix.cookie_consent`</span> variable. Whenever the value changes, a <span class="pre">`pretix:cookie-consent:change`</span> event is fired on the <span class="pre">`document`</span> object.

The variable will generally have one of the following states:

| State | Interpretation |
|----|----|
| <span class="pre">`pretix`</span>` `<span class="pre">`===`</span>` `<span class="pre">`undefined`</span>` `<span class="pre">`||`</span>` `<span class="pre">`pretix.cookie_consent`</span>` `<span class="pre">`===`</span>` `<span class="pre">`undefined`</span> | Your JavaScript has loaded before the cookie consent script. Wait for the event to be fired, then try again, do not yet set a cookie. |
| <span class="pre">`pretix.cookie_consent`</span>` `<span class="pre">`===`</span>` `<span class="pre">`null`</span> | The cookie consent mechanism has not been enabled. This usually means that you can set cookies however you like. |
| <span class="pre">`pretix.cookie_consent[identifier]`</span>` `<span class="pre">`===`</span>` `<span class="pre">`undefined`</span> | The cookie consent mechanism is loaded, but has no data on your cookie yet, wait for the event to be fired, do not yet set a cookie. |
| <span class="pre">`pretix.cookie_consent[identifier]`</span>` `<span class="pre">`===`</span>` `<span class="pre">`true`</span> | The user has consented to your cookie. |
| <span class="pre">`pretix.cookie_consent[identifier]`</span>` `<span class="pre">`===`</span>` `<span class="pre">`false`</span> | The user has actively rejected your cookie. |

If you are integrating e.g. a tracking provider with native cookie consent support such as Facebook’s Pixel, you can integrate it like this:

<div class="highlight-javascript notranslate">

<div class="highlight">

    1var consent = (window.pretix || {}).cookie_consent;
    2if (consent !== null && !(consent || {}).facebook) {
    3    fbq('consent', 'revoke');
    4}
    5fbq('init', ...);
    6document.addEventListener('pretix:cookie-consent:change', function (e) {
    7    fbq('consent', (e.detail || {}).facebook ? 'grant' : 'revoke');
    8})

</div>

</div>

If you have a JavaScript function that you only want to load if consent for a specific <span class="pre">`identifier`</span> is given, you can wrap it like this:

<div class="highlight-javascript notranslate">

<div class="highlight">

     1var consent_identifier = "youridentifier";
     2var consent = (window.pretix || {}).cookie_consent;
     3if (consent === null || (consent || {})[consent_identifier] === true) {
     4    // Cookie consent tool is either disabled or consent is given
     5    addScriptElement(src);
     6    return;
     7}
     8
     9// Either cookie consent tool has not loaded yet or consent is not given
    10document.addEventListener('pretix:cookie-consent:change', function onChange(e) {
    11    var consent = e.detail || {};
    12    if (consent === null || consent[consent_identifier] === true) {
    13        addScriptElement(src);
    14        document.removeEventListener('pretix:cookie-consent:change', onChange);
    15    }
    16})

</div>

</div>

</div>

</div>

</div>

</div>
