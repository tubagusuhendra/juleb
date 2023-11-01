import io
import xlrd
import babel
import logging
import tempfile
import binascii
from io import StringIO
from datetime import date, datetime, time
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError
_logger = logging.getLogger(__name__)

try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

class ImportProduct(models.TransientModel):
    _name='import.product.wizard'
    
    filename = fields.Char()
    file = fields.Binary(string="Upload File")

    def create_product(self):
        if not self.file:
            raise ValidationError(_("Please Upload File!"))
        try:
            file = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
            file.write(binascii.a2b_base64(self.file))
            file.seek(0)
            values = {}
            workbook = xlrd.open_workbook(file.name)
            sheet = workbook.sheet_by_index(0)
        except Exception:
            raise ValidationError(_("Please Select Valid File Format !"))

        for row_no in range(sheet.nrows):
            val = {}
            if row_no <= 0:
                fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
            else:
                product_obj = self.env['product.product']
                line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                product_ids = product_obj.search([('default_code','=',line[0])])
                if len(product_ids) > 1:
                    raise ValidationError(_("Product Duplicate: %s") % (product_ids[0]))
                elif product_ids:
                    product_ids.write({'barcode':line[1],
                                       'name':line[2],
                                       'standard_price':line[3],
                                       'lst_price':line[4],
                                       'tracking':line[5]})
                elif not product_ids:
                    product_obj.create({'default_code':line[0],
                                        'barcode':line[1],
                                       'name':line[2],
                                       'standard_price':line[3],
                                       'lst_price':line[4],
                                       'tracking':line[5]})
