# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Especie(models.Model):
	_name = 'vetclin.especie'
	_description = 'Espécie'

	id = fields.Integer()
	name = fields.Char(string="Espécie")

class Raca(models.Model):
	_name = 'vetclin.raca'
	_description = 'Raças'

	id = fields.Integer()
	name = fields.Char(string="Raça")
	especie_id = fields.Many2one('vetclin.especie', ondelete='cascade')
	especie_name = fields.Char(related='especie_id.name')

class Consulta(models.Model):
	_name = 'vetclin.consulta'
	_description = 'Consulta'

	id = fields.Integer()
	observacao = fields.Text(string="Observações")
	
	
	
	animal_id = fields.Many2one('vetclin.animal', ondelete='cascade', string="Animal")		
	veterinario_id = fields.Many2one('res.partner', ondelete='cascade', string="Veterinário")
	consultorio_id = fields.Many2one('vetclin.consultorio', ondelete='cascade', string="Consultorio", required=True)		
	
	serv_ids = fields.One2many('product.template.servico','cons_id',string="Serviços")
	med_prod_ids = fields.One2many('product.template.med_prod','cons_id',string="Medicamento e Produtos")
	
	start_date = fields.Datetime()
	duration = fields.Float(digits=(6, 2), help="Duração em dias")
	end_date = fields.Datetime(string="Agendamento de Consultas")
	name = fields.Text(string='Consultas')
	@api.multi
	@api.depends('serv_ids', 'serv_ids.preco_serv')
	def _calc_preco_serv_total(self):
		precototal1 = 0
		for servico in self.serv_ids:
			precototal1 += servico.preco_serv
		self.preco_total_serv = precototal1
	
	preco_total_serv = fields.Float(string="Preço Total Serviço", digits=(7,2), compute='_calc_preco_serv_total', readonly=True)
	
	@api.multi
	@api.depends('med_prod_ids', 'med_prod_ids.preco_med_prod')
	def _calc_preco_med_prod_total(self):
		precototal2 = 0
		for mprod in self.med_prod_ids:
			precototal2 += mprod.preco_med_prod
		self.preco_total_med_prod = precototal2
	
	preco_total_med_prod = fields.Float(string="Preço Total Medicamento e Produto", digits=(7,2), compute='_calc_preco_med_prod_total', readonly=True)#, default='0'

	@api.multi
	@api.depends('preco_total_med_prod','preco_total_serv')
	def _calc_preco_final_total(self):
		precototal3 = 0
		precototal3 = self.preco_total_serv + self.preco_total_med_prod
		self.preco_total_final = precototal3
	
	preco_total_final = fields.Float(string="Preço Total Final", digits=(7,2), compute='_calc_preco_total_final', readonly=True)
    
class Animal(models.Model):
	_name = 'vetclin.animal'
	_description = 'Animal'	

	id = fields.Integer()
	name = fields.Char(string="Nome do animal")
	cliente_id = fields.Many2one('res.partner', ondelete='cascade', string="Dono")
	especie_id = fields.Many2one('vetclin.especie', ondelete='cascade', string="Espécie")
	raca_id = fields.Many2one('vetclin.raca', ondelete='cascade', string="Raça")	

class Produto(models.Model):
	_inherit = 'product.template'
	_description = 'Custom Products'

	name = fields.Char(string="Nome do Produto/Medicamento/Serviço")
	is_prod = fields.Boolean(string="Novo Produto", readonly=True, default=False)
	is_serv = fields.Boolean(string="Novo Servico", readonly=True, default=False)
	is_med = fields.Boolean(string="Novo Medicamento", readonly=True, default=False)
	cmp_ids = fields.One2many('product.template.cmp_quimica','med_id',string='Composição')
	serv_id = fields.Many2one('product.template.servico')
	mprod_id = fields.Many2one('product.template.med_prod')

class Consultorio(models.Model):
    _name = 'vetclin.consultorio'
    _description = 'Consultorio'

    id = fields.Integer()
    name = fields.Text(string="Nome")
    descricao = fields.Text(string="Descrição")
    ramal = fields.Char(string="Ramal")

