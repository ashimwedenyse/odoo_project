from odoo import fields,models
class EstateMixin(models.AbstractModel):
    _name = "estate.mixin"

    name=fields.Char(required=True)