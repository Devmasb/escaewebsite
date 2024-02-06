
from odoo import models, fields, api,_
from datetime import datetime
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
    description = fields.Char(string='Descripción')
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
     campo_agrupamiento = fields.Char(string='Efectividad')
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
    pdt_control = fields.Char(string='Producto o actividad a realizar')
    pdt_control_descripcionnorma = fields.Char(string='Descripción')
    pdt_categoria = fields.Char(string='PDT - Categoría')
    pdt_orden = fields.Integer(string="Control - Secuencia",default=1)
    m_madurez_id = fields.Many2one(string='Modelo de Madurez',related="pdt_id.m_madurez_id", store=True)
    fecha_diagnostico = fields.Datetime('Fecha de diagnóstico', default=fields.Datetime.now())
    fecha_final = fields.Datetime('Fecha final de implementación')
    task_proyect_pdt_id = fields.Many2one('project.task', string='Tarea Principal')
    task_pdt_controls = fields.One2many('project.task', 'task_proyect_pdt_id',
                                                  string='Controles')
    pdt_control_revisado = fields.Boolean(
        string="Control revisado",
        help="Visualiza si el control ha sido revisado ",
    )
    desfase = fields.Integer("Desviación de la actividad", compute="_compute_desfase",store=True, group_operator="avg")

    pdt_control_progreso = fields.Integer("Progreso Esperado",group_operator="avg")
    pdt_control_progreso_auxcalc = fields.Integer("Progreso Esperado", compute="_compute_avances_act")

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



    @api.depends("nivelefectividad", "autodiag_calificacion_actiual", "planned_date_end", "planned_date_begin")
    def _compute_avances(self):
        hoy = datetime.now()
        for reg in self:
            if (reg.nivelefectividad - reg.autodiag_calificacion_actiual) > 0:
                reg.niveldeavanceimplementacion = (reg.nivelefectividad - reg.autodiag_calificacion_actiual)*100/(100-reg.autodiag_calificacion_actiual)
            else:
                reg.niveldeavanceimplementacion = 100 if reg.nivelefectividad == 100 else 0
                reg.implementa_valoracionlist_id = reg.valoracionlist_id

            if    reg.planned_date_end and  reg.planned_date_begin:
                if (hoy <= reg.planned_date_end) and  (hoy >= reg.planned_date_begin):
                  duration = (reg.planned_date_end - reg.planned_date_begin).total_seconds() / 3600.0
                  reg.pdt_control_progreso = ((reg.planned_date_end - hoy).total_seconds() / 3600.0) / duration *100
                elif (hoy > reg.planned_date_end):
                    reg.pdt_control_progreso_auxcalc = 100
                else:
                    reg.pdt_control_progreso_auxcalc = 0


    def _compute_avances_act(self):
        hoy = datetime.now()
        for reg in self:
            if reg.planned_date_end and reg.planned_date_begin:
                if (hoy <= reg.planned_date_end) and (hoy >= reg.planned_date_begin):
                    duration = (reg.planned_date_end - reg.planned_date_begin).total_seconds() / 3600.0
                    reg.pdt_control_progreso = ((reg.planned_date_end - hoy).total_seconds() / 3600.0) / duration * 100
                elif (hoy > reg.planned_date_end):
                    reg.pdt_control_progreso_auxcalc = 100
                else:
                    reg.pdt_control_progreso_auxcalc = 0
            reg.write({
                'pdt_control_progreso': reg.pdt_control_progreso_auxcalc,
            })

    @api.depends("planned_date_end", "planned_date_begin", "date_deadline")
    def _compute_desfase(self):
        for reg in self:
            if reg.planned_date_end and reg.planned_date_begin and reg.fecha_final:
                hoy = reg.fecha_final
                if (hoy <= reg.planned_date_end) and (hoy >= reg.planned_date_begin):
                    duration = (reg.planned_date_end - reg.planned_date_begin).total_seconds() / 3600.0
                    reg.desfase =(((hoy-reg.planned_date_begin  ).total_seconds() / 3600.0) / duration * 100)
                elif (hoy > reg.planned_date_end):
                    reg.desfase = 100
                else:
                    reg.desfase = 0
            else:
                reg.desfase = 100




class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project']

    pdt_count = fields.Integer(compute='_compute_pdt_count', string="PDT en Proyecto")
    pdt_ids = fields.One2many('proyecto_pdt', 'project_id',
                                   string='PDT del proyecto')

    def _compute_pdt_count(self):
        for reg in self:
            reg.pdt_count = len(reg.pdt_ids)


