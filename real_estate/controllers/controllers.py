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

    @http.route('/api/real_estate/properties', type='jsonrpc', auth='public', methods=['GET'])
    def api_list_properties(self, **kw):
        properties = http.request.env['estate.property'].search([('active', '=', True)])

        result = []
        for prop in properties:
            result.append({
                'id': prop.id,
                'name': prop.name,
                'expected_price': prop.expected_price,
                'selling_price': prop.selling_price,
                'bedrooms': prop.bedrooms,
                'living_area': prop.living_area,
                'description': prop.description,
                'postcode': prop.postcode,
                'state': prop.state,
                # ✅ Added image URL for dashboard
                'image': f'/web/image/estate.property/{prop.id}/image' if prop.image else '/web/static/img/placeholder.png'
            })

        return {'properties': result}

    @http.route('/api/real_estate/properties/<int:property_id>', type='jsonrpc', auth='public', methods=['GET'])
    def api_property_detail(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return {'error': 'Property not found'}
        return property_obj.read(['name', 'expected_price', 'selling_price', 'bedrooms', 'living_area', 'description', 'postcode', 'state', 'date_availability', 'garden', 'garden_area', 'garden_orientation', 'garage', 'facades'])[0]

    @http.route('/api/real_estate/properties', type='jsonrpc', auth='user', methods=['POST'])
    def api_create_property(self, **kw):
        data = json.loads(http.request.httprequest.data)
        property_obj = http.request.env['estate.property'].create(data)
        return {'id': property_obj.id, 'message': 'Property created'}

    @http.route('/api/real_estate/properties/<int:property_id>', type='jsonrpc', auth='user', methods=['PUT'])
    def api_update_property(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return {'error': 'Property not found'}
        data = json.loads(http.request.httprequest.data)
        property_obj.write(data)
        return {'message': 'Property updated'}

    @http.route('/api/real_estate/properties/<int:property_id>', type='jsonrpc', auth='user', methods=['DELETE'])
    def api_delete_property(self, property_id, **kw):
        property_obj = http.request.env['estate.property'].browse(property_id)
        if not property_obj.exists():
            return {'error': 'Property not found'}
        property_obj.unlink()
        return {'message': 'Property deleted'}

    # Handle tracking requests to prevent 404 errors
    @http.route('/hybridaction/zybTrackerStatisticsAction', type='jsonrpc', auth='public', methods=['GET'])
    def zyb_tracker_statistics(self, **kw):
        # Return empty dict for JSONP response
        return {}

    @http.route('/api/real_estate/dashboard', type='jsonrpc', auth='public', methods=['POST'])
    def api_dashboard_data(self, **kw):
        """Get dashboard statistics for real estate module"""
        try:
            # Get total properties count
            total_properties = http.request.env['estate.property'].search_count([])

            # Get sold properties count
            sold_properties = http.request.env['estate.property'].search_count([('state', '=', 'sold')])

            # Get properties by type
            property_types_data = http.request.env['estate.property'].read_group(
                [('active', '=', True)],
                ['property_type_id'],
                ['property_type_id']
            )

            property_types = []
            colors = ['#4A90E2', '#E24A4A', '#F5A623', '#50C878', '#9B59B6', '#E67E22']
            for i, group in enumerate(property_types_data):
                if group['property_type_id']:
                    type_name = group['property_type_id'][1]
                    count = group['property_type_id_count']
                    property_types.append({
                        'type': type_name,
                        'count': count,
                        'color': colors[i % len(colors)]
                    })

            # Get property status distribution
            status_data = http.request.env['estate.property'].read_group(
                [('active', '=', True)],
                ['state'],
                ['state']
            )

            status_labels = {
                'new': 'New',
                'offer_received': 'Offer Received',
                'offer_accepted': 'Offer Accepted',
                'sold': 'Sold',
                'cancelled': 'Cancelled'
            }

            property_status = []
            for group in status_data:
                status = group['state']
                if status:
                    property_status.append({
                        'status': status_labels.get(status, status),
                        'count': group['state_count']
                    })

            # Get recent properties (last 20 for pagination)
            recent_properties = http.request.env['estate.property'].search(
                [('active', '=', True)],
                order='create_date desc',
                limit=20
            )

            recent_properties_data = []
            for prop in recent_properties:
                recent_properties_data.append({
                    'id': prop.id,
                    'name': prop.name,
                    'price': prop.selling_price or prop.expected_price,
                    'state': prop.state,
                    'stateLabel': status_labels.get(prop.state, prop.state),
                    'image': f'/web/image/estate.property/{prop.id}/image' if prop.image else '/web/static/img/placeholder.png'
                })

            return {
                'totalProperties': total_properties,
                'soldProperties': sold_properties,
                'propertyTypes': property_types,
                'propertyStatus': property_status,
                'recentProperties': recent_properties_data
            }

        except Exception as e:
            return http.request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')]
            )