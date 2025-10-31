from odoo import models, fields, api  # ✅ added api import for future computed/inverse methods

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # Basic fields
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today())

    expected_price = fields.Float(required=True)
    best_offer = fields.Float(readonly=True)
    selling_price = fields.Float(copy=False)

    description = fields.Text()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True,
        ondelete="restrict",
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    tag_ids = fields.Many2many(
        "estate.property.tags",
        string="Tags",
    )
