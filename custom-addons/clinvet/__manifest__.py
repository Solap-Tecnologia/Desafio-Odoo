# -*- coding: utf-8 -*-
{
    'name': "vetclin",
    'summary': """
        Módulo para gestão de clínica veterinária.""",
    'description': """
        Módulo destinado para gestão e controle de uma clínica veterinária, 
        com opção até de nota fiscal paulista.
    """,
    'author': "Grupo SOLAP",
    'website': "https://www.solap.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Management',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base',
                'product'],
    # always loaded
    'data': [
        'views/menu.xml',
        'views/medicamento.xml',
        'views/tipodeanimal.xml',
        'views/dono.xml',
        'views/animal.xml',
        'views/produto.xml',
        'views/procedimento.xml',
        'views/veterinario.xml',
        'views/clinica.xml',
        'views/consultorio.xml',
        'views/consulta.xml',
        #'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}
