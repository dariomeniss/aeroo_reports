# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestAerooReport(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAerooReport, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'My Partner',
        })
        cls.report = cls.env.ref('report_aeroo_sample.aeroo_sample_report_id')
        cls.report.write({
            'attachment': None,
            'attachment_use': False,
        })

    def test_01_sample_report_doc(self):
        self.report.out_format = self.env.ref(
            'report_aeroo.report_mimetypes_doc_odt')
        self.partner.print_report('sample_report', {})

    def test_02_sample_report_pdf(self):
        self.report.out_format = self.env.ref(
            'report_aeroo.report_mimetypes_pdf_odt')
        self.partner.print_report('sample_report', {})

    def test_03_sample_report_pdf_with_attachment(self):
        self.report.write({
            'attachment_use': True,
            'attachment': "'%s.pdf' % (object.name)",
        })
        self.report.out_format = self.env.ref(
            'report_aeroo.report_mimetypes_pdf_odt')
        self.partner.print_report('sample_report', {})

        attachment = self.env['ir.attachment'].search([
            ('res_id', '=', self.partner.id),
            ('res_model', '=', 'res.partner'),
            ('datas_fname', '=', 'My Partner.pdf'),
        ])
        self.assertEqual(len(attachment), 1)

        self.partner.print_report('sample_report', {})
