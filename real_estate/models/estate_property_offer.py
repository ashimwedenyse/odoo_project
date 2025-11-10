from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made for real estate"
    _order = "price desc"

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

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
                offer.validity = (offer.date_deadline - base_date).days

    @api.model
    def create(self, vals):
        offer = super().create(vals)
        if offer.property_id and offer.property_id.state == 'new':
            offer.property_id.state = 'offer_received'  # FIXED: Changed from 'received' to 'offer_received'
        return offer

    def write(self, vals):
        """Override write to automatically update property state when offer status changes"""
        res = super().write(vals)

        if 'status' in vals:
            for offer in self:
                if offer.status == 'accepted':
                    offer.property_id.write({
                        'state': 'offer_accepted',
                        'selling_price': offer.price,
                        'best_offer': offer.price,
                    })
                elif offer.status == 'refused':
                    # FIXED: Corrected typo 'acceptedd' to 'accepted'
                    accepted_offers = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
                    if not accepted_offers:
                        offer.property_id.write({
                            'state': 'cancelled',
                            'selling_price': 0,
                        })
        return res

    def action_accept(self):
        self.ensure_one()
        accepted_offers = self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != self.id)
        if accepted_offers:
            raise UserError(_("An offer has already been accepted for this property."))

        other_offers = self.property_id.offer_ids.filtered(lambda o: o.id != self.id)
        other_offers.write({'status': 'refused'})
        self.status = 'accepted'
        return True

    def action_refuse(self):
        self.ensure_one()
        self.status = 'refused'
        return True