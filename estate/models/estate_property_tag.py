from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiquetas de las propiedades"
    _order = "sequence"
    
    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(string="Activo", default=True)
    sequence = fields.Integer(string="Orden", default=10)

    _sql_constraints = [
        ("name_unique", "unique(name)", "Ya existe una etiqueta con ese nombre"),
    ]
