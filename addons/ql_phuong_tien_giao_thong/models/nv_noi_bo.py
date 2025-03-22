from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
import re

class NhanVienNoiBo(models.Model):
    _name = 'nv_noi_bo'
    _description = 'Bảng chứa thông tin nhân viên nội bộ'

    ma_nv_noi_bo = fields.Char("Mã nhân viên nội bộ", required=True)
    ho_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    cccd = fields.Char("Căn cước công dân", required=True)
    sdt = fields.Char("Số điện thoại", required=True)
    email = fields.Char("Email", required=True)
    dia_chi = fields.Char("Địa chỉ")
    ma_phong_ban = fields.Many2one("phong_ban", "Phòng ban", required=True)
    ngay_dang_ky = fields.Date("Ngày đăng ký", default=fields.Date.today)

    _sql_constraints = [
        ('unique_ma_nv_noi_bo', 'unique(ma_nv_noi_bo)', 'Mã nhân viên nội bộ này đã được sử dụng, vui lòng chọn mã khác!'),
        ('unique_cccd', 'unique(cccd)', 'Căn cước công dân này đã tồn tại, vui lòng kiểm tra lại!'),
        ('unique_sdt', 'unique(sdt)', 'Số điện thoại này đã có trong hệ thống, vui lòng nhập số khác!'),
        ('unique_email', 'unique(email)', 'Email này đã được đăng ký, vui lòng sử dụng email khác!'),
    ]

    @api.constrains('sdt', 'email', 'cccd')
    def _validate_contact_info(self):
        for record in self:
            if record.sdt and not re.match(r'^(0\d{9,10}|\+84\d{9,10})$', record.sdt):
                raise ValidationError(
                    "Số điện thoại không hợp lệ! Số điện thoại phải bắt đầu bằng '0' hoặc '+84' và có 10-11 chữ số.")

            if record.email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', record.email):
                raise ValidationError(
                    "Email không hợp lệ! Vui lòng nhập đúng định dạng email (ví dụ: example@email.com).")

            if record.cccd and not re.match(r'^\d{12}$', record.cccd):
                raise ValidationError("Căn cước công dân phải có đúng 12 chữ số!")

    @api.constrains('ngay_sinh')
    def _check_ngay_sinh(self):
        for record in self:
            if record.ngay_sinh and record.ngay_sinh > date.today():
                raise ValidationError("Ngày sinh không thể lớn hơn ngày hiện tại!")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.ho_ten} ({record.ma_nv_noi_bo})"
            result.append((record.id, name))
        return result
