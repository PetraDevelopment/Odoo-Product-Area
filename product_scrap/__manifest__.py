{
    'name':'Product Scrap',
    'summary':'Product Scrap',
    'depends': ['base', 'product','sale','stock','web_tour','purchase','web'],
    'category':'Inventoy',
    'website': 'www.t-petra.com',
    'author':'Petra Software',
    'company': 'Petra Software',
    'maintainer': 'Petra Software',
    'images': ['static/description/banner.png'],
    'data':[
        # 'views/list/list_renderer.xml',
        # 'views/assets.xml',
    #    'static/src/css/rtl_overrides.css',
        'reports/base_document_layout.xml',
        'views/attribute_view.xml',
            'views/saleorderline.xml',
            'views/purchase_orderline.xml',
            'views/return_orderline.xml',
            'views/configure_selection.xml',
            'views/quick_sale_report.xml',
            'views/stockmove.xml',
            'static/src/js/selection_value.js',
            'static/src/js/calculating_file.js',
            'reports/sale_report_inherit.xml',
            'reports/purchase_order_report_inherit.xml',
            'reports/purchase_quotation_report_inherit.xml',
            'reports/invoices_pdf.xml',
            'static/src/js/over_conf.js',
            'views/scrap_view.xml',
            'views/base_inherit.xml',
           


            ],      
    'assets': {
        # 'web.report_assets_common': [
        #     'product_scrap/static/css/report_css.css',
        # ],
        'web_editor.assets_wysiwyg': [

            'product_scrap/static/css/button_css.css'
        ],
     
        'web.assets_backend': [
            # 'product_scrap/static/src/js/calculating_file.js',
            'product_scrap/static/src/xml/sale_purchase_list_button.xml',
        ]
       
   


    }, 

     'license': 'AGPL-3',
     'price':100,
      'currency':'USD',       
       
        
    }