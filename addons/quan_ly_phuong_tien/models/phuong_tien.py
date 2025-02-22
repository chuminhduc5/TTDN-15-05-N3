from odoo import models, fields, api


class PhuongTien(models.Model):
    _name = 'phuong_tien'
    _description = 'Bảng chứa thông tin phương tiện'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    bien_so = fields.Char("Biển số xe", required=True)
    loai_xe = fields.Selection([
        ('oto', 'Ô tô'),
        ('xe_tai', 'Xe tải'),
        ('xe_may', 'Xe máy'),
        ('khac', 'Khác')
    ], string="Loại xe", required=True)
    hang_san_xuat = fields.Char("Hãng sản xuất")
    mau_xe = fields.Char("Mẫu xe")
    nam_san_xuat = fields.Integer("Năm sản xuất")
    trang_thai = fields.Selection([
        ('dang_hoat_dong', 'Đang hoạt động'),
        ('bao_tri', 'Bảo trì'),
        ('dang_cho', 'Đang chờ'),
        ('khong_hoat_dong', 'Không hoạt động')
    ], string="Trạng thái", default='dang_hoat_dong')