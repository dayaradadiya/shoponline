
from datetime import datetime
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import User
from accounts.validators import validate_file_mimetype
from app.models import Brand, Section
from category.models import Category, Fifth_Level_Category, Fourth_Level_Category, Main_Category, Sub_Category
from django.core.validators import FileExtensionValidator
from vendor.models import Vendor
from django.db.models import Avg ,Count
from django.utils.html import mark_safe


VARIANTS = (
        ('None','None'),
        ('Color','Color'),
        ('Size','Size'),
        ('Size-Color','Size-Color'),
       #  ('StorageCapacity','StorageCapacity'),
       #  ('StorageCapacity-Color','StorageCapacity-Color'),
       #  ('ModelCompatibility','ModelCompatibility'),
       #  ('VehicleBrand','VehicleBrand'),
       #  ('Size-VehicleBrand','Size-VehicleBrand'),   
)
cond_choice = (
       ('Old','Old'),
       ('New','New'),
)

ext_validator = FileExtensionValidator(['jpg','png','jpeg'])   
class Product(models.Model):
        vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE,null=True)
        stock = models.IntegerField()
        is_available = models.BooleanField(default=True)
        featured_image = models.FileField(upload_to='vendor/product_images',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
        product_name = models.CharField(max_length=500)
        brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
        price = models.DecimalField(max_digits=7, decimal_places=2)
        discount = models.IntegerField(default=0,null=True,blank=True)
        product_information = RichTextField(null=True,blank=True)
        model_name = models.CharField(max_length=100,null=True,blank=True)
        main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products',blank=True,null=True)
        sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE,blank=True,null=True)
        fourth_level_category = models.ForeignKey(Fourth_Level_Category, on_delete=models.CASCADE,blank=True,null=True)
        tags = models.CharField(max_length=100,null=True,blank=True)
        description = RichTextField(null=True,blank=True)
        section = models.ForeignKey(Section,on_delete=models.DO_NOTHING,null=True,blank=True)
        slug = models.SlugField(default='',max_length=500,null=True,blank=True)
        created_date = models.DateTimeField(default=datetime.now)
        modified_date = models.DateTimeField(default=datetime.now)
        variant = models.CharField(max_length=25,choices=VARIANTS,default='None')
        parcel_size_W = models.FloatField(default=0, null=True,blank=True)
        parcel_size_L = models.FloatField(default=0, null=True,blank=True)
        parcel_size_H = models.FloatField(default=0, null=True,blank=True)
        weight = models.FloatField(default=0)
        shipping_fee_cover_byseller = models.BooleanField(default=False)
        shipping_fee = models.FloatField(default=0)
        max_allowed_quantity = models.IntegerField()
        min_order_quantity = models.IntegerField(default=1, null=True,blank=True)
        condition =  models.CharField(max_length=25,choices=cond_choice,default='New',null=True,blank=True)
        is_active = models.BooleanField(default=False)

        def get_url(self):
                return reverse('product_detail',args=[self.category.slug, self.slug])
        
        def __str__(self):  
                return self.product_name
        
        def image_tag(self):
               return  mark_safe('<img src="{}" height="50"/>'.format(self.featured_image.url))
        
        image_tag.short_description = 'Image'
        
        @property
        def averageReview(self):
                reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg("rating"))
                avg=0
                if reviews['average'] is not None:
                         avg =  float(reviews['average'])
                return avg
        @property
        def countReview(self):
                reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count("id"))
                count=0
                if  reviews['count'] is not None: 
                         count =  int(reviews['count'])
                return count 
        @property
        def get_max_allowed_qty(self):
                if self.stock < self.max_allowed_quantity:
                     return  self.stock 
                else :
                      return  self.max_allowed_quantity  
      
class Color(models.Model):
       name  = models.CharField(max_length=40)
       code= models.CharField(max_length=10,blank=True,null=True)

       def __str__(self):
              return self.name
       def color_tag(self):
              if self.code is not None:
                        return  mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
              else:
                        return ""
       
class Size(models.Model):
       name  = models.CharField(max_length=20)
       code= models.CharField(max_length=10,blank=True,null=True)

       def __str__(self):
              return self.name
       
# class StorageCapacity(models.Model):
#        name  = models.CharField(max_length=20)
#        code= models.CharField(max_length=10,blank=True,null=True)

#        def __str__(self):
#               return self.name
# class ModelCompatibility(models.Model):
#        name  = models.CharField(max_length=20)
#        code= models.CharField(max_length=10,blank=True,null=True)

#        def __str__(self):
#               return self.name

# class VehicleBrand(models.Model):
#        name  = models.CharField(max_length=20)
#        code= models.CharField(max_length=10,blank=True,null=True)

#        def __str__(self):
#               return self.name



class Images(models.Model):
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       title = models.CharField(max_length=50,blank=True)
       image = models.FileField(upload_to='image/product',validators=[ext_validator,validate_file_mimetype])

       def __str__(self):
              return self.title
       
       
       def image_tag(self):
                if self.image is not None:
                        return  mark_safe('<img src="{}" style="height:50px;"/>'.format(self.image.url))
                else:
                        return "" 
                

                

                
