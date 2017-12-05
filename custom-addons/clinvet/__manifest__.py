# -*- coding: utf-8 -*-
{
    'name': "clinvet",
    'summary': """
        Clínica Veterinária
    """,
    'description': """
        Módulo destinado para gestão e controle de uma clínica veterinária.
    """,
    'author': "Grupo SOLAP",
    'website': "https://www.solap.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Management',
    'version': '1.1',
    # any module necessary for this one to work correctly
    'depends': ['base',
                'product'],
    # always loaded
    'data': [
        'views/menu.xml',
        'views/tipodeanimal.xml',
        'views/animal.xml',
        'views/cliente_veterinario.xml',
        'views/servico.xml',
        'views/produto.xml',
        'views/medicamento.xml',
        'views/clinica.xml',
        'views/consultorio.xml',
        'views/consulta.xml',
        #'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}
