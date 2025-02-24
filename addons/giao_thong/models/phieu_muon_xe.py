from pygments.lexer import default
from odoo import models, fields, api

class PhieuMuonXe(models.Model):
    _name = 'phieu_muon_xe'
    _description = 'Bảng chứa thông tin phiếu mượn xe'

    ngay_muon = fields.Datetime("Ngày mượn", required=True, default=fields.Datetime.now())
    ngay_tra = fields.Date("Ngày trả", required=True)
    trang_thai = fields.Selection([
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả'),
    ], string="Trạng thái")
    ghi_chu = fields.Text("Ghi chú")
    ngay_tao = fields.Datetime("Ngày tạo", required=True, default=fields.Datetime.now())
    ngay_cap_nhat = fields.Datetime("Ngày cập nhật", required=True, default=fields.Datetime.now())

    def write(self, vals):
        vals['ngay_cap_nhat'] = fields.Datetime.now().date()
        return super(PhieuMuonXe, self).write(vals)