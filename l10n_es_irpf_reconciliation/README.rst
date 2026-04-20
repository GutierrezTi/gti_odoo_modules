====================================
Auditoría y Conciliación de IRPF
====================================

.. |badge1| image:: https://img.shields.io/badge/GutierezTI-2026-7349FB
   :target: https://gutierrezti.es
   :alt: gutierrezti: resources

.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-ffba00
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

.. |badge3| image:: https://img.shields.io/badge/odoo-18.0-31013F
   :target: https://github.com/OCA/OCB/tree/18.0
   :alt: Odoo: 18.0

|badge1| |badge2| |badge3|


Este módulo permite a las empresas realizar una auditoría exhaustiva de las retenciones de IRPF comparando los registros contables de Odoo con los datos oficiales proporcionados por la Agencia Tributaria (AEAT).

Facilita la detección de discrepancias y proporciona un canal de comunicación directo y automatizado con los clientes a través de un portal web dedicado y correos electrónicos.

**Índice de contenidos**

.. contents::
   :local:

Configuración
=============

1. **Cuentas Contables**: Asegúrate de que tus cuentas de retención de IRPF (generalmente las que empiezan por la raíz 473) estén configuradas correctamente en Odoo.
2. **Plantillas de Correo**: El módulo incluye dos plantillas predeterminadas. Puedes revisarlas y ajustarlas desde
   ``Ajustes > Técnico > Correo electrónico > Plantillas``:

   * IRPF Audit: Quarterly Information Circular (Circular informativa trimestral).
   * IRPF Audit: Annual Discrepancy Alert (Alerta de discrepancia anual).

3. **URL Externa**: Asegúrate de que el parámetro del sistema ``web.base.url`` esté configurado correctamente con tu dominio para que los enlaces al portal que se envían por correo funcionen.

Uso
===

**Crear una Auditoría**

1. Ve a ``Facturación > Informes > Auditoría IRPF``.
2. Crea un nuevo registro, selecciona el **Ejercicio Fiscal** y el **Periodo** (1T, 2T, 3T, 4T o Anual).
3. Haz clic en **Calcular Auditoría**. Odoo buscará todos los apuntes contables en las cuentas ``473*`` para el periodo seleccionado.

**Importación de Datos de la AEAT (Solo Anual)**

1. Si el periodo seleccionado es **Anual (Modelo 190)**, aparecerá el botón **Importar Datos AEAT**.
2. Sube el archivo Excel exportado desde el portal de la Agencia Tributaria (Datos Fiscales).
3. El sistema emparejará automáticamente los importes buscando por el NIF de cada cliente y calculará las diferencias al céntimo.

**Comunicación con los Clientes**

1. Haz clic en **Notificar Clientes** para enviar los correos automáticos a todos los contactos de la lista.
2. Cada cliente recibirá un informe en PDF adjunto con el desglose de sus facturas y un enlace seguro al portal.
3. **Portal del Cliente**: A través del enlace privado, el cliente podrá:

   * **Dar su conformidad**: El estado de la línea cambia a "Cuadrado".
   * **Informar de un error**: El cliente debe indicar un motivo (ej. falta una factura). Esta respuesta se registrará automáticamente en el historial (Chatter) de la línea para que el contable lo revise.

**Revisión de Detalles y Resolución**

* Usa el **Smart Button "Facturas"** dentro de cada línea de auditoría para ir directamente a los apuntes contables de ese cliente e investigar rápidamente las diferencias.
* Haz clic en **Imprimir Informe** en cualquier línea para descargar su PDF detallado de forma manual.
* Usa el botón **Restablecer a Borrador** en la cabecera si necesitas limpiar los cálculos y volver a empezar la auditoría.

Próximos desarrollos
====================

* Integración nativa con el Modelo 111.
* Soporte para retenciones aplicadas en facturas con divisa extranjera.

Soporte y Errores
=================

Para reportar incidencias, sugerir mejoras o solicitar soporte sobre este módulo, por favor contacta directamente a través de los canales de soporte de GutierrezTi.

Créditos
========

Autores
~~~~~~~

* Joaquín Gutiérrez Pedrosa

Mantenedores
~~~~~~~~~~~~

Este módulo es desarrollado y mantenido por Joaquín Gutiérrez Pedrosa (GutierrezTi).

Para más información, visita https://gutierrezti.es.
