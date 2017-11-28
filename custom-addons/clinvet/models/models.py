# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoDeAnimal(models.Model):
	_name = 'vetclin.tipodeanimal'
	_description = 'Tipo de Animal'

	id = fields.Integer()
	name = fields.Char(string="Especie")
	raca = fields.Char(string="Raca")
	animal_ids = fields.One2many('vetclin.animal', 'tipodeanimal_id', string="Animais")

class Servico(models.Model):
	_name = 'vetclin.servico'
	_description = 'Serviços'

	id = fields.Integer()
	name = fields.Char(string="Serviço")
	descricao = fields.Text(string="Descrição do Serviço")
	consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Consulta")

class Consulta(models.Model):
	_name = 'vetclin.consulta'
	_description = 'Consulta'

	id = fields.Integer()
	observacao = fields.Char(string="Observações")
	procedimento_id = fields.One2many('vetclin.servico' , 'consulta_id', string="Serviço")
	medicamento_id = fields.One2many('vetclin.medicamento' , 'consulta_id', string="Medicamento")
	animal_id = fields.Many2one('vetclin.animal', ondelete='cascade', string="Animal")		
	#veterinario_id = fields.Many2one('res.partner', ondelete='cascade', string="veterinario")
	consultorio_id = fields.Many2one('vetclin.consultorio', ondelete='cascade', string="Consultorio")		

class Medicamento(models.Model):
	_name = 'vetclin.medicamento'
	_description = 'Medicamento'

	id = fields.Integer()
	name = fields.Char(string="Medicamento")
	comp_quimica = fields.Char(string="Composição Química")
	consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Medicamento")

class Animal(models.Model):
	_name = 'vetclin.animal'
	_description = 'Animal'

	id = fields.Integer()
	name = fields.Char(string="Nome do animal")
	tipodeanimal_id = fields.Many2one('vetclin.tipodeanimal', ondelete='cascade', string="Tipo de animal")
	cliente_id = fields.Many2one('res.partner', ondelete='cascade', string="Dono")
	consulta_id = fields.One2many('vetclin.consulta' , 'animal_id', string="animal")

class Produto(models.Model):
	_name = 'vetclin.produto'
	_description = 'Produto'

	id = fields.Integer()
	nome_produto = fields.Char(string="Produto")
	desc_produto = fields.Char(string="Descrição do Produto")

class Clinica(models.Model):
    _inherit =  'res.company'
    _description = 'Clinica'

    razão_social = fields.Text(string="Razão Social")
    consultorio_ids = fields.One2many('vetclin.consultorio', 'clinica_id')

class Consultorio(models.Model):
    _name = 'vetclin.consultorio'
    _description = 'Consultorio'

    id = fields.Integer()
    nome = fields.Text(string="Nome")
    descricao = fields.Text(string="Descrição")
    ramal = fields.Char(string="Ramal")
    clinica_id = fields.Many2one('res.company', ondelete='cascade')

class Partner(models.Model):
	_inherit = 'res.partner'
	_description = 'Custom Partners'

	#Generico
	numero_casa = fields.Char(string="Num. Casa")
	#Dono
	cpf = fields.Char(string="CPF do Cliente")	
	is_dono = fields.Boolean(string="Dono", readonly=True, default=False)
	#Veterinario
	salario = fields.Float(digits=(7,2), string="Salario")
	crmv = fields.Char(string="Registro Veterinario")
	data_admissao = fields.Date(string="Data de admissao")
	data_demissao = fields.Date(string="Data de demissao")
	is_veterinario = fields.Boolean(string="Veterinario", readonly=True, default=False)
	#ja existentes
	email = fields.Char(string="Email")
	phone = fields.Char(string="Telefone")	
	mobile = fields.Char(string="Celular")
	#relações
	animal_ids = fields.One2many('vetclin.animal', 'cliente_id', string="Animais")