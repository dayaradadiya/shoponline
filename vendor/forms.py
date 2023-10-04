from colorama import Style
from django import forms
from accounts.models import BusinessProfile
from app.models import Brand
from category.models import Category, Fourth_Level_Category, Main_Category, Sub_Category, Vendor_Category, Vendor_Main_Category, Vendor_Sub_Category
from orders.models import DisputeImages, ReturnDispute
from shipping.models import Shipping
from store.models import Images,  Product, Specification,  Variants
from vendor.models import Vendor
from accounts.validators import allow_only_images_validator, file_size
from djrichtextfield.widgets import RichTextWidget
from dynamic_forms import DynamicField, DynamicFormMixin
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from store.models import Images,Product, Variants
import datetime



class ImageForm(forms.ModelForm):
    class Meta :
        model = Images  
        fields = ['image','title']

        image = forms.FileField(widget=forms.FileInput(attrs={
                'accept':'.jpg,.png,.jpeg',
                'class' : 'btn btn-info', }),
         )
        # title = forms.CharField(widget=forms.TextInput(attrs={
        #     'placeholder' : 'Start typing...','required':'required',
        #     'class' : 'form-control',
        # }))

        def __init__(self, *args, **kwargs):
                self.request = kwargs.pop('request', None)
                super (ImageForm, self).__init__(*args, **kwargs)
                self.fields['image'].required=True
    
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_liscence','stype']
        exclude = ['is_approved','created_at','modified_at','vendor_slug','user','user_profile']

    SELLER_TYPE_CHOICES = [
    (1, "Indivisual"),
    (2, "Business")]  
        
    # shelf_life =  forms.CharField(widget=forms.Select(choices=SELLER_TYPE_CHOICES,attrs={'class' : 'form-control', }))
    stype = forms.ChoiceField(widget=forms.RadioSelect, choices=SELLER_TYPE_CHOICES)

    
      
    vendor_liscence = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}),validators=[allow_only_images_validator])
    
    vendor_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter vendor Name',
        'class' : 'form-control',
    }))

    
   
class VendForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_liscence','free_del_amount_limit']
        exclude = ['is_approved','created_at','modified_at','vendor_slug','user','user_profile','stype']

    
      
    vendor_liscence = forms.FileField(widget=forms.FileInput(attrs=
                                                             {
                                                                  'accept':'.jpg,.png,.jpeg',
                                                                  'class' : 'btn btn-info'}),
                                                             )
    
    vendor_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter vendor Name',
        'class' : 'form-control',
    }))

    free_del_amount_limit = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter vendor Name',
        'class' : 'form-control',
    }))

    

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        exclude   = ['company_name','license_number','entity_type','company_address','license_document']
         
    
        



class BPForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields  = ['company_name','license_number','entity_type','company_address','license_document']
         
 
        
    
    ENTITY_TYPE_CHOICES = [
         ('Sole Proprietorship','Sole Proprietorship'),
         ('Partnership','Partnership'),
         ('Limited Liability Partnership','Limited Liability Partnership'),
         ('Private Limited','Private Limited'),
    ]
    

    company_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class' : 'form-control',
    }))

    license_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Licence No',
        'class' : 'form-control',
    }))

    # entity_type = forms.ComboField(widget=forms.SelectDateWidget,choices=ENTITY_TYPE_CHOICES)
    
    entity_type = forms.CharField(
        widget=forms.Select(choices=ENTITY_TYPE_CHOICES,attrs={
             'class' : 'form-control', 
        })
    )



    company_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Licence No',
        'class' : 'form-control',
    }))

    license_document = forms.FileField(widget=forms.FileInput(attrs={
        'accept':'.jpg,.png,.jpeg',
        'class' : 'btn btn-info', }),
       )


class VariantsForm(forms.ModelForm):
    class Meta :
        model = Variants
        fields = ['title','color','size','image_id','variant_stock','variant_price','image_variant','variant_discount','variant_max_allowed_quantity']
        image_id  = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={
            'placeholder' : 'Enter Image Id',
            'class' : 'form-control',
             }))
       
        
        image_variant = forms.FileField(widget=forms.FileInput(attrs={
            'accept':'.jpg,.png,.jpeg',    
            'class' : 'btn btn-info', 
        }))

        
        # def image_choices(form):
        #     product = form['product'].value()
        #     return Images.objects.filter(product=product)
        
        # def initial_image(form):
        #     product = form['product'].value()
        #     return Images.objects.filter(product=product).first()
        
        # product = forms.ModelChoiceField(
        #     queryset=Product.objects.all(),
        #     initial=Product.objects.first(),
        # )

        # picture = DynamicField(forms.ModelChoiceField,
        #                      queryset=image_choices,
        #                      initial=initial_image,)
        

        def __init__(self, *args, **kwargs):
                self.request = kwargs.pop('request', None)
                super (VariantsForm, self).__init__(*args, **kwargs)
                self.fields['title'].required=True
                self.fields['color'].required=False
                self.fields['size'].required=False
                self.fields['product'].required=False
                # self.fields['storage_capacity'].required=False
                # self.fields['model_compatibility'].required=False
                # self.fields['vehicle_brand'].required=False


class DisputeImage_Form(forms.ModelForm):
     class Meta :
        model = ReturnDispute
        fields = ['videofile','videopod' ]

    #     image = forms.FileField(widget=forms.FileInput(attrs={
    #     'accept':'.jpg,.png,.jpeg',
    #     'class' : 'btn btn-info', })
    #    )
        
        videofile = forms.FileField(widget=forms.FileInput(attrs={
        'class' : 'btn btn-info'}),
        validators=[file_size]
       )
        
        videopod = forms.FileField(widget=forms.FileInput(attrs={
        'class' : 'btn btn-info'}),
        validators=[file_size]
       )
       

