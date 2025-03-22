from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class PhuongTien(models.Model):
    _name = 'phuong_tien'
    _description = 'Bảng chứa thông tin phương tiện'
    _rec_name = 'ten_phuong_tien'

    ma_phuong_tien = fields.Char("Mã phương tiện", required=True)
    ten_phuong_tien = fields.Char("Tên phương tiện", required=True)
    loai_xe = fields.Many2one('loai_xe', string="Loại xe", required=True)
    bien_so = fields.Char("Biển số xe")
    hang_san_xuat = fields.Char("Hãng sản xuất")
    so_cho = fields.Integer("Số chỗ", required=True)
    mau_xe = fields.Char("Màu xe")
    nam_san_xuat = fields.Integer("Năm sản xuất")

    ma_tieu_hao_nhien_lieu = fields.One2many("nhien_lieu", "ma_phuong_tien", "Thông tin nhiên liệu")
    ma_vi_tri = fields.One2many("vi_tri", "ma_phuong_tien", string="Lịch sử vị trí")
    ma_bao_tri = fields.One2many("bao_tri", "ma_phuong_tien", string="Lịch sử bảo trì")

    trang_thai = fields.Selection([
        ('dang_hoat_dong', 'Đang hoạt động'),
        ('bao_tri', 'Bảo trì'),
        ('san_sang', 'Sẵn sàng')
    ], string="Trạng thái", default='san_sang')

    _sql_constraints = [
        ('unique_ma_phuong_tien', 'unique(ma_phuong_tien)', 'Mã phương tiện đã tồn tại, vui lòng nhập mã khác!'),
        ('unique_bien_so', 'unique(bien_so)', 'Biển số xe này đã tồn tại, vui lòng kiểm tra lại!'),
    ]

    @api.constrains('so_cho')
    def _check_so_cho(self):
        for record in self:
            if record.so_cho <= 0:
                raise ValidationError("Số chỗ phải lớn hơn 0!")

    @api.constrains('nam_san_xuat')
    def _check_nam_san_xuat(self):
        for record in self:
            if record.nam_san_xuat and record.nam_san_xuat > datetime.now().year:
                raise ValidationError("Năm sản xuất không thể lớn hơn năm hiện tại!")

    def name_get(self):
        return [(record.id, record.ten_phuong_tien) for record in self]

