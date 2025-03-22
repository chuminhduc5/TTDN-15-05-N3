from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class PhieuMuonXe(models.Model):
    _name = 'phieu_muon_xe'
    _description = 'Bảng chứa thông tin phiếu mượn xe'

    ma_phieu_muon_xe = fields.Char("Mã phiếu mượn", required=True)

    ma_nv_noi_bo = fields.Many2one('nv_noi_bo', string="Nhân viên nội bộ", required=True)

    ma_phuong_tien = fields.Many2one('phuong_tien', string="Phương tiện", required=True)

    ma_nhan_vien = fields.Many2one("nhan_vien", "Nhân viên phụ trách", required=True)

    diem_bat_dau = fields.Char("Điểm bắt đầu", required=True)
    
    diem_ket_thuc = fields.Char("Điểm kết thúc", required=True)

    ngay_dang_ky_muon = fields.Datetime("Ngày đăng ký mượn", required=True, default=fields.Datetime.now)
    ngay_dang_ky_tra = fields.Datetime("Ngày đăng ký trả", required=True)

    ngay_muon_thuc_te = fields.Datetime("Ngày mượn thực tế")
    ngay_tra_thuc_te = fields.Datetime("Ngày trả thực tế")

    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('dang_muon', 'Đang mượn'),
        ('hoan_thanh', 'Hoàn thành'),
        ('tra_muon', 'Trả muộn')
    ], string="Trạng thái", default='cho_duyet')
    muc_dich = fields.Text("Mục đích", required=True)
    ghi_chu = fields.Text("Ghi chú")
    ngay_tao = fields.Datetime("Ngày tạo", default=fields.Datetime.now, readonly=True)
    ngay_cap_nhat = fields.Datetime("Ngày cập nhật", default=fields.Datetime.now)
    ma_lich_su_su_dung = fields.One2many("lich_su_su_dung", "ma_phieu_muon_xe", "Lịch sử sử dụng")

    _sql_constraints = [
        ('unique_ma_phieu_muon_xe', 'unique(ma_phieu_muon_xe)', 'Mã phiếu mượn đã tồn tại, vui lòng nhập mã khác!')
    ]

    @api.constrains('ngay_muon', 'ngay_tra')
    def _check_dates(self):
        for record in self:
            if record.ngay_tra and record.ngay_muon and record.ngay_tra < record.ngay_muon:
                raise ValidationError("Ngày trả không thể trước ngày mượn!")

    @api.constrains('ma_phuong_tien')
    def _check_vehicle_availability(self):
        for record in self:
            if record.ma_phuong_tien.trang_thai == 'dang_hoat_dong':
                raise ValidationError("Phương tiện này đang được sử dụng!")

    @api.model
    def create(self, vals):
        return super(PhieuMuonXe, self).create(vals)

    def write(self, vals):
        res = super(PhieuMuonXe, self).write(vals)

        for record in self:
            if 'trang_thai' in vals:
                if vals['trang_thai'] == 'dang_muon' and record.ma_phuong_tien:
                    record.ma_phuong_tien.write({'trang_thai': 'dang_hoat_dong'})

                elif vals['trang_thai'] == 'hoan_thanh' and record.ma_phuong_tien:
                    record.ma_phuong_tien.write({'trang_thai': 'san_sang'})
        return res

    def _them_lich_su_su_dung(self):
        for record in self:
            if record.trang_thai in ['hoan_thanh', 'tra_muon']:
                self.env['lich_su_su_dung'].create({
                    'ma_phieu_muon_xe': record.id,
                    'ma_phuong_tien': record.ma_phuong_tien.id,
                    'trang_thai': record.trang_thai,
                    'thoi_gian_muon_xe': record.ngay_muon_thuc_te,
                    'thoi_gian_tra_xe': record.ngay_tra_thuc_te
                })

    def action_duyet(self):
        for record in self:
            if record.trang_thai != 'cho_duyet':
                raise ValidationError("Chỉ có thể duyệt phiếu khi ở trạng thái 'Chờ duyệt'!")
            record.trang_thai = 'dang_muon'
            record.ngay_muon_thuc_te = fields.Datetime.now()

    def action_huy_duyet(self):
        for record in self:
            if record.trang_thai != 'dang_muon':
                raise ValidationError("Chỉ có thể hủy duyệt khi phiếu đang ở trạng thái 'Đang mượn'!")
            record.trang_thai = 'cho_duyet'
            record.ngay_muon_thuc_te = False
            for phuong_tien in record.ma_phuong_tien:
                if phuong_tien.trang_thai == 'dang_hoat_dong':
                    phuong_tien.trang_thai = 'san_sang'

    def action_hoan_thanh(self):
        for record in self:
            if record.trang_thai != 'dang_muon':
                raise ValidationError("Chỉ có thể hoàn thành khi phiếu đang ở trạng thái 'Đang mượn'!")

            record.ngay_tra_thuc_te = fields.Datetime.now()

            if record.ngay_tra_thuc_te > record.ngay_dang_ky_tra:
                record.trang_thai = 'tra_muon'
            else:
                record.trang_thai = 'hoan_thanh'

            if record.ma_phuong_tien:
                bao_tri = self.env['bao_tri'].search([
                    ('ma_phuong_tien', '=', record.ma_phuong_tien.id),
                    ('trang_thai', '=', 'dang_bao_tri')
                ], limit=1)

                if bao_tri:
                    record.ma_phuong_tien.trang_thai = 'bao_tri'
                else:
                    record.ma_phuong_tien.trang_thai = 'san_sang'

            record._them_lich_su_su_dung()

    def name_get(self):
        return [(record.id, record.ma_phieu_muon_xe) for record in self]