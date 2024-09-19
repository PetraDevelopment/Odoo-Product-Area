from odoo import fields, models, api
import re


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_calculate_product_qty_sales(self):
        for line in self.order_line:
            line.calculate_product_qty_sales()

    def action_calculate_uom_and_total_sales(self):
        for line in self.order_line:
            line.calculate_uom_and_total_sales()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    uom_per_unit = fields.Float(string="Uom Per Unit")
    total = fields.Float(string=' ')
    total_area = fields.Float(string='Area', default=0)
    width = fields.Float(string='Width', default=0)
    height = fields.Float(string='Height', default=0)
    qty_tiles = fields.Float(string='Quantity Of Tiles', default=0)
    total_text = fields.Char("Total Text", compute='_compute_total_tooltip', help='عدد البلاط') 
    uom_per_unit_text = fields.Char("Uom Per Unit Text", compute='_compute_uom_text', help='عدد الكراتين') 
    price_unit=fields.Float(string='Unit Price')
    lenght=fields.Float(string='')
    cartoninmeter=fields.Float(string='')
    tilesinmeter=fields.Float(string='')
    totalquantity=fields.Float()
    product_uom_qty=fields.Float(default=0)
    # carton_text=fields.Char(string=' ',default='كرتونة')
    # tiles_text=fields.Char(string=' ',default='بلاطة')
    flag=fields.Boolean(default=False)
    qty_flag=fields.Boolean(default=False)
    product_id = fields.Many2one('product.product', string='Product')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    product_uom_is_m = fields.Boolean(string='Is Product UOM "m"', compute='_compute_product_uom_is_m')
    product_uom_qty = fields.Float(string='Quantity')
    carton_text = fields.Char(string=' ', compute='_compute_visibility', store=True)
    tiles_text = fields.Char(string='  ', compute='_compute_visibility', store=True)
    blank_field=fields.Char(string='  ')

    

   



    @api.depends('product_uom')
    def _compute_product_uom_is_m(self):
        for rec in self:
            rec.product_uom_is_m = rec.product_uom.name == "m"
    
    @api.depends('product_uom_is_m')
    def _compute_visibility(self):
        for rec in self:
            if rec.product_uom_is_m:
                rec.carton_text = 'كرتونة'
                rec.tiles_text = 'بلاطة'
            else:
                rec.carton_text = '  '
                rec.tiles_text = '  '
    
    def calculate_product_qty_sales(self):
        if self.product_template_id and self.product_template_id.attribute_line_ids:
            for record in self.product_template_id.attribute_line_ids:
                attr = record.attribute_id
                display_typee = attr.display_type if attr else False
                pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'

                if display_typee == 'new_radio_selection' and self.product_uom.name == "m" :
                    for one in self.product_id.product_template_attribute_value_ids:
                        x = 0
                        onerecord = [one.name]
                        if re.match(pattern, onerecord[x]):
                            value_to_be_parted = onerecord[x]
                            cleaned_string = re.sub(r'[^0-9.*]', '', value_to_be_parted)
                            dimensions = [float(num) for num in cleaned_string.split('*')]
                            if len(dimensions) == 3:
                                width = dimensions[0]
                                height = dimensions[1]
                                qty_tiles = dimensions[2]
                                self.total_area = width * height * qty_tiles
                                self.uom_per_unit = self.product_uom_qty / self.total_area
                                self.total = self.uom_per_unit * qty_tiles
                                return self.total


    def calculate_uom_and_total_sales(self):
        if self.product_template_id and self.product_template_id.attribute_line_ids:
                for record in self.product_template_id.attribute_line_ids:
                    attr = record.attribute_id
                    display_typee = attr.display_type if attr else False
                    pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'
                    if display_typee=='new_radio_selection' and self.product_uom.name =="m" :
                        pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'
                        for one in self.product_id.product_template_attribute_value_ids:
                            x=0
                            onerecord = [one.name]
                            if re.match(pattern, onerecord[x]):
                                value_to_be_parted = onerecord[x]
                                cleaned_string = re.sub(r'[^0-9.*]', '', value_to_be_parted)
                                dimensions = [float(num) for num in cleaned_string.split('*')]
                                self.width=dimensions[0]
                                self.height=dimensions[1]
                                self.lenght=dimensions[2]
                                self.cartoninmeter=self.width*self.height*self.lenght*self.uom_per_unit
                                self.tilesinmeter=self.width*self.height*self.total
                                self.totalquantity=self.cartoninmeter+self.tilesinmeter
                                self.product_uom_qty=self.totalquantity   
                            x+=1  


