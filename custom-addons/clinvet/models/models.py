# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api

class TipoDeAnimal(models.Model):
	_name = 'vetclin.tipodeanimal'
	_description = 'Tipo de Animal'

	id = fields.Integer()
	name = fields.Char(string="Espécie")
	raca = fields.Char(string="Raça")
	animal_ids = fields.One2many('vetclin.animal', 'tipodeanimal_id', string="Animais")

class Servico(models.Model):
	_name = 'vetclin.servico'
	_description = 'Serviços'

	id = fields.Integer()
	name = fields.Char(string="Serviço")
	descricao = fields.Text(string="Descrição do Serviço")
	preco = fields.Float(string="Preço", digits=(7,2))
	#consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Consulta")

class Consulta(models.Model):
	_name = 'vetclin.consulta'
	_description = 'Consulta'

	id = fields.Integer()
	observacao = fields.Text(string="Observações")
	servicos_id = fields.Many2many('vetclin.servico')
	#medicamento_id = fields.One2many('vetclin.medicamento' , 'consulta_id', string="Medicamento")
	animal_id = fields.Many2one('vetclin.animal', ondelete='cascade', string="Animal")		
	veterinario_id = fields.Many2one('res.partner', ondelete='cascade', string="Veterinário")
	consultorio_id = fields.Many2one('vetclin.consultorio', ondelete='cascade', string="Consultorio")
	start_date = fields.Datetime()
	duration = fields.Float(digits=(6, 2), help="Duração em dias")
	end_date = fields.Datetime(string="Agendamento de Consultas")
	name = fields.Text(string='Consultas')
    
	'''@api.depends('start_date', 'duration')
	def _get_end_date(self):
		for r in self:
			if not (r.start_date and r.duration):
				r.end_date = r.start_date
				continue

			start = fields.Datetime.from_string(r.start_date)
			duration = timedelta(days=r.duration)
			r.end_date = start + duration

	def _set_end_date(self):
		for r in self:
			if not (r.start_date and r.end_date):
				continue

			start_date = fields.Datetime.from_string(r.start_date)
			end_date = fields.Datetime.from_string(r.end_date)
			r.duration = (end_date - start_date).days''' 




	'''clinica_id = fields.Many2one('res.company',ondelete='cascade', string="Clínica")'''	

#class CalendarioDeConsulta(models.Model):
#    _name = "vetclin.calendario" 
#    _columns = {
#        'name': fields.Char('Calendário',size=20,required=True),
#        'date_start':fields.Datetime(string='Início Consulta'),
#       'date_stop':fields.Datetime(string='Fim Consulta'),
#    }
    	

''' Relacionar com a classe Produto '''
#class Medicamento(models.Model):
#	_name = 'vetclin.medicamento'
#	_description = 'Medicamento'
#
#	id = fields.Integer()
#	name = fields.Char(string="Medicamento")
#	comp_quimica = fields.Text(string="Composição Química")
#	consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Medicamento")

class Animal(models.Model):
	_name = 'vetclin.animal'
	_description = 'Animal'

	id = fields.Integer()
	name = fields.Char(string="Nome do animal")
	tipodeanimal_id = fields.Many2one('vetclin.tipodeanimal', ondelete='cascade', string="Tipo de animal")
	cliente_id = fields.Many2one('res.partner', ondelete='cascade', string="Dono")
	consulta_id = fields.One2many('vetclin.consulta' , 'animal_id', string="animal")

''' Extender o model product.template '''
#class Produto(models.Model):
#	_name = 'vetclin.produto'
#	_description = 'Produto'
#
#	id = fields.Integer()
#	name = fields.Char(string="Nome")
#	descricao = fields.Text(string="Descrição do Produto")

class Clinica(models.Model):
    _inherit =  'res.company'
    _description = 'Clinica'

    razão_social = fields.Text(string="Razão Social")
    consultorio_ids = fields.One2many('vetclin.consultorio', 'clinica_id')
    '''consulta_id = fields.Many2one('vetclin.consulta', 'consulta_id')'''

class Consultorio(models.Model):
    _name = 'vetclin.consultorio'
    _description = 'Consultorio'

    id = fields.Integer()
    name = fields.Text(string="Nome")
    descricao = fields.Text(string="Descrição")
    ramal = fields.Char(string="Ramal")
    clinica_id = fields.Many2one('res.company', ondelete='cascade')
#    consulta_id = fields.Many2one('vetclin.consulta', 'consulta_id')


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
	email = fields.Char(string="Email", placeholder="Ex.: email@dominio.com")
	phone = fields.Char(string="Telefone", placeholder="Ex.: (00) 00000-0000")	
	mobile = fields.Char(string="Celular", placeholder="Ex.: (00) 0000-0000")
	#relações
	animal_ids = fields.One2many('vetclin.animal', 'cliente_id', string="Animais")
	consulta_ids = fields.One2many('vetclin.consulta', 'veterinario_id', string="Veterinários")