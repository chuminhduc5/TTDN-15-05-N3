from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo import api

class BaoTri(models.Model):
    _name = "bao_tri"
    _description = "Bảng chứa thông tin bảo trì xe"

    ma_bao_tri = fields.Char("Mã bảo trì", required=True)
    ma_phuong_tien = fields.Many2one('phuong_tien', string="Phương tiện", required=True)
    bien_so = fields.Char(string="Biển số xe", related="ma_phuong_tien.bien_so", store=True)
    ngay_bao_tri = fields.Date(string="Ngày bảo trì", required=True, default=fields.Date.today)
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('dang_bao_tri', 'Đang bảo trì'),
        ('hoan_thanh', 'Hoàn thành')
    ], string="Trạng thái", default="cho_duyet", required=True)
    mo_ta = fields.Text("Mô tả")
    chi_phi = fields.Float(string="Chi phí bảo trì")
    ngay_bao_tri_tiep_theo = fields.Date(string="Ngày bảo trì tiếp theo")

    ma_phieu_muon_xe = fields.Many2one('phieu_muon_xe', string="Phiếu mượn liên quan", domain="[('ma_phuong_tien', '=', ma_phuong_tien)]")

    @api.onchange('ngay_bao_tri')
    def _compute_next_maintenance(self):
        for record in self:
            if record.ngay_bao_tri:
                record.ngay_bao_tri_tiep_theo = record.ngay_bao_tri + relativedelta(months=6)

    @api.constrains('chi_phi')
    def _check_chi_phi(self):
        for record in self:
            if record.chi_phi < 0:
                raise ValidationError("Chi phí bảo trì không thể nhỏ hơn 0!")

    @api.model
    def create(self, vals):
        record = super(BaoTri, self).create(vals)
        if record.ma_phuong_tien and record.trang_thai == 'dang_bao_tri':
            record.ma_phuong_tien.write({'trang_thai': 'bao_tri'})
        return record

    def write(self, vals):
        res = super(BaoTri, self).write(vals)
        if 'trang_thai' in vals:
            for record in self:
                if vals['trang_thai'] == 'dang_bao_tri':
                    record.ma_phuong_tien.trang_thai = 'bao_tri'
                elif vals['trang_thai'] == 'hoan_thanh':
                    record.ma_phuong_tien.trang_thai = 'san_sang'
        return res

    def action_duyet(self):
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({'trang_thai': 'dang_bao_tri'})
                record.ma_phuong_tien.write({'trang_thai': 'bao_tri'})

    def action_huy_duyet(self):
            if record.trang_thai != 'dang_bao_tri':
                raise ValidationError("Không thể hủy duyệt nếu chưa được duyệt!")
            record.write({'trang_thai': 'cho_duyet'})
            record.ma_phuong_tien.write({'trang_thai': 'san_sang'})

    def action_hoan_thanh(self):
        for record in self:
            if record.trang_thai != 'dang_bao_tri':
                raise ValidationError("Chỉ có thể hoàn thành khi trạng thái là 'Đang bảo trì'!")
            record.write({'trang_thai': 'hoan_thanh'})
            record.ma_phuong_tien.write({'trang_thai': 'san_sang'})

    def name_get(self):
        return [(record.id, record.ma_bao_tri) for record in self]