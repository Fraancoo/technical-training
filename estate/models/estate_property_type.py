from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Modelo para ver los tipos de propiedades"
    _order = "name"
    
    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(string='Activo', default=True)
    property_ids = fields.One2many(string="Propiedades", comodel_name="estate.property", inverse_name="property_type_id")

    _sql_constraints = [
        ("name_unique", "unique(name)", "Ya existe un tipo de propiedad con ese nombre"),
    ]