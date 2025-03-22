from odoo import models, fields, api

class LichSuSuDung(models.Model):
    _name = 'lich_su_su_dung'
    _description = 'Bảng chứa thông tin lịch sử sử dụng'

    ma_phieu_muon_xe = fields.Many2one("phieu_muon_xe", "Phiếu mượn xe", required=True)
    ma_nv_noi_bo = fields.Many2one("nv_noi_bo", "Nhân viên nội bộ", related="ma_phieu_muon_xe.ma_nv_noi_bo", store=True)
    ma_phuong_tien = fields.Many2one("phuong_tien", "Phương tiện", related="ma_phieu_muon_xe.ma_phuong_tien",
                                     store=True)
    trang_thai = fields.Selection([
        ('hoan_thanh', 'Hoàn thành'),
        ('tra_muon', 'Trả muộn')
    ], string="Trạng thái", required=True)
    thoi_gian_muon_xe = fields.Datetime("Thời gian mượn xe", required=True)
    thoi_gian_tra_xe = fields.Datetime("Thời gian trả xe", required=True)
    mo_ta = fields.Text("Mô tả")

    def name_get(self):
        result = []
        for record in self:
            name = record.ma_phieu_muon_xe.ma_phieu_muon_xe
            result.append((record.id, name))
        return result
