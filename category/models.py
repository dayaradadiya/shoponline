from datetime import datetime
from django.db import models
from django.urls import reverse
from accounts.validators import validate_file_mimetype
from django.core.validators import FileExtensionValidator
from vendor.models import Vendor
from django.db.models.signals import post_save

ext_validator = FileExtensionValidator(['jpg','png','jpeg'])  

class Main_Category(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length = 255, blank = True)
    cat_image = models.FileField(upload_to='photos/categories',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
    slug = models.SlugField(max_length=100,blank=True)
    is_active = models.BooleanField(default=False)

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name

# class category_manager(models.Manager):
#         def clothing(self):
#                 return super(category_manager,self).filter(main_category = 'clothing')
       
   

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,blank=True)
    pattern  = models.BooleanField(default=False)
    petite = models.BooleanField(default=False)
    waist_height = models.BooleanField(default=False)
    season = models.BooleanField(default=False)
    plus_size = models.BooleanField(default=False)
    occasion = models.BooleanField(default=False)
    dress_skirt_style = models.BooleanField(default=False)
    origin_country = models.BooleanField(default=False)
    bottoms_length = models.BooleanField(default=False)
    style = models.BooleanField(default=False)
    dress_skirt_length = models.BooleanField(default=False)
    brand = models.BooleanField(default=True) 
    material = models.BooleanField(default=False)
    bottoms_fit_type = models.BooleanField(default=False)
    neckline = models.BooleanField(default=False)
    sleeve_length = models.BooleanField(default=False)
    Weddding_dress_style = models.BooleanField(default=False)
    outerwear_length = models.BooleanField(default=False)
    top_length = models.BooleanField(default=False)
    costume_theme = models.BooleanField(default=False)
    tall_fit = models.BooleanField(default=False)
    fly_type = models.BooleanField(default=False)
    shorts_type = models.BooleanField(default=False)
    towel_robe_fabric = models.BooleanField(default=False)
    apparel_type = models.BooleanField(default=False)
    fragrance_concentration = models.BooleanField(default=False)
    jewellery_material_type = models.BooleanField(default=False)
    accessories_set = models.BooleanField(default=False)
    fashion_style = models.BooleanField(default=False)
    fashion_occasion = models.BooleanField(default=False)
    couple_accessories = models.BooleanField(default=False)
    earing_style = models.BooleanField(default=False)
    scarve_or_shawl_material = models.BooleanField(default=False)
    neckware_type = models.BooleanField(default=False)
    necklace_bracelet_style = models.BooleanField(default=False)
    hat_style = models.BooleanField(default=False)
    necklace_length = models.BooleanField(default=False)
    accessories_style = models.BooleanField(default=False)
    battery_capacity_measurement  = models.BooleanField(default=False)
    rechargable_battery_type  = models.BooleanField(default=False)
    non_rechargable_battery_type  = models.BooleanField(default=False)
    battery_size =  models.BooleanField(default=False)
    
    # objects = category_manager()

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return  self.main_category.name + " -- " + self.name
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])  


