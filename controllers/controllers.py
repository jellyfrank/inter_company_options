# -*- coding: utf-8 -*-
from odoo import http

# class ZpwInterCompany(http.Controller):
#     @http.route('/zpw_inter_company/zpw_inter_company/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zpw_inter_company/zpw_inter_company/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zpw_inter_company.listing', {
#             'root': '/zpw_inter_company/zpw_inter_company',
#             'objects': http.request.env['zpw_inter_company.zpw_inter_company'].search([]),
#         })

#     @http.route('/zpw_inter_company/zpw_inter_company/objects/<model("zpw_inter_company.zpw_inter_company"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zpw_inter_company.object', {
#             'object': obj
#         })