class ProductForm(DynamicFormMixin,forms.ModelForm):
    class Meta :
        model = Product
        fields = ['stock','is_available','model_name','featured_image','product_name','brand','price','discount',
                  'product_information','model_name','tags','description','section','slug','variant','main_category',
                  'category','sub_category','fourth_level_category','parcel_size_W','parcel_size_L','parcel_size_H',
                  'weight','shipping_fee_cover_byseller','shipping_fee','max_allowed_quantity']

    cond_choice = (
       ('Old','Old'),
       ('New','New'),
            )
    def category_choices(form):
         main_cat = form['main_category'].value()
         return Category.objects.filter(main_category=main_cat)
    
    
    def initial_module(form):
         main_cat = form['main_category'].value()
         return Category.objects.filter(main_category=main_cat).first()
    
    
    def sub_category_choices(form):
         category = form['category'].value()
         return Sub_Category.objects.filter(category=category)
    
    def fourth_level_category_choices(form):
         sub_category = form['sub_category'].value()
         return Fourth_Level_Category.objects.filter(sub_category=sub_category)
    
    def subcat_initial_module(form):
         category = form['category'].value()
         return Sub_Category.objects.filter(category=category).first()
    
    def flevelcat_initial_module(form):
         sub_category = form['sub_category'].value()
         return Fourth_Level_Category.objects.filter(sub_category=sub_category).first()
    
    
    featured_image = forms.FileField(widget=forms.FileInput(attrs={
         'accept':'.jpg,.png,.jpeg',
        'class' : 'file-drop-btn btn btn-primary btn-sm mb-2'
        }))

    # product_information = forms.CharField(required=False,widget=RichTextWidget(field_settings='advanced'))

    product_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Product Name',
        'class' : 'form-control',
    }))

    stock = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Stock',
        'class' : 'form-control',
    }))

    brand = forms.Select(attrs={
        'placeholder' : 'Enter Brand',
        'class' : 'form-control',
    })

 

    price = forms.FloatField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Price',
        'class' : 'form-control',
    }))

    discount = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Discount',
        'class' : 'form-control',
    }))

    is_available = forms.BooleanField(required=False)

    model_name = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Model Name',
        'class' : 'form-control',
    }))

    main_category = forms.ModelChoiceField(
         queryset = Main_Category.objects.filter(is_active=True),
         initial = Main_Category.objects.filter(is_active=True).first
    )
    
    category = DynamicField(
         forms.ModelChoiceField,
         queryset = category_choices,
        #  initial = initial_module,
    )

    sub_category = DynamicField(
         forms.ModelChoiceField,
         queryset = sub_category_choices,
         initial = subcat_initial_module,
    )
       
    
    fourth_level_category  = DynamicField(
         forms.ModelChoiceField,
         queryset = fourth_level_category_choices,
         initial = flevelcat_initial_module,
    )

    section = forms.Select(attrs={
        'class' : 'form-select me-3 form-control',
    })


    tags = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Tags',
        'class' : 'form-control',
    }))

    variant = forms.Select(attrs={
        'class' : 'form-select me-3',
    })

    slug = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Slug',
        'class' : 'form-control',
    }))
    parcel_size_W = forms.FloatField(required=False,widget=forms.NumberInput(attrs={
          'placeholder' : 'W (Integer) cm',
        'class' : 'form-control',
    }))
    parcel_size_L = forms.FloatField(required=False,widget=forms.NumberInput(attrs={
         'placeholder' : 'L (Integer) cm',
        'class' : 'form-control',
    }))
    parcel_size_H = forms.FloatField(required=False,widget=forms.NumberInput(attrs={
         'placeholder' : 'H (Integer) cm',
        'class' : 'form-control',
    }))
    weight = forms.FloatField(required=False,widget=forms.NumberInput(attrs={
        'class' : 'form-control',
    }))
    shipping_fee = forms.FloatField(required=False,widget=forms.NumberInput(attrs={
        'class' : 'form-control',
    }))
    max_allowed_quantity = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={
         'class' : 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super (ProductForm, self).__init__(*args, **kwargs)
        self.fields['brand'].required=False
        self.fields['section'].required=False
        self.fields['fourth_level_category'].required=False
        self.fields['category'].required=False
        self.fields['sub_category'].required=False


ProductFormSet = forms.inlineformset_factory(
    Product,
    Variants,
    VariantsForm,
    ProductForm,
    can_delete=False,
    min_num=2,
    extra=0,
)  

class SpecificationForm(forms.ModelForm):
    class Meta :
        model = Specification
        # fields = ['crepped_top','top_length','season','plus_size','petite','origin_country']
        fields = ['brand','crepped_top','top_length','season','plus_size','material','petite','origin_country','pattern',
                  'prod_style','sleeve_length','neckline','occasion','waist_height','bottoms_length',
                  'bottoms_fit_type','dress_skirt_style','dress_skirt_length','overalls_type',
                  'outerwear_length','jacket_type','apparel_type','bra_style','pack_type','bra_type',
                  'sexy_lingerie_style','bra_coverage','panty_style','panties_type','shaper_style','length','waist_height','Weddding_dress_style','costume_theme',
                  'tall_fit','fly_type','shorts_type','towel_robe_fabric','fragrance_concentration','jewellery_material_type','accessories_set','fashion_style',
                  'fashion_occasion','couple_accessories','earing_style','scarve_or_shawl_material','neckware_type','necklace_bracelet_style','hat_style','necklace_length',
                  'accessories_style','battery_capacity_measurement','rechargable_battery_type','non_rechargable_battery_type','battery_size','length','bottom_style','pack_type',
                  'access_type','socks_length','socks_type','pantyhose_type','button_style','leather_type','collar_type','top_fit_style','vent_style','suit_style','EAN','cuff_type',
                  'underwear_type','hair_care_benefits','packaging_type','shampoo_formulation','hair_finish','tool_function','cleanser_type','acne_treatment_type','lotion_type','gender',
                  'specialty_diet','food_type','weight_mgmt_supplement_functions','consumables_form','flavour','beauty_supplement_funcns','fitness_supplement_funcns','life_stage','medical_functions','scale_and_body_fat_analyzers_type','electrical_device','massage_equipment_type','NEA_registration_no','specs_frame_material','sunglass_lens_type','sg_frame_shape','frame_type','tie_width','cufflink_type','projector_contrast_ratio','resolution','projector_input_conetivty','projector_features','projector_type','projector_brightness','input_voltage_in_V','power_vonsumption_in_W','dimension_LxWxH','sewing_machine_material','no_of_stitches','sewing_machine_features','stitches_per_minute','iron_steamer_type','soleplate_type','iron_features','max_moisture_removal','vacuum_cleaner_funcn','run_time','airwatts','cord_length','suction_power','robot_vacuum_featrs','vacuum_clnr_featrs','corded_or_cordless','vaccume_cleaner_floor_care','smart_TV','tv_port_input','tv_features','tv_type','tv_screen_size','tv_screen_type','water_heater_type','antenna_type','manual_device','water_dispenser_type','water_purifification','water_dispenser_features','tv_mount_feature','receiver_type','kettle_material','kettle_features','blender_type','blender_features','juicer_features','juicer_type','coffee_machine_type','coffee_machine_capacity','coffee_machine_features','mixer_features','mixer_type','stove_type','burner_type','induction_cooker_features','no_of_burners','air_fryer_features','microwave_type','microwave_features','oven_features','meat_grinder_type','power','bettery_capacity','food_processor_sets','multifunction_cooker_material','pressure_cooker_features','rice_cooker_features','rice_cooker_features','no_of_people','rice_cooker_type','cooling_system_type','energy_tick_rating','refrigerator_features','refrigerator_motor_type','refrigerator_type','freezer_type','hood_features','hood_mount_type','cord_length','house_alarm_type','alarm_volume','ingredient','igredient_preference','formulation','nutrient_type','expiry_date','bodycare_benefits','volume','HSA_notification_no','shelf_life','scrub_formulation','skin_type','product_size','application_area','weight','handwash_pack_size','handwash_packsize_measure','handwash_formulation','quantity','production_batch_number','INVIMA_certification','FDA_registration_no','manufacturer_or_trader_name','warranty_duration','warranty_type','scent','makeup_furmulation','skin_tone','SPF_choices','foundation_coverage','makeup_finish','bb_or_cc_scare_benefits','waterproof','lip_benefits','facial_steamer_skincare_benefits','power_source','safety_mark','mask_type','device_compatibility','injury_support_area','contact_lens_type','lens_power','bristle_hardness','oral_care_benefits','wings','scent_function','flow_level','sanitary_pad_use','air_flow','air_purifier_filtration_type','cadr_rating','noise_level','air_purifier_features','room_size_m2','max_moisture_removal','washing_machine_type','washing_machine_features','spin_speed','washing_features','motor_type','weight_capacity_kg','WELS_tick_rating','model_name','WELS_water_consumption_liters_per_min','supported_weight','supported_weight'] 


   
                
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

        crepped_top = forms.CharField(
                widget=forms.Select(choices=yn_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        plus_size = forms.CharField(
                widget=forms.Select(choices=yn_choices,attrs={
                    'class' : 'form-control', 
                })
            )

        petite = forms.CharField(
                widget=forms.Select(choices=yn_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        
        top_length = forms.CharField(
                widget=forms.Select(choices=length_choices,attrs={
                    'class' : 'form-control', 
                })
            )

        season = forms.CharField(
                widget=forms.Select(choices=Season_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        
        origin_country = CountryField().formfield(
                    widget=CountrySelectWidget(
                    attrs={"class": "form-control"}
                                )
                            )
        
        brand = forms.ModelChoiceField(
         queryset = Brand.objects.all(),
         initial = Brand.objects.first()
            )
        
        prod_style = forms.CharField(
                widget=forms.Select(choices=prod_style_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        
        material = forms.CharField(
                widget=forms.Select(choices=material_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        
        pattern = forms.CharField(
                widget=forms.Select(choices=pattern_choices,attrs={
                    'class' : 'form-control', 
                })
            )
                
        apparel_type = forms.CharField(
                widget=forms.Select(choices=apparel_type_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        jacket_type = forms.CharField(
                widget=forms.Select(choices=jacket_type_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        outerwear_length = forms.CharField(
                widget=forms.Select(choices=outerwear_length_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        dress_skirt_length = forms.CharField(
                widget=forms.Select(choices=dress_skirt_length_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        overalls_type = forms.CharField(
                widget=forms.Select(choices=overalls_type_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        dress_skirt_style = forms.CharField(
                widget=forms.Select(choices=dress_skirt_style_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        bottoms_length = forms.CharField(
                widget=forms.Select(choices=bottoms_length_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        bottoms_fit_type = forms.CharField(
                widget=forms.Select(choices=bottoms_fit_type_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        waist_height = forms.CharField(
                widget=forms.Select(choices=waist_height_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        occasion = forms.CharField(
                widget=forms.Select(choices=occasion_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        neckline = forms.CharField(
                widget=forms.Select(choices=neckline_choices,attrs={
                    'class' : 'form-control', 
                })
            )			
        length  = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter length in meters',
        'class' : 'form-control',
         }))

                    
        sexy_lingerie_style = forms.CharField(
                widget=forms.Select(choices=sexy_lingerie_style_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        shaper_style = forms.CharField(
                widget=forms.Select(choices=shaper_style_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        panties_type = forms.CharField(
                widget=forms.Select(choices=panties_type_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        panty_style = forms.CharField(
                widget=forms.Select(choices=panty_style_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        bra_coverage = forms.CharField(
                widget=forms.Select(choices=bra_coverage_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        bra_type = forms.CharField(
                widget=forms.Select(choices=bra_type_choices,attrs={
                    'class' : 'form-control', 
                })
            )
        pack_type = forms.CharField(
                widget=forms.Select(choices=pack_type_choices,attrs={'class' : 'form-control', }))
        
        
        bra_style = forms.CharField(widget=forms.Select(choices=bra_style_choices,attrs={
                    'class' : 'form-control', 
                })
            )

        ############################   bigger change

        pack_type = forms.CharField(widget=forms.Select(choices=pack_type_choices,attrs={'class' : 'form-control', }))
        bra_type = forms.CharField(widget=forms.Select(choices=bra_type_choices,attrs={'class' : 'form-control', }))
        sexy_lingerie_style = forms.CharField(widget=forms.Select(choices=sexy_lingerie_style_choices,attrs={'class' : 'form-control', }))
        bra_coverage = forms.CharField(widget=forms.Select(choices=bra_coverage_choices,attrs={'class' : 'form-control', }))
        panty_style = forms.CharField(widget=forms.Select(choices=panty_style_choices,attrs={'class' : 'form-control', }))
        panties_type = forms.CharField(widget=forms.Select(choices=panties_type_choices,attrs={'class' : 'form-control', }))
        shaper_style = forms.CharField(widget=forms.Select(choices=shaper_style_choices,attrs={'class' : 'form-control', }))
        bottom_style = forms.CharField(widget=forms.Select(choices=bottom_style_choices,attrs={'class' : 'form-control', }))
        pack_size = forms.CharField(widget=forms.Select(choices=pack_choices,attrs={'class' : 'form-control', }))
        access_type = forms.CharField(widget=forms.Select(choices=access_choices,attrs={'class' : 'form-control', }))
        socks_length = forms.CharField(widget=forms.Select(choices=socks_length_choices,attrs={'class' : 'form-control', }))
        socks_type = forms.CharField(widget=forms.Select(choices=socks_type_choices,attrs={'class' : 'form-control', }))
        pantyhose_type = forms.CharField(widget=forms.Select(choices=pantyhose_choices,attrs={'class' : 'form-control', }))
        Weddding_dress_style = forms.CharField(widget=forms.Select(choices=Wed_dress_style_choices,attrs={'class' : 'form-control', }))
        costume_theme = forms.CharField(widget=forms.Select(choices=costume_theme_choices,attrs={'class' : 'form-control', }))
        tall_fit = forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', }))
        button_style = forms.CharField(widget=forms.Select(choices=buttons_style_choices,attrs={'class' : 'form-control', }))
        leather_type = forms.CharField(widget=forms.Select(choices=leather_type_choices,attrs={'class' : 'form-control', }))
        collar_type = forms.CharField(widget=forms.Select(choices=collar_type_choices,attrs={'class' : 'form-control', }))
        top_fit_style = forms.CharField(widget=forms.Select(choices=top_fit_style_choices,attrs={'class' : 'form-control', }))
        vent_style =  forms.CharField(widget=forms.Select(choices=vent_style_choices,attrs={'class' : 'form-control', }))
        suit_style = forms.CharField(widget=forms.Select(choices=suit_style_choices,attrs={'class' : 'form-control', })) 
        
        fly_type = forms.CharField(widget=forms.Select(choices=fly_type_choices,attrs={'class' : 'form-control', }))
        cuff_type = forms.CharField(widget=forms.Select(choices=cuff_type_choices,attrs={'class' : 'form-control', }))
        underwear_type = forms.CharField(widget=forms.Select(choices=underwear_type_choices,attrs={'class' : 'form-control', }))
        shorts_type = forms.CharField(widget=forms.Select(choices=shorts_type_choices,attrs={'class' : 'form-control', }))
        towel_robe_fabric  = forms.CharField(widget=forms.Select(choices=towel_robe_fabric_choices,attrs={'class' : 'form-control', }))
       
        igredient_preference  = forms.CharField(widget=forms.Select(choices=igredient_preference_choices,attrs={'class' : 'form-control', }))
        formulation  = forms.CharField(widget=forms.Select(choices=formulation_choices,attrs={'class' : 'form-control', }))
        nutrient_type = forms.CharField(widget=forms.Select(choices=nutrient_type_choices,attrs={'class' : 'form-control', })) 
    
        bodycare_benefits = forms.CharField(widget=forms.Select(choices=bodycare_benefits_choices,attrs={'class' : 'form-control', }))
        volume = forms.CharField(widget=forms.Select(choices=volume_choices,attrs={'class' : 'form-control', }))
     
        shelf_life =  forms.CharField(widget=forms.Select(choices=shelflife_choices,attrs={'class' : 'form-control', }))
        scrub_formulation =  forms.CharField(widget=forms.Select(choices=scrub_formulation_choices,attrs={'class' : 'form-control', }))
        skin_type =  forms.CharField(widget=forms.Select(choices=skin_type_choices,attrs={'class' : 'form-control', }))
        product_size =  forms.CharField(widget=forms.Select(choices=product_size_choices,attrs={'class' : 'form-control', }))
        application_area =  forms.CharField(widget=forms.Select(choices=application_area_choices,attrs={'class' : 'form-control', }))
        weight =  forms.CharField(widget=forms.Select(choices=weight_choices,attrs={'class' : 'form-control', }))
        
        handwash_packsize_measure = forms.CharField(widget=forms.Select(choices=handwash_packsize_choices,attrs={'class' : 'form-control', }))
        handwash_formulation =  forms.CharField(widget=forms.Select(choices=handwash_formulation_choices,attrs={'class' : 'form-control', }))
       
        
        warranty_duration  =  forms.CharField(widget=forms.Select(choices=warranty_duration_choices,attrs={'class' : 'form-control', }))
        warranty_type  =  forms.CharField(widget=forms.Select(choices=warranty_type_choices,attrs={'class' : 'form-control', }))
        hair_care_benefits =  forms.CharField(widget=forms.Select(choices=hair_care_benefits_choices,attrs={'class' : 'form-control', }))
        packaging_type =  forms.CharField(widget=forms.Select(choices=packaging_type_choices,attrs={'class' : 'form-control', }))
        shampoo_formulation = forms.CharField(widget=forms.Select(choices=shampoo_formulation_choices,attrs={'class' : 'form-control', }))
        scent = forms.CharField(widget=forms.Select(choices=scent_choices,attrs={'class' : 'form-control', }))
        shave_gel_or_cream_appn_area  = forms.CharField(widget=forms.Select(choices=shavegel_appn_area_choices,attrs={'class' : 'form-control', }))
        makeup_furmulation  = forms.CharField(widget=forms.Select(choices=makeup_furmulation_choices,attrs={'class' : 'form-control', }))
        skin_tone  = forms.CharField(widget=forms.Select(choices=skin_tone_choices,attrs={'class' : 'form-control', }))
        SPF_choices  = forms.CharField(widget=forms.Select(choices=SPF_choices,attrs={'class' : 'form-control', }))
        foundation_coverage  = forms.CharField(widget=forms.Select(choices=foundn_coverg_choices,attrs={'class' : 'form-control', }))
        makeup_finish =  forms.CharField(widget=forms.Select(choices=makeup_finish_choices,attrs={'class' : 'form-control', }))
        bb_or_cc_scare_benefits =  forms.CharField(widget=forms.Select(choices=cc_scare_bene_choices,attrs={'class' : 'form-control', }))
        waterproof =  forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', }))
       
        lip_benefits  =  forms.CharField(widget=forms.Select(choices=lip_benefit_choices,attrs={'class' : 'form-control', }))
        facial_steamer_skincare_benefits =  forms.CharField(widget=forms.Select(choices=face_steamr_bene_choices,attrs={'class' : 'form-control', }))
     
        mask_type =  forms.CharField(widget=forms.Select(choices=mask_type_choices,attrs={'class' : 'form-control', }))
        hair_finish =  forms.CharField(widget=forms.Select(choices=hair_finish_choices,attrs={'class' : 'form-control', }))
        tool_function =  forms.CharField(widget=forms.Select(choices=tool_function_choices,attrs={'class' : 'form-control', }))
        cleanser_type =  forms.CharField(widget=forms.Select(choices=cleanser_type_choices,attrs={'class' : 'form-control', }))
        acne_treatment_type = forms.CharField(widget=forms.Select(choices=acne_tment_type_choices,attrs={'class' : 'form-control', }))
        lotion_type = forms.CharField(widget=forms.Select(choices=lotion_type_choices,attrs={'class' : 'form-control', }))
        fragrance_concentration = forms.CharField(widget=forms.Select(choices=fragrance_concn_choices,attrs={'class' : 'form-control', }))
        gender = forms.CharField(widget=forms.Select(choices=gender_choices,attrs={'class' : 'form-control', }))
        specialty_diet = forms.CharField(widget=forms.Select(choices=specialty_diet_choices,attrs={'class' : 'form-control', }))
        food_type = forms.CharField(widget=forms.Select(choices=food_type_choices,attrs={'class' : 'form-control', }))
        weight_mgmt_supplement_functions= forms.CharField(widget=forms.Select(choices=weight_mgmt_supplt_funs_choices,attrs={'class' : 'form-control', }))
        consumables_form = forms.CharField(widget=forms.Select(choices=consumables_form_choices,attrs={'class' : 'form-control', }))
        flavour = forms.CharField(widget=forms.Select(choices=flavour_choices,attrs={'class' : 'form-control', }))
        beauty_supplement_funcns = forms.CharField(widget=forms.Select(choices=beauty_supplmt_funcs_choices,attrs={'class' : 'form-control', }))
        fitness_supplement_funcns = forms.CharField(widget=forms.Select(choices=fitness_supplmt_funcs_choices,attrs={'class' : 'form-control', }))
        life_stage = forms.CharField(widget=forms.Select(choices=life_stage_choices,attrs={'class' : 'form-control', }))
        wellbeing_supplement_funcns = forms.CharField(widget=forms.Select(choices=wellbeing_supplmt_funcs_choices,attrs={'class' : 'form-control', }))
        medical_functions = forms.CharField(widget=forms.Select(choices=medical_funcn_choices,attrs={'class' : 'form-control', }))
        device_compatibility =  forms.CharField(widget=forms.Select(choices=device_comp_choices,attrs={'class' : 'form-control', }))
        scale_and_body_fat_analyzers_type =  forms.CharField(widget=forms.Select(choices=sbf_analyzers_type_choices,attrs={'class' : 'form-control', }))
        injury_support_area=  forms.CharField(widget=forms.Select(choices=injury_support_area_choices,attrs={'class' : 'form-control', }))
        contact_lens_type = forms.CharField(widget=forms.Select(choices=contact_lens_choices,attrs={'class' : 'form-control', }))
        lens_power = forms.CharField(widget=forms.Select(choices=lens_power_choices,attrs={'class' : 'form-control', }))
        bristle_hardness = forms.CharField(widget=forms.Select(choices=bristle_hardness_choices,attrs={'class' : 'form-control', })) 
        oral_care_benefits = forms.CharField(widget=forms.Select(choices=oralcare_bene_choices,attrs={'class' : 'form-control', })) 
        wings = forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', })) 
        scent_function = forms.CharField(widget=forms.Select(choices=scent_funcn_choices,attrs={'class' : 'form-control', })) 
        flow_level = forms.CharField(widget=forms.Select(choices=flow_level_choices,attrs={'class' : 'form-control', })) 
        sanitary_pad_use = forms.CharField(widget=forms.Select(choices=sanitary_pad_use_choices,attrs={'class' : 'form-control', })) 
        electrical_device = forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', })) 
        massage_equipment_type = forms.CharField(widget=forms.Select(choices=massage_equipmt_choices,attrs={'class' : 'form-control', })) 
       
        jewellery_material_type = forms.CharField(widget=forms.Select(choices=jewel_material_type_choices,attrs={'class' : 'form-control', })) 
        accessories_set = forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', })) 
        fashion_style = forms.CharField(widget=forms.Select(choices=fashion_style_choices,attrs={'class' : 'form-control', })) 
        fashion_occasion = forms.CharField(widget=forms.Select(choices=fashion_occasion_choices,attrs={'class' : 'form-control', })) 
        couple_accessories = forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', })) 
        earing_style =  forms.CharField(widget=forms.Select(choices=earing_style_choices,attrs={'class' : 'form-control', })) 
        scarve_or_shawl_material =  forms.CharField(widget=forms.Select(choices=scarve_material_choices,attrs={'class' : 'form-control', })) 
        neckware_type   =  forms.CharField(widget=forms.Select(choices=neckware_type_choices,attrs={'class' : 'form-control', })) 
        necklace_bracelet_style =  forms.CharField(widget=forms.Select(choices=necklace_style_choices,attrs={'class' : 'form-control', })) 
        hat_style =  forms.CharField(widget=forms.Select(choices=hat_style_choices,attrs={'class' : 'form-control', })) 
        accessories_style =  forms.CharField(widget=forms.Select(choices=accessories_style_choices,attrs={'class' : 'form-control', })) 
        necklace_length = forms.CharField(widget=forms.Select(choices=necklace_length_choices,attrs={'class' : 'form-control', })) 
        specs_frame_material = forms.CharField(widget=forms.Select(choices=specs_frame_material_choices,attrs={'class' : 'form-control', })) 
        sunglass_lens_type = forms.CharField(widget=forms.Select(choices=sg_lens_type_choices,attrs={'class' : 'form-control', })) 
        sg_frame_shape  = forms.CharField(widget=forms.Select(choices=sg_frame_shape_choices,attrs={'class' : 'form-control', })) 
        frame_type = forms.CharField(widget=forms.Select(choices=frame_type_choices,attrs={'class' : 'form-control', })) 
        tie_width = forms.CharField(widget=forms.Select(choices=tie_width_choices,attrs={'class' : 'form-control', })) 
        cufflink_type = forms.CharField(widget=forms.Select(choices=cufflink_type_choices,attrs={'class' : 'form-control', })) 
        projector_contrast_ratio =  forms.CharField(widget=forms.Select(choices=proj_contrast_ratio_choices,attrs={'class' : 'form-control', })) 
        resolution  =  forms.CharField(widget=forms.Select(choices=resolution_choices,attrs={'class' : 'form-control', })) 
        projector_input_conetivty = forms.CharField(widget=forms.Select(choices=proj_input_conetivty_choices,attrs={'class' : 'form-control', })) 
        projector_features = forms.CharField(widget=forms.Select(choices=proj_features_choices,attrs={'class' : 'form-control', })) 
        projector_type = forms.CharField(widget=forms.Select(choices=proj_type_choices,attrs={'class' : 'form-control', })) 
        projector_brightness	= forms.CharField(widget=forms.Select(choices=proj_brightness_choices,attrs={'class' : 'form-control', })) 
    
        sewing_machine_material = forms.CharField(widget=forms.Select(choices=sewing_material_choices,attrs={'class' : 'form-control', })) 
        no_of_stitches = forms.CharField(widget=forms.Select(choices=no_of_stitche_choices,attrs={'class' : 'form-control', })) 
        sewing_machine_features = forms.CharField(widget=forms.Select(choices=sewing_machine_feat_choices,attrs={'class' : 'form-control', })) 
        stitches_per_minute = forms.CharField(widget=forms.Select(choices=stitches_per_minute_choices,attrs={'class' : 'form-control', })) 
        iron_steamer_type = forms.CharField(widget=forms.Select(choices=iron_steamer_type_choices,attrs={'class' : 'form-control', })) 				
        soleplate_type = forms.CharField(widget=forms.Select(choices=soleplate_type_choices,attrs={'class' : 'form-control', })) 		
        iron_features = forms.CharField(widget=forms.Select(choices=iron_features_choices,attrs={'class' : 'form-control', })) 
        air_flow = forms.CharField(widget=forms.Select(choices=air_flow_choices,attrs={'class' : 'form-control', })) 
        air_purifier_filtration_type = forms.CharField(widget=forms.Select(choices=air_purifier_filtn_type_choices,attrs={'class' : 'form-control', })) 
        cadr_rating = forms.CharField(widget=forms.Select(choices=cadr_rating_choices,attrs={'class' : 'form-control', })) 
        noise_level = forms.CharField(widget=forms.Select(choices=noise_level_choices,attrs={'class' : 'form-control', })) 
        air_purifier_features = forms.CharField(widget=forms.Select(choices=air_purifier_features_choices,attrs={'class' : 'form-control', })) 
       
        max_moisture_removal = forms.CharField(widget=forms.Select(choices=max_moisture_removal_choices,attrs={'class' : 'form-control', })) 
        vacuum_cleaner_funcn = forms.CharField(widget=forms.Select(choices=vacuum_cleaner_funcn_choices,attrs={'class' : 'form-control', })) 
        run_time= forms.CharField(widget=forms.Select(choices=run_time_choices,attrs={'class' : 'form-control', })) 
        airwatts = forms.CharField(widget=forms.Select(choices=airwatts_choices,attrs={'class' : 'form-control', })) 
        cord_length = forms.CharField(widget=forms.Select(choices=cord_length_choices,attrs={'class' : 'form-control', })) 
        suction_power = forms.CharField(widget=forms.Select(choices=suction_power_choices,attrs={'class' : 'form-control', })) 
        robot_vacuum_featrs = forms.CharField(widget=forms.Select(choices=robot_vacuum_featrs_choices,attrs={'class' : 'form-control', })) 
        vacuum_clnr_featrs = forms.CharField(widget=forms.Select(choices=vacuum_clnr_featrs_choices,attrs={'class' : 'form-control', })) 
        corded_or_cordless = forms.CharField(widget=forms.Select(choices=corded_or_cordless_choices,attrs={'class' : 'form-control', })) 
        vaccume_cleaner_floor_care = forms.CharField(widget=forms.Select(choices=vc_floor_care_choices,attrs={'class' : 'form-control', })) 
        washing_machine_type = forms.CharField(widget=forms.Select(choices=wm_type_choices,attrs={'class' : 'form-control', })) 
        washing_machine_features = forms.CharField(widget=forms.Select(choices=wm_features_choices,attrs={'class' : 'form-control', })) 
        spin_speed = forms.CharField(widget=forms.Select(choices=spin_speed_choices,attrs={'class' : 'form-control', })) 
        washing_features = forms.CharField(widget=forms.Select(choices=washing_features_choices,attrs={'class' : 'form-control', })) 
        motor_type = forms.CharField(widget=forms.Select(choices=motor_type_choices,attrs={'class' : 'form-control', })) 
        
        WELS_tick_rating = forms.CharField(widget=forms.Select(choices=WELS_tick_rating_choices,attrs={'class' : 'form-control', }))
      
       
        smart_TV =forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', }))
        tv_port_input = forms.CharField(widget=forms.Select(choices=tv_port_input_choices,attrs={'class' : 'form-control', }))
        tv_features = forms.CharField(widget=forms.Select(choices=tv_features_choices,attrs={'class' : 'form-control', }))
        tv_type = forms.CharField(widget=forms.Select(choices=tv_type_choices,attrs={'class' : 'form-control', }))
        tv_screen_size = forms.CharField(widget=forms.Select(choices=tv_screen_size_choices,attrs={'class' : 'form-control', }))
        tv_screen_type = forms.CharField(widget=forms.Select(choices=tv_screen_type_choices,attrs={'class' : 'form-control', }))
        water_heater_type = forms.CharField(widget=forms.Select(choices=wh_type_choices,attrs={'class' : 'form-control', }))
        antenna_type = forms.CharField(widget=forms.Select(choices=antenna_type_choices,attrs={'class' : 'form-control', }))
        manual_device = forms.CharField(widget=forms.Select(choices=yn_choices,attrs={'class' : 'form-control', }))
        water_dispenser_type = forms.CharField(widget=forms.Select(choices=water_disp_type_choices,attrs={'class' : 'form-control', }))
        water_purifification = forms.CharField(widget=forms.Select(choices=water_purifn_choices,attrs={'class' : 'form-control', }))
        water_dispenser_features = forms.CharField(widget=forms.Select(choices=water_disp_features_choices,attrs={'class' : 'form-control', }))
        tv_mount_feature = forms.CharField(widget=forms.Select(choices=tv_mount_feature_choices,attrs={'class' : 'form-control', }))
        receiver_type = forms.CharField(widget=forms.Select(choices=receiver_type_choices,attrs={'class' : 'form-control', }))
        kettle_material = forms.CharField(widget=forms.Select(choices=kettle_material_choices,attrs={'class' : 'form-control', }))
        kettle_features= forms.CharField(widget=forms.Select(choices=kettle_features_choices,attrs={'class' : 'form-control', }))
        blender_type= forms.CharField(widget=forms.Select(choices=blender_type_choices,attrs={'class' : 'form-control', }))	
        blender_features= forms.CharField(widget=forms.Select(choices=blender_features_choices,attrs={'class' : 'form-control', }))	
        juicer_features= forms.CharField(widget=forms.Select(choices=juicer_features_choices,attrs={'class' : 'form-control', }))
        juicer_type= forms.CharField(widget=forms.Select(choices=juicer_type_choices,attrs={'class' : 'form-control', }))
        cofee_machine_type= forms.CharField(widget=forms.Select(choices=cm_type_choices,attrs={'class' : 'form-control', }))
        cofee_machine_capacity= forms.CharField(widget=forms.Select(choices=cm_capacity_choices,attrs={'class' : 'form-control', }))
        cofee_machine_features= forms.CharField(widget=forms.Select(choices=cm_features_choices,attrs={'class' : 'form-control', }))
        mixer_features= forms.CharField(widget=forms.Select(choices=mixer_features_choices,attrs={'class' : 'form-control', }))
        mixer_type= forms.CharField(widget=forms.Select(choices=mixer_type_choices,attrs={'class' : 'form-control', }))
        stove_type = forms.CharField(widget=forms.Select(choices=stove_type_choices,attrs={'class' : 'form-control', }))
        burner_type = forms.CharField(widget=forms.Select(choices=burner_type_choices,attrs={'class' : 'form-control', }))
        induction_cooker_features= forms.CharField(widget=forms.Select(choices=ic_features_choices,attrs={'class' : 'form-control', }))
        no_of_burners = forms.CharField(widget=forms.Select(choices=no_of_burners_choices,attrs={'class' : 'form-control', }))
        air_fryer_features = forms.CharField(widget=forms.Select(choices=air_fryer_features_choices,attrs={'class' : 'form-control', }))
        microwave_type = forms.CharField(widget=forms.Select(choices=mwave_type_choices,attrs={'class' : 'form-control', }))
        microwave_features = forms.CharField(widget=forms.Select(choices=mwave_features_choices,attrs={'class' : 'form-control', }))
        oven_features = forms.CharField(widget=forms.Select(choices=oven_features_choices,attrs={'class' : 'form-control', }))
        meat_grinder_type = forms.CharField(widget=forms.Select(choices=meat_grinder_choices,attrs={'class' : 'form-control', }))
  
        food_processor_sets = forms.CharField(widget=forms.Select(choices=food_proce_sets_choices,attrs={'class' : 'form-control', }))
        multifunction_cooker_material = forms.CharField(widget=forms.Select(choices=mf_cooker_material_choices,attrs={'class' : 'form-control', }))
        pressure_cooker_features = forms.CharField(widget=forms.Select(choices=pres_cookr_features_choices,attrs={'class' : 'form-control', }))
        rice_cooker_features = forms.CharField(widget=forms.Select(choices=rice_cook_features_choices,attrs={'class' : 'form-control', }))
        no_of_people = forms.CharField(widget=forms.Select(choices=no_of_people_choices,attrs={'class' : 'form-control', }))
        rice_cooker_type = forms.CharField(widget=forms.Select(choices=rice_cooker_type_choices,attrs={'class' : 'form-control', }))
        cooling_system_type = forms.CharField(widget=forms.Select(choices=cooling_system_type_choices,attrs={'class' : 'form-control', }))
        energy_tick_rating = forms.CharField(widget=forms.Select(choices=energy_tick_rating_choices,attrs={'class' : 'form-control', }))
        refrigerator_features = forms.CharField(widget=forms.Select(choices=refri_features_choices,attrs={'class' : 'form-control', }))
        refrigerator_motor_type = forms.CharField(widget=forms.Select(choices=refrig_motor_type_choices,attrs={'class' : 'form-control', }))
        refrigerator_type = forms.CharField(widget=forms.Select(choices=refrige_type_choices,attrs={'class' : 'form-control', }))
        freezer_type = forms.CharField(widget=forms.Select(choices=freezer_type_choices,attrs={'class' : 'form-control', }))
        hood_features = forms.CharField(widget=forms.Select(choices=hood_features_choices,attrs={'class' : 'form-control', }))
        hood_mount_type = forms.CharField(widget=forms.Select(choices=hood_mount_type_choices,attrs={'class' : 'form-control', }))
        cord_length = forms.CharField(widget=forms.Select(choices=cord_length_choices,attrs={'class' : 'form-control', }))
        house_alarm_type = forms.CharField(widget=forms.Select(choices=house_alarm_type_choices,attrs={'class' : 'form-control', }))
        alarm_volume = forms.CharField(widget=forms.Select(choices=alarm_volume_choices,attrs={'class' : 'form-control', }))
        battery_capacity_measurement = forms.CharField(widget=forms.Select(choices=battery_capacity_msment_choices,attrs={'class' : 'form-control', }))
        rechargable_battery_type = forms.CharField(widget=forms.Select(choices=rbattery_type_choices,attrs={'class' : 'form-control', }))
        non_rechargable_battery_type = forms.CharField(widget=forms.Select(choices=nr_bat_type_choices,attrs={'class' : 'form-control', }))
        battery_size = forms.CharField(widget=forms.Select(choices=battery_size_choices,attrs={'class' : 'form-control', }))
        mascara_benefits =  forms.CharField(widget=forms.Select(choices=mascara_ben_chioces,attrs={'class' : 'form-control', }))
        power_source =  forms.CharField(widget=forms.Select(choices=power_source_choces,attrs={'class' : 'form-control', }))


        
        EAN = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        handwash_pack_size =   forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        quantity = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        production_batch_number =   forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        manufacturer_or_trader_name  =   forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        INVIMA_certification =   forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        FDA_registration_no  =   forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        manufacturer_or_trader_address  =   forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        safety_mark  = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        NEA_registration_no = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        input_voltage_in_V = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        power_vonsumption_in_W = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        dimension_LxWxH = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        room_size_m2 = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        weight_capacity_kg =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        model_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        WELS_water_consumption_liters_per_min  = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        supported_weight = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        power = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        bettery_capacity = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        HSA_notification_no =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        expiry_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class' : 'form-control', }))
        ingredient  = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', }))




# class ShippingForm(forms.ModelForm):
#     class Meta:
#         model = Shipping
#         fields = ('pickup_date',)
#         widgets = {
#             'times_pick': forms.DateInput(
#                 options={
#                     'minDate': (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'),
#                     'maxDate': (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d 23:59:59'),
#                     'enabledHours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
#                 }
#             ),
#         }        
        
#         pickup_date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), label='Date effet')


class MainCategoryForm(forms.ModelForm):
     class Meta:
        model = Vendor_Main_Category
        fields  = ['name','description']

     name = forms.ModelChoiceField(
         queryset = Main_Category.objects.filter(is_active=True),
         initial = Main_Category.objects.filter(is_active=True).first
    )


     description = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Description',
        'class' : 'form-control',
    }))

class CategoryForm(DynamicFormMixin,forms.ModelForm):
    class Meta:
        model = Vendor_Category
        fields  = ['main_category','name']
    
    main_category = forms.ModelChoiceField(
         queryset = Vendor_Main_Category.objects.all(),
         initial = Vendor_Main_Category.objects.all().first
    )
    

    

class SubCategoryForm(DynamicFormMixin,forms.ModelForm):
    class Meta:
        model = Vendor_Sub_Category
        fields  = ['main_category','category','name']

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super(SubCategoryForm, self).__init__(*args, **kwargs)
        
    #     vendor = Vendor.objects.get(user=self.request.user)
 
    #     self.fields["main_category"].queryset = Vendor_Main_Category.objects.filter(vendor=vendor)
    #     self.fields["category"].queryset = Vendor_Category.objects.filter(vendor=vendor)
        
    
    # def clean(self):
    #     print(self.request.user)

    def category_choices(form):
         main_cat = form['main_category'].value()
         return Vendor_Category.objects.filter(main_category=main_cat)
    
    
    def initial_module(form):
         main_cat = form['main_category'].value()
         return Vendor_Category.objects.filter(main_category=main_cat).first()
    
    
    main_category = forms.ModelChoiceField(
         queryset = Vendor_Main_Category.objects.all(),
         initial = Vendor_Main_Category.objects.all().first
    )
    
    category = DynamicField(
         forms.ModelChoiceField,
         queryset = category_choices,
        #  initial = initial_module,
    )

  

    