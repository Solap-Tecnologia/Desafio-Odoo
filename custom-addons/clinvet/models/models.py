# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

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

class Consulta(models.Model):
	_name = 'vetclin.consulta'
	_description = 'Consulta'

	id = fields.Integer()
	observacao = fields.Text(string="Observações")
	preco_total = fields.Float(string="Preço Total", digits=(7,2), compute='calc_preco_total', readonly=True)
	servicos_id = fields.Many2many('vetclin.servico')
	produtos_id = fields.Many2many('product.template')
	animal_id = fields.Many2one('vetclin.animal', ondelete='cascade', string="Animal")		
	veterinario_id = fields.Many2one('res.partner', ondelete='cascade', string="Veterinário")
	consultorio_id = fields.Many2one('vetclin.consultorio', ondelete='cascade', string="Consultorio")
	start_date = fields.Datetime(string="Data e Horário de início")
	duration = fields.Float(digits=(6, 2), help="Duração em dias")
	end_date = fields.Datetime(string="Término da Consulta")
	name = fields.Text(string='Consultas')
    
	@api.one
	@api.depends('servicos_id', 'servicos_id.preco', 'produtos_id', 'produtos_id.list_price')
	def calc_preco_total(self):
		precoatual = 0
		for servico in self.servicos_id:
			precoatual += servico.preco
		for produto in self.produtos_id:
			precoatual += produto.list_price
		self.preco_total = precoatual

class Animal(models.Model):
	_name = 'vetclin.animal'
	_description = 'Animal'

	id = fields.Integer()
	name = fields.Char(string="Nome do animal")
	tipodeanimal_id = fields.Many2one('vetclin.tipodeanimal', ondelete='cascade', string="Tipo de animal")
	cliente_id = fields.Many2one('res.partner', ondelete='cascade', string="Dono")
	consulta_ids = fields.One2many('vetclin.consulta' , 'animal_id', string="Animal")

class Produto(models.Model):
	_inherit = 'product.template'
	_description = 'Custom Products'

	name = fields.Char(string="Produto")
	description  = fields.Text(string="Descrição")
	list_price = fields.Float(string="Preço de Venda")
	medic_ids = fields.Many2many('vetclin.medicamento','vet_prod_med_rel',string="Medicamentos")

class Clinica(models.Model):
    _inherit =  'res.company'
    _description = 'Clinica'

    name = fields.Char(string="Clínica")
    razão_social = fields.Text(string="Razão Social")
    consultorio_ids = fields.One2many('vetclin.consultorio', 'clinica_id')

    @api.multi
    @api.onchange('company_registry')
    def check_cnpj(self):
        if self.company_registry:
            if (len(self.company_registry) == 14):
                if self.check_cnpj_com_numeros_iguais(self.company_registry): 
                    raise UserError('CNPJ Inválido')
                elif self.verifica_cnpj(self.company_registry,12,5) != int(self.company_registry[12]) and self.verifica_cnpj(self.company_registry,13,6) != int(self.company_registry[13]):
                    raise UserError('CNPJ Inválido')
                else:
                    print("ok")
            else:
                raise UserError('CNPJ Inválido')

    def check_cnpj_com_numeros_iguais(self, cnpj):
        indice = 0
        while indice < len(cnpj)-1:
            if cnpj[indice] == cnpj[indice+1]:
                boolean = True
            else:
                boolean = False
                break			
            indice += 1		
        return boolean
    
    def verifica_cnpj(self, cnpj, vezes, cont):
        soma = 0
        for n in range(0, vezes):
            soma += cont * int(cnpj[n])
            if cont == 2:
                cont = 9
            else:
                cont -= 1
        if (soma % 11) < 2:
            digito = 0
        else:
            digito = 11 - (soma % 11)		
        return digito

class Consultorio(models.Model):
    _name = 'vetclin.consultorio'
    _description = 'Consultorio'

    id = fields.Integer()
    name = fields.Text(string="Nome")
    descricao = fields.Text(string="Descrição")
    ramal = fields.Char(string="Ramal")
    clinica_id = fields.Many2one('res.company', ondelete='cascade')

class Partner(models.Model):
	_inherit = 'res.partner'
	_description = 'Custom Partners'

	#Generico
	numero_casa = fields.Char(string="Num. Casa")
	#Dono
	cpf = fields.Char(string="CPF do Cliente", default="45532325880")	
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

class Medicamento(models.Model):
	_name = 'vetclin.medicamento'
	_description = 'Medicamento'

	id = fields.Integer()
	name = fields.Char(string="Medicamento")
	comp_quimica = fields.Text(string="Composição Química")
	consulta_id = fields.Many2one('vetclin.consulta', ondelete='cascade', string="Medicamento")