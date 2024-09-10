from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


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
    _order = "id desc"

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

    _sql_constraints = [
        ("expected_price_check", "check(expected_price > 0)", "El precio deseado debe ser mayor a 0"),
    ]

    @api.constrains('expected_price', 'selling_price', 'state')
    def _constrains_selling_price_check(self):
        for record in self:
            if record.state == 'sold':
                if float_is_zero(record.selling_price, precision_digits=1):
                    raise ValidationError("El precio de venta es inválido")
                expected_price_90 = record.expected_price / 100 * 90
                if float_compare(record.selling_price, expected_price_90, precision_digits=1) < 0:
                    raise ValidationError("El precio de venta debe ser al menos el 90%% del precio deseado")
    
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

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        offers_exist = len(self.offer_ids)
        if offers_exist and self.state == 'new':
            self.state = 'offer_received'
        elif not offers_exist and (self.state == 'offer_received' or self.state == 'offer_accepted'):
            self.state = 'new'

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError('Las propiedades vendidas no pueden ser canceladas')
            record.state = "cancel"
        return True

    def action_sell_property(self):
        for record in self:
            if record.state == "cancel":
                raise UserError('Las propiedades canceladas no pueden ser vendidas')
            record.state = "sold"
        return True