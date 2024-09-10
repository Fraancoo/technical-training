from odoo import models, fields, api
from odoo.exceptions import UserError


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

    def action_refuse_offer(self):
        for record in self:
            if record.state == "accepted":
                raise UserError('Las ofertas aceptadas no pueden ser rechazadas')
            record.state = "refused"
        return True

    def action_accept_offer(self):
        for record in self:
            if record.state == "refused":
                raise UserError('Las ofertas rechazadas no pueden ser aceptadas')
            another_accepted_offer = self.env['estate.property.offer'].search([
                ('state', '=', 'accepted'),
                ('property_id.id', '=', record.property_id.id),
            ], limit=1)
            if another_accepted_offer:
                raise UserError('Ya existe una oferta aceptada para esta propiedad')
            record.state = "accepted"
            record.property_id.partner_id = record.partner_id
            record.selling_price = record.price
        return True