class StockMove(models.Model):
    _inherit = 'stock.move'

    priceunit = fields.Float(string='Price', compute='_compute_unit_price', store=True)
    cal_unit = fields.Float(string="Uom Per Unit", compute='_compute_uom_values')
    uom_total = fields.Float(string=' ', store=True)
    total_area = fields.Float(string='Area')
    width = fields.Float(string='Width', store=True)
    height = fields.Float(string='Height', store=True)
    qty_tiles = fields.Float(string='Quantity Of Tiles', store=True)

    location_id = fields.Many2one('stock.location', string='Location')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouses')
    usage = fields.Selection(related='location_id.usage', string='Usage', store=True)
    namess = fields.Char(related='warehouse_id.name')

    @api.depends('product_id')
    def _compute_unit_price(self):
        for rec in self :
            product = rec.env['product.product'].browse(rec.product_id.id)
            rec.priceunit=product.list_price



    @api.depends('product_id')
    def _compute_uom_values(self):
        for rec in self:
                rec.cal_unit = 0.0
                rec.uom_total = 0.0
                product = rec.env['product.product'].browse(rec.product_id.id)
                rec.priceunit=product.list_price
                if product.uom_name == 'm':
                    pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'
                    for one in rec.product_id.product_template_attribute_value_ids:
                        x=0
                        onerecord = [one.name]
                        if re.match(pattern, onerecord[x]):
    
                            value_to_be_parted = onerecord[x]
                            cleaned_string = re.sub(r'[^0-9.*]', '', value_to_be_parted)
                            dimensions = [float(num) for num in cleaned_string.split('*')]
                            if len(dimensions) == 3:
                                width = dimensions[0]
                                height = dimensions[1]
                                qty_tiles = dimensions[2]
                                rec.total_area = width * height * qty_tiles
                                if rec.total_area != 0:  
                                    rec.cal_unit = rec.product_uom_qty / rec.total_area
                                    rec.uom_total = rec.cal_unit * qty_tiles
                                else:
                                    rec.cal_unit = 0.0
                                    rec.uom_total = 0.0
                            else:
                                rec.cal_unit = 0.0
                                rec.uom_total =0
                                rec.total_area = 0.0
                else:
                    rec.cal_unit = 0.0
                    rec.uom_total = 0.0
                    rec.total_area = 0.0
        
 
      
              

                                   
                                       

# display radio size  selection field on attribute page

class CalculateArea(models.Model):
    _inherit = 'product.attribute'
    
    display_type = fields.Selection([
         ('new_radio_selection', 'Radio Size'),
        ('radio', 'Radio'),
        ('pills', 'Pills'),
        ('select', 'Select'),
        ('color', 'Color')], default='radio', required=True, help="The display type used in the Product Configurator.")

    hint_msg=fields.Char(string=' ',readonly=True,store=True,compute='_compute_display_message')
   

    @api.depends("display_type")
    def _compute_display_message(self):
        for attribute in self:
            if attribute.display_type == 'new_radio_selection':
                attribute.hint_msg = "To calculate the area of type, enter in value the length and width of the tile multiply the number of tile in carton."
            else:
                attribute.hint_msg = ""

    


        
class scrapscrap(models.Model):
    _inherit = 'stock.scrap'

    numberofcarton=fields.Float()
    numberoftiles=fields.Float()
    cartoninmeter=fields.Float(string='',store=True)
    tilesinmeter=fields.Float(string='')
    height=fields.Float(string='')
    width=fields.Float(string='')   
    lenght=fields.Float(string='')
    totalquantity=fields.Float()


    @api.onchange('product_id','numberoftiles','numberofcarton')
    def units_m(self):
            if self.product_uom_id.name == 'm':
                for rec in self:
                    pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'
                    for one in rec.product_id.product_template_attribute_value_ids:
                            x=0
                            onerecord = [one.name]
                            if re.match(pattern, onerecord[x]):
                                value_to_be_parted = onerecord[x]
                                cleaned_string = re.sub(r'[^0-9.*]', '', value_to_be_parted)
                                dimensions = [float(num) for num in cleaned_string.split('*')]
                                rec.width=dimensions[0]
                                rec.height=dimensions[1]
                                rec.lenght=dimensions[2]
                                rec.cartoninmeter=rec.width*rec.height*rec.lenght*rec.numberofcarton
                                rec.tilesinmeter=rec.width*rec.height*rec.numberoftiles
                                rec.totalquantity=rec.cartoninmeter+rec.tilesinmeter
                                rec.scrap_qty=rec.totalquantity 
                            x+=1    

            
            else:
                self.numberoftiles=0
                self.numberofcarton=0
                self.scrap_qty=0        

