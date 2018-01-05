# -*- coding: utf-8 -*-
{
    'name': "Clínica Veterinária",
    'summary': """
        Módulo para gestão e controle de uma clínica veterinária.
    """,
    'description': """
        Esse módulo foi um desafio proposto pela equipe da BradooTech, que serviu como 
        um pontapé inicial para o Grupo Solap imergir no mundo do ERP OpenSource Odoo.
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
                'crm',
                'stock',
                'sale_management',
                'mail',
                'calendar',
                'account_invoicing',
                'contacts',],
    # always loaded
    'data': [
        'views/menu.xml',
        'views/animal.xml',
        'views/cliente_veterinario.xml',
        'views/produto.xml',
        'views/comp_quimica.xml',
        #'views/clinica.xml',
        'views/consultorio.xml',
        'views/consulta.xml',
        'views/especie.xml',
        'views/raca.xml',
        'views/fatura_pmed.xml',
        'views/fatura_serv.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
    'application':True,
}
