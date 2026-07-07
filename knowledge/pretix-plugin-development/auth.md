---
title: "Pluggable authentication backends"
source: "https://docs.pretix.eu/dev/development/api/auth.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/auth.html](https://docs.pretix.eu/dev/development/api/auth.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="pluggable-authentication-backends" class="section">

# Pluggable authentication backends

Plugins can supply additional authentication backends. This is mainly useful in self-hosted installations and allows you to use company-wide login mechanisms such as LDAP or OAuth for accessing pretix’ backend.

Every authentication backend contains an implementation of the interface defined in <span class="pre">`pretix.base.auth.BaseAuthBackend`</span> (see below). Note that pretix authentication backends work differently than plain Django authentication backends. Basically, three pre-defined flows are supported:

- Authentication mechanisms that rely on a **set of input parameters**, e.g. a username and a password. These can be implemented by supplying the <span class="pre">`login_form_fields`</span> property and a <span class="pre">`form_authenticate`</span> method.

- Authentication mechanisms that rely on **external sessions**, e.g. a cookie or a proxy HTTP header. These can be implemented by supplying a <span class="pre">`request_authenticate`</span> method.

- Authentication mechanisms that rely on **redirection**, e.g. to an OAuth provider. These can be implemented by supplying a <span class="pre">`authentication_url`</span> method and implementing a custom return view.

For security reasons, authentication backends are *not* automatically discovered through a signal. Instead, they must explicitly be set through the <span class="pre">`auth_backends`</span> directive in the <span class="pre">`pretix.cfg`</span> <span class="xref std std-ref">configuration file</span>.

In each of these methods (<span class="pre">`form_authenticate`</span>, <span class="pre">`request_authenticate`</span>, or your custom view) you are supposed to use <span class="pre">`User.objects.get_or_create_for_backend`</span> to get a <a href="models.md#pretix.base.models.User" class="reference internal" title="pretix.base.models.User"><span class="pre"><code class="sourceCode python xref py py-class docutils literal notranslate">pretix.base.models.User</code></span></a> object from the database or create a new one.

There are a few rules you need to follow:

- You **MUST** have some kind of identifier for a user that is globally unique and **SHOULD** never change, even if the user’s name or email address changes. This could e.g. be the ID of the user in an external database. The identifier must not be longer than 190 characters. If you worry your backend might generated longer identifiers, consider using a hash function to trim them to a constant length.

- You **SHOULD** not allow users created by other authentication backends to log in through your code, and you **MUST** only create, modify or return users with <span class="pre">`auth_backend`</span> set to your backend.

- Every user object **MUST** have an email address. Email addresses are globally unique. If the email address is already registered to a user who signs in through a different backend, you **SHOULD** refuse the login.

<span class="pre">`User.objects.get_or_create_for_backend`</span> will follow these rules for you automatically. It works like this:

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.models.auth.</span></span><span class="sig-name descname"><span class="pre">UserManager</span></span><span class="sig-paren">(</span>*<span class="o"><span class="pre">\*</span></span><span class="n"><span class="pre">args</span></span>*, *<span class="o"><span class="pre">\*\*</span></span><span class="n"><span class="pre">kwargs</span></span>*<span class="sig-paren">)</span>  
This is the user manager for our custom user model. See the User model documentation to see what’s so special about our user model.

<span class="sig-name descname"><span class="pre">get_or_create_for_backend</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">backend</span></span>*, *<span class="n"><span class="pre">identifier</span></span>*, *<span class="n"><span class="pre">email</span></span>*, *<span class="n"><span class="pre">set_always</span></span>*, *<span class="n"><span class="pre">set_on_creation</span></span>*<span class="sig-paren">)</span>  
This method should be used by third-party authentication backends to log in a user. It either returns an already existing user or creates a new user.

In pretix 4.7 and earlier, email addresses were the only property to identify a user with. Starting with pretix 4.8, backends SHOULD instead use a unique, immutable identifier based on their backend data store to allow for changing email addresses.

This method transparently handles the conversion of old user accounts and adds the backend identifier to their database record.

This method will never return users managed by a different authentication backend. If you try to create an account with an email address already blocked by a different authentication backend, <span class="pre">`EmailAddressTakenError`</span> will be raised. In this case, you should display a message to the user.

Parameters<span class="colon">:</span>  
- **backend** – The identifier attribute of the authentication backend

- **identifier** – The unique, immutable identifier of this user, max. 190 characters

- **email** – The user’s email address

- **set_always** – A dictionary of fields to update on the user model on every login

- **set_on_creation** – A dictionary of fields to set on the user model if it’s newly created

Returns<span class="colon">:</span>  
A User instance.

<div id="the-backend-interface" class="section">

## The backend interface