class Variants(models.Model):
       title = models.CharField(max_length=100,default='sample1')
       image_variant = models.FileField(upload_to='image/variantimage',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
       size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
       # storage_capacity = models.ForeignKey(StorageCapacity, on_delete=models.CASCADE,blank=True,null=True)
       # model_compatibility = models.ForeignKey(ModelCompatibility, on_delete=models.CASCADE,blank=True,null=True)
       # vehicle_brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE,blank=True,null=True)
       image_id = models.IntegerField(blank=True,null=True,default=0)
       variant_stock = models.IntegerField(blank=True,null=True)
       variant_price = models.DecimalField(blank=True,null=True, max_digits=7, decimal_places=2)
       variant_discount = models.IntegerField(default=0,blank=True,null=True)
       variant_max_allowed_quantity = models.IntegerField(default=100,blank=True,null=True)
       

#        picture = models.ForeignKey(Images, on_delete=models.CASCADE,blank=True,null=True)

       def __str__(self) :
              return self.title
       @property
       def image(self):
        #       img = Images.objects.get(id=self.image_id)

              if self.image_variant:
                     varimage = self.image_variant.url
              else :
                     varimage = ""
              return varimage
       @property
       def image_tag(self):
                # img = Images.objects.get(id=self.image_id)
                if self.image_variant:
                        return  mark_safe('<img src="{}" style="height:50px;"/>'.format(self.image_variant.url))
                else:
                        return ""   
       @property
       def image_tag_url(self):
                # img = Images.objects.get(id=self.image_id)
                if self.image_variant:
                        return  mark_safe('<img src="{}" style="height:100px;"/>'.format(self.image_variant.url))
                else:
                        return "" 
       @property
       def get_max_allowed_qty(self):
              if self.variant_stock  and  self.variant_max_allowed_quantity:    
                     if self.variant_stock < self.variant_max_allowed_quantity:
                            return  self.variant_stock 
                     else :
                            return  self.variant_max_allowed_quantity  
              else :
                     return 100
        
socks_type_choices = (
       ('Others','Others'),
        ('Sports Socks','Sports Socks'),
        ('Toe Socks','Toe Socks'),
)

costume_theme_choices = (
('Animals / Bugs','Animals / Bugs'),
('Career','Career'),
('Classic Halloween Costumes','Classic Halloween Costumes'),
('Decades','Decades'),
('Disney','Disney'),
('Fairytale','Fairytale'),
('Famous People / Celebrity','Famous People / Celebrity'),
('Food / Drink','Food / Drink'),
('Holidays','Holidays'),
('Horror / Gothic','Horror / Gothic'),
('Pirates','Pirates'),
('Religious','Religious'),
('Sci Fi','Sci Fi'),
('Sports','Sports'),
('TV / Movies','TV / Movies'),
('Video Games','Video Games'),
)
        
socks_length_choices = (
        ('Ankle','Ankle'),
        ('Calf High','Calf High'),
        ('Invisible','Invisible'),
        ('Knee High','Knee High'),
        ('Others','Others'),
        ('Thigh High','Thigh High'),
        )
access_choices = (
       ('Bust Seam', 'Bust Seam'),
        ('Button Down','Button Down'),
        ('Lift Up','Lift Up'),
        ('Pull Aside','Pull Aside'),
        ('Side Seam','Side Seam'),
        ('Vertical Seam','Vertical Seam'),
)

pack_choices = (
        ('Bundle' ,'Bundle'),
        ('Single','Single'),
) 
        
yn_choices = (
        ('Yes' ,'Yes'),
        ('No','No'),
)       
length_choices = (
        ('Long' ,'Long'),
        ('Regular','Regular'),
) 
Season_choices = (
       ('Winter','Winter'),
        ('Summer','Summer'),
        ('Spring','Spring'),
        ('Autumn','Autumn'),
        )

pantyhose_choices = (
       ('Black','Black'),
('Fishnet','Fishnet'),
('Grey','Grey'),
('Nude','Nude'),
('Tights','Tights'),
('Stockings & Knee-high socks','Stockings & Knee-high socks'),
)

Wed_dress_style_choices = (
('A Line','A Line'),
('Ballgown','Ballgown'),
('Column','Column'),
('Empire','Empire'),
('Mermaid','Mermaid'),
('Princess','Princess'),
('Tea Length','Tea Length'),
('Trumpet','Trumpet'),
)

prod_style_choices = (
('Athletic','Athletic'),
('Basic','Basic'),
('Boho','Boho'),
('Korean','Korean'),
('Minimalist','Minimalist'),
('Retro','Retro'),
('Sexy','Sexy'),
('Street Style','Street Style'),
('Tailored','Tailored'),
('Vintage','Vintage'),
)

material_choices = (
('Chiffon','Chiffon'),
('Chinos','Chinos'),
('Cotton','Cotton'),
('Denim','Denim'),
('Down','Down'),
('Felt','Felt'),
('Flannelette','Flannelette'),
('Fleece','Fleece'),
('Fur','Fur'),
('Khaki','Khaki'),
('Knit','Knit'),
('Lace','Lace'),
('Leather','Leather'),
('Linen','Linen'),
('Nylon','Nylon'),
('Others','Others'),
('Quilted','Quilted'),
('Silk','Silk'),
('Synthetic','Synthetic'),
('Textile','Textile'),
)
pattern_choices = (
('Batik','Batik'),
('Checkered/ Plaid','Checkered/ Plaid'),
('Floral','Floral'),
('Others','Others'),
('Plain','Plain'),
('Polka Dotted','Polka Dotted'),
('Print','Print'),
('Striped','Striped'),
('Tie Dye','Tie Dye'),
)

sleeve_length_choices = (
('3/4 Sleeves','3/4 Sleeves'),
('Long Sleeves','Long Sleeves'),
('Others','Others'),
('Short Sleeves','Short Sleeves'),
('Sleeveless','Sleeveless'),
)

neckline_choices = (
('Asymmetric','Asymmetric'),
('Boat Neck','Boat Neck'),
('Collar','Collar'),
('Halter','Halter'),
('Off Shoulder','Off Shoulder'),
('Others','Others'),
('Round Neck','Round Neck'),
('Turtle Neck','Turtle Neck'),
('V Neck','V Neck'),
)
occasion_choices = (('Casual','Casual'),
('Work','Work'),
('Party','Party'),
('Prom','Prom'),
('Others','Others'),
)
waist_height_choices = (
("High Waist","High Waist"),
("Low Waist","Low Waist"),
("Mid Waist","Mid Waist"),
("Others","Others"),
)
bottoms_length_choices = (
("3/4 Length / Capri", "3/4 Length / Capri"),
("Others","Others"),
("Full Length","Full Length"),
("Cropped","Cropped"),
)
bottoms_fit_type_choices = (
("Boyfriend","Boyfriend"),
("Fit & Flare","Fit & Flare"),
("Others","Others"),
("Regular","Regular"),
("Skinny","Skinny"),
("Slim Fit","Slim Fit"),
("Straight","Straight"),
("Tapered","Tapered"),
("Wide Leg","Wide Leg"),
)
dress_skirt_style_choices = (
("A-Line","A-Line"),
("Bodycon","Bodycon"),
("Fishtail","Fishtail"),
("Fit & Flare/Skater","Fit & Flare/Skater"),
("Others","Others"),
("Pencil","Pencil"),
("Pleated","Pleated"),
("Wrap","Wrap"),
)

dress_skirt_length_choices = (
("Maxi","Maxi"),
("Midi","Midi"),
("Mini","Mini"),
("Others","Others"),
)
overalls_type_choices = (
("Pants","Pants"),
("Shorts","Shorts"),
("Skirt","Skirt"),
)
outerwear_length_choices = (
("Medium","Medium"),
("3/4 Length","3/4 Length"),
("Long","Long"),
("Short","Short"),
)
jacket_type_choices = (
('Short','Short'),
('Baseball Jackets','Baseball Jackets'),
('Bomber Jackets','Bomber Jackets'),
('Others','Others'),
('Windbreakers','Windbreakers'),
('Normal Jackets','Normal Jackets'),
('Denim jackets','Denim jackets'),
('Leather jackets','Leather jackets'),
)
apparel_type_choices = (
('Long','Long'),
('Dresses','Dresses'),
('Jeans','Jeans'),
('Maternity Wear','Maternity Wear'),
('Others','Others'),
('Outerwear','Outerwear'),
('Pants & Leggings','Pants & Leggings'),
('Shorts','Shorts'),
('Innerwear & Underwear','Innerwear & Underwear'),
('Pants','Pants'),
('Sleepwear','Sleepwear'),
('Socks','Socks'),
('Tops','Tops'),

)
bra_style_choices = (
('Skirts','Skirts'),
('Others','Others'),
('Seamless','Seamless'),
('Strapless','Strapless'),
('Wireless','Wireless'),
)
pack_type_choices = (
        ('Bundle','Bundle'),
        ('Single','Single'),
        ('Value Size','Value Size'),
)
bra_type_choices = (
('Single','Single'),
('Bandeau','Bandeau'),
('Lightly Lined','Lightly Lined'),
('Plunge','Plunge'),
('Push Up','Push Up'),
('T Shirt','T Shirt'),
)
sexy_lingerie_style_choices = (
('Waist Cincher','Waist Cincher'),
('Accessories','Accessories'),
('Baby Dolls','Baby Dolls'),
('Bodysuits','Bodysuits'),
('Bustiers / Sexy Bras','Bustiers / Sexy Bras'),
('Cami Sets','Cami Sets'),
('Corsets / Shape Wear','Corsets / Shape Wear'),
('Costumes','Costumes'),
('Garters / Hosiery','Garters / Hosiery'),
)
bra_coverage_choices = (('Lingerie Sets','Lingerie Sets'),
('3/4 Coverage','3/4 Coverage'),
('Full Coverage','Full Coverage'),
('Others','Others'),
)
panty_style_choices = (
('Stick On','Stick On'),
('Bikini','Bikini'),
('Boy Short','Boy Short'),
('Cheeky','Cheeky'),
('Disposable','Disposable'),
('Hipster','Hipster'),

)
panties_type_choices = (
('Others','Others'),
('G-string','G-string'),
('Others','Others'),
('Period Panties','Period Panties'),
)
shaper_style_choices = (
('Push Up Panties','Push Up Panties'),
('Leg Shaper','Leg Shaper'),
('Mid Thigh Shaper','Mid Thigh Shaper'),
('Shapewear Corset','Shapewear Corset'),
('Shaping Panties','Shaping Panties'),

)
bottom_style_choices = (
('Cargo','Cargo'),
('Cigarette Trousers','Cigarette Trousers'),
('Culottes','Culottes'),
('Harem','Harem'),
('Joggers','Joggers'),
('Others','Others'),
)
buttons_style_choices = (
('Three Button', 'Three Button'),
('Two Button','Two Button'),
)
leather_type_choices = (
('Cow Hide', 'Cow Hide'),
('Lamb Skin','Lamb Skin'),
)
collar_type_choices = (
        ('Mandarin Collar','Mandarin Collar'),
        ('Spread Collar','Spread Collar'),
('Pinned Collar','Pinned Collar'),
('Mandarin Collar','Mandarin Collar'),
('Grandad Collar','Grandad Collar'),
('Club Collar','Club Collar'),
('Classic Collar','Classic Collar'),
('Button Down Collar','Button Down Collar'),
)
top_fit_style_choices = (
       ( 'Classic','Classic'),
('Loose','Loose'),
('Muscle','Muscle'),
('Oversized','Oversized'),
('Slim','Slim'),
('Tight Fit','Tight Fit'),
)
vent_style_choices = (
('Center Vent','Center Vent'),
('Side Vent','Side Vent'),
)
suit_style_choices =(
        ('Double Breasted','Double Breasted'),
('Single Breasted','Single Breasted'),
)
fly_type_choices = (
('Buttons','Buttons'),
('Zip','Zip'),
)
cuff_type_choices = (
        ('Barrel Cuff',  'Barrel Cuff'),
('French Cuff' ,'French Cuff'),
)
underwear_type_choices = (
('Briefs','Briefs'),
('Boxers & Trunks','Boxers & Trunks'),
('Others','Others'),
('Thongs','Thongs'),
)
shorts_type_choices =(
('Bermudas','Bermudas'),
('Board/Beach','Board/Beach'),
('Cargo','Cargo'),
('Jersey','Jersey'),
('Others','Others'),
)
towel_robe_fabric_choices =(
      ('Cotton','Cotton'),
('Microfiber','Microfiber'),
('Others','Others'),
('Tencel','Tencel'),
('Terry Cloth','Terry Cloth'),
  )
igredient_preference_choices = (
('AHA/ Glycolic Acid','AHA/ Glycolic Acid'),
('Anti-oxidants','Anti-oxidants'),
('BHA','BHA'),
('Ceramides','Ceramides'),
('Fragrance Free','Fragrance Free'),
('Hyaluronic Acid','Hyaluronic Acid'),
('Mineral','Mineral'),
('Naturally Derived','Naturally Derived'),
)
formulation_choices = (
('Oil','Oil'),
('Cream','Cream'),
('Gel','Gel'),
)
scrub_formulation_choices = (
('Scrub','Scrub'),
('Gel','Gel'),
('Stick','Stick'),
('Cream','Cream'),
('Liquid','Liquid'),
)
bodycare_benefits_choices = (
('Anti Aging','Anti Aging'),
('Anti Bacterial','Anti Bacterial'),
('Anti Fungal','Anti Fungal'),
('Anti Odour','Anti Odour'),
('Anti Perspiration','Anti Perspiration'),
('Cellulite & Stretch Marks','Cellulite & Stretch Marks'),
('Cracked Heel','Cracked Heel'),
('Eczema','Eczema'),
)
volume_choices = (
('10ml','10ml'),
('20ml','20ml'),
('30ml','30ml'),
('50ml','50ml'),
('100ml','100ml'),
('150ml','150ml'),
('200ml','200ml'),
('250ml','250ml'),
)
shelflife_choices =(
('1 Month','1 Month'),
('2 Months','2 Months'),
('3 Months','3 Months'),
('6 Months','6 Months'),
('12 Months','12 Months'),
('24 Months','24 Months'),
)
skin_type_choices = (
('All Skin Type','All Skin Type'),
('Oily Skin','Oily Skin'),
('Acne-prone','Acne-prone'),
('Sensitive','Sensitive'),
('Dry','Dry'),
('Normal','Normal'),
)
product_size_choices =(
        ('Large Size','Large Size'),
('Travel Size','Travel Size'),
)
application_area_choices = (
('Face','Face'),
('Nose','Nose'),
('Hair','Hair'),
('Body','Body'),
)


weight_choices = (
('10g','10g'),
('20g','20g'),
('30g','30g'),
('50g','50g'),
('100g','100g'),
('150g','150g'),
('200g','200g'),
('250g','250g'),
)
handwash_packsize_choices =(
('ML','ML'),
('L','L'),
('MG','MG'),
('G/GR','G/GR'),
('KG','KG'),
('CM','CM'),
('M','M'),
('Dozen','Dozen'),
('Piece','Piece'),
('Pack','Pack'),
('Set','Set'),
('Box','Box'),
)
handwash_formulation_choices = (
        ('Cream','Cream'),
('Powder','Powder'),
('Gel','Gel'),
)
warranty_duration_choices = (
('12 Months','12 Months'),
('24 Months','24 Months'),
('Lifetime Warranty','Lifetime Warranty'),
('No Warranty','No Warranty'),
)
warranty_type_choices = (
('Manufacturer Warranty','Manufacturer Warranty'),
('Supplier Warranty','Supplier Warranty'),
)
hair_care_benefits_choices = (
('Anti Thinning/Hair Loss','Anti Thinning/Hair Loss'),
('Anti-Dandruff','Anti-Dandruff'),
('Anti-Frizz','Anti-Frizz'),
('Colour Protection','Colour Protection'),
('Curl Enhancement','Curl Enhancement'),
('Damaged Hair/Split Ends','Damaged Hair/Split Ends'),
('Hydrating','Hydrating'),
('Oil Control','Oil Control'),
('Others','Others'),
('Volumizing','Volumizing'),
)
packaging_type_choices = (
('Capsule','Capsule'),
('Palette','Palette'),
('Refill','Refill'),
('Sachet','Sachet'),
)
shampoo_formulation_choices = (
('Cream','Cream'),
('Gel','Gel'),
('Solid','Solid'),
('Mousse','Mousse'),
('Powder','Powder'),
('Spray','Spray'),
('Oil','Oil'),
('Wipes','Wipes'),
('Scrub','Scrub'),
('Liquid','Liquid'),
('Patch','Patch'),
('Others','Others'),
('Stick','Stick'),
)
scent_choices = (
('Citrus','Citrus'),
('Earthy','Earthy'),
('Floral','Floral'),
('Fresh','Fresh'),
('Fruity','Fruity'),
('Woody','Woody'),
)
shavegel_appn_area_choices = (
('Body','Body'),
('Face','Face'),
('Foot','Foot'),
('Hair','Hair'),
('Hand','Hand'),
('Head','Head'),
('Neck','Neck'),
('Nose','Nose'),
)
makeup_furmulation_choices = (
('Cream','Cream'),
('Powder','Powder'),
('Gel','Gel'),
('Compact','Compact'),
('Liquid','Liquid'),
('Others','Others'),
('Loose','Loose'),
('Pencil','Pencil'),
('Spray','Spray'),
('Stick','Stick'),
)
skin_tone_choices = (
('Dark','Dark'),
('Fair','Fair'),
('Medium','Medium'),
('Pale','Pale'),
('Tan','Tan'),
)
SPF_choices = (
('15','15'),
('25','25'),
('30','30'),
('40','40'),
('50','50'),
('100','100'),
('120','120'),
('150','150'),
)
foundn_coverg_choices = (
('Full','Full'),
('Light','Light'),
('Medium','Medium'),  
)
makeup_finish_choices = (
('Dewy','Dewy'),
('Glitter','Glitter'),
('High Shine','High Shine'),
('Matte','Matte'),
('Metallic','Metallic'),
('Natural','Natural'),
('Radiant','Radiant'),
('Satin','Satin'),
)
cc_scare_bene_choices=(
('Dark spots/ Hyperpigmentation','Dark spots/ Hyperpigmentation'),
('Oiliness','Oiliness'),
('Fineline/ Wrinkles','Fineline/ Wrinkles'),
('Enlarged Pores','Enlarged Pores'),
('Redness','Redness'),
('Acne/ Blemishes','Acne/ Blemishes'),
('Anti Aging','Anti Aging'),
('Puffiness','Puffiness'),
('Dullness/ Uneven texture','Dullness/ Uneven texture'),
('Dryness','Dryness'),
('Blackheads','Blackheads'),
('Uneven skin tone','Uneven skin tone'),
('Dark circles','Dark circles'),
)
mascara_ben_chioces=(
('Curling','Curling'),
('Lengthening','Lengthening'),
('Long-wearing','Long-wearing'),
('Volumizing','Volumizing'),
)
lip_benefit_choices = (
('Long Wearing','Long Wearing'),
('Hydrating','Hydrating'),
('Others','Others'),
('Plumping','Plumping'),
)
face_steamr_bene_choices = (
('Acne/ Blemishes','Acne/ Blemishes'),
('Anti Aging','Anti Aging'),
('Blackheads','Blackheads'),
('Clogged Pores','Clogged Pores'),
('Dark circles','Dark circles'),
('Dark spots/ Hyperpigmentation','Dark spots/ Hyperpigmentation'),
('Dryness','Dryness'),
('Dullness/ Uneven texture','Dullness/ Uneven texture'),
('Enlarged Pores','Enlarged Pores'),
('Fineline/ Wrinkles','Fineline/ Wrinkles'),
('Oiliness','Oiliness'),
('Others','Others'),
('Puffiness','Puffiness'),
('Redness','Redness'),
('Uneven skin tone','Uneven skin tone'),
)
power_source_choces = (
 ('Battery','Battery'),
('Electric','Electric'),
('Manual','Manual'),
)
mask_type_choices =(
('Cream Mask','Cream Mask'),     
)
hair_finish_choices =(
    ('Matte','Matte'),
('Shine','Shine'),
)
tool_function_choices =(
('Anti-ingrown','Anti-ingrown'),
('Cleaning','Cleaning'),
('Damaged Hair','Damaged Hair'),
('Eliminating Unwanted Hair','Eliminating Unwanted Hair'),
('Epilator','Epilator'),
('Hair Removal','Hair Removal'),
('Shaving','Shaving'),
('Trimming','Trimming'),
('Wax Pad','Wax Pad'),
('Wax Paper','Wax Paper'),
('Waxing','Waxing'),
)
cleanser_type_choices = (
('Face Wipes','Face Wipes'),
('Foam Cleanser','Foam Cleanser'),
('Gel Cleanser','Gel Cleanser'),
('Milk Cleanser','Milk Cleanser'),
('Powder Cleanser','Powder Cleanser'),
)
acne_tment_type_choices = (
       ('Acne Creams','Acne Creams'),
('Acne Patches','Acne Patches'),
)
lotion_type_choices = (
   ('Body Butter','Body Butter'),
('Body Cream','Body Cream'),
('Body Lotion','Body Lotion'),
('Milk Lotion','Milk Lotion'),
('Others','Others'), 
)
fragrance_concn_choices = (
      ( 'EDP','EDP'),
('EDT','EDT'),
('Others','Others'),
)
gender_choices =(
       ('Unisex','Unisex'),
('Male','Male'),
('Female','Female'),
)
nutrient_type_choices = (
  ('Alpha Lipoic Acid','Alpha Lipoic Acid'),
('Amino Acids','Amino Acids'),
('Antioxident','Antioxident'),
('BCAAs','BCAAs'),
('Calcium','Calcium'),
('Chromium','Chromium'),
('Collagen','Collagen'),
('CoQ10','CoQ10'),
('others','others'),   
)
specialty_diet_choices = (
    ('Gluten Free','Gluten Free'),
('Halal','Halal'),
('Pork Free','Pork Free'),
('Sugar Free','Sugar Free'),
('Vegan','Vegan'),
('GMO Free','GMO Free'),
)
food_type_choices =(
       ('Bars','Bars'),
('Coffee','Coffee'),
('Cookies','Cookies'),
('Honey','Honey'),
('Juice','Juice'),
('Ready-to-Eat Meals','Ready-to-Eat Meals'),
('Seeds & Grains','Seeds & Grains'),
('Shakes','Shakes'),
)
weight_mgmt_supplt_funs_choices =(
       ('Appetite Suppressants','Appetite Suppressants'),
('Detox','Detox'),
('Fat Blocker','Fat Blocker'),
('Fat Burner','Fat Burner'),
('Meal Replacement','Meal Replacement'),
('Others','Others'),
('Slimming','Slimming'),
)
consumables_form_choices = (
    ('Bustlets','Bustlets'),
('Capsules','Capsules'),
('Chewables','Chewables'),
('Granules','Granules'),
('Jelly','Jelly'),
('Lozenges','Lozenges'),
('Powders','Powders'),
('Salts','Salts'),   
)
flavour_choices = (
       ('Acai Berry','Acai Berry'),
('Apple','Apple'),
('Banana','Banana'),
('Blueberry','Blueberry'),
('Caramel','Caramel'),
('Cherry','Cherry'),
('Chocolate','Chocolate'),
('Chocolate Chip','Chocolate Chip'),
)
beauty_supplmt_funcs_choices = (
       ('Acne Care','Acne Care'),
('Anti-ageing','Anti-ageing'),
('Bust','Bust'),
('Collagen','Collagen'),
('Hair, Skin & Nails','Hair, Skin & Nails'),
('Others','Others'),
('Whitening','Whitening'),
)
fitness_supplmt_funcs_choices = (
  ('Amino Acids','Amino Acids'),
('Mass Gainer','Mass Gainer'),
('Others','Others'),
('Post-Workout and Recovery','Post-Workout and Recovery'),
('Pre-Workout','Pre-Workout'),
('Protein','Protein'),     
)
life_stage_choices = (
       ('Adult','Adult'),
('Child','Child'),
('Elderly','Elderly'),
)
wellbeing_supplmt_funcs_choices = (
   ('Brain & Memory','Brain & Memory'),
('Diabetic Support','Diabetic Support'),
('Digestion & Liver','Digestion & Liver'),
('Heart & Blood Pressure','Heart & Blood Pressure'),
('Immunity','Immunity'),
('Joints, Muscles & Bones','Joints, Muscles & Bones'),
('Multivitamin & Minerals','Multivitamin & Minerals'),
('Nutritional Food & Drinks','Nutritional Food & Drinks'),
('Others','Others'),
('Pregnancy Care','Pregnancy Care'),
('Sexual Health','Sexual Health'),
('Stress, Sleep, and Anxiety','Stress, Sleep, and Anxiety'),
('Vision Care','Vision Care'),    
)
medical_funcn_choices = (
('Allergy','Allergy'),
('Anti-inflammatory','Anti-inflammatory'),
('Antibacterial & Antifungal','Antibacterial & Antifungal'),
('Coughs, Colds & Flu','Coughs, Colds & Flu'),
('Eye, Nose, Throat Care','Eye, Nose, Throat Care'),
('Gastrointestinal','Gastrointestinal'),
('Others','Others'),
('Pain Relief & Fever','Pain Relief & Fever'),
)
device_comp_choices =(
       ('iOS','iOS'),
('Universal','Universal'),
)
sbf_analyzers_type_choices = (
       ('Digital','Digital'),
('Manual','Manual'),
)
injury_support_area_choices =(
       ('Back & Lumbar','Back & Lumbar'),
('Knees & Ankles','Knees & Ankles'),
('Neck & Head','Neck & Head'),
('Others','Others'),
('Wrists, Elbows & Shoulders','Wrists, Elbows & Shoulders'),
)
contact_lens_choices =(
       ('3 Months Disposable','3 Months Disposable'),
('Daily Disposable','Daily Disposable'),
('Monthly Disposable','Monthly Disposable'),
('Weekly Disposable','Weekly Disposable'),
)
lens_power_choices = (
       ('5.25+','5.25+'),
('5+','5+'),
('4.75+','4.75+'),
('4.5+','4.5+'),
('4.25+','4.25+'),
('4+','4+'),
('3.75+','3.75+'),
('3.5+','3.5+'),
('3.25+','3.25+'),
('3+','3+'),
('2.75+','2.75+'),
('2.5+','2.5+'),
('2.25+','2.25+'),
('2+','2+'),
('1.75+','1.75+'),
('1.5+','1.5+'),
('1.25+','1.25+'),
('1+','1+'),
('5.25-','5.25-'),
('5-','5-'),
('4.75-','4.75-'),
('4.5-','4.5-'),
('4.25-','4.25-'),
('4-','4-'),
('3.75-','3.75-'),
('3.5-','3.5-'),
('3.25-','3.25-'),
('3-','3-'),
('2.75-','2.75-'),
('2.5-','2.5-'),
('2.25-','2.25-'),
('2-','2-'),
('1.75-','1.75-'),
('1.5-','1.5-'),
('1.25-','1.25-'),
('1-','1-'),
)
bristle_hardness_choices = (
('Hard','Hard'),
('Medium','Medium'),
('Soft','Soft'),
)
oralcare_bene_choices = (
('Anti-Cavity','Anti-Cavity'),
('Fresh','Fresh'),
('Sensitive Gums & Teeth','Sensitive Gums & Teeth'),
('Tooth Decay','Tooth Decay'),
('Whitening','Whitening'),
)
scent_funcn_choices = (
       ('Scented','Scented'),
       ('Unscented','Unscented'),
)
flow_level_choices = (
 ('Heavy','Heavy'),
('Light','Light'),
('Maternity','Maternity'),
('Regular','Regular'),      
)
sanitary_pad_use_choices = (
       ('Day','Day'),
('Night','Night'),
)
massage_equipmt_choices = (
       ('Massage Gun','Massage Gun'),
('Others','Others'),
)
jewel_material_type_choices = (
       ('Diamond','Diamond'),
('Fabric','Fabric'),
('Jade','Jade'),
('K-Gold','K-Gold'),
('Leather','Leather'),
('Metal Coating','Metal Coating'),
('Others','Others'),
('Pearl','Pearl'),
('Platinum','Platinum'),
('Silver','Silver'),
('Steel','Steel'),
('Titanium, Bismuth & Magnet','Titanium, Bismuth & Magnet'),
('Agate','Agate'),
('Amethyst','Amethyst'),
('Crystal','Crystal'),
('Garnet','Garnet'),
('Quartz','Quartz'),
('Tiger Eye','Tiger Eye'),
)
fashion_style_choices =(
('Casual','Casual'),
('Elegant','Elegant'),
('Ethnic','Ethnic'),
('Vintage','Vintage'),
)
fashion_occasion_choices = (
       ('Anniversary','Anniversary'),
('Auspicious','Auspicious'),
('Birthday','Birthday'),
('Engagement','Engagement'),
('Wedding','Wedding'),
)
earing_style_choices = (
('Clip Earrings','Clip Earrings'),
('Drop Earrings','Drop Earrings'),
('Hook Earrings','Hook Earrings'),
('Hoop Earrings','Hoop Earrings'),
('Magnet Earrings','Magnet Earrings'),
('Others','Others'),
('Plug Earrings','Plug Earrings'),
('Stud Earrings','Stud Earrings'),
)
scarve_material_choices = (
('Canvas','Canvas'),
('Knitted','Knitted'),
('Lace','Lace'),
('Leather','Leather'),
('Others','Others'),
('Silk','Silk'),
('Wool','Wool'),
)
neckware_type_choices = (
('Others','Others'),
('Scarves','Scarves'),
('Shawls','Shawls'),
)
necklace_style_choices = (
('Bead','Bead'),
('Chain & Link','Chain & Link'),
('Charmed','Charmed'),
('Choker','Choker'),
('Others','Others'),
('Pendant','Pendant'),
)
hat_style_choices = (
('Baseball Caps','Baseball Caps'),
('Beach Hats','Beach Hats'),
('Beanies','Beanies'),
('Berets','Berets'),
('Bucket Hats','Bucket Hats'),
('Fedora','Fedora'),
('Newsboy Hats','Newsboy Hats'),
('Others','Others'),
('Snapback Caps','Snapback Caps'),
('Visors','Visors'),
)
accessories_style_choices = (
('Caps','Caps'),
('Beanies','Beanies'),
('Hats','Hats'),
('Headbands & Earpieces','Headbands & Earpieces'),
)
necklace_length_choices = (
('Long','Long'),
('Others','Others'),
('Short','Short'),
)
specs_frame_material_choices = (
('Acetate','Acetate'),
('Celluloid','Celluloid'),
('Metal','Metal'),
('Plastic','Plastic'),
('Resin','Resin'),
('Stainless Steel','Stainless Steel'),
('Titanium','Titanium'),
('Wood Texture','Wood Texture'),
)
sg_lens_type_choices = (
('UV Protection Lens','UV Protection Lens'),
('Polarised Lens','Polarised Lens'),
('Blue Light Blocking Lens','Blue Light Blocking Lens'),
)
sg_frame_shape_choices = (
('Aviators','Aviators'),
('Cat Eye / Horn','Cat Eye / Horn'),
('Clubmaster','Clubmaster'),
('Oval','Oval'),
('Over Sized','Over Sized'),
('Rectangle','Rectangle'),
('Round','Round'),
('Square','Square'),
)
frame_type_choices = (
('Full Rim','Full Rim'),
('Rimless','Rimless'),
('Semi Rimless','Semi Rimless'),
)
tie_width_choices = (
('Skinny','Skinny'),
('Standard','Standard'),
('Wide','Wide'),
)
cufflink_type_choices = (
       ('Bar','Bar'),
('Chain Link','Chain Link'),
('Silk Knot','Silk Knot'),
('Stud / Button','Stud / Button'),
('Toggle','Toggle'),
('Whale Back','Whale Back'),
)
proj_contrast_ratio_choices = (
('10000:1','10000:1'),
('20000:1','20000:1'),
('30000:1','30000:1'),
)
resolution_choices = (
('4K UHD','4K UHD'),
('8K UHD','8K UHD'),
('Full HD','Full HD'),
('HD','HD'),
('SD','SD'),
)
proj_input_conetivty_choices =( 				
('Bluetooth','Bluetooth'),
('HDMI','HDMI'),
('HDMI ARC','HDMI ARC'),
('Optical','Optical'),
('RCA','RCA'),
('Stereo','Stereo'),
('USB','USB'),
('VGA','VGA'),
('Wifi','Wifi'),
)
proj_features_choices = (			
('Build-in Audio','Build-in Audio'),
('DLP Technology','DLP Technology'),
('LCD Technology','LCD Technology'),
('Long Throw distance','Long Throw distance'),
('Portable','Portable'),
('Short Throw distance','Short Throw distance'),
('Ultra-Short Throw Distance','Ultra-Short Throw Distance'),
('Wireless','Wireless'),
)
proj_type_choices = (	
('Business Use','Business Use'),
('Home Use','Home Use'),
)
proj_brightness_choices	= (
('450Lumens','450Lumens'),
('800Lumens','800Lumens'),
('1100Lumens','1100Lumens'),
('1600Lumens','1600Lumens'),
('2600Lumens','2600Lumens'),
('5800Lumens','5800Lumens'),
)
sewing_material_choices = (
       ('Metal','Metal'),
('Others','Others'),
('Plastic','Plastic'),
)
no_of_stitche_choices = (
('10','10'),	
('12','12'),	
('20','20'),	
('50','50'),	
)
sewing_machine_feat_choices = (				
('Commercial','Commercial'),	
('Computerised','Computerised'),	
('Embroidery','Embroidery'),	
('Handheld','Handheld'),	
('Heavy Duty','Heavy Duty'),	
('Mini Portable','Mini Portable'),	
('Overlocker','Overlocker'),	
('Oversized Table','Oversized Table'),	
('Quilting','Quilting'),	
)
stitches_per_minute_choices = (					
('1000-1500 Stiches Per Minute','1000-1500 Stiches Per Minute'),	
('500-1000 Stiches Per Minute','500-1000 Stiches Per Minute'),	
('Up to 1000 Stiches Per Minute','Up to 1000 Stiches Per Minute'),	
('Up to 1300 Stiches Per Minute','Up to 1300 Stiches Per Minute'),	
('Up to 800 Stiches Per Minute','Up to 800 Stiches Per Minute'),	
('Up to 860 Stiches Per Minute','Up to 860 Stiches Per Minute'),	
)

iron_steamer_type_choices = (
('Dry Irons','Dry Irons'),
('Garment Steamers','Garment Steamers'),
('Others','Others'),
('Steam Generator Irons','Steam Generator Irons'),
('Steam Irons','Steam Irons'),
)						
soleplate_type_choices = (			
('Ceramic','Ceramic'),
('Coated non-stick','Coated non-stick'),
('Linished (non-coated)','Linished (non-coated)'),
('Others','Others'),
('Peraluman','Peraluman'),
('Premium multi-layer coating','Premium multi-layer coating'),
('Stainless Steel','Stainless Steel'),
)			
iron_features_choices	= (			
('Anti-Burn','Anti-Burn'),
('Auto Shut-Off','Auto Shut-Off'),
('Carry Lock','Carry Lock'),
('Detachable Water Tank','Detachable Water Tank'),
('Drip Stop','Drip Stop'),
('Eco Mode','Eco Mode'),
('Self-Cleaning','Self-Cleaning'),
('Spray','Spray'),
('Steam','Steam'),
('Temperature Control','Temperature Control'),
)


air_flow_choices = (
('350CFM','350CFM'),
('900CFM','900CFM'),
('600CFM','600CFM'),
('1000m³/h','1000m³/h'),
('750m³/h','750m³/h'),
('500m³/h','500m³/h'),
)			
air_purifier_filtn_type_choices	= (		
('Electrostatic','Electrostatic'),
('HEPA Filter','HEPA Filter'),
('Ionizer','Ionizer'),
('ULPA','ULPA'),
)
cadr_rating_choices = (
('200CFM','200CFM'),
('300CFM','300CFM'),
('400CFM','400CFM'),
('500CFM','500CFM'),
)
noise_level_choices = (	
('30dB','30dB'),
('40dB','40dB'),
('50dB','50dB'),
('60dB','60dB'),
)	
air_purifier_features_choices = (
('Anti-Allergy','Anti-Allergy'),
('Anti-Bacteria','Anti-Bacteria'),
('Anti-Odor','Anti-Odor'),
('Anti-virus','Anti-virus'),
('App Control','App Control'),
('Dehumidifier','Dehumidifier'),
('Energy Saving Mode','Energy Saving Mode'),
('HEPA','HEPA'),
('Humidifier','Humidifier'),
('Ionizer','Ionizer'),
('Mosquito Catcher','Mosquito Catcher'),
('Washable Filter','Washable Filter'),
)
max_moisture_removal_choices = (
('500ml/day','500ml/day'),
('1000ml/day','1000ml/day'),
('1500ml/day','1500ml/day'),
)

vacuum_cleaner_funcn_choices =(				
('Anti-Dust Mite Vacuums','Anti-Dust Mite Vacuums'),
('Others','Others'),
('Wet & Dry Vacuums','Wet & Dry Vacuums'),)
run_time_choices = (				
('60mins','60mins'),
('90mins','90mins'),
('120mins','120mins'),
('150mins','150mins'),
('180mins','180mins'),
)
airwatts_choices = (				
('100Airwatts','100Airwatts'),
('150Airwatts','150Airwatts'),
('220Airwatts','220Airwatts'),
('115Airwatts','115Airwatts'),
)
cord_length_choices = (
('2m','2m'),
('2.5m','2.5m'),
('3m','3m'),
)	
suction_power_choices = (			
('18000Pa','18000Pa'),
('19000Pa','19000Pa'),
('8000Pa','8000Pa'),
('12000Pa','12000Pa'),
)
robot_vacuum_featrs_choices = ( 			
('Anti-Collision','Anti-Collision'),
('App Control','App Control'),
('Automatic Dirt Disposal','Automatic Dirt Disposal'),
('Automatic Recharge','Automatic Recharge'),
('Gyroscope','Gyroscope'),
('HEPA Filter','HEPA Filter'),
('Infrared','Infrared'),
('Mopping','Mopping'),
('Multiple Cleaning modes','Multiple Cleaning modes'),
('Remote control','Remote control'),
('Smart Navigation','Smart Navigation'),
('Smart Sensor','Smart Sensor'),
('Voice Control','Voice Control'),
('Add a new','Add a new'),
)
vacuum_clnr_featrs_choices	= (			
('360° Suction Nozzle','360° Suction Nozzle'),
('Bagged','Bagged'),
('Bagless','Bagless'),
('Blower','Blower'),
('Detachable Handheld','Detachable Handheld'),
('Dustmite Attachment Head','Dustmite Attachment Head'),
('Rechargeable Battery','Rechargeable Battery'),
('Removable Battery','Removable Battery'),
('Roller Brush','Roller Brush'),
('UV Light','UV Light'),
('Wheels','Wheels'),
('HEPA Filtration','HEPA Filtration'),
)
corded_or_cordless_choices = (			
('Corded','Corded'),
('Cordless','Cordless'),
)
vc_floor_care_choices	= (			
('Cannister Vacuums','Cannister Vacuums'),
('Electric Brooms & Mops','Electric Brooms & Mops'),
('Floor Polishers','Floor Polishers'),
('Handheld Vacuums','Handheld Vacuums'),
('Others','Others'),
('Robot Vacuums','Robot Vacuums'),
('Steam Cleaners','Steam Cleaners'),
('Stick Vacuums','Stick Vacuums'),
('1500ml/day','1500ml/day'),
)

wm_type_choices = (				
('Front Load','Front Load'),
('Others','Others'),
('Top Load','Top Load'),
('Twin Tub','Twin Tub'),
)
wm_features_choices	= (			
('Automatic dispenser','Automatic dispenser'),
('Automatic temperature control','Automatic temperature control'),
('Bleach Dispenser','Bleach Dispenser'),
('Fuzzy Logic','Fuzzy Logic'),
('Manual Dispenser','Manual Dispenser'),
('Soap Dispenser','Soap Dispenser'),
)
spin_speed_choices	= (			
('1400RPM','1400RPM'),
('1500RPM','1500RPM'),
('800RPM','800RPM'),
('600RPM','600RPM'),
)
washing_features_choices = (				
('Anti-Allergy','Anti-Allergy'),
('Delicates','Delicates'),
('Extra rinse cycle','Extra rinse cycle'),
('Handwash','Handwash'),
('Large Capacity','Large Capacity'),
('Quick Wash','Quick Wash'),
('Quiet Operation','Quiet Operation'),
('Shoe Washing','Shoe Washing'),
('Spin Dry','Spin Dry'),
('Steam washing','Steam washing'),
)
motor_type_choices = (				
('Fixed Frequency Motor','Fixed Frequency Motor'),
('Inverter Motor','Inverter Motor'),
)
WELS_tick_rating_choices = (
       ('0 Tick','0 Tick'),
('1 Tick','1 Tick'),
('2 Ticks','2 Ticks'),
('3 Ticks','3 Ticks'),
)
wh_type_choices = (
      ('Instant' , 'Instant'),
('Storage','Storage'),
)

tv_screen_type_choices = (				
('LCD/ LED','LCD/ LED'),
('OLED','OLED'),
('Others','Others'),
('QLED','QLED'),
)
tv_screen_size_choices = (			
('< 33 Inches','< 33 Inches'),
('> 60 Inches','> 60 Inches'),
('33 - 39 Inches','33 - 39 Inches'),
('40 - 49 Inches','40 - 49 Inches'),
('50 - 60 Inches','50 - 60 Inches'),
)
tv_type_choices = (			
('Analog TV','Analog TV'),
('Digital TV','Digital TV'),
('Smart TV','Smart TV'),
)
tv_features_choices = (				
('Bluetooth Connectivity','Bluetooth Connectivity'),
('Cinema 3D','Cinema 3D'),
('Curved TV','Curved TV'),
('DTS Audio','DTS Audio'),
('HDR','HDR'),
('Mobile Screen Mirroring','Mobile Screen Mirroring'),
('Netflix','Netflix'),
('Voice Control','Voice Control'),
('Web Browser','Web Browser'),
('Wireless Connectivity','Wireless Connectivity'),
('Youtube','Youtube'),
)
tv_port_input_choices = (				
('Audio Out (Mini Jack)','Audio Out (Mini Jack)'),
('Component in (Y/PB/Pr)','Component in (Y/PB/Pr)'),
('Composite in (AV)','Composite in (AV)'),
('Digital Audio Out(Optical)','Digital Audio Out(Optical)'),
('Ethernet (LAN)','Ethernet (LAN)'),
)
antenna_type_choices = (
('Indoor','Indoor'),
('Indoor & Outdoor','Indoor & Outdoor'),
('Outdoor','Outdoor'),
)
receiver_type_choices	= (			
('Digital','Digital'),
('Satellite','Satellite'),
)
tv_mount_feature_choices = (
('Ceiling','Ceiling'),
('Fixed Wall','Fixed Wall'),
('Full Motion','Full Motion'),
('Tilt','Tilt'),
('TV Stand','TV Stand'),
)
water_disp_features_choices = (				
('Child Lock','Child Lock'),
('Cold Water','Cold Water'),
('Fast Heating','Fast Heating'),
('Hot Water','Hot Water'),
('Self-Cleaning','Self-Cleaning'),
('Temperature Select','Temperature Select'),
('Water Purification','Water Purification'),
)			
water_purifn_choices = (				
('Activated Carbon','Activated Carbon'),
('Conditioner','Conditioner'),
('Distiller','Distiller'),
('Gravity Micro Filtration','Gravity Micro Filtration'),
('Ion Exchange Resin','Ion Exchange Resin'),
('Ionizer','Ionizer'),
('Ozone Water Purifier','Ozone Water Purifier'),
('Reverse Osmosis','Reverse Osmosis'),
('Ultrafiltration','Ultrafiltration'),
)
water_disp_type_choices	= (			
('Desktop','Desktop'),
('Freestanding','Freestanding'),
)
kettle_material_choices = (
       ('Aluminum','Aluminum'),
('Ceramic','Ceramic'),
('Copper','Copper'),
('Glass','Glass'),
('Others','Others'),
('Plastic','Plastic'),
('Stainless Steel','Stainless Steel'),
('Cast Iron','Cast Iron'),
)
kettle_features_choices	= (			
('Cold Touch','Cold Touch'),
('Cordless','Cordless'),
('Detachable Lid','Detachable Lid'),
('Fast Boil','Fast Boil'),
('Keep Warm','Keep Warm'),
('Lid Release Button','Lid Release Button'),
('Overheat Protection','Overheat Protection'),
('Removable Filter','Removable Filter'),
('Swivel Base','Swivel Base'),
('Temperature Select','Temperature Select'),
('Washable Anti-Scale Filter','Washable Anti-Scale Filter'),
('Water Indicator','Water Indicator'),
)
blender_type_choices	= (			
('Bullet Blender','Bullet Blender'),
('Commercial Blender','Commercial Blender'),
('Countertop Blender','Countertop Blender'),
('Portable Blender','Portable Blender'),
('Stick Blender','Stick Blender'),
)
blender_features_choices = (				
('Detachable Blades','Detachable Blades'),
('Ice Crushing','Ice Crushing'),
('Nutrition Extraction','Nutrition Extraction'),
('Variable speeds','Variable speeds'),
)
juicer_features_choices	= (			
('Anti-slip feet','Anti-slip feet'),
('Dishwasher Safe','Dishwasher Safe'),
('Knob Control','Knob Control'),
('Oversize Feeder Mouth','Oversize Feeder Mouth'),
('Pulp Control','Pulp Control'),
('Reverse Speed','Reverse Speed'),
('Safety Lock','Safety Lock'),
('Smart Control','Smart Control'),
('Thermal Cut-off Protection','Thermal Cut-off Protection'),
('Variable speeds','Variable speeds'),
('Whole Fruit Juicer','Whole Fruit Juicer'),
)
juicer_type_choices = (				
('Centrifugal juicers','Centrifugal juicers'),
('Citrus Juicer','Citrus Juicer'),
('Slow/Cold Juicer','Slow/Cold Juicer'),
)
cm_type_choices = (				
('Automatic Espresso Machine','Automatic Espresso Machine'),
('Capsule Coffee Machine','Capsule Coffee Machine'),
('Coffee Grinder','Coffee Grinder'),
('Drip Coffee Maker','Drip Coffee Maker'),
('Milk Frother','Milk Frother'),
('Others','Others'),
('Portable Coffee Machine','Portable Coffee Machine'),
('Semi-Automatic Espresso Machine','Semi-Automatic Espresso Machine'),
('Super-Automatic Espresso Machine','Super-Automatic Espresso Machine'),
)
cm_capacity_choices	= (			
('12 Cups & Above','12 Cups & Above'),
('5 to 8 Cups','5 to 8 Cups'),
('9 to 11 Cups','9 to 11 Cups'),
('Up to 4 Cups','Up to 4 Cups'),
)
cm_features_choices	= (			
('Coffee Grinder','Coffee Grinder'),
('Descaling','Descaling'),
('Milk System','Milk System'),
('Programmable','Programmable'),
('Smart Control','Smart Control'),
('Timer','Timer'),
)
mixer_features_choices	= (			
('Dought','Dought'),
('Fold','Fold'),
('Pouring Shield','Pouring Shield'),
('Rotating Bowl','Rotating Bowl'),
('Soft Start','Soft Start'),
('Speed Control','Speed Control'),
('Whisk','Whisk'),
)
mixer_type_choices = (
('Stand Mixer','Stand Mixer'),
('Hand Mixer','Hand Mixer'),
)
stove_type_choices = (				
('Electricity / Induction / Infra-red','Electricity / Induction / Infra-red'),
('Gas','Gas'),
('Others','Others'),
)
burner_type_choices = (				
('Electrical Induction','Electrical Induction'),
('Gas','Gas'),
)
ic_features_choices  = (				
('Child Lock','Child Lock'),
('Cool Touch','Cool Touch'),
('Digital Control','Digital Control'),
('Easy Clean','Easy Clean'),
('Induction Cooker Features','Induction Cooker Features'),
('Keep Warm','Keep Warm'),
('Precise Temperature Control','Precise Temperature Control'),
('Smart Control','Smart Control'),
('Timer','Timer'),
)
no_of_burners_choices	 = (			
('1','1'),
('2','2'),
('3','3'),
('4','4'),
)
air_fryer_features_choices	 = (			
('App Control','App Control'),
('Favorite Setting Save','Favorite Setting Save'),
('Keep Warm','Keep Warm'),
('Knob Control','Knob Control'),
('LED Display','LED Display'),
('Non-Stick','Non-Stick'),
('Pre-set Menu','Pre-set Menu'),
('Pre-set Timer','Pre-set Timer'),
('Temperature Control','Temperature Control'),
('Touch Control','Touch Control'),
)
mwave_type_choices  = (			
('Built-in','Built-in'),
('Countertop','Countertop'),
('Over-the-Range','Over-the-Range'),
)
mwave_features_choices  = (				
('App Control','App Control'),
('Convection','Convection'),
('Deodorizer','Deodorizer'),
('Easy Clean','Easy Clean'),
('Flat Table','Flat Table'),
('Grill','Grill'),
('Non-Stick','Non-Stick'),
('Quick Defrost','Quick Defrost'),
('Stainless steel','Stainless steel'),
('Steam','Steam'),
('Tempered Glass Top','Tempered Glass Top'),
('Touch Control','Touch Control'),
)
oven_features_choices  = (			
('Convection','Convection'),
('Cool Touch','Cool Touch'),
('Digital Control','Digital Control'),
('Digital Display','Digital Display'),
('Easy Cleaning','Easy Cleaning'),
('Mechanical Control','Mechanical Control'),
('Removable Trays','Removable Trays'),
('Smart Control','Smart Control'),
('Timer','Timer'),
)
meat_grinder_choices  = (			
('Electric','Electric'),
('Manual','Manual'),
)
food_proce_sets_choices = (				
('Variable (Manual)','Variable (Manual)'),
('7 Speed + Pulse','7 Speed + Pulse'),
('6 Speed + Pulse','6 Speed + Pulse'),
('5 speed + Pulse','5 speed + Pulse'),
('4 speed + Pulse','4 speed + Pulse'),
('3 speed + Pulse','3 speed + Pulse'),
('2 speed + Pulse','2 speed + Pulse'),
('1 speed + Pulse','1 speed + Pulse'),
('>7 Speed + Pulse','>7 Speed + Pulse'),
)
mf_cooker_material_choices	= (			
('Aluminum','Aluminum'),
('Anodized Aluminum','Anodized Aluminum'),
('Ceramic','Ceramic'),
('Clay','Clay'),
('Coated','Coated'),
('Multi-Layer','Multi-Layer'),
('Non-coated','Non-coated'),
('Others','Others'),
('Stainless Steel','Stainless Steel'),
)
pres_cookr_features_choices	= (			
('Easy Clean','Easy Clean'),
('Keep Warm','Keep Warm'),
('LED Panel','LED Panel'),
('Pre-set Menu','Pre-set Menu'),
('Saute/ Sear','Saute/ Sear'),
('Slow Cook','Slow Cook'),
('Timer','Timer'),
)
rice_cook_features_choices	= (			
('Aluminium Inner Pot','Aluminium Inner Pot'),
('Detachable Steam Vent','Detachable Steam Vent'),
('Easy Clean Design','Easy Clean Design'),
('Fast Cooking','Fast Cooking'),
('Keep Warm Function','Keep Warm Function'),
('Non-stick Coating','Non-stick Coating'),
('Porridge','Porridge'),
('Pre-set Timer','Pre-set Timer'),
('Stainless Steel Cover','Stainless Steel Cover'),
)
no_of_people_choices	= (			
('2','2'),
('4','4'),
('6','6'),
('8','8'),
('10','10'),
)
rice_cooker_type_choices	= (			
('Digital','Digital'),
('Others','Others'),
)
cooling_system_type_choices	= (			
('Auto Defrost','Auto Defrost'),
('Manual Defrost','Manual Defrost'),
('No Frost','No Frost'),
)
energy_tick_rating_choices	= (			
('1 Tick','1 Tick'),
('2 Ticks','2 Ticks'),
('3 Ticks','3 Ticks'),
('4 Ticks','4 Ticks'),
('5 Ticks','5 Ticks'),
)
refri_features_choices = (				
('Adjustable Shelves','Adjustable Shelves'),
('Automatic Ice-Maker','Automatic Ice-Maker'),
('Built-in Filter','Built-in Filter'),
('Built-in Water Dispenser','Built-in Water Dispenser'),
('Door in Door','Door in Door'),
('Reversible Doors','Reversible Doors'),
('Showcase Door','Showcase Door'),
('Wifi Connected','Wifi Connected'),
)
refrig_motor_type_choices	= (			
('Fixed Frequency Motor','Fixed Frequency Motor'),
('Inverter Motor','Inverter Motor'),
)
refrige_type_choices	= (			
('Compact / Mini','Compact / Mini'),
('Others','Others'),
('Side-by-side','Side-by-side'),
('Single Door','Single Door'),
('Two-Door','Two-Door'),
)
freezer_type_choices	= (			
('Built-in','Built-in'),
('Chest','Chest'),
('Mini','Mini'),
('Upright','Upright'),
)
hood_features_choices = (				
('Charcoal Filter','Charcoal Filter'),
('Grease Filter','Grease Filter'),
('LED Light','LED Light'),
('Retractable','Retractable'),
('Smart Control','Smart Control'),
('Speed Control','Speed Control'),
('Touch Control','Touch Control'),
('Washable Filter','Washable Filter'),
)
hood_mount_type_choices = (				
('Island Mount','Island Mount'),
('Under Cabinet','Under Cabinet'),
('Wall Mount','Wall Mount'),
)
cord_length_choices	= (			
('2m','2m'),
('2.5m','2.5m'),
('3m','3m'),
)
house_alarm_type_choices = (				
('Door Sensor','Door Sensor'),
('Entry Alarm','Entry Alarm'),
('Home Security System','Home Security System'),
('Motion Sensor','Motion Sensor'),
('Water Leakage Sensor','Water Leakage Sensor'),
)
alarm_volume_choices	= (			
('65dB','65dB'),
('95dB','95dB'),
('120dB','120dB'),
)
battery_capacity_msment_choices	= (			
('mAh','mAh'),
('cell','cell'),
('Wh','Wh'),
)
rbattery_type_choices = (				
('Lead Acid Gel','Lead Acid Gel'),
('Lithium-ion (Li-ion)','Lithium-ion (Li-ion)'),
('Nickel-Cadmium (NiCd)','Nickel-Cadmium (NiCd)'),
('Nickel-Metal Hydride (NiMH)','Nickel-Metal Hydride (NiMH)'),
)
nr_bat_type_choices	= (			
('Alkaline','Alkaline'),
('Carbon Zinc','Carbon Zinc'),
('Lithium (Primary)','Lithium (Primary)'),
('Mercury','Mercury'),
('Silver Oxide','Silver Oxide'),
('Zinc Air','Zinc Air'),
)
battery_size_choices	= (			
('3V','3V'),
('6V','6V'),
('9V','9V'),
('AA','AA'),
('AAA','AAA'),
('C','C'),
('D','D'),
('357','357'),
('377','377'),
('392','392'),
)

class Specification(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        fourth_level_category = models.ForeignKey(Fourth_Level_Category,on_delete=models.CASCADE, blank=True,null=True)
        sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE, blank=True,null=True)
        category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True,null=True)
        brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
        crepped_top = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True)
        prod_style = models.CharField(max_length=50,choices=prod_style_choices, blank=True,null=True)
        top_length = models.CharField(max_length=50,choices=length_choices, blank=True,null=True)
        season =  models.CharField(max_length=50,choices=Season_choices, blank=True,null=True)
        plus_size = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True)
        material = models.CharField(max_length=50,choices=material_choices, blank=True,null=True)
        petite = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True)
        origin_country = models.CharField(max_length=50, blank=True,null=True)
        pattern = models.CharField(max_length=50,choices=pattern_choices, blank=True,null=True)
        sleeve_length = models.CharField(max_length=50,choices=sleeve_length_choices, blank=True,null=True)
        length = models.CharField(max_length=50,null=True,blank=True)
        neckline = models.CharField(max_length=50,choices=neckline_choices, blank=True,null=True)
        occasion = models.CharField(max_length=50,choices=occasion_choices, blank=True,null=True)
        waist_height = models.CharField(max_length=50,choices=waist_height_choices, blank=True,null=True)
        bottoms_length = models.CharField(max_length=50,choices=bottoms_length_choices, blank=True,null=True)
        bottoms_fit_type = models.CharField(max_length=50,choices=bottoms_fit_type_choices, blank=True,null=True)
        dress_skirt_style = models.CharField(max_length=50,choices=dress_skirt_style_choices, blank=True,null=True)
        dress_skirt_length = models.CharField(max_length=50,choices=dress_skirt_length_choices, blank=True,null=True)
        jacket_type = models.CharField(max_length=50,choices=jacket_type_choices, blank=True,null=True)
        overalls_type = models.CharField(max_length=50,choices=overalls_type_choices, blank=True,null=True)
        outerwear_length = models.CharField(max_length=50,choices=outerwear_length_choices, blank=True,null=True)
        apparel_type = models.CharField(max_length=50,choices=apparel_type_choices, blank=True,null=True)
        bra_style = models.CharField(max_length=50,choices=bra_style_choices, blank=True,null=True)
        pack_type = models.CharField(max_length=50,choices=pack_type_choices, blank=True,null=True)
        bra_type = models.CharField(max_length=50,choices=bra_type_choices, blank=True,null=True)
        sexy_lingerie_style = models.CharField(max_length=50,choices=sexy_lingerie_style_choices, blank=True,null=True)
        bra_coverage = models.CharField(max_length=50,choices=bra_coverage_choices, blank=True,null=True)
        panty_style = models.CharField(max_length=50,choices=panty_style_choices, blank=True,null=True)
        panties_type = models.CharField(max_length=50,choices=panties_type_choices, blank=True,null=True)
        shaper_style = models.CharField(max_length=50,choices=shaper_style_choices, blank=True,null=True)
        bottom_style = models.CharField(max_length=50,choices=bottom_style_choices, blank=True,null=True)
        pack_size = models.CharField(max_length=50,choices=pack_choices, blank=True,null=True)
        access_type = models.CharField(max_length=50,choices=access_choices, blank=True,null=True)
        socks_length = models.CharField(max_length=50,choices=socks_length_choices, blank=True,null=True)
        socks_type = models.CharField(max_length=50,choices=socks_type_choices, blank=True,null=True)
        pantyhose_type = models.CharField(max_length=50,choices=pantyhose_choices, blank=True,null=True)
        Weddding_dress_style = models.CharField(max_length=50,choices=Wed_dress_style_choices, blank=True,null=True)
        costume_theme = models.CharField(max_length=50,choices=costume_theme_choices, blank=True,null=True)
        tall_fit = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True)
        button_style = models.CharField(max_length=50,choices=buttons_style_choices, blank=True,null=True)
        leather_type = models.CharField(max_length=50,choices=leather_type_choices, blank=True,null=True)
        collar_type = models.CharField(max_length=50,choices=collar_type_choices, blank=True,null=True)
        top_fit_style = models.CharField(max_length=50,choices=top_fit_style_choices, blank=True,null=True)
        vent_style =  models.CharField(max_length=50,choices=vent_style_choices, blank=True,null=True)
        suit_style = models.CharField(max_length=50,choices=suit_style_choices, blank=True,null=True) 
        EAN = models.CharField(max_length=50,null=True,blank=True)
        fly_type = models.CharField(max_length=50,choices=fly_type_choices, blank=True,null=True)
        cuff_type = models.CharField(max_length=50,choices=cuff_type_choices, blank=True,null=True)
        underwear_type = models.CharField(max_length=50,choices=underwear_type_choices, blank=True,null=True)
        shorts_type = models.CharField(max_length=50,choices=shorts_type_choices, blank=True,null=True)
        towel_robe_fabric  = models.CharField(max_length=50,choices=towel_robe_fabric_choices, blank=True,null=True)
        ingredient  = models.CharField(max_length=500, blank=True,null=True)
        igredient_preference  = models.CharField(max_length=50,choices=igredient_preference_choices, blank=True,null=True)
        formulation  = models.CharField(max_length=50,choices=formulation_choices, blank=True,null=True)
        nutrient_type = models.CharField(max_length=50,choices=nutrient_type_choices, blank=True,null=True) 
        expiry_date = models.DateTimeField(blank=True,null=True)
        bodycare_benefits = models.CharField(max_length=50,choices=bodycare_benefits_choices, blank=True,null=True)
        volume = models.CharField(max_length=50,choices=volume_choices, blank=True,null=True)
        HSA_notification_no =  models.CharField(max_length=100, blank=True,null=True)
        shelf_life =  models.CharField(max_length=50,choices=shelflife_choices, blank=True,null=True)
        scrub_formulation =  models.CharField(max_length=50,choices=scrub_formulation_choices, blank=True,null=True)
        skin_type =  models.CharField(max_length=50,choices=skin_type_choices, blank=True,null=True)
        product_size =  models.CharField(max_length=50,choices=product_size_choices, blank=True,null=True)
        application_area =  models.CharField(max_length=50,choices=application_area_choices, blank=True,null=True)
        weight =  models.CharField(max_length=50,choices=weight_choices, blank=True,null=True)
        handwash_pack_size =   models.CharField(max_length=50, blank=True,null=True)
        handwash_packsize_measure = models.CharField(max_length=50,choices=handwash_packsize_choices, blank=True,null=True)
        handwash_formulation =  models.CharField(max_length=50,choices=handwash_formulation_choices, blank=True,null=True)
        quantity = models.CharField(max_length=50, blank=True,null=True)
        production_batch_number =   models.CharField(max_length=50, blank=True,null=True)
        manufacturer_or_trader_name  =   models.CharField(max_length=50, blank=True,null=True)
        INVIMA_certification =   models.CharField(max_length=50, blank=True,null=True)
        FDA_registration_no  =   models.CharField(max_length=50, blank=True,null=True)
        manufacturer_or_trader_address  =   models.CharField(max_length=250, blank=True,null=True)
        warranty_duration  =  models.CharField(max_length=50,choices=warranty_duration_choices, blank=True,null=True)
        warranty_type  =  models.CharField(max_length=50,choices=warranty_type_choices, blank=True,null=True)
        hair_care_benefits =  models.CharField(max_length=50,choices=hair_care_benefits_choices, blank=True,null=True)
        packaging_type =  models.CharField(max_length=50,choices=packaging_type_choices, blank=True,null=True)
        shampoo_formulation = models.CharField(max_length=50,choices=shampoo_formulation_choices, blank=True,null=True)
        scent = models.CharField(max_length=50,choices=scent_choices, blank=True,null=True)
        shave_gel_or_cream_appn_area  = models.CharField(max_length=50,choices=shavegel_appn_area_choices, blank=True,null=True)
        makeup_furmulation  = models.CharField(max_length=50,choices=makeup_furmulation_choices, blank=True,null=True)
        skin_tone  = models.CharField(max_length=50,choices=skin_tone_choices, blank=True,null=True)
        SPF_choices  = models.CharField(max_length=50,choices=SPF_choices, blank=True,null=True)
        foundation_coverage  = models.CharField(max_length=50,choices=foundn_coverg_choices, blank=True,null=True)
        makeup_finish =  models.CharField(max_length=50,choices=makeup_finish_choices, blank=True,null=True)
        bb_or_cc_scare_benefits =  models.CharField(max_length=50,choices=cc_scare_bene_choices, blank=True,null=True)
        waterproof =  models.CharField(max_length=50,choices=yn_choices, blank=True,null=True)
        mascara_benefits =  models.CharField(max_length=50,choices=mascara_ben_chioces, blank=True,null=True)
        lip_benefits  =  models.CharField(max_length=50,choices=lip_benefit_choices, blank=True,null=True)
        facial_steamer_skincare_benefits =  models.CharField(max_length=50,choices=face_steamr_bene_choices, blank=True,null=True)
        power_source =  models.CharField(max_length=50,choices=power_source_choces, blank=True,null=True)
        safety_mark  = models.CharField(max_length=50,null=True,blank=True)
        mask_type =  models.CharField(max_length=50,choices=mask_type_choices, blank=True,null=True)
        hair_finish =  models.CharField(max_length=50,choices=hair_finish_choices, blank=True,null=True)
        tool_function =  models.CharField(max_length=50,choices=tool_function_choices, blank=True,null=True)
        cleanser_type =  models.CharField(max_length=50,choices=cleanser_type_choices, blank=True,null=True)
        acne_treatment_type = models.CharField(max_length=50,choices=acne_tment_type_choices, blank=True,null=True)
        lotion_type = models.CharField(max_length=50,choices=lotion_type_choices, blank=True,null=True)
        fragrance_concentration = models.CharField(max_length=50,choices=fragrance_concn_choices, blank=True,null=True)
        gender = models.CharField(max_length=50,choices=gender_choices, blank=True,null=True)
        specialty_diet = models.CharField(max_length=50,choices=specialty_diet_choices, blank=True,null=True)
        food_type = models.CharField(max_length=50,choices=food_type_choices, blank=True,null=True)
        weight_mgmt_supplement_functions= models.CharField(max_length=50,choices=weight_mgmt_supplt_funs_choices, blank=True,null=True)
        consumables_form = models.CharField(max_length=50,choices=consumables_form_choices, blank=True,null=True)
        flavour = models.CharField(max_length=50,choices=flavour_choices, blank=True,null=True)
        beauty_supplement_funcns = models.CharField(max_length=50,choices=beauty_supplmt_funcs_choices, blank=True,null=True)
        fitness_supplement_funcns = models.CharField(max_length=50,choices=fitness_supplmt_funcs_choices, blank=True,null=True)
        life_stage = models.CharField(max_length=50,choices=life_stage_choices, blank=True,null=True)
        wellbeing_supplement_funcns = models.CharField(max_length=50,choices=wellbeing_supplmt_funcs_choices, blank=True,null=True)
        medical_functions = models.CharField(max_length=50,choices=medical_funcn_choices, blank=True,null=True)
        device_compatibility =  models.CharField(max_length=50,choices=device_comp_choices, blank=True,null=True)
        scale_and_body_fat_analyzers_type =  models.CharField(max_length=50,choices=sbf_analyzers_type_choices, blank=True,null=True)
        injury_support_area=  models.CharField(max_length=50,choices=injury_support_area_choices, blank=True,null=True)
        contact_lens_type = models.CharField(max_length=50,choices=contact_lens_choices, blank=True,null=True)
        lens_power = models.CharField(max_length=50,choices=lens_power_choices, blank=True,null=True)
        bristle_hardness = models.CharField(max_length=50,choices=bristle_hardness_choices, blank=True,null=True) 
        oral_care_benefits = models.CharField(max_length=50,choices=oralcare_bene_choices, blank=True,null=True) 
        wings = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True) 
        scent_function = models.CharField(max_length=50,choices=scent_funcn_choices, blank=True,null=True) 
        flow_level = models.CharField(max_length=50,choices=flow_level_choices, blank=True,null=True) 
        sanitary_pad_use = models.CharField(max_length=50,choices=sanitary_pad_use_choices, blank=True,null=True) 
        electrical_device = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True) 
        massage_equipment_type = models.CharField(max_length=50,choices=massage_equipmt_choices, blank=True,null=True) 
        NEA_registration_no = models.CharField(max_length=50, blank=True,null=True)
        jewellery_material_type = models.CharField(max_length=50,choices=jewel_material_type_choices, blank=True,null=True) 
        accessories_set = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True) 
        fashion_style = models.CharField(max_length=50,choices=fashion_style_choices, blank=True,null=True) 
        fashion_occasion = models.CharField(max_length=50,choices=fashion_occasion_choices, blank=True,null=True) 
        couple_accessories = models.CharField(max_length=50,choices=yn_choices, blank=True,null=True) 
        earing_style =  models.CharField(max_length=50,choices=earing_style_choices, blank=True,null=True) 
        scarve_or_shawl_material =  models.CharField(max_length=50,choices=scarve_material_choices, blank=True,null=True) 
        neckware_type   =  models.CharField(max_length=50,choices=neckware_type_choices, blank=True,null=True) 
        necklace_bracelet_style =  models.CharField(max_length=50,choices=necklace_style_choices, blank=True,null=True) 
        hat_style =  models.CharField(max_length=50,choices=hat_style_choices, blank=True,null=True) 
        accessories_style =  models.CharField(max_length=50,choices=accessories_style_choices , blank=True,null=True) 
        necklace_length = models.CharField(max_length=50,choices=necklace_length_choices , blank=True,null=True) 
        specs_frame_material = models.CharField(max_length=50,choices=specs_frame_material_choices , blank=True,null=True) 
        sunglass_lens_type = models.CharField(max_length=50,choices=sg_lens_type_choices , blank=True,null=True) 
        sg_frame_shape  = models.CharField(max_length=50,choices=sg_frame_shape_choices , blank=True,null=True) 
        frame_type = models.CharField(max_length=50,choices=frame_type_choices , blank=True,null=True) 
        tie_width = models.CharField(max_length=50,choices=tie_width_choices , blank=True,null=True) 
        cufflink_type = models.CharField(max_length=50,choices=cufflink_type_choices , blank=True,null=True) 
        projector_contrast_ratio =  models.CharField(max_length=50,choices=proj_contrast_ratio_choices , blank=True,null=True) 
        resolution  =  models.CharField(max_length=50,choices=resolution_choices , blank=True,null=True) 
        projector_input_conetivty = models.CharField(max_length=50,choices=proj_input_conetivty_choices , blank=True,null=True) 
        projector_features = models.CharField(max_length=50,choices=proj_features_choices , blank=True,null=True) 
        projector_type = models.CharField(max_length=50,choices=proj_type_choices , blank=True,null=True) 
        projector_brightness	= models.CharField(max_length=50,choices=proj_brightness_choices , blank=True,null=True) 
        input_voltage_in_V = models.CharField(max_length=50,null=True,blank=True)
        power_vonsumption_in_W = models.CharField(max_length=50,null=True,blank=True)
        dimension_LxWxH = models.CharField(max_length=50,null=True,blank=True)
        sewing_machine_material = models.CharField(max_length=50,choices=sewing_material_choices , blank=True,null=True) 
        no_of_stitches = models.CharField(max_length=50,choices=no_of_stitche_choices , blank=True,null=True) 
        sewing_machine_features = models.CharField(max_length=50,choices=sewing_machine_feat_choices , blank=True,null=True) 
        stitches_per_minute = models.CharField(max_length=50,choices=stitches_per_minute_choices , blank=True,null=True) 
        iron_steamer_type = models.CharField(max_length=50,choices=iron_steamer_type_choices , blank=True,null=True) 				
        soleplate_type = models.CharField(max_length=50,choices=soleplate_type_choices , blank=True,null=True) 		
        iron_features = models.CharField(max_length=50,choices=iron_features_choices , blank=True,null=True) 
        air_flow = models.CharField(max_length=50,choices=air_flow_choices , blank=True,null=True) 
        air_purifier_filtration_type = models.CharField(max_length=50,choices=air_purifier_filtn_type_choices , blank=True,null=True) 
        cadr_rating = models.CharField(max_length=50,choices=cadr_rating_choices , blank=True,null=True) 
        noise_level = models.CharField(max_length=50,choices=noise_level_choices , blank=True,null=True) 
        air_purifier_features = models.CharField(max_length=50,choices=air_purifier_features_choices , blank=True,null=True) 
        room_size_m2 = models.CharField(max_length=50,null=True,blank=True)
        max_moisture_removal = models.CharField(max_length=50,choices=max_moisture_removal_choices , blank=True,null=True) 
        vacuum_cleaner_funcn = models.CharField(max_length=50,choices=vacuum_cleaner_funcn_choices , blank=True,null=True) 
        run_time= models.CharField(max_length=50,choices=run_time_choices , blank=True,null=True) 
        airwatts = models.CharField(max_length=50,choices=airwatts_choices , blank=True,null=True) 
        cord_length = models.CharField(max_length=50,choices=cord_length_choices , blank=True,null=True) 
        suction_power = models.CharField(max_length=50,choices=suction_power_choices , blank=True,null=True) 
        robot_vacuum_featrs = models.CharField(max_length=50,choices=robot_vacuum_featrs_choices , blank=True,null=True) 
        vacuum_clnr_featrs = models.CharField(max_length=50,choices=vacuum_clnr_featrs_choices , blank=True,null=True) 
        corded_or_cordless = models.CharField(max_length=50,choices=corded_or_cordless_choices , blank=True,null=True) 
        vaccume_cleaner_floor_care = models.CharField(max_length=50,choices=vc_floor_care_choices , blank=True,null=True) 
        washing_machine_type = models.CharField(max_length=50,choices=wm_type_choices , blank=True,null=True) 
        washing_machine_features = models.CharField(max_length=50,choices=wm_features_choices , blank=True,null=True) 
        spin_speed = models.CharField(max_length=50,choices=spin_speed_choices , blank=True,null=True) 
        washing_features = models.CharField(max_length=50,choices=washing_features_choices , blank=True,null=True) 
        motor_type = models.CharField(max_length=50,choices=motor_type_choices , blank=True,null=True) 
        weight_capacity_kg =  models.CharField(max_length=50,null=True,blank=True)
        WELS_tick_rating = models.CharField(max_length=50,choices=WELS_tick_rating_choices , blank=True,null=True)
        model_name = models.CharField(max_length=100,null=True,blank=True)
        WELS_water_consumption_liters_per_min  = models.CharField(max_length=100,null=True,blank=True)
        supported_weight = models.CharField(max_length=100,null=True,blank=True)
        smart_TV =models.CharField(max_length=50,choices=yn_choices , blank=True,null=True)
        tv_port_input = models.CharField(max_length=50,choices=tv_port_input_choices , blank=True,null=True)
        tv_features = models.CharField(max_length=50,choices=tv_features_choices , blank=True,null=True)
        tv_type = models.CharField(max_length=50,choices=tv_type_choices , blank=True,null=True)
        tv_screen_size = models.CharField(max_length=50,choices=tv_screen_size_choices , blank=True,null=True)
        tv_screen_type = models.CharField(max_length=50,choices=tv_screen_type_choices , blank=True,null=True)
        water_heater_type = models.CharField(max_length=50,choices=wh_type_choices , blank=True,null=True)
        antenna_type = models.CharField(max_length=50,choices=antenna_type_choices , blank=True,null=True)
        manual_device = models.CharField(max_length=50,choices=yn_choices , blank=True,null=True)
        water_dispenser_type = models.CharField(max_length=50,choices=water_disp_type_choices , blank=True,null=True)
        water_purifification = models.CharField(max_length=50,choices=water_purifn_choices , blank=True,null=True)
        water_dispenser_features = models.CharField(max_length=50,choices=water_disp_features_choices , blank=True,null=True)
        tv_mount_feature = models.CharField(max_length=50,choices=tv_mount_feature_choices , blank=True,null=True)
        receiver_type = models.CharField(max_length=50,choices=receiver_type_choices , blank=True,null=True)
        kettle_material = models.CharField(max_length=50,choices=kettle_material_choices , blank=True,null=True)
        kettle_features= models.CharField(max_length=50,choices=kettle_material_choices , blank=True,null=True)
        blender_type= models.CharField(max_length=50,choices=blender_type_choices , blank=True,null=True)	
        blender_features= models.CharField(max_length=50,choices=blender_features_choices , blank=True,null=True)	
        juicer_features= models.CharField(max_length=50,choices=juicer_features_choices , blank=True,null=True)
        juicer_type= models.CharField(max_length=50,choices=juicer_type_choices , blank=True,null=True)
        coffee_machine_type= models.CharField(max_length=50,choices=cm_type_choices , blank=True,null=True)
        coffee_machine_capacity= models.CharField(max_length=50,choices=cm_capacity_choices , blank=True,null=True)
        coffee_machine_features= models.CharField(max_length=50,choices=cm_features_choices , blank=True,null=True)
        mixer_features= models.CharField(max_length=50,choices=mixer_features_choices , blank=True,null=True)
        mixer_type= models.CharField(max_length=50,choices=mixer_type_choices , blank=True,null=True)
        stove_type = models.CharField(max_length=50,choices=stove_type_choices , blank=True,null=True)
        burner_type = models.CharField(max_length=50,choices=burner_type_choices , blank=True,null=True)
        induction_cooker_features= models.CharField(max_length=50,choices=ic_features_choices , blank=True,null=True)
        no_of_burners = models.CharField(max_length=50,choices=no_of_burners_choices , blank=True,null=True)
        air_fryer_features = models.CharField(max_length=50,choices=air_fryer_features_choices , blank=True,null=True)
        microwave_type = models.CharField(max_length=50,choices=mwave_type_choices , blank=True,null=True)
        microwave_features = models.CharField(max_length=50,choices=mwave_features_choices , blank=True,null=True)
        oven_features = models.CharField(max_length=50,choices=oven_features_choices , blank=True,null=True)
        meat_grinder_type = models.CharField(max_length=50,choices=meat_grinder_choices , blank=True,null=True)
        power = models.CharField(max_length=100,null=True,blank=True)
        bettery_capacity = models.CharField(max_length=100,null=True,blank=True)
        food_processor_sets = models.CharField(max_length=50,choices=food_proce_sets_choices , blank=True,null=True)
        multifunction_cooker_material = models.CharField(max_length=50,choices=mf_cooker_material_choices , blank=True,null=True)
        pressure_cooker_features = models.CharField(max_length=50,choices=pres_cookr_features_choices , blank=True,null=True)
        rice_cooker_features = models.CharField(max_length=50,choices=rice_cook_features_choices , blank=True,null=True)
        no_of_people = models.CharField(max_length=50,choices=no_of_people_choices , blank=True,null=True)
        rice_cooker_type = models.CharField(max_length=50,choices=rice_cooker_type_choices , blank=True,null=True)
        cooling_system_type = models.CharField(max_length=50,choices=cooling_system_type_choices , blank=True,null=True)
        energy_tick_rating = models.CharField(max_length=50,choices=energy_tick_rating_choices , blank=True,null=True)
        refrigerator_features = models.CharField(max_length=50,choices=refri_features_choices , blank=True,null=True)
        refrigerator_motor_type = models.CharField(max_length=50,choices=refrig_motor_type_choices , blank=True,null=True)
        refrigerator_type = models.CharField(max_length=50,choices=refrige_type_choices , blank=True,null=True)
        freezer_type = models.CharField(max_length=50,choices=freezer_type_choices , blank=True,null=True)
        hood_features = models.CharField(max_length=50,choices=hood_features_choices , blank=True,null=True)
        hood_mount_type = models.CharField(max_length=50,choices=hood_mount_type_choices , blank=True,null=True)
        cord_length = models.CharField(max_length=50,choices=cord_length_choices , blank=True,null=True)
        house_alarm_type = models.CharField(max_length=50,choices=house_alarm_type_choices , blank=True,null=True)
        alarm_volume = models.CharField(max_length=50,choices=alarm_volume_choices , blank=True,null=True)
        battery_capacity_measurement = models.CharField(max_length=50,choices=battery_capacity_msment_choices , blank=True,null=True)
        rechargable_battery_type = models.CharField(max_length=50,choices=rbattery_type_choices , blank=True,null=True)
        non_rechargable_battery_type = models.CharField(max_length=50,choices=nr_bat_type_choices , blank=True,null=True)
        battery_size = models.CharField(max_length=50,choices=battery_size_choices , blank=True,null=True)

        def __str__(self):      
              return self.name

        def get_fields(self,include_parents=True):
              return [(field.verbose_name,field.value_from_object(self) if field.verbose_name not in ['ID','product','sub category','category','brand'] else '') for field in self.__class__._meta.fields]
   
