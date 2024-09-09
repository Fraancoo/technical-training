from odoo import models, fields


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