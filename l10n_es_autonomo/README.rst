======================================================
Spanish Autonomo: Partial Deducibility Management
======================================================

.. ![](/static/description/icon.png)

.. |badge1| image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

|badge1|

Este módulo permite gestionar la deducibilidad parcial del IVA y del Gasto (IRPF) para autónomos en España,
especialmente útil para bienes afectos parcialmente a la actividad económica (como vehículos al 50% o suministros del hogar al 30%).

Installation
============

Para instalar este módulo, simplemente descárguelo o clónelo en su directorio de *addons* y proceda a instalarlo
desde el menú de Aplicaciones de Odoo. Requiere el módulo base de Contabilidad (`account`).

Configuration
=============

1. **Perfiles de Deducción**: Vaya a *Contabilidad > Configuración > Autónomo > Perfiles de Deducción* y cree los perfiles necesarios (ej. Vehículos 50%).
2. **Productos**: En la ficha del producto, pestaña *Compra*, marque "Deducibilidad Parcial" y asigne un perfil.
3. **Proveedores**: En la ficha del contacto, pestaña *Venta y Compra*, puede asignar un perfil por defecto para todas las facturas de ese proveedor.

Usage
=====

Instrucciones de uso en español:
-------------------------------

1. **Configuración del Perfil**:
   Defina el porcentaje de IVA que legalmente puede deducirse. Por ejemplo, para un coche afecto a la actividad,
   cree un perfil con el 50% de IVA deducible. Elija la estrategia "Añadir a la línea base" para que el
   IVA no deducible se sume automáticamente como mayor valor del gasto.

2. **Automatización en Facturas**:
   Al crear una factura de proveedor, el sistema buscará automáticamente el perfil de deducción.
   Primero mirará si el **Proveedor** tiene uno asignado; si no, mirará si el **Producto** lo tiene.
   Usted siempre podrá cambiarlo manualmente en la línea de la factura si fuera necesario.

3. **Resumen Fiscal (Banner)**:
   Antes de confirmar la factura, verá un banner informativo de color azul en la parte superior. Este banner
   le mostrará en tiempo real:
   * **IVA Deducible**: El importe exacto que recuperará en el Modelo 303.
   * **Gasto Neto (IRPF)**: El importe total que podrá desgravarse como gasto (Base + IVA no deducible).

4. **Confirmación y Auditoría**:
   Al hacer clic en "Confirmar", Odoo realizará los ajustes contables automáticamente:
   * Reducirá la cuota de IVA en la cuenta 472.
   * Aumentará el valor en la cuenta de gasto (6xx) o activo (2xx).
   * Podrá verificar todo el desglose en la pestaña **"Ajuste Fiscal"** dentro de la propia factura.

5. **Informes Oficiales**:
   El sistema está diseñado para que el **Modelo 303** y el **Libro de Registro de IVA** tomen solo la parte
   deducible, mientras que el informe de **Pérdidas y Ganancias** refleje el gasto real incrementado.

Credits
=======

Authors
-------

* GutierrezTi

Contributors
------------

* GutierrezTi Team <info@gutierrezti.es>

Maintainer
----------

Este módulo es mantenido por GutierrezTi.

Para más información, visita https://gutierrezti.es