class variation_manager(models.Manager):
        def colors(self):
                return super(variation_manager,self).filter(variation_category = 'color',is_active=True)
        def sizes(self):
                return super(variation_manager,self).filter(variation_category = 'size',is_active=True)
        

        
variation_category_choice = (
        ('color' ,'color'),
        ('size','size')
)
        
class Variation(models.Model):
        product = models.ForeignKey(Product,on_delete=models.CASCADE)
        variation_category = models.CharField(max_length=100,choices=variation_category_choice)
        variation_value = models.CharField(max_length=100)
        variation_price  = models.FloatField()
        is_active = models.BooleanField(default=True)
        created_date = models.DateTimeField(default=datetime.now)
        

        objects = variation_manager()

        def __str__(self):
                return self.variation_value
        
        def averageReview(self):
                reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg("rating"))
                avg=0
                if reviews['average'] is not None:
                        avg =  float(reviews['average'])
                return avg
       
        def countReview(self):
                reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count("id"))
                count=0
                if reviews['count'] is not None: 
                        count =  int(reviews['count'])
                return count  
        

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length = 100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.subject
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product,default=None, on_delete = models.CASCADE)
    image = models.FileField(upload_to='store/products',validators=[ext_validator,validate_file_mimetype])

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'Product gallerys'
        verbose_name_plural = 'Product gallery'

class WishlistModel(models.Model):
        product = models.ForeignKey(Product,default=None, on_delete = models.CASCADE)
        user = models.ForeignKey(User,on_delete=models.CASCADE)
        
        def __str__(self):
         return self.product.product_name

class Contact(models.Model):
       sno = models.AutoField(primary_key = True)
       name = models.CharField(max_length=255)
       phone = models.CharField(max_length=13)
       email = models.CharField(max_length=100)
       subject = models.CharField(max_length=100)
       content = models.TextField()
       timeStamp  = models.DateTimeField(auto_now_add=True, blank=True)

       def __str__(self):
              return 'Message from ' + self.name + ' - ' + self.email
       
