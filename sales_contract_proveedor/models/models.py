# -*- coding: utf-8 -*-

from odoo import models, fields, api

# ---------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------
class sales_contract_proveedor(models.Model):
     _name = 'sales_contract_proveedor'
     _description = 'sales_contract_proveedor'
     _order = 'fecha_inicio desc, id desc'

     name = fields.Char(string='Registro', required=True, copy=False, readonly=True, index=True,
                        default=lambda self: self.newvalue())
     cod_clasificador = fields.Char(string='Código del clasificador de bienes y servicios de las Naciones Unidas')
     obj_contract = fields.Char(string='Objeto del contrato')

     fecha_inicio = fields.Date(string='Fecha de inicio')
     fecha_final = fields.Date(string='Fecha de terminación')
     float_valor = fields.Float('Valor')
     contacto = fields.Char(string='Datos de contacto del área de la Entidad Estatal encargada del supervisión del contrato')
     contratante = fields.Char( string='Contratante (sector público o privado)')
     contratista = fields.Char(string='Contratista (singular o plural)')

     cotizacion = fields.Many2one('sale.order', ondelete="cascade")


#     @api.model
#    def create(self, vals):
#          if vals.get('name', 'New') == 'New':
#               vals['name'] = self.env['ir.sequence'].next_by_code(
#                    'listacontrato.sequence') or 'New'
#          result = super(sales_contract_proveedor, self).create(vals)
#          return result

     def newvalue(self):
          result = self.env['ir.sequence'].next_by_code(
                    'listacontrato.sequence') or 'New'
          return result

# ---------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------



class SaleOrder(models.Model):
    _inherit = "sale.order"

    listacontrato = fields.One2many('sales_contract_proveedor', 'cotizacion', 'Contrato',ondelete="cascade")
    obj_contract = fields.Char(string='Objeto del contrato')
    cod_clasificador = fields.Char(string='Código del clasificador de bienes y servicios de las Naciones Unidas')
    contacto = fields.Char(string='Datos de contacto del área de la Entidad Estatal encargada del supervisión del contrato')
    has_active_listacontrato = fields.Boolean('Esta habilitado?', compute='_compute_has_active_listacontrato')

    @api.depends('listacontrato')
    def _compute_has_active_listacontrato(self):
        self.has_active_listacontrato = self.env['sales_contract_proveedor'].search_count([('cotizacion', '=', self.id)]) > 0



    def crearlistcontrato(self):
        self.env['sales_contract_proveedor'].create({
            'fecha_inicio': self.date_order,
            'float_valor': self.amount_total,
            'obj_contract': self.obj_contract,
            'cod_clasificador': self.cod_clasificador,
            'contratante': self.partner_id.name,
            'cotizacion': self.id,
            'contacto': self.contacto
        })

