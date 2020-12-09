#!/usr/bin/python3
# @Time    : 2020-12-07
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _


class res_config_settings(models.TransientModel):

    _inherit = "res.config.settings"

    sale_purchase_line_uom = fields.Boolean(
        "使用明细单位传递", default=False, config_parameter="inter.sale.purchase.uom")
    purchase_sale_line_uom = fields.Boolean(
        "使用明细单位传递", default=False, config_parameter="inter.purchase.sale.uom")
