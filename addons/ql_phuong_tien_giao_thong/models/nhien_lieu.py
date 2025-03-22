from odoo import models, fields

class NhienLieu(models.Model):
    _name = 'nhien_lieu'
    _description = 'Bảng chứa thông tin tiêu hao nhiên liệu'

    ma_phuong_tien = fields.Many2one('phuong_tien', string="Phương tiện", required=True)

    luong_tieu_hao_nhien_lieu = fields.Float(string="Lượng tiêu hao nhiên liệu (L/100km)")
    thoi_gian_cap_nhat = fields.Datetime(string="Cập nhật lần cuối", default=fields.Datetime.now)

    def name_get(self):
        result = []
        for record in self:
            name = record.ma_phuong_tien.ma_phuong_tien
            result.append((record.id, name))
        return result