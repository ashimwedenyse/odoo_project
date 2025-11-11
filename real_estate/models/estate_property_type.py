from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of Real Estate Property"
    _inherit = "estate.mixin"

    # -----------------------
    # General Fields
    # -----------------------
    name = fields.Char(string='Name', required=True)
    property_model = fields.Char(string='Model / Version')  # renamed from 'model'
    category = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('vehicle', 'Vehicle'),
        ('land', 'Land'),
    ], string='Category')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color Index')


    # -----------------------
    # House / Land Specific Fields
    # -----------------------
    area = fields.Float(string='Area (m²)')
    number_of_rooms = fields.Integer(string='Number of Rooms')
    number_of_bathrooms = fields.Integer(string='Number of Bathrooms')
    number_of_floors = fields.Integer(string='Number of Floors')
    garden = fields.Boolean(string='Garden')
    garage = fields.Boolean(string='Garage')
    year_built = fields.Integer(string='Year Built')
    location = fields.Char(string='Location')

    # -----------------------
    # Vehicle Specific Fields
    # -----------------------
    make = fields.Char(string='Make')  # e.g., Toyota, Ford
    vehicle_model = fields.Char(string='Vehicle Model')  # renamed from 'model'
    year = fields.Integer(string='Year')
    engine_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], string='Engine Type')
    transmission = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ], string='Transmission')
    car_color = fields.Char(string='Color')
    mileage = fields.Float(string='Mileage')
    seats = fields.Integer(string='Seats')
    fuel_capacity = fields.Float(string='Fuel Capacity')
