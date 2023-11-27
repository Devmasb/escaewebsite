
from odoo import models, fields, api,_

class ModeloMadurez(models.Model):
    _name = 'modelomadurez'


    name = fields.Char(string='Nombre', required=True)
    valoracionlist_ids = fields.One2many('task.valoracionlist', 'm_madurez_id',
                                   string='Niveles de Madurez')

    description = fields.Html(string='Descripción detallada')
    descriptioncorta = fields.Html(string='Descripción Breve')

class TaskPdtvaloracionList(models.Model):
    _name = 'task.valoracionlist'

    name = fields.Char(string='Nombre', required=True)
    m_madurez_id = fields.Many2one('modelomadurez', string='Modelo de Madurez')
    description = fields.Char(string='Description')
    tasklist_ids = fields.One2many('project.task', 'valoracionlist_id',
                                    string='CheckList Items')
    description = fields.Char(string='Descripción', required=True)
    significado = fields.Char(string='Significado', required=True)
    nivelefectividad = fields.Integer(string='Efectividad', required=True , group_operator="avg")




class Proyecto_PDT(models.Model):
     _name = 'proyecto_pdt'
     _description = 'proyecto_pdt'

     name = fields.Char(string='Nombre', required=True)
     description = fields.Char(string='Descripción', required=True)
     project_id = fields.Many2one('project.project', string='Proyecto')
     pdt_task_ids = fields.One2many('project.task', 'pdt_id',
                                     string='Tareas del PDT')
     campo_agrupamiento = fields.Char(string='Efectividad', required=True)
     m_madurez_id = fields.Many2one('modelomadurez', string='Modelo de Madurez')


     def action_open_pdt_task(self):
         return {
             'name': _('PDT Tareas'),
             'view_mode': 'tree',
             'res_model': 'project.task',
             'type': 'ir.actions.act_window',
             'context': self._context,
             'view_mode':'gantt'
         }


class Task_Proyecto_PDT(models.Model):
    _inherit = 'project.task'
    _order = 'pdt_orden asc'

    pdt_id = fields.Many2one('proyecto_pdt')
    pdt_componente = fields.Char(string='Componente')
    pdt_numeral = fields.Char(string='Numeral')
    pdt_control = fields.Char(string='Producto')
    pdt_control_descripcionnorma = fields.Char(string='Descripción')
    pdt_categoria = fields.Char(string='PDT - Categoría')
    pdt_orden = fields.Integer(string="Control - Secuencia",default=1)
    m_madurez_id = fields.Many2one(string='Modelo de Madurez',related="pdt_id.m_madurez_id", store=True)
    fecha_diagnostico = fields.Datetime('Fecha de diagnóstico', default=fields.Datetime.now())


    #DIAGNOSTICO******************************************************************************
    valoracionlist_id = fields.Many2one('task.valoracionlist', string='Madurez Inicial', domain="[('m_madurez_id','=',m_madurez_id)]")
    autodiag_calificacion_actiual = fields.Integer("Evaluación de Diagnóstico",
                                                   related="valoracionlist_id.nivelefectividad", store=True,
                                                   group_operator="avg")
    pdt_observaciones = fields.Html("Observaciones en Etapa diagnóstico")

    #IMPLEMENTACION ***************************************************************************
    implementa_valoracionlist_id = fields.Many2one('task.valoracionlist', string='Madurez Actual', domain="[('m_madurez_id','=',m_madurez_id)]")
    nivelefectividad = fields.Integer("Calificación actual del requisito", related="implementa_valoracionlist_id.nivelefectividad",
                                      store=True, group_operator="avg")
    pdt_observaciones_implementa = fields.Html("Observaciones en Etapa Implementación")
    niveldeavanceimplementacion = fields.Integer("Nivel de avance", compute="_compute_avances", store=True ,group_operator="avg")



    @api.depends("nivelefectividad", "autodiag_calificacion_actiual")
    def _compute_avances(self):
        for reg in self:
            if (reg.nivelefectividad - reg.autodiag_calificacion_actiual) > 0:
                reg.niveldeavanceimplementacion = (reg.nivelefectividad - reg.autodiag_calificacion_actiual)*100/(100-reg.autodiag_calificacion_actiual)
            else:
                reg.niveldeavanceimplementacion = 100 if reg.nivelefectividad == 100 else 0
                reg.implementa_valoracionlist_id = reg.valoracionlist_id


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project']

    pdt_count = fields.Integer(compute='_compute_pdt_count', string="PDT en Proyecto")
    pdt_ids = fields.One2many('proyecto_pdt', 'project_id',
                                   string='PDT del proyecto')

    def _compute_pdt_count(self):
        for reg in self:
            reg.pdt_count = len(reg.pdt_ids)


