from odoo import models, fields, api


STATE_OPTS = [
    ("accepted", "Aceptada"),
    ("refused", "Rechazada"),
]


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Ofertas de las propiedades'
    
    price = fields.Float(string='Precio', required=True)
    state = fields.Selection(string='Estatus', selection=STATE_OPTS, copy=False)
    partner_id = fields.Many2one(string='Partner', comodel_name='res.partner', required=True)
    property_id = fields.Many2one(string='Propiedad', comodel_name='estate.property', required=True)
    validity = fields.Integer(string='Validación', required=True, default=7)
    date_deadline = fields.Date(string='Fecha límite', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            resp_date = record.date_deadline - fields.Date.today()
            record.validity = resp_date.days