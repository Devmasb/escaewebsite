# -*- coding: utf-8 -*-
# from odoo import http


# class SalesContractProveedor(http.Controller):
#     @http.route('/sales_contract_proveedor/sales_contract_proveedor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_contract_proveedor/sales_contract_proveedor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_contract_proveedor.listing', {
#             'root': '/sales_contract_proveedor/sales_contract_proveedor',
#             'objects': http.request.env['sales_contract_proveedor.sales_contract_proveedor'].search([]),
#         })

#     @http.route('/sales_contract_proveedor/sales_contract_proveedor/objects/<model("sales_contract_proveedor.sales_contract_proveedor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_contract_proveedor.object', {
#             'object': obj
#         })
