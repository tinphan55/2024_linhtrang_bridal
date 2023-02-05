from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from services_admin.models import Clothe

class ProductResource(resources.ModelResource):
    region = fields.Field(
        column_name ='region',
        attribute = 'region',
        widget=ForeignKeyWidget(Clothe, 'name')
    )
    class Meta:
        model = Clothe
        skip_unchanged = True
        fields= ('id','name', 'ranking','qty','color' )
        
        