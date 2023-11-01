# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Juleb test',
    'version': '1.0.0',
    'category': 'Custom',
    'summary': 'Custom',
    'description': 'Import Bulk Dependencies',
    'sequence': '1',
    'website': 'https://www.juleb.com',
    'author': 'Odoo Mates, Odoo SA',
    'maintainer': 'Tubagus Suhendra',
    'license': 'LGPL-3',
    'support': 'tubagus.suhendra08@gmail.com',
    'depends': [
        'base','stock',
    ],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/import_product_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