class Partner(models.Model):
	_inherit = 'res.partner'
	_description = 'Custom Partners'

	numero_casa = fields.Char(string="Num. Casa")
	cpf = fields.Char(string="CPF do Cliente")	
	is_dono = fields.Boolean(string="Dono", readonly=True, default=False)
	salario = fields.Float(digits=(7,2), string="Salario")
	crmv = fields.Char(string="Registro Veterinario")
	data_admissao = fields.Date(string="Data de admissao")
	data_demissao = fields.Date(string="Data de demissao")
	is_veterinario = fields.Boolean(string="Veterinario", readonly=True, default=False)
	email = fields.Char(string="Email")
	phone = fields.Char(string="Telefone")	
	mobile = fields.Char(string="Celular")
	animal_ids = fields.One2many('vetclin.animal', 'cliente_id', string="Animais")
	consulta_ids = fields.One2many('vetclin.consulta', 'veterinario_id', string="Veterinários")
	
	@api.multi
	@api.onchange('cpf')
	def check_cpf(self):
		if self.cpf:
			if (len(self.cpf) == 11):
				if self.check_cpf_com_numeros_iguais(self.cpf): 
					raise UserError('CPF Inválido')
				elif self.return_digito_verificador(self.cpf, 9, 10) != int(self.cpf[9]) and \
				 	self.return_digito_verificador(self.cpf, 10, 11) != int(self.cpf[10]):
					
					raise UserError('CPF Inválido')
				else:
					print("ok")
			else:
				raise UserError('CPF Inválido')

	def check_cpf_com_numeros_iguais(self, cpf):
		indice = 0
		while indice < len(cpf)-1:
			if cpf[indice] == cpf[indice+1]:
				boolean = True
			else:
				boolean = False
				break			
			indice += 1		
		return boolean

	def return_digito_verificador(self, cpf, vezes, cont):
		soma = 0
		for n in range(0, vezes):
			soma += cont * int(cpf[n])
			cont -= 1	
		if (soma % 11) < 2:
			digito = 0
		else:
			digito = 11 - (soma % 11)		
		return digito

class Cmp_Quimica(models.Model):
	_name = 'vetclin.cmp_quimica'
	_description = 'Composto Quimicos'

	id = fields.Integer()
	name = fields.Char(string="Nome do Composto Quimico")

class Medic_comp(models.Model):
	_name = 'product.template.cmp_quimica'
	_description = "Relação de composição e medicamento"

	cmp_id = fields.Many2one('vetclin.cmp_quimica',string='Componentes Químicos')
	med_id = fields.Many2one('product.template')
	value = fields.Float(digits=(7,2),string='Quantidade do Componente')
	uom_id = fields.Many2one('product.uom',string="Unidade de Medida")

class Cons_serv(models.Model):
	_name = 'product.template.servico'
	_description = 'Relação de servico e consulta'

	serv_ids = fields.One2many('product.template','serv_id',string='Serviços')
	cons_id = fields.Many2one('vetclin.consulta')
	qtd = fields.Integer(string='Quantidade',default='1')
	
	@api.one
	@api.depends('serv_ids', 'serv_ids.list_price', 'qtd')
	def _calc_preco_serv(self):
		precoserv =  0.0
		for servico in self.serv_ids:
			precoserv = (servico.list_price * self.qtd)
		self.preco_serv = precoserv
	
	preco_serv = fields.Float(string="Preço Serviço", digits=(7,2), compute='_calc_preco_serv', readonly=True)
	
	@api.multi
	@api.depends('serv_ids','serv_ids.list_price')
	def _calc_preco_uni_serv(self):
		precoserv = 0	
		#precoserv =  serv_id.list_price
		for servico in self.serv_ids:
			precoserv = servico.list_price 
		self.preco_serv_uni = precoserv
	
	preco_serv_uni = fields.Float(string="Preço Unitário", digits=(7,2), compute='_calc_preco_uni_serv', readonly=True)

class Cons_med_prod(models.Model):
	_name = 'product.template.med_prod'
	_description = 'Relação de medicamento/produto e consulta'

	med_prod_ids = fields.One2many('product.template','mprod_id',string='Med/Prod')
	cons_id = fields.Many2one('vetclin.consulta')
	qtd = fields.Integer(string='Quantidade',default='1')

	#preco_med_prod_uni = fields.Float(digits=(7,2), related="med_prod_id.list_price", readonly=True, string="Preço unitário")
	@api.one
	@api.depends('med_prod_ids', 'med_prod_ids.list_price', 'qtd')
	def _calc_preco_med_prod(self):
		precomprod = 0.0
		for mprod in self.med_prod_ids:
			precomprod = (mprod.list_price * qtd)
		self.preco_med_prod = precomprod
	
	preco_med_prod = fields.Float(string="Preço Serviço", digits=(7,2), compute='_calc_preco_med_prod', readonly=True)

	@api.one
	@api.depends('med_prod_ids','med_prod_ids.list_price')
	def _calc_preco_uni_med_prod(self):
		precomprod = 0
		#precomprod = med_prod_id.list_price
		for mprod in self.med_prod_ids:
			precomprod = mprod.list_price * 1 
		self.preco_med_prod_uni = precomprod

	preco_med_prod_uni = fields.Float(string="Preço Unitário", digits=(7,2), compute='_calc_preco_uni_med_prod', readonly=True)