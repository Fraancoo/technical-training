from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Modelo para ver los tipos de propiedades"
    _order = "sequence"
    
    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(string='Activo', default=True)
    sequence = fields.Integer(string='Orden', default=10)
    property_ids = fields.One2many(string="Propiedades", comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(string='Ofertas', comodel_name='estate.property.offer', inverse_name='property_type_id')
    offer_count = fields.Integer(string='# de ofertas', compute='_compute_offer_count')

    _sql_constraints = [
        ("name_unique", "unique(name)", "Ya existe un tipo de propiedad con ese nombre"),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)