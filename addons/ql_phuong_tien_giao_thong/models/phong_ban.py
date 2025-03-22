from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban")
    mo_ta = fields.Char("Mô tả")
    ma_nv_noi_bo = fields.One2many("nv_noi_bo", "ma_phong_ban", "Phòng ban")

    @api.model
    def create(self, vals):
        if 'ma_phong_ban' in vals:
            existing = self.env['phong_ban'].search([('ma_phong_ban', '=', vals['ma_phong_ban'])])
            if existing:
                raise exceptions.ValidationError("Mã phòng ban đã tồn tại! Vui lòng chọn mã khác.")

        if 'ten_phong_ban' in vals and not vals['ten_phong_ban'].strip():
            raise exceptions.ValidationError("Tên phòng ban không được để trống!")

        return super(PhongBan, self).create(vals)

    def name_get(self):
        return [(record.id, record.ten_phong_ban) for record in self]