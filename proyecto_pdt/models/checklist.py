
from odoo import models, fields, api, _


class TaskChecklistpdt(models.Model):
    _name = 'task.checklistpdt'

    name = fields.Char(string='Name')
    description = fields.Char(string='Descripción')
    project_id = fields.Many2one('proyecto_pdt', string='PDT')
    task_ids = fields.Many2one('project.task', string='Tarea de PDT')

    checklist_ids = fields.One2many('pdtchecklist.item', 'checklist_id',
                                    string='CheckList Items', required=True)


class ChecklistItem(models.Model):
    _name = 'pdtchecklist.item'
    _description = 'Checklist Item'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    description = fields.Char()
    projects_id = fields.Many2one('project.task')
    checklist_id = fields.Many2one('task.checklistpdt')
    state = fields.Selection(
        string='Estado', required=True, readonly=True, copy=False,
        tracking=True, selection=[
            ('todo', 'Por hacer'),
            ('in_progress', 'En progreso'),
            ('done', 'Realizado'),
            ('cancel', 'Cancelado'),
        ], default='todo', )

    def approve_and_next(self):
        self.state = 'in_progress'

    def mark_completed(self):
        self.state = 'done'

    def mark_canceled(self):
        self.state = 'cancel'

    def reset_stage(self):
        self.state = 'todo'


class ChecklistProgress(models.Model):
    _inherit = 'project.task'

    checkstart_date = fields.Datetime(string='Start Date')
    checkend_date = fields.Datetime(string='End Date')
    checkprogress = fields.Float(compute='_compute_progress', string='Progress in %')
    checkchecklist_id = fields.Many2one('task.checklistpdt', string='Checklist')
    checkchecklists = fields.One2many('pdtchecklist.item', 'projects_id',
                                 string='CheckList Items', required=True)

    @api.onchange('checkchecklist_id')
    def _onchange_project_id(self):
        self.checkchecklists = []
        checklist = self.env['task.checklistpdt'].search(
            [('name', '=', self.checkchecklist_id.name)])
        for rec in checklist:
            self.checkchecklists += rec.checklist_ids

    def _compute_progress(self):
        for rec in self:
            total_completed = 0
            for activity in rec.checkchecklists:
                if activity.state in ['cancel', 'done', 'in_progress']:
                    total_completed += 1
            if total_completed:
                rec.checkprogress = float(total_completed) / len(
                    rec.checkchecklists) * 100
            else:
                rec.checkprogress = 0.0
