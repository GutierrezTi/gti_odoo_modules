=========================================
GutierrezTi: Odoo 18.0 Financial Addons
=========================================

.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

.. image:: https://img.shields.io/badge/odoo-18.0-875A7B.svg
    :target: https://www.odoo.com/documentation/18.0
    :alt: Odoo 18.0

Este repositorio contiene módulos avanzados para Odoo 18.0 Community desarrollados por **GutierrezTi**, enfocados en la optimización de la gestión fiscal española, el cumplimiento normativo y la automatización contable para autónomos y PYMES.

Tabla de Contenidos de Módulos
==============================

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Módulo
     - Descripción Funcional
   * - `l10n_es_autonomo`
     - Gestión de deducibilidad parcial de IVA e IRPF (Gastos afectos).
   * - `account_irpf_audit`
     - Auditoría y conciliación de retenciones IRPF con datos de la AEAT.

Descripción de los Módulos
==========================

l10n_es_autonomo (Spanish Autonomo: Partial Deducibility)
---------------------------------------------------------
Este módulo resuelve la problemática contable de los activos y gastos parcialmente afectos a la actividad económica (como vehículos al 50% o suministros de vivienda).

* **Automatización Contable**: Ajusta dinámicamente las cuentas de IVA (472) y gasto (6xx) basándose en perfiles de deducción.
* **Inteligencia de Datos**: El sistema sugiere el perfil según el Proveedor o el Producto seleccionado.
* **Dashboard en Factura**: Incorpora un banner reactivo que muestra el impacto real en el Modelo 303 y el gasto neto deducible en IRPF antes de validar.
* **Auditoría**: Pestaña específica de "Ajuste Fiscal" para trazabilidad total del asiento de reclasificación.

account_irpf_audit (Auditoría y Conciliación de IRPF)
-----------------------------------------------------
Herramienta de control interno diseñada para garantizar la integridad de las retenciones frente a la Agencia Tributaria.

* **Conciliación AEAT**: Importación directa de archivos Excel de la AEAT (Modelo 190) para detectar discrepancias al céntimo por NIF.
* **Canal de Comunicación**: Envío automatizado de circulares informativas y alertas de discrepancia.
* **Portal del Cliente**: Integración con el portal de Odoo para que los clientes validen sus certificados de retenciones o informen de errores directamente al Chatter de la auditoría.
* **Flujo de Trabajo**: Estados de revisión (Borrador, Calculado, Notificado, Cuadrado) para una gestión profesional del cierre anual o trimestral.

Instalación
===========
1. Clone este repositorio en su ruta de `addons`.
2. Actualice la lista de aplicaciones en su instancia de Odoo 18.0.
3. Instale los módulos deseados (ambos requieren el módulo base `account`).

Créditos y Soporte
==================

**Autores e Ingeniería:**
* Joaquín Gutiérrez Pedrosa (GutierrezTi)
* Equipo Técnico GutierrezTi <info@gutierrezti.es>

Para reportar errores o solicitar mejoras, por favor abra un *Issue* en este repositorio o visite https://gutierrezti.es.