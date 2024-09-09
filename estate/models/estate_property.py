from odoo import models, fields


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
    date_availability = fields.Date(string="Disponibilidad", copy=True, default=fields.Date.add(fields.Date.today(), months=3))
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
    property_type_id = fields.Many2one(string="Tipo", comodel_name="estate.property.type")
    partner_id = fields.Many2one(string="Comprador", comodel_name="res.partner", copy=False)
    user_id = fields.Many2one(string="Vendedor", comodel_name="res.users", default=lambda self: self.env.user)
