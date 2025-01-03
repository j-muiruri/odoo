# -*- coding: utf-8 -*-
# from odoo import http


# class PropertyUsers(http.Controller):
#     @http.route('/property_users/property_users', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/property_users/property_users/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('property_users.listing', {
#             'root': '/property_users/property_users',
#             'objects': http.request.env['property_users.property_users'].search([]),
#         })

#     @http.route('/property_users/property_users/objects/<model("property_users.property_users"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('property_users.object', {
#             'object': obj
#         })

