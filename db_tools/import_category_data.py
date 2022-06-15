import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

import django

django.setup()
from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

for level1_cat in row_data:
    level1_instance = GoodsCategory()
    level1_instance.code = level1_cat['code']
    level1_instance.name = level1_cat['name']
    level1_instance.category_type = 1
    level1_instance.save()

    for level2_cat in level1_cat['sub_categorys']:
        level2_instance = GoodsCategory()
        level2_instance.code = level2_cat['code']
        level2_instance.name = level2_cat['name']
        level2_instance.category_type = 2
        level2_instance.parent_category = level1_instance
        level2_instance.save()

        for level3_cat in level2_cat['sub_categorys']:
            level3_instance = GoodsCategory()
            level3_instance.code = level3_cat['code']
            level3_instance.name = level3_cat['name']
            level3_instance.category_type = 3
            level3_instance.parent_category = level2_instance
            level3_instance.save()