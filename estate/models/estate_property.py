from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


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
    living_area = fields.Integer(string="Area de la sala (m2)")
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
    tag_ids = fields.Many2many(string='Etiquetas', comodel_name='estate.property.tag')
    offer_ids = fields.One2many(string='Ofertas', comodel_name='estate.property.offer', inverse_name='property_id')
    total_area = fields.Float(string='Área total (m2)', compute='_compute_total_area', readonly=True)
    best_price = fields.Float(string='Mejor precio', compute='_compute_best_price', readonly=True)
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids):
                best_price = max(record.offer_ids.mapped('price'))
            else:
                best_price = 0
            record.best_price = best_price