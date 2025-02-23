from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhuongTien(models.Model):
    _name = 'phuong_tien'
    _description = 'Bảng chứa thông tin phương tiện'

    ma_phuong_tien = fields.Char("Mã phương tiện", required=True)
    bien_so = fields.Char("Biển số xe", required=True)
    loai_xe = fields.Selection([
        ('oto', 'Ô tô'),
        ('xe_may', 'Xe máy'),
        ('khac', 'Khác')
    ], string="Loại xe", required=True)
    hang_san_xuat = fields.Char("Hãng sản xuất")
    mau_xe = fields.Char("Mẫu xe")
    nam_san_xuat = fields.Integer("Năm sản xuất")
    trang_thai = fields.Selection([
        ('dang_hoat_dong', 'Đang hoạt động'),
        ('bao_tri', 'Bảo trì'),
        ('khong_hoat_dong', 'Không hoạt động')
    ], string="Trạng thái", default='dang_hoat_dong')

    _sql_constraints = [
        ('unique_ma_phuong_tien', 'unique(ma_phuong_tien)', 'Mã phương tiện đã tồn tại, vui lòng nhập mã khác!'),
        ('unique_bien_so', 'unique(bien_so)', 'Biển số xe này đã tồn tại, vui lòng kiểm tra lại!'),
    ]

    @api.constrains('bien_so', 'loai_xe', 'nam_san_xuat')
    def _validate_vehicle_constraints(self):
        for record in self:
            existing_vehicle = self.env['phuong_tien'].search([
                ('bien_so', '=', record.bien_so),
                ('loai_xe', '=', record.loai_xe),
                ('id', '!=', record.id)
            ])
            if existing_vehicle:
                raise ValidationError("Biển số xe này đã tồn tại cho loại xe này, vui lòng kiểm tra lại!")

            # current_year = fields.Date.today().year
            # if record.nam_san_xuat and (record.nam_san_xuat < 1900 or record.nam_san_xuat > current_year):
            #     raise ValidationError("Năm sản xuất không hợp lệ! Vui lòng nhập năm từ 1900 đến hiện tại.")

    @api.model
    def create(self, vals):
        if vals.get('ma_phuong_tien', 'New') == 'New':
            vals['ma_phuong_tien'] = self.env['ir.sequence'].next_by_code('phuong_tien.sequence') or 'PT0001'
        return super(PhuongTien, self).create(vals)
