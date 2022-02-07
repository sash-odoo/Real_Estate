from email.policy import default
from odoo import models , fields , api
from odoo.exceptions import UserError , ValidationError

# Relational Mapping ... [Many2One]

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'EstatePropertyType'

    name = fields.Char()
    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    _sql_constraints = [('unique_property_type_name','unique(name)','Type cannot be duplicate ')] # Constraints ...
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


#buyer

class Buyer_Partner(models.Model) :
    _inherit = 'res.partner'

    is_buyer = fields.Boolean(domain = "[('is_buyer' , '=' , ['True'])]")


#my property

class EstatePropertyMyproperty(models.Model):
    _name = 'estate.property.myproperty'
    _description = 'This is the Task Menu'

    def _get_description(self) :
        if self.env.context.get('is_my_property') :
            return self.env.user.name + "'s property"
        
    name = fields.Char()
    salesman_id = fields.Many2one('res.users',default=lambda self:self.env.user)
    description = fields.Text(default=_get_description)
    property_id = fields.Many2one('estate.property')
    partner_id = fields.Many2one('res.partner')
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')])
    bedrooms = fields.Integer()
    name = fields.Char(default="unknown" , required=True , string="Name")
    price = fields.Float()
    living_area = fields.Integer()
    name = fields.Char('res.partner',default=lambda user:user.partner_id.id)
    description = fields.Text()
    postcode = fields.Char()
    date_availability =  fields.Date(default=lambda self:fields.Datetime.now() , copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades =  fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
        ])
    image = fields.Image()
    total_area = fields.Integer() #If you want to store this field in the database ---> (store=True) Otherwise By Default this field is not store in databse.
    best_price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()
    # salesman_id = fields.Many2one('res.users')
    state = fields.Selection([('new','New'),('sold','Sold'),('cancle','Cancle')],default='new')


# Relational Mapping ... [Many2Many]

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'EstatePropertyTag'

    name = fields.Char()
    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    _sql_constraints = [('unique_property_tag_name','unique(name)','Tag cannot be duplicate ')] # Constraints ...
    color = fields.Integer()



# Relational Mapping ... [One2Many]

class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'EstatePropertyOffer'

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)



# Accepted and Rejected Action ...

    def action_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refused(self):
        for record in self:
            record.status = 'refused'
    

# Create Model ...
 
class EstateProperty(models.Model) :
    _name = 'estate.property'
    _inherit ='portal.mixin'
    _description = 'This is the Real Estate Module'
    _sql_constraints = [('positive_price','check(expected_price > 0)','Enter Positive value')] # Constraints [Exception Error] ...

    
    name = fields.Char()
    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    name = fields.Char(default="Unknown" , required=True  , string="Name")
    description = fields.Text()
    postcode = fields.Char()
    date_availability =  fields.Date(default=lambda self:fields.Datetime.now() , copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades =  fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
        ])
    image = fields.Image()
    total_area = fields.Integer(compute="_compute_area" , inverse="_inverse_area") #If you want to store this field in the database ---> (store=True) Otherwise By Default this field is not store in databse.
    best_price = fields.Float(compute="_compute_best_price")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")
    state = fields.Selection([('new','New'),('sold','Sold'),('cancle','Cancle')],default='new')

    def open_offers(self):
        view_id_all = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_all, 'tree']],
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }

    def open_confirm_offers(self):
        view_id_accept = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_accept, 'tree']],
            "domain": [('property_id', '=', self.id),('status','=','accepted')]
            }

    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = 'my/properties.%s' % (record.id)


    # Many2One ...
    property_type_id = fields.Many2one('estate.property.type')
    salesman_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')

    # Many2Many ...
    property_tag_ids = fields.Many2many('estate.property.tag')

    # One2Many ...
    property_offer_ids = fields.Many2many('estate.property.offer' , 'property_id')

    
    # Compute - Fields ...

    @api.depends('living_area' , 'garden_area')
    def _compute_area(self): # Recordset [Collection od Record]
        for record in self:
            record.total_area = record.living_area + record.garden_area


    # Just Exercise ... [Compute - Field]

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    # Just Exercise ...

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability,days=record.validity)


    # Inverse Function ...

    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2

    
    # Onchange Method ...

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area=10
                record.garden_orientation='north'
            else:
                record.garden_area=0
                record.garden_orientation=None

    
    # Sold and Cancle Button ...

    def action_sold(self):
        for record in self:
            if record.state == 'cancle':
                raise UserError ("Cancle Property cannot be Sold")
            record.state = 'sold'
    
    def action_cancle(self):
        for record in self:
            if record.state == 'sold':
                 raise UserError ("Sold Property cannot be cancle")
            record.state = 'cancle'


    # Constraints [Validation Error] ...

    @api.constrains('living_area' , 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError ("Garden cannot biggest than the Living area")
