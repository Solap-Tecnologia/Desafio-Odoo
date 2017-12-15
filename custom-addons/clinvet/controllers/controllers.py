# -*- coding: utf-8 -*-
from odoo import http

# class Vetclin(http.Controller):
#     @http.route('/vetclin/vetclin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vetclin/vetclin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vetclin.listing', {
#             'root': '/vetclin/vetclin',
#             'objects': http.request.env['vetclin.vetclin'].search([]),
#         })

#     @http.route('/vetclin/vetclin/objects/<model("vetclin.vetclin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vetclin.object', {
#             'object': obj
#         })