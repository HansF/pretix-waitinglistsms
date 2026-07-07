---
title: "Plugin development"
source: "https://docs.pretix.eu/dev/development/api/index.html"
source_type: "pretix docs"
retrieved: "2026-07-07"
---

> Source: [https://docs.pretix.eu/dev/development/api/index.html](https://docs.pretix.eu/dev/development/api/index.html)

<div id="plugin-development" class="section">

# Plugin development

Contents:

<div class="toctree-wrapper compound">

- <a href="plugins.md" class="reference internal">Creating a plugin</a>
  - <a href="plugins.md#plugin-metadata" class="reference internal">Plugin metadata</a>
  - <a href="plugins.md#plugin-registration" class="reference internal">Plugin registration</a>
  - <a href="plugins.md#signals" class="reference internal">Signals</a>
  - <a href="plugins.md#registries" class="reference internal">Registries</a>
  - <a href="plugins.md#views" class="reference internal">Views</a>
- <a href="exporter.md" class="reference internal">Writing an exporter plugin</a>
  - <a href="exporter.md#exporter-registration" class="reference internal">Exporter registration</a>
  - <a href="exporter.md#the-exporter-class" class="reference internal">The exporter class</a>
- <a href="ticketoutput.md" class="reference internal">Writing a ticket output plugin</a>
  - <a href="ticketoutput.md#output-registration" class="reference internal">Output registration</a>
  - <a href="ticketoutput.md#the-output-class" class="reference internal">The output class</a>
- <a href="payment.md" class="reference internal">Writing a payment provider plugin</a>
  - <a href="payment.md#provider-registration" class="reference internal">Provider registration</a>
  - <a href="payment.md#the-provider-class" class="reference internal">The provider class</a>
  - <a href="payment.md#additional-views" class="reference internal">Additional views</a>
- <a href="email.md" class="reference internal">Writing an HTML e-mail renderer plugin</a>
  - <a href="email.md#output-registration" class="reference internal">Output registration</a>
  - <a href="email.md#the-renderer-class" class="reference internal">The renderer class</a>
  - <a href="email.md#helper-class-for-template-base-renderers" class="reference internal">Helper class for template-base renderers</a>
- <a href="placeholder.md" class="reference internal">Writing a template placeholder plugin</a>
  - <a href="placeholder.md#placeholder-registration" class="reference internal">Placeholder registration</a>
  - <a href="placeholder.md#context-mechanism" class="reference internal">Context mechanism</a>
  - <a href="placeholder.md#the-placeholder-class" class="reference internal">The placeholder class</a>
  - <a href="placeholder.md#helper-class-for-simple-placeholders" class="reference internal">Helper class for simple placeholders</a>
  - <a href="placeholder.md#signals" class="reference internal">Signals</a>
- <a href="invoice.md" class="reference internal">Writing an invoice renderer plugin</a>
  - <a href="invoice.md#output-registration" class="reference internal">Output registration</a>
  - <a href="invoice.md#the-renderer-class" class="reference internal">The renderer class</a>
  - <a href="invoice.md#helper-class-for-reportlab-base-renderers" class="reference internal">Helper class for reportlab-base renderers</a>
- <a href="invoicetransmission.md" class="reference internal">Writing an invoice transmission plugin</a>
  - <a href="invoicetransmission.md#output-registration" class="reference internal">Output registration</a>
  - <a href="invoicetransmission.md#the-provider-class" class="reference internal">The provider class</a>
- <a href="shredder.md" class="reference internal">Writing a data shredder</a>
  - <a href="shredder.md#shredder-registration" class="reference internal">Shredder registration</a>
  - <a href="shredder.md#the-shredder-class" class="reference internal">The shredder class</a>
  - <a href="shredder.md#example" class="reference internal">Example</a>
- <a href="import.md" class="reference internal">Extending the import process</a>
  - <a href="import.md#import-process" class="reference internal">Import process</a>
  - <a href="import.md#column-registration" class="reference internal">Column registration</a>
  - <a href="import.md#the-column-class-api" class="reference internal">The column class API</a>
  - <a href="import.md#example" class="reference internal">Example</a>
- <a href="customview.md" class="reference internal">Creating custom views</a>
  - <a href="customview.md#control-panel-views" class="reference internal">Control panel views</a>
  - <a href="customview.md#event-settings-view" class="reference internal">Event settings view</a>
  - <a href="customview.md#frontend-views" class="reference internal">Frontend views</a>
  - <a href="customview.md#rest-api-viewsets" class="reference internal">REST API viewsets</a>
- <a href="cookieconsent.md" class="reference internal">Handling cookie consent</a>
  - <a href="cookieconsent.md#server-side-integration" class="reference internal">Server-side integration</a>
  - <a href="cookieconsent.md#javascript-side-integration" class="reference internal">JavaScript-side integration</a>
- <a href="auth.md" class="reference internal">Pluggable authentication backends</a>
  - <a href="auth.md#pretix.base.models.auth.UserManager" class="reference internal"><span class="pre"><code class="docutils literal notranslate">UserManager</code></span></a>
  - <a href="auth.md#the-backend-interface" class="reference internal">The backend interface</a>
  - <a href="auth.md#logging-users-in" class="reference internal">Logging users in</a>
- <a href="datasync.md" class="reference internal">Data sync providers</a>
  - <a href="datasync.md#property-mappings" class="reference internal">Property mappings</a>
  - <a href="datasync.md#implementation-examples" class="reference internal">Implementation examples</a>
  - <a href="datasync.md#the-outboundsyncprovider-base-class" class="reference internal">The OutboundSyncProvider base class</a>
  - <a href="datasync.md#property-mapping-format" class="reference internal">Property mapping format</a>
  - <a href="datasync.md#translating-mappings-on-event-copy" class="reference internal">Translating mappings on Event copy</a>
- <a href="general.md" class="reference internal">General APIs</a>
  - <a href="general.md#module-pretix.base.signals" class="reference internal">Core</a>
  - <a href="general.md#module-pretix.presale.signals" class="reference internal">Frontend</a>
  - <a href="general.md#module-pretix.control.signals" class="reference internal">Backend</a>
  - <a href="general.md#api" class="reference internal">API</a>
- <a href="quality.md" class="reference internal">Plugin quality checklist</a>
  - <a href="quality.md#a-meta" class="reference internal">A. Meta</a>
  - <a href="quality.md#b-isolation" class="reference internal">B. Isolation</a>
  - <a href="quality.md#c-security" class="reference internal">C. Security</a>
  - <a href="quality.md#d-privacy" class="reference internal">D. Privacy</a>
  - <a href="quality.md#e-internationalization" class="reference internal">E. Internationalization</a>
  - <a href="quality.md#f-functionality" class="reference internal">F. Functionality</a>
  - <a href="quality.md#g-code-quality" class="reference internal">G. Code quality</a>
  - <a href="quality.md#h-specific-to-pretix-eu" class="reference internal">H. Specific to pretix.eu</a>

</div>

</div>