class PurchaseOrderLinenew(models.Model):
    _inherit = 'purchase.order'


    carton_text1=fields.Char(string=' ',default='كرتونة')
    tiles_text1=fields.Char(string=' ' ,default='بلاطة')


    @api.onchange('product_id')
    def settingquantityorginal(self):
        for rec in self:
            if rec.product_uom.name !="m":
                print(rec.product_uom.name,'1111111111111111')
                rec.carton_text1='  '
                rec.tiles_text1='  '

            else:
                print(rec.product_uom.name,'2222222222222222')

                rec.carton_text1='كرتونة'
                rec.tiles_text1='بلاطة'





class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    uom_per_unit = fields.Float(string="Uom Per Unit")
    total = fields.Float(string=' ')
    total_area = fields.Float(string='Area', default=0)
    width = fields.Float(string='Width', default=0)
    height = fields.Float(string='Height', default=0)
    qty_tiles = fields.Float(string='Quantity Of Tiles', default=0)
    total_text = fields.Char("Total Text", compute='_compute_total_tooltip', help='عدد البلاط') 
    uom_per_unit_text = fields.Char("Uom Per Unit Text", compute='_compute_uom_text', help='عدد الكراتين') 
    price_unit=fields.Float(string='Unit Price')
    lenght=fields.Float(string='')
    cartoninmeter=fields.Float(string='')
    tilesinmeter=fields.Float(string='')
    totalquantity=fields.Float()
    product_qty=fields.Float(default=0)
    carton_text=fields.Char(string=' ',default='كرتونة')
    tiles_text=fields.Char(string=' ' ,default='بلاطة')
    flag=fields.Boolean(default=False)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    product_uom_is_m = fields.Boolean(string='Is Product UOM "m"', compute='_compute_product_uom_is_m')
    product_uom_qty = fields.Float(string='Quantity')
    carton_text = fields.Char(string='Carton Text', compute='_compute_visibility', store=True)
    tiles_text = fields.Char(string='Tiles Text', compute='_compute_visibility', store=True)
    blank_field=fields.Char(string='  ')

    
    @api.depends('product_uom')
    def _compute_product_uom_is_m(self):
        for rec in self:
            rec.product_uom_is_m = rec.product_uom.name == "m"
    
    @api.depends('product_uom_is_m')
    def _compute_visibility(self):
        for rec in self:
            if rec.product_uom_is_m:
                rec.carton_text = 'كرتونة'
                rec.tiles_text = 'بلاطة'
            else:
                rec.carton_text = '  '
                rec.tiles_text = '  '
  

    @api.onchange('product_id','product_qty')        
    def setPrice(self):
        for rec in self:
            self.price_unit=rec.product_id.standard_price


    def calculate_product_qty_purchase(self):
        if self.product_id and self.product_id.attribute_line_ids:
                for record in self.product_id.attribute_line_ids:
                    attr = record.attribute_id
                    display_typee = attr.display_type if attr else False
                    pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'
                

                    if  display_typee=='new_radio_selection' and self.product_uom.name =="m" :
                        for one in self.product_id.product_template_attribute_value_ids:
                            x=0

                            onerecord = [one.name]
                            if re.match(pattern, onerecord[x]):
                                value_to_be_parted = onerecord[x] 
                                cleaned_string = re.sub(r'[^0-9.*]', '', value_to_be_parted)
                                dimensions = [float(num) for num in cleaned_string.split('*')]
                                if len(dimensions) == 3 :
                                    width = dimensions[0]
                                    height = dimensions[1]
                                    qty_tiles = dimensions[2]
                                    self.total_area = width * height * qty_tiles
                                    self.uom_per_unit =  self.product_qty / self.total_area
                                    self.total = self.uom_per_unit * qty_tiles 
    
    def calculate_product_uon_and_total_purchase(self):
        if self.product_id and self.product_id.attribute_line_ids:
            for record in self.product_id.attribute_line_ids:
                attr = record.attribute_id
                display_typee = attr.display_type if attr else False
                pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'

            if display_typee=='new_radio_selection' and self.product_uom.name =="m":
                pattern = r'^\d+\.\d+\*\d+\.\d+\*\d+$'
                for one in self.product_id.product_template_attribute_value_ids:
                    x=0
                    onerecord = [one.name]
                    if re.match(pattern, onerecord[x]):
                        value_to_be_parted = onerecord[x]
                        cleaned_string = re.sub(r'[^0-9.*]', '', value_to_be_parted)
                        dimensions = [float(num) for num in cleaned_string.split('*')]
                        self.width=dimensions[0]
                        self.height=dimensions[1]
                        self.lenght=dimensions[2]
                        self.cartoninmeter=self.width*self.height*self.lenght*self.uom_per_unit
                        self.tilesinmeter=self.width*self.height*self.total
                        self.totalquantity=self.cartoninmeter+self.tilesinmeter
                        self.product_qty=self.totalquantity  
                        
                    x+=1              
