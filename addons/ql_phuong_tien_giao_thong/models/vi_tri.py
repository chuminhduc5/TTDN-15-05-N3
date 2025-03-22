from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class ViTri(models.Model):
    _name = 'vi_tri'
    _description = 'Bảng chứa thông tin vị trí phương tiện'

    kinh_do = fields.Float("Kinh độ", required=True)
    vi_do = fields.Float("Vĩ độ", required=True)
    thoi_gian_cap_nhat = fields.Datetime("Thời gian cập nhật", default=fields.Datetime.now, required=True)

    ma_phuong_tien = fields.Many2one("phuong_tien", string="Phương tiện", required=True, ondelete="cascade")

    _sql_constraints = [
        ('check_kinh_do', 'CHECK(kinh_do >= -180 AND kinh_do <= 180)', 'Kinh độ phải nằm trong khoảng -180 đến 180!'),
        ('check_vi_do', 'CHECK(vi_do >= -90 AND vi_do <= 90)', 'Vĩ độ phải nằm trong khoảng -90 đến 90!')
    ]

    @api.constrains('thoi_gian_cap_nhat')
    def _check_thoi_gian_cap_nhat(self):
        for record in self:
            if record.thoi_gian_cap_nhat > fields.Datetime.now():
                raise ValidationError("Thời gian cập nhật không thể ở tương lai!")

    def name_get(self):
        result = []
        for record in self:
            name = record.ma_phuong_tien.ma_phuong_tien
            result.append((record.id, name))
        return result
