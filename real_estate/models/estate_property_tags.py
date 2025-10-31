from odoo import fields, models
class PropertyTags(models.Model):
    _name="estate.property.tags"
    _description="tag of  real estate model"

    name =fields.Char(required=True)