{
    'name':'RealEstate',
    'category':'Sales',
    'application':True,
    'depends' : ['base' , 'account' , 'website' , 'portal'],
    'data':[
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'wizard/add_offer_views.xml',
        'security/real_estate_security.xml',
        'views/estate_index.xml',
        'views/estate_portal_view.xml',
    ],
}