<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">pretix.base.auth.</span></span><span class="sig-name descname"><span class="pre">BaseAuthBackend</span></span>  
The central object of each backend is the subclass of <span class="pre">`BaseAuthBackend`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">identifier</span></span>  
A short and unique identifier for this authentication backend. This should only contain lowercase letters and in most cases will be the same as your package name.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">verbose_name</span></span>  
A human-readable name of this authentication backend.

This is an abstract attribute, you **must** override this!

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">login_form_fields</span></span>  
This property may return form fields that the user needs to fill in to log in.

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">visible</span></span>  
Whether or not this backend can be selected by users actively. Set this to <span class="pre">`False`</span> if you only implement <span class="pre">`request_authenticate`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">form_authenticate</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span>*, *<span class="n"><span class="pre">form_data</span></span>*<span class="sig-paren">)</span>  
This method will be called after the user filled in the login form. <span class="pre">`request`</span> will contain the current request and <span class="pre">`form_data`</span> the input for the form fields defined in <span class="pre">`login_form_fields`</span>. You are expected to either return a <span class="pre">`User`</span> object (if login was successful) or <span class="pre">`None`</span>.

You are expected to either return a <span class="pre">`User`</span> object (if login was successful) or <span class="pre">`None`</span>. You should obtain this user object using <span class="pre">`User.objects.get_or_create_for_backend`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">request_authenticate</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span>*<span class="sig-paren">)</span>  
This method will be called when the user opens the login form. If the user already has a valid session according to your login mechanism, for example a cookie set by a different system or HTTP header set by a reverse proxy, you can directly return a <span class="pre">`User`</span> object that will be logged in.

<span class="pre">`request`</span> will contain the current request.

You are expected to either return a <span class="pre">`User`</span> object (if login was successful) or <span class="pre">`None`</span>. You should obtain this user object using <span class="pre">`User.objects.get_or_create_for_backend`</span>.

<span class="sig-prename descclassname"><span class="pre">BaseAuthBackend.</span></span><span class="sig-name descname"><span class="pre">authentication_url</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span>*<span class="sig-paren">)</span>  
This method will be called to populate the URL for your authentication method’s tab on the login page. For example, if your method works through OAuth, you could return the URL of the OAuth authorization URL the user needs to visit.

If you return <span class="pre">`None`</span> (the default), the link will point to a page that shows the form defined by <span class="pre">`login_form_fields`</span>.

</div>

<div id="logging-users-in" class="section">

## Logging users in

If you return a user from <span class="pre">`form_authenticate`</span> or <span class="pre">`request_authenticate`</span>, the system will handle everything else for you correctly. However, if you use a redirection method and build a custom view to verify the login, we strongly recommend that you use the following utility method to correctly set session values and enforce two-factor authentication (if activated):

<span class="sig-prename descclassname"><span class="pre">pretix.control.views.auth.</span></span><span class="sig-name descname"><span class="pre">process_login</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">request</span></span>*, *<span class="n"><span class="pre">user</span></span>*, *<span class="n"><span class="pre">keep_logged_in</span></span>*<span class="sig-paren">)</span>  
This method allows you to return a response to a successful log-in. This will set all session values correctly and redirect to either the URL specified in the <span class="pre">`next`</span> parameter, or the 2FA login screen, or the dashboard.

Returns<span class="colon">:</span>  
This method returns a <span class="pre">`HttpResponse`</span>.

A custom view that is called after a redirect from an external identity provider could look like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1from django.contrib import messages
     2from django.shortcuts import redirect
     3from django.urls import reverse
     4
     5from pretix.base.models import User
     6from pretix.base.models.auth import EmailAddressTakenError
     7from pretix.control.views.auth import process_login
     8
     9
    10def return_view(request):
    11    # Verify validity of login with the external provider's API
    12    api_response = my_verify_login_function(
    13        code=request.GET.get('code')
    14    )
    15
    16    try:
    17        u = User.objects.get_or_create_for_backend(
    18            'my_backend_name',
    19            api_response['userid'],
    20            api_response['email'],
    21            set_always={
    22                'fullname': '{} {}'.format(
    23                    api_response.get('given_name', ''),
    24                    api_response.get('family_name', ''),
    25                ),
    26            },
    27            set_on_creation={
    28                'locale': api_response.get('locale').lower()[:2],
    29                'timezone': api_response.get('zoneinfo', 'UTC'),
    30            }
    31        )
    32    except EmailAddressTakenError:
    33        messages.error(
    34            request, _('We cannot create your user account as a user account in this system '
    35                       'already exists with the same email address.')
    36        )
    37        return redirect(reverse('control:auth.login'))
    38    else:
    39        return process_login(request, u, keep_logged_in=False)

</div>

</div>

</div>

</div>

</div>

</div>
