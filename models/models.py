#!/usr/bin/python3
# @Time    : 2020-12-07
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _


class purchase_order(models.Model):

    _inherit = "purchase.order"

    @api.model
    def _prepare_sale_order_line_data(self, line, company, sale_id):
        """ Generate the Sales Order Line values from the PO line
            :param line : the origin Purchase Order Line
            :rtype line : purchase.order.line record
            :param company : the company of the created SO
            :rtype company : res.company record
            :param sale_id : the id of the SO
        """
        # it may not affected because of parallel company relation
        price = line.price_unit or 0.0
        taxes = line.taxes_id
        if line.product_id:
            taxes = line.product_id.taxes_id
        company_taxes = [
            tax_rec for tax_rec in taxes if tax_rec.company_id.id == company.id]
        if sale_id:
            so = self.env["sale.order"].sudo(
                company.intercompany_user_id).browse(sale_id)
            company_taxes = so.fiscal_position_id.map_tax(
                company_taxes, line.product_id, so.partner_id)
        # 读取系统设置
        using_line = self.env['ir.config_parameter'].sudo(
        ).get_param("inter.purchase.sale.uom") or False
        quantity = line.product_qty if using_line else line.product_id and line.product_uom._compute_quantity(
            line.product_qty, line.product_id.uom_id) or line.product_qty
        price = price if using_line else line.product_id and line.product_uom._compute_price(
            price, line.product_id.uom_id) or price
        
        return {
            'name': line.name,
            'order_id': sale_id,
            'product_uom_qty': quantity,
            'product_id': line.product_id and line.product_id.id or False,
            'product_uom': line.product_uom.id if using_line else line.product_id and line.product_id.uom_id.id or line.product_uom.id,
            'price_unit': price,
            'customer_lead': line.product_id and line.product_id.sale_delay or 0.0,
            'company_id': company.id,
            'tax_id': [(6, 0, company_taxes.ids)],
        }


class sale_order(models.Model):

    _inherit = "sale.order"

    @api.model
    def _prepare_purchase_order_line_data(self, so_line, date_order, purchase_id, company):
        """ Generate purchase order line values, from the SO line
            :param so_line : origin SO line
            :rtype so_line : sale.order.line record
            :param date_order : the date of the orgin SO
            :param purchase_id : the id of the purchase order
            :param company : the company in which the PO line will be created
            :rtype company : res.company record
        """
        # price on PO so_line should be so_line - discount
        price = so_line.price_unit - \
            (so_line.price_unit * (so_line.discount / 100))

        # computing Default taxes of so_line. It may not affect because of parallel company relation
        taxes = so_line.tax_id
        if so_line.product_id:
            taxes = so_line.product_id.supplier_taxes_id

        # fetch taxes by company not by inter-company user
        company_taxes = taxes.filtered(lambda t: t.company_id == company)
        if purchase_id:
            po = self.env["purchase.order"].sudo(
                company.intercompany_user_id).browse(purchase_id)
            company_taxes = po.fiscal_position_id.map_tax(
                company_taxes, so_line.product_id, po.partner_id)

        # 读取系统设置
        using_line = self.env['ir.config_parameter'].sudo(
        ).get_param("inter.sale.purchase.uom") or False

        quantity = so_line.product_uom_qty if using_line else so_line.product_id and so_line.product_uom._compute_quantity(
            so_line.product_uom_qty, so_line.product_id.uom_po_id) or so_line.product_uom_qty
        price = price if using_line else so_line.product_id and so_line.product_uom._compute_price(
            price, so_line.product_id.uom_po_id) or price
        
        return {
            'name': so_line.name,
            'order_id': purchase_id,
            'product_qty': quantity,
            'product_id': so_line.product_id and so_line.product_id.id or False,
            'product_uom': so_line.product_uom.id if using_line else so_line.product_id and so_line.product_id.uom_po_id.id or so_line.product_uom.id,
            'price_unit': price or 0.0,
            'company_id': company.id,
            'date_planned': so_line.order_id.expected_date or date_order,
            'taxes_id': [(6, 0, company_taxes.ids)],
        }
