import pikepdf
import sys
from datetime import datetime
from pikepdf.models.metadata import encode_pdf_date

d = encode_pdf_date(datetime(year=2023, month=12, day=25))
pdf = pikepdf.open(sys.argv[1])
with pdf.open_metadata() as meta:
    meta['pdf:Author'] = { "Test Contributor" }
    meta['pdf:Title'] = "Title"
    meta['pdf:CreationDate'] = d

pdf.save(sys.argv[2])
