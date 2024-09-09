from odoo import models, fields, api
from datetime import timedelta


GARDEN_ORIENTATION_OPTS = [
    ("north", "Norte"),
    ("south", "Sur"),
    ("east", "Este"),
    ("west", "Oeste"),
]

STATE_OPTS = [
    ("new", "Nuevo"),
    ("offer_received", "Oferta recibida"),
    ("offer_accepted", "Oferta aceptada"),
    ("sold", "Vendido"),
    ("cancel", "Cancelado"),
]


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Modelo para ver las propiedades"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código postal")
    date_availability = fields.Date(string="Disponibilidad", copy=True, default=lambda self: self._default_date_availability())
    expected_price = fields.Float(string="Precio deseado", required=True)
    selling_price = fields.Float(string="Precio de venta", readonly=True, copy=True)
    bedrooms = fields.Integer(string="Cuartos", default=2)
    living_area = fields.Integer(string="Salas")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Parqueadero")
    garden = fields.Boolean(string="Jardín")
    garden_area = fields.Integer(string="Area del jardín (m2)")
    garden_orientation = fields.Selection(
        string="Orientación del jardín",
        selection=GARDEN_ORIENTATION_OPTS
    )
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection(string="Estado", selection=STATE_OPTS, required=True, copy=False, default='new')

    @api.model
    def _default_date_availability(self):
        return fields.Date.today() + timedelta(days=90)
