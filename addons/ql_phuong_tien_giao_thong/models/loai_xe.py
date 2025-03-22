from odoo import models, fields, api

class LoaiXe(models.Model):
    _name = 'loai_xe'
    _description = 'Bảng chứa thông tin loại xe'
    _rec_name = 'ten_loai_xe'

    ten_loai_xe = fields.Char("Tên loại xe", required=True)
    ma_phuong_tien = fields.One2many('phuong_tien', 'loai_xe', string="Phương tiện")

    tong_so_luong = fields.Integer(string="Tổng số lượng", compute="_compute_so_luong")
    so_luong_san_sang = fields.Integer(string="Sẵn sàng", compute="_compute_so_luong")
    so_luong_dang_hoat_dong = fields.Integer(string="Đang hoạt động", compute="_compute_so_luong")
    so_luong_bao_tri = fields.Integer(string="Bảo trì", compute="_compute_so_luong")

    @api.depends('ma_phuong_tien.trang_thai')
    def _compute_so_luong(self):
        for record in self:
            san_sang = hoat_dong = bao_tri = 0
            for pt in record.ma_phuong_tien:
                if pt.trang_thai == 'san_sang':
                    san_sang += 1
                elif pt.trang_thai == 'dang_hoat_dong':
                    hoat_dong += 1
                elif pt.trang_thai == 'bao_tri':
                    bao_tri += 1

            record.tong_so_luong = len(record.ma_phuong_tien)
            record.so_luong_san_sang = san_sang
            record.so_luong_dang_hoat_dong = hoat_dong
            record.so_luong_bao_tri = bao_tri

    @api.constrains('ten_loai_xe')
    def _check_ten_loai_xe(self):
        for record in self:
            if self.env['loai_xe'].search([('ten_loai_xe', '=', record.ten_loai_xe), ('id', '!=', record.id)]):
                raise ValidationError("Tên loại xe đã tồn tại, vui lòng nhập tên khác!")

    def name_get(self):
        return [(record.id, record.ten_loai_xe) for record in self]
