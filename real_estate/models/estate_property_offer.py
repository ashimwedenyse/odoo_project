from odoo import fields, models

class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made for real estate"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade"
    )