class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)                 
    slug = models.SlugField(max_length=100)    
    crepped_top = models.BooleanField(default=False)
    overalls_type = models.BooleanField(default=False)
    jacket_type = models.BooleanField(default=False)
    bra_style = models.BooleanField(default=False)
    pack_type = models.BooleanField(default=False)
    bra_type = models.BooleanField(default=False)
    sexy_lingerie_style = models.BooleanField(default=False)
    bra_coverage = models.BooleanField(default=False)
    panty_style = models.BooleanField(default=False)
    panties_type = models.BooleanField(default=False)
    shaper_style = models.BooleanField(default=False)
    length = models.BooleanField(default=False)
    bottom_style = models.BooleanField(default=False)
    pack_type = models.BooleanField(default=False)
    access_type = models.BooleanField(default=False)
    socks_length = models.BooleanField(default=False)
    socks_type = models.BooleanField(default=False)
    pantyhose_type = models.BooleanField(default=False)
    button_style = models.BooleanField(default=False)
    leather_type = models.BooleanField(default=False)
    collar_type = models.BooleanField(default=False)
    top_fit_style = models.BooleanField(default=False)
    vent_style = models.BooleanField(default=False)
    suit_style = models.BooleanField(default=False)
    EAN = models.BooleanField(default=False)
    cuff_type = models.BooleanField(default=False)
    underwear_type = models.BooleanField(default=False)
    hair_care_benefits_choices = models.BooleanField(default=False)
    packaging_type = models.BooleanField(default=False)
    shampoo_formulation = models.BooleanField(default=False)
    hair_finish = models.BooleanField(default=False)
    tool_function = models.BooleanField(default=False)
    cleanser_type = models.BooleanField(default=False)
    acne_treatment_type = models.BooleanField(default=False)
    lotion_type = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    specialty_diet = models.BooleanField(default=False)
    food_type = models.BooleanField(default=False)
    weight_mgmt_supplement_functions = models.BooleanField(default=False)
    consumables_form = models.BooleanField(default=False)
    flavour = models.BooleanField(default=False)
    beauty_supplement_funcs = models.BooleanField(default=False)
    fitness_supplement_funcns = models.BooleanField(default=False)
    life_stage = models.BooleanField(default=False)
    medical_functions= models.BooleanField(default=False)
    scale_and_body_fat_analyzers_type = models.BooleanField(default=False)
    electrical_device = models.BooleanField(default=False)
    massage_equipment_type = models.BooleanField(default=False)
    NEA_registration_no = models.BooleanField(default=False)
    specs_frame_material = models.BooleanField(default=False)
    sunglass_lens_type = models.BooleanField(default=False)
    sg_frame_shape = models.BooleanField(default=False)
    frame_type = models.BooleanField(default=False)
    tie_width = models.BooleanField(default=False)
    cufflink_type = models.BooleanField(default=False)
    projector_contrast_ratio = models.BooleanField(default=False)
    resolution = models.BooleanField(default=False)
    projector_input_conetivty  = models.BooleanField(default=False)
    projector_features  = models.BooleanField(default=False)
    projector_type  = models.BooleanField(default=False)
    projector_brightness  = models.BooleanField(default=False)
    input_voltage_in_V = models.BooleanField(default=False)
    power_vonsumption_in_W = models.BooleanField(default=False)
    dimension_LxWxH = models.BooleanField(default=False)
    sewing_machine_material = models.BooleanField(default=False)
    no_of_stitche_choice = models.BooleanField(default=False)
    sewing_machine_features = models.BooleanField(default=False)
    stitches_per_minute = models.BooleanField(default=False)
    iron_steamer_type = models.BooleanField(default=False)
    soleplate_type = models.BooleanField(default=False)
    viron_features = models.BooleanField(default=False)
    max_moisture_removal =models.BooleanField(default=False)
    vacuum_cleaner_funcn =models.BooleanField(default=False)
    run_tme=models.BooleanField(default=False)
    airwatts =models.BooleanField(default=False)
    cord_length =models.BooleanField(default=False)
    suction_power =models.BooleanField(default=False)
    robot_vacuum_featrs =models.BooleanField(default=False)
    vacuum_clnr_featrs =models.BooleanField(default=False)
    corded_or_cordless =models.BooleanField(default=False)
    vaccume_cleaner_floor_care =models.BooleanField(default=False)
    smart_TV =models.BooleanField(default=False)
    tv_port_input =models.BooleanField(default=False)
    tv_features =models.BooleanField(default=False)
    tv_type=models.BooleanField(default=False)
    tv_screen_size =models.BooleanField(default=False)
    tv_screen_type=models.BooleanField(default=False)
    water_heater_type =models.BooleanField(default=False)
    antenna_type = models.BooleanField(default=False)
    manual_device =models.BooleanField(default=False)
    water_dispenser_type = models.BooleanField(default=False)
    water_purifification = models.BooleanField(default=False)
    water_dispenser_features =models.BooleanField(default=False)
    tv_mount_feature     = models.BooleanField(default=False)
    receiver_type   = models.BooleanField(default=False)
    kettle_material = models.BooleanField(default=False)
    kettle_features = models.BooleanField(default=False)
    blender_type    = models.BooleanField(default=False)
    blender_features= models.BooleanField(default=False)
    juicer_features = models.BooleanField(default=False)
    juicer_type     = models.BooleanField(default=False)
    coffee_machine_type = models.BooleanField(default=False)
    coffee_machine_capacity = models.BooleanField(default=False)
    coffee_machine_features  = models.BooleanField(default=False)
    mixer_features= models.BooleanField(default=False)
    mixer_type = models.BooleanField(default=False)
    stove_type = models.BooleanField(default=False)
    burner_type = models.BooleanField(default=False)
    induction_cooker_features = models.BooleanField(default=False)
    no_of_burners = models.BooleanField(default=False)
    air_fryer_features = models.BooleanField(default=False)
    microwave_type = models.BooleanField(default=False)
    microwave_features = models.BooleanField(default=False)
    oven_features = models.BooleanField(default=False)
    meat_grinder_type  = models.BooleanField(default=False)
    power  =models.BooleanField(default=False)
    bettery_capacity =models.BooleanField(default=False)
    food_processor_sets   = models.BooleanField(default=False)
    multifunction_cooker_material = models.BooleanField(default=False)
    pressure_cooker_features = models.BooleanField(default=False)
    rice_cooker_features  = models.BooleanField(default=False)
    rice_cooker_features = models.BooleanField(default=False)
    no_of_people = models.BooleanField(default=False)
    rice_cooker_type = models.BooleanField(default=False)
    cooling_system_type = models.BooleanField(default=False)
    energy_tick_rating = models.BooleanField(default=False)
    refrigerator_features = models.BooleanField(default=False)
    refrigerator_motor_type = models.BooleanField(default=False)
    refrigerator_type= models.BooleanField(default=False)
    freezer_type = models.BooleanField(default=False)
    hood_features = models.BooleanField(default=False)
    hood_mount_type = models.BooleanField(default=False)
    cord_length  = models.BooleanField(default=False)
    house_alarm_type = models.BooleanField(default=False)
    alarm_volume = models.BooleanField(default=False)
                    
    
    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
       return  self.category.main_category.name + " -- " + self.category.name + " -- " + self.name
    
    def get_fields(self,include_parents=True):
              return [(field.name,field.value_from_object(self) if field.name not in ['category','name','vendor','slug'] else '') for field in self.__class__._meta.fields]
   

