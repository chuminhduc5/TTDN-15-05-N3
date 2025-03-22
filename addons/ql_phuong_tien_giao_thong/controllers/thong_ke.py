# from odoo import http
# from odoo.http import request
# import json
#
# class ThongKeController(http.Controller):
#     @http.route('/thongke/chart_data', type='json', auth='user')
#     def get_chart_data(self):
#         data = {
#             'labels': ['Sẵn sàng', 'Đang hoạt động', 'Bảo trì'],
#             'datasets': [{
#                 'data': [
#                     request.env['phuong_tien'].search_count([('trang_thai', '=', 'san_sang')]),
#                     request.env['phuong_tien'].search_count([('trang_thai', '=', 'dang_hoat_dong')]),
#                     request.env['phuong_tien'].search_count([('trang_thai', '=', 'bao_tri')])
#                 ],
#                 'backgroundColor': ['#36A2EB', '#FFCE56', '#FF6384']
#             }]
#         }
#         return data
