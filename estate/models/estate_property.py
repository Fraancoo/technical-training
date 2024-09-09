from odoo import models, fields


GARDEN_ORIENTATION_OPTS = [
    ("north", "Norte"),
    ("south", "Sur"),
    ("east", "Este"),
    ("west", "Oeste"),
]


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Modelo para ver las propiedades"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código postal")
    date_availability = fields.Date(string="Disponibilidad")
    expected_price = fields.Float(string="Precio deseado", required=True)
    selling_price = fields.Float(string="Precio de venta")
    bedrooms = fields.Integer(string="Cuartos")
    living_area = fields.Integer(string="Salas")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Parqueadero")
    garden = fields.Boolean(string="Jardín")
    garden_area = fields.Integer(string="Area del jardín (m2)")
    garden_orientation = fields.Selection(
        string="Orientación del jardín",
        selection=GARDEN_ORIENTATION_OPTS
    )