class Fourth_Level_Category(models.Model):
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)                 
    slug = models.SlugField(max_length=100)
    ingredient = models.BooleanField(default=False)
    igredient_preference = models.BooleanField(default=False)
    formulation = models.BooleanField(default=False)
    nutrient_type = models.BooleanField(default=False)
    expiry_date = models.BooleanField(default=False)
    bodycare_benefits = models.BooleanField(default=False)
    volume = models.BooleanField(default=False)
    HSA_notification_no = models.BooleanField(default=False)
    shelf_life = models.BooleanField(default=False)
    scrub_formulation = models.BooleanField(default=False)
    skin_type = models.BooleanField(default=False)
    product_size = models.BooleanField(default=False)
    application_area = models.BooleanField(default=False)
    weight = models.BooleanField(default=False)
    handwash_pack_size = models.BooleanField(default=False)
    handwash_packsize_measure = models.BooleanField(default=False)
    handwash_formulation = models.BooleanField(default=False)
    quantity = models.BooleanField(default=False)
    production_batch_number = models.BooleanField(default=False)
    INVIMA_certification = models.BooleanField(default=False)
    FDA_registration_no = models.BooleanField(default=False)
    manufacturer_or_trader_name = models.BooleanField(default=False)
    warranty_duration = models.BooleanField(default=False)
    warranty_type = models.BooleanField(default=False)
    scent = models.BooleanField(default=False)
    makeup_furmulation = models.BooleanField(default=False)
    skin_tone = models.BooleanField(default=False)
    SPF_choices = models.BooleanField(default=False)
    foundation_coverage = models.BooleanField(default=False)
    makeup_finish = models.BooleanField(default=False)
    bb_or_cc_scare_benefits = models.BooleanField(default=False)
    waterproof = models.BooleanField(default=False)
    lip_benefits = models.BooleanField(default=False)
    facial_steamer_skincare_benefits = models.BooleanField(default=False)
    power_source = models.BooleanField(default=False)
    safety_mark = models.BooleanField(default=False)
    mask_type = models.BooleanField(default=False)
    device_compatibility = models.BooleanField(default=False)
    injury_support_area = models.BooleanField(default=False)
    contact_lens_type = models.BooleanField(default=False)
    lens_power = models.BooleanField(default=False)
    bristle_hardness = models.BooleanField(default=False)
    oral_care_benefits = models.BooleanField(default=False)
    wings = models.BooleanField(default=False)
    scent_function = models.BooleanField(default=False)
    flow_level = models.BooleanField(default=False)
    sanitary_pad_use = models.BooleanField(default=False)
    air_flow  = models.BooleanField(default=False)
    air_purifier_filtration_type = models.BooleanField(default=False)
    cadr_rating = models.BooleanField(default=False)
    noise_level = models.BooleanField(default=False)
    air_purifier_features = models.BooleanField(default=False)
    room_size_m2  = models.BooleanField(default=False)
    max_moisture_removal = models.BooleanField(default=False)
    washing_machine_type = models.BooleanField(default=False)
    washing_machine_features = models.BooleanField(default=False)
    spin_speed = models.BooleanField(default=False)
    washing_features = models.BooleanField(default=False)
    motor_type  = models.BooleanField(default=False)
    weight_capacity_kg  = models.BooleanField(default=False)
    WELS_tick_rating  = models.BooleanField(default=False)
    model_name        = models.BooleanField(default=False)
    WELS_water_consumption_liters_per_min = models.BooleanField(default=False)
    supported_weight = models.BooleanField(default=False)
    supported_weight = models.BooleanField(default=False)


    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
       return  self.sub_category.category.main_category.name + " -- " + self.sub_category.category.name + " -- " + self.sub_category.name + " -- "+ self.name
    
