from odoo import fields, models


class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Tags for real estate properties"
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name should be unique")
    ]
    _inherit = "estate.mixin"
    color = fields.Integer()
    _order = "name desc"