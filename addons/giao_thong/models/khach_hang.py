from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Bảng chứa thông tin khách hàng'

    ma_khach_hang = fields.Char("Mã khách hàng", required=True)
    ho_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    cccd = fields.Char("Căn cước công dân", required=True)
    sdt = fields.Char("Số điện thoại", required=True)
    email = fields.Char("Email", required=True)
    dia_chi = fields.Char("Địa chỉ")
    ngay_dang_ky = fields.Date("Ngày đăng ký",default=fields.Date.today)

    _sql_constraints = [
        ('unique_ma_khach_hang', 'unique(ma_khach_hang)', 'Mã khách hàng này đã được sử dụng, vui lòng chọn mã khác!'),
        ('unique_cccd', 'unique(cccd)', 'Căn cước công dân này đã tồn tại, vui lòng kiểm tra lại!'),
        ('unique_sdt', 'unique(sdt)', 'Số điện thoại này đã có trong hệ thống, vui lòng nhập số khác!'),
        ('unique_email', 'unique(email)', 'Email này đã được đăng ký, vui lòng sử dụng email khác!'),
    ]

    @api.constrains('sdt', 'email')
    def _validate_contact_info(self):
        for record in self:
            if record.sdt and not record.sdt.isdigit():
                raise ValidationError("Số điện thoại phải là số!")

            if record.email and '@' not in record.email:
                raise ValidationError("Email không hợp lệ!")
