from django.contrib import admin

from orders.models import DisputeImages, Order, OrderProduct, OrderUpdate, Payment, Refund, Return_main_reason, Return_reason, VendorPayout,Return_VendorPayout

# Register your models here.

def make_refund_accepted(modeladmin,request,queryset):
    queryset.update(refund_requested = False,refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order','product','variant','quantity','product_price','ordered','created_at','updated_at','refund_requested','refund_granted','is_cancelled','ref_code','accepted','status','vendor']
    list_filter = ['order','product','variant','quantity','product_price','ordered','created_at','updated_at','refund_requested','refund_granted','is_cancelled','ref_code','accepted','status','vendor']

    # def get_queryset(self, request):
    #     qs = super(OrderProductAdmin, self).get_queryset(request)
    #     return qs.annotate(num_fixture_metas=Count('fixturemeta'))

    # def num_fixture_metas_count(self, obj):
    #   return obj.num_fixture_metas
    # num_fixture_metas_count.short_description = 'Fixture Count'
    # num_fixture_metas_count.admin_order_field = 'num_fixture_metas'    

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','product','quantity','ref_code','product_price','refund_requested','is_cancelled')
    extra=0



class OrderAdmin(admin.ModelAdmin) :
    list_display = ['order_number','ref_code','first_name','last_name','phone','email','order_total','tax','status','order_placed_to','is_ordered','created_at','received','refund_requested','refund_granted','days_since_created']
    list_filter = ['status','is_ordered','received','refund_requested','refund_granted','created_at']
    search_fields = ['order_number','first_name','last_name','phone','email','ref_code']
    list_per_page=20
    inlines = [OrderProductInline]
    actions = [make_refund_accepted]

class ReturnReasonAdmin(admin.ModelAdmin) :
    list_display = ['main_reason','reason']
    list_editable = ('reason',)
   

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Payment)
admin.site.register(OrderUpdate)
admin.site.register(Refund)
admin.site.register(Return_main_reason)
admin.site.register(Return_reason)
admin.site.register(DisputeImages)

