# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoDeAnimal(models.Model):
	_name = 'vetclin.tipodeanimal'
	_description = 'Tipo de Animal'

	id = fields.Integer()
	name = fields.Char(string="Especie")
	raca = fields.Char(string="Raca")
	animal_ids = fields.One2many('vetclin.animal', 'tipodeanimal_id', string="Animais")

class Animal(models.Model):
	_name = 'vetclin.animal'
	_description = 'Animal'

	id = fields.Integer()
	nome = fields.Char(string="Nome do animal")
	tipodeanimal_id = fields.Many2one('vetclin.tipodeanimal', ondelete='cascade', string="Tipo de animal")
	cliente_id = fields.Many2one('res.partner', ondelete='cascade', string="Dono")

class Procedimento(models.Model):
	_name = 'vetclin.procedimento'
	_description = 'Procedimento'

	id = fields.Integer()
	name = fields.Char(string="Procedimento")
	desc_procedimento = fields.Char(string="Descrição do Procedimento")
	#consulta_id = fields.One2many('vetclin.consulta' , 'procedimento_id', string="Consulta")
	consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Consulta")

class Consulta(models.Model):
	_name = 'vetclin.consulta'
	_description = 'Consulta'

	id = fields.Integer()
	observacao = fields.Char(string="Observações")
	#procedimento_id = fields.Many2one('vetclin.procedimento', ondelete='cascade', string="Procedimento")	
	procedimento_id = fields.One2many('vetclin.procedimento' , 'consulta_id', string="Procedimento")
	medicamento_id = fields.One2many('vetclin.medicamento' , 'consulta_id', string="Medicamento")
	#medicamento_id = fields.Many2one('vetclin.medicamento', ondelete='cascade', string="Medicamento")
	animal_id = fields.Many2one('vetclin.animal', ondelete='cascade', string="Animal")		
	veterinario_id = fields.Many2one('res.partner', ondelete='cascade', string="veterinario")

class Medicamento(models.Model):
	_name = 'vetclin.medicamento'
	_description = 'Medicamento'

	id = fields.Integer()
	name = fields.Char(string="Medicamento")
	comp_quimica = fields.Char(string="Composição Química")
	#consulta_id = fields.One2many('vetclin.consulta' , 'medicamento_id', string="medicamento")
	consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Medicamento")


class Partner(models.Model):
	_inherit = 'res.partner'
	_description = 'Custom Partners'


	#Generico
	numero_casa = fields.Char(string="Num. Casa")
	#Dono
	cpf = fields.Char(string="CPF do Cliente")	
	is_dono = fields.Boolean(string="Dono", readonly=True, default=False)
	name_dono = fields.Char('Nome', placeholder='Nome do Cliente')
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
	consulta_id = fields.One2many('vetclin.consulta', 'veterinario_id', string="Veterinário")

#class Clinica(models.Model):
#	_name =  'vetclin.clinica'
#	_description = 'Clinica'
#
#	id = fields.Integer()
#	endereco = fields.Char(string="Endereco")
#	telefone = fields.Char(string="Telefone")
#	email = fields.Char(string="Email")
#	razao_social = fields.Char(string="Razão Social")
#	cnpj =  fields.Char(string="CNPJ da Empresa")
#	consultorio_id = fields.One2many('vetclin.Consultorio', 'id')

#class Consultorio(models.Model):
#	_name = 'vetclin.consultorio'
#	_description = 'Consultorio'
#
#	id = fields.Integer()
#	descricao = fields.Text(string="Descrição")
#	ramal = fields.Char(string="Ramal")
#	clinica_ids = fields.Many2one('vetclin.clinica', ondelete='cascade')

#class Servico(models.Model):
#	_inherit = 'product.template'
#	
#	tipo = fields.Selection([('produto', 'Produto'),('servico', 'Serviço')], string="Tipo")
#	descricao = fields.Text(string="Descrição do servico/produto")
#	preco = fields.Float(digits=(6,2), string="Preço")	
#	servico_medicamento = fields.Many2many('vetclin.medicamento', string="Medicamento_Serviço/Produto")


#class Servico(models.Model):
#	_name = 'vetclin.servico'
#	_description = 'Serviços'

#class Produto(models.Model):
#	_inherit = 'product.template'


class Medicamento(models.Model):
	_name = 'vetclin.medicamento'
	_description = 'Medicamento'

	id = fields.Integer()
	nome = fields.Char(string="Nome do medicamento")
	composicao_quimica = fields.Char(string="Composição Química")

#class Consulta(models.Model):
#	_name = 'vetclin.consulta'
#	_description = 'Consulta'
#
#	id = fields.Integer()
#	data_hora = fields.Datetime.now()
#	observacoes = fields.Text(string="Observações")
#	preco_total = fields.Float(digits=(8,2), string="Preço total")
#	animal_id = fields.Many2one('vetclin.animal', ondelete='cascade', string="Animal")
#	veterinario_id = fields.Many2one('vetclin.veterinario', ondelete='cascade', string="Veterinário")
#	consultorio_id = fields.Many2one('vetclin.consultorio', ondelete='cascade', string="Consultório")
#	servico_consulta = fields.Many2many('vetclin.servico', string="Servicos_Consultas")
