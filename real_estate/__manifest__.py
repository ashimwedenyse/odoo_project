{
    "name": "Real Estate",
    "version": "1.0",
    "author": "Your Name",
    "license": "LGPL-3",
    "depends": ["crm", "web", "website"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/estate_actions.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "views/property_templates.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "assets": {
        'web.assets_backend': [
            'real_estate/static/src/xml/estate_property_dashboard_templates.xml',  # Ensure this is correct
            'real_estate/static/src/js/estate_property_dashboard.js',
        ],
        "web.assets_frontend": [
            "real_estate/static/src/css/style.css",  # Fixed missing comma
            "real_estate/static/src/js/script.js",
        ],
    },
    "installable": True,
    "application": True,
}
