from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # Basic fields
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today())

    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id
                                  )
    expected_price = fields.Monetary(required=True, currency_field='currency_id')
    selling_price = fields.Monetary(copy=False, readonly=True, currency_field='currency_id')

    description = fields.Text()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
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

    # Computed fields
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")


    #   COMPUTED METHODS

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # ------------------------
    #   ONCHANGE & CONSTRAINTS
    # ------------------------
    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0

    @api.constrains("date_availability")
    def _check_date_availability(self):
        for record in self:
            if record.date_availability and record.date_availability < fields.Date.today():
                raise ValidationError(_("The availability date cannot be in the past."))

    @api.constrains("state")
    def _check_offer_state(self):
        for record in self:
            if record.state == "cancelled" and "accepted" in record.offer_ids.mapped("status"):
                raise ValidationError(_("Cannot cancel a property with an accepted offer!"))

    @api.constrains("offer_ids")
    def _check_has_offers(self):
        """Ensure property has at least one offer before saving"""
        for record in self:
            if not record.offer_ids:
                raise ValidationError(_("Cannot save property without at least one offer!"))


    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise ValidationError(_("Canceled properties cannot be sold!"))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise ValidationError(_("Sold properties cannot be canceled!"))
            record.state = "cancelled"
        return True

    def action_view_offers(self):
        """Open related offers for this property"""
        self.ensure_one()
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }