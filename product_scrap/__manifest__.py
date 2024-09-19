{
    'name':'Product Scrap',
    'summary':'Calculate product in scrap state',
    'depends': ['base', 'product','sale','stock','web_tour'],
    'category':'Inventoy',
    'data':[
        'views/attribute_view.xml',
            'views/sales_orderline.xml',
            'views/configure_selection.xml',
            'views/quick_sale_report.xml',
            'views/stockmove.xml',
            'static/src/js/selection_value.js',
            # 'reports/sale_report_inherit.xml',
            'views/scrap_view.xml',
            'views/purchase_orderline.xml',
            ],      
        
        'web.assets_backend': [
            'product_scrap/static/src/xml/sale_purchase_list_button.xml',
        ],
        'website': 'www.t-petra.com',
    'author':'Petra Software',
    'company': 'Petra Software',
    'maintainer': 'Petra Software',
    'images': ['static/description/banner.png'],
    'price':100,
      'currency':'USD',
    }