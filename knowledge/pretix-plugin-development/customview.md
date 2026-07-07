---
title: "Creating custom views"
source: "https://docs.pretix.eu/dev/development/api/customview.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/customview.html](https://docs.pretix.eu/dev/development/api/customview.html)

<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="creating-custom-views" class="section">

<span id="customview"></span>

# Creating custom views

This page describes how to provide a custom view from within your plugin. Before you start reading this page, please read and understand how <a href="urlconfig.md#urlconf" class="reference internal"><span class="std std-ref">URL handling</span></a> works in pretix.

<div id="control-panel-views" class="section">

## Control panel views

If you want to add a custom view to the control area of an event, just register an URL in your <span class="pre">`urls.py`</span> that lives in the <span class="pre">`/control/`</span> subpath:

<div class="highlight-python notranslate">

<div class="highlight">

    1from django.urls import re_path
    2
    3from . import views
    4
    5urlpatterns = [
    6    re_path(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/mypluginname/',
    7            views.admin_view, name='backend'),
    8]

</div>

</div>

It is required that your URL parameters are called <span class="pre">`organizer`</span> and <span class="pre">`event`</span>. If you want to install a view on organizer level, you can leave out the <span class="pre">`event`</span>.

You can then implement the view as you would normally do. Our middleware will automatically detect the <span class="pre">`/control/`</span> subpath and will ensure the following things if this is an URL with both the <span class="pre">`event`</span> and <span class="pre">`organizer`</span> parameters:

- The user is logged in

- The <span class="pre">`request.event`</span> attribute contains the current event

- The <span class="pre">`request.organizer`</span> attribute contains the event’s organizer

- The user has permission to access view the current event

If only the <span class="pre">`organizer`</span> parameter is present, it will be ensured that:

- The user is logged in

- The <span class="pre">`request.organizer`</span> attribute contains the event’s organizer

- The user has permission to access view the current organizer

If you want to require specific permission types, we provide you with a decorator or a mixin for your views:

<div class="highlight-python notranslate">

<div class="highlight">

     1from pretix.control.permissions import (
     2    event_permission_required, EventPermissionRequiredMixin
     3)
     4
     5class AdminView(EventPermissionRequiredMixin, View):
     6    permission = 'event.orders:read'
     7
     8    ...
     9
    10
    11@event_permission_required('event.orders:read')
    12def admin_view(request, organizer, event):
    13    ...

</div>

</div>

Similarly, there is <span class="pre">`organizer_permission_required`</span> and <span class="pre">`OrganizerPermissionRequiredMixin`</span>. In case of event-related views, there is also a signal that allows you to add the view to the event navigation like this:

<div class="highlight-python notranslate">

<div class="highlight">

     1from django.urls import resolve, reverse
     2from django.dispatch import receiver
     3from django.utils.translation import gettext_lazy as _
     4from pretix.control.signals import nav_event
     5
     6
     7@receiver(nav_event, dispatch_uid='friends_tickets_nav')
     8def navbar_info(sender, request, **kwargs):
     9    url = resolve(request.path_info)
    10    if not request.user.has_event_permission(request.organizer, request.event, 'event.vouchers:read'):
    11        return []
    12    return [{
    13        'label': _('My plugin view'),
    14        'icon': 'heart',
    15        'url': reverse('plugins:myplugin:index', kwargs={
    16            'event': request.event.slug,
    17            'organizer': request.organizer.slug,
    18        }),
    19        'active': url.namespace == 'plugins:myplugin' and url.url_name == 'review',
    20    }]

</div>

</div>

</div>

<div id="event-settings-view" class="section">

## Event settings view

A special case of a control panel view is a view hooked into the event settings page. For this case, there is a special navigation signal:

<div class="highlight-python notranslate">

<div class="highlight">

     1@receiver(nav_event_settings, dispatch_uid='friends_tickets_nav_settings')
     2def navbar_settings(sender, request, **kwargs):
     3    url = resolve(request.path_info)
     4    return [{
     5        'label': _('My settings'),
     6        'url': reverse('plugins:myplugin:settings', kwargs={
     7            'event': request.event.slug,
     8            'organizer': request.organizer.slug,
     9        }),
    10        'active': url.namespace == 'plugins:myplugin' and url.url_name == 'settings',
    11    }]

</div>

</div>

Also, your view should inherit from <span class="pre">`EventSettingsViewMixin`</span> and your template from <span class="pre">`pretixcontrol/event/settings_base.html`</span> for good integration. If you just want to display a form, you could do it like the following:

<div class="highlight-python notranslate">

<div class="highlight">

     1class MySettingsView(EventSettingsViewMixin, EventSettingsFormView):
     2    model = Event
     3    permission = 'event.settings.general:write'
     4    form_class = MySettingsForm
     5    template_name = 'my_plugin/settings.html'
     6
     7    def get_success_url(self, **kwargs):
     8        return reverse('plugins:myplugin:settings', kwargs={
     9            'organizer': self.request.event.organizer.slug,
    10            'event': self.request.event.slug,
    11        })

