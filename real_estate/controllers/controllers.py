from odoo import http
import json


class RealEstateController(http.Controller):

    @http.route('/real_estate/properties', auth='public', website=True)
    def list_properties(self, **kw):
        properties = http.request.env['estate.property'].search([('active', '=', True)])
        return http.request.render('real_estate.property_listing', {
            'properties': properties,
        })

    @http.route('/real_estate/properties/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return http.request.not_found()
        return http.request.render('real_estate.property_detail', {
            'property': property_obj,
        })

    # API Endpoints
    @http.route('/api/real_estate/properties', type='json', auth='public', methods=['GET'])
    def api_list_properties(self, **kw):
        properties = http.request.env['estate.property'].search_read(
            [('active', '=', True)],
            ['name', 'expected_price', 'selling_price', 'bedrooms', 'living_area', 'description', 'postcode', 'state']
        )
        return {'properties': properties}

    @http.route('/api/real_estate/properties/<int:property_id>', type='json', auth='public', methods=['GET'])
    def api_property_detail(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return {'error': 'Property not found'}
        return property_obj.read(['name', 'expected_price', 'selling_price', 'bedrooms', 'living_area', 'description', 'postcode', 'state', 'date_availability', 'garden', 'garden_area', 'garden_orientation', 'garage', 'facades'])[0]

    @http.route('/api/real_estate/properties', type='json', auth='user', methods=['POST'])
    def api_create_property(self, **kw):
        data = json.loads(http.request.httprequest.data)
        property_obj = http.request.env['estate.property'].create(data)
        return {'id': property_obj.id, 'message': 'Property created'}

    @http.route('/api/real_estate/properties/<int:property_id>', type='json', auth='user', methods=['PUT'])
    def api_update_property(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return {'error': 'Property not found'}
        data = json.loads(http.request.httprequest.data)
        property_obj.write(data)
        return {'message': 'Property updated'}

    @http.route('/api/real_estate/properties/<int:property_id>', type='json', auth='user', methods=['DELETE'])
    def api_delete_property(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return {'error': 'Property not found'}
        property_obj.unlink()
        return {'message': 'Property deleted'}

    # Handle tracking requests to prevent 404 errors
    @http.route('/hybridaction/zybTrackerStatisticsAction', type='json', auth='public', methods=['GET'])
    def zyb_tracker_statistics(self, **kw):
        # Return empty dict for JSONP response
        return {}

