{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "19.0.1.0.0",
    "author": "Your Name or Company",
    "license": "LGPL-3",
    "depends": ["crm", "web"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/estate_actions.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "real_estate/static/src/css/style.css",
            "real_estate/static/src/js/script.js",
        ],
        "web.assets_qweb": [
            "real_estate/static/src/xml/templates.xml",
        ],
    },
    "installable": True,
    "application": True,
}
