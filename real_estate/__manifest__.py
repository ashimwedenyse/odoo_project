{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "19.0.1.0.0",
    "author": "Your Name or Company",
    "license": "LGPL-3",
    "depends": ["crm"],
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
    "installable": True,
    "application": True,
}