</div>

</div>

With this template:

<div class="highlight-python notranslate">

<div class="highlight">

     1{% extends "pretixcontrol/event/settings_base.html" %}
     2{% load i18n %}
     3{% load bootstrap3 %}
     4{% block title %} {% trans "Friends Tickets Settings" %} {% endblock %}
     5{% block inside %}
     6    <form action="" method="post" class="form-horizontal">
     7        {% csrf_token %}
     8        <fieldset>
     9            <legend>{% trans "Friends Tickets Settings" %}</legend>
    10            {% bootstrap_form form layout="horizontal" %}
    11        </fieldset>
    12        <div class="form-group submit-group">
    13            <button type="submit" class="btn btn-primary btn-save">
    14                {% trans "Save" %}
    15            </button>
    16        </div>
    17    </form>
    18{% endblock %}

</div>

</div>

</div>

<div id="frontend-views" class="section">

## Frontend views

Including a custom view into the participant-facing frontend is a little bit different as there is no path prefix like <span class="pre">`control/`</span>.

First, define your URL in your <span class="pre">`urls.py`</span>, but this time in the <span class="pre">`event_patterns`</span> section and wrapped by <span class="pre">`event_url`</span>:

<div class="highlight-python notranslate">

<div class="highlight">

    1from pretix.multidomain import event_url
    2
    3from . import views
    4
    5event_patterns = [
    6    event_url(r'^mypluginname/', views.frontend_view, name='frontend'),
    7]

</div>

</div>

You can then implement a view as you would normally do. It will be automatically ensured that:

- The requested event exists

- The requested event is active (you can disable this check using <span class="pre">`event_url(…,`</span>` `<span class="pre">`require_live=True)`</span>)

- The event is accessed via the domain it should be accessed

- The <span class="pre">`request.event`</span> attribute contains the correct <span class="pre">`Event`</span> object

- The <span class="pre">`request.organizer`</span> attribute contains the correct <span class="pre">`Organizer`</span> object

- Your plugin is enabled

- The locale is set correctly

</div>

<div id="rest-api-viewsets" class="section">

## REST API viewsets

Our REST API is built upon <a href="http://www.django-rest-framework.org/" class="reference external">Django REST Framework</a> (DRF). DRF has two important concepts that are different from standard Django request handling: There are <a href="http://www.django-rest-framework.org/api-guide/viewsets/" class="reference external">ViewSets</a> to group related views in a single class and <a href="http://www.django-rest-framework.org/api-guide/routers/" class="reference external">Routers</a> to automatically build URL configurations from them.

To integrate a custom viewset with pretix’ REST API, you can just register with one of our routers within the <span class="pre">`urls.py`</span> module of your plugin:

<div class="highlight-python notranslate">

<div class="highlight">

    1from pretix.api.urls import event_router, router, orga_router
    2
    3router.register('global_viewset', MyViewSet)
    4orga_router.register('orga_level_viewset', MyViewSet)
    5event_router.register('event_level_viewset', MyViewSet)

</div>

</div>

Routes registered with <span class="pre">`router`</span> are inserted into the global API space at <span class="pre">`/api/v1/`</span>. Routes registered with <span class="pre">`orga_router`</span> will be included at <span class="pre">`/api/v1/organizers/(organizer)/`</span> and routes registered with <span class="pre">`event_router`</span> will be included at <span class="pre">`/api/v1/organizers/(organizer)/events/(event)/`</span>.

In case of <span class="pre">`orga_router`</span> and <span class="pre">`event_router`</span>, permission checking is done for you similarly as with custom views in the control panel. However, you need to make sure on your own only to return the correct subset of data! <span class="pre">`request`</span>` `<span class="pre">`.event`</span> and <span class="pre">`request.organizer`</span> are available as usual.

To require a special permission like <span class="pre">`event.orders:read`</span>, you do not need to inherit from a special ViewSet base class, you can just set the <span class="pre">`permission`</span> attribute on your viewset:

<div class="highlight-python notranslate">

<div class="highlight">

    class MyViewSet(ModelViewSet):
        permission = 'event.orders:read'
        ...

</div>

</div>

If you want to check the permission only for some methods of your viewset, you have to do it yourself. Note here that API authentications can be done via user sessions or API tokens and you should therefore check something like the following:

<div class="highlight-python notranslate">

<div class="highlight">

    perm_holder = (request.auth if isinstance(request.auth, TeamAPIToken) else request.user)
    if perm_holder.has_event_permission(request.event.organizer, request.event, 'event.orders:read'):
        ...

</div>

</div>

<div class="admonition warning">

Warning

It is important that you do this in the <span class="pre">`yourplugin.urls`</span> module, otherwise pretix will not find your routes early enough during system startup.

</div>

</div>

</div>

</div>

</div>
