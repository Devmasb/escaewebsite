# -*- coding: utf-8 -*-
# from odoo import http


# class ProyectoPdt(http.Controller):
#     @http.route('/proyecto_pdt/proyecto_pdt', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proyecto_pdt/proyecto_pdt/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('proyecto_pdt.listing', {
#             'root': '/proyecto_pdt/proyecto_pdt',
#             'objects': http.request.env['proyecto_pdt.proyecto_pdt'].search([]),
#         })

#     @http.route('/proyecto_pdt/proyecto_pdt/objects/<model("proyecto_pdt.proyecto_pdt"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proyecto_pdt.object', {
#             'object': obj
#         })