class Fifth_Level_Category(models.Model):
    fourth_level_category = models.ForeignKey(Fourth_Level_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)                 
    slug = models.SlugField(max_length=100)

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
       return  self.category.main_category.name + " -- " + self.sub_category.category.name + " -- " + self.fourth_level_category.sub_category.name + " -- "+ self.fourth_level_category.name + " -- "+ self.name
    


    



class Vendor_Main_Category(models.Model):
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE,null=True,blank=True)
    description = models.TextField(max_length = 255, blank = True)
    slug = models.SlugField(max_length=100,blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name

# class category_manager(models.Manager):
#         def clothing(self):
#                 return super(category_manager,self).filter(main_category = 'clothing')
       

class Vendor_Category(models.Model):
    main_category = models.ForeignKey(Vendor_Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    slug = models.SlugField(max_length=100,blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    # objects = category_manager()

    def clean(self):
        self.name = self.name

    def __str__(self):
        return  self.name
        # return  self.main_category.name + " -- " + self.name
        
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])  
    


class Vendor_Sub_Category(models.Model):
    main_category = models.ForeignKey(Vendor_Main_Category,on_delete=models.CASCADE,null=True, blank=True)
    category = models.ForeignKey(Vendor_Category,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)                 
    vendor = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    slug = models.SlugField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def clean(self):
        self.name = self.name

    def __str__(self):
       return  self.category.main_category.name + " -- " + self.category.name + " -- " + self.name
    
class Category_Upload(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,null=True,blank=True)
    fourth_level_category = models.ForeignKey(Fourth_Level_Category,on_delete=models.CASCADE,null=True,blank=True)

    def clean(self):
        self.id = self.id