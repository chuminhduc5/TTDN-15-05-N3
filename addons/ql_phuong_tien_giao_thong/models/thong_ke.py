# from odoo import models, fields, api
#
# class ThongKe(models.TransientModel):
#     _name = 'thong_ke'
#     _description = 'Thống kê phương tiện'
#
#     tong_so_phuong_tien = fields.Integer(string="Tổng số phương tiện", compute="_compute_statistics")
#     so_luong_san_sang = fields.Integer(string="Sẵn sàng", compute="_compute_statistics")
#     so_luong_dang_hoat_dong = fields.Integer(string="Đang hoạt động", compute="_compute_statistics")
#     so_luong_bao_tri = fields.Integer(string="Bảo trì", compute="_compute_statistics")
#
#     def _compute_statistics(self):
#         phuong_tien_data = self.env['phuong_tien'].search([])
#         for record in self:
#             record.tong_so_phuong_tien = len(phuong_tien_data)
#             record.so_luong_san_sang = len(phuong_tien_data.filtered(lambda x: x.trang_thai == 'san_sang'))
#             record.so_luong_dang_hoat_dong = len(phuong_tien_data.filtered(lambda x: x.trang_thai == 'dang_hoat_dong'))
#             record.so_luong_bao_tri = len(phuong_tien_data.filtered(lambda x: x.trang_thai == 'bao_tri'))
#
#     def compute_stats(self):
#         self._compute_statistics()
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'thong_ke',
#             'view_mode': 'graph,form',
#             'res_id': self.id,
#             'target': 'current',
#         }