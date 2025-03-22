# -*- coding: utf-8 -*-
{
    'name': "QL Phương Tiện Giao Thông",
    'depends': ['base', 'nhan_su'],

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/thong_ke.xml',
        'views/phuong_tien.xml',
        'views/loai_xe.xml',
        'views/nhien_lieu.xml',
        'views/bao_tri.xml',
        'views/nv_noi_bo.xml',
        'views/phong_ban.xml',
        'views/vi_tri.xml',
        'views/phieu_muon_xe.xml',
        'views/lich_su_su_dung.xml',
        'views/menu.xml',
        # 'data/sequence.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
