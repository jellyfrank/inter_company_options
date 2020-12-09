# -*- coding: utf-8 -*-
{
    'name': "多公司业务规则",

    'summary': """
        提供了多公司间业务规则的选择设置功能
    """,

    'description': """
        * 销售到采购 同步计量单位、数量和价格
        * 采购到销售 同步计量单位、数量和价格
    """,

    'author': "KevinKong",
    'website': "http://www.odoomommy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '12.1',

    # any module necessary for this one to work correctly
    'depends': ['inter_company_rules'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}