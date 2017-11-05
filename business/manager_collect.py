from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL
from business.manager_models import *
from business.inbuilt_tax_codes import *
import csv
from django.http import HttpResponse

class GstBusiness:
  def __init__(self,fm_date,to_date,inv_type,business='Demo Company Indian GST'):
    m=manager_object(ROOT_URL,USER_NAME,business=business)
    sinvoices=m.get_sales_invoices()
    try:
      tcodes=m.get_taxCodes()
    except:
      tcodes=[]
    customers=m.get_customers()
    customFields=m.get_customfields()
    businessdetails=m.get_businessdetails()
    #suppliers=m.get_suppliers()

    taxli=[] #List of TaxCode objects
    for tax in tcodes:
      taxli.append(TaxCode(tcodes[tax],tax))
    taxli.append(TaxCode(CGST_SGST_3_JSON,CGST_SGST_3_CODE))
    taxli.append(TaxCode(CGST_SGST_5_JSON,CGST_SGST_5_CODE))
    taxli.append(TaxCode(CGST_SGST_12_JSON,CGST_SGST_12_CODE))
    taxli.append(TaxCode(CGST_SGST_18_JSON,CGST_SGST_18_CODE))
    taxli.append(TaxCode(CGST_SGST_28_JSON,CGST_SGST_28_CODE))
    taxli.append(TaxCode(IGST_0_JSON,IGST_0_CODE))
    taxli.append(TaxCode(IGST_3_JSON,IGST_3_CODE))
    taxli.append(TaxCode(IGST_5_JSON,IGST_5_CODE))
    taxli.append(TaxCode(IGST_12_JSON,IGST_12_CODE))
    taxli.append(TaxCode(IGST_18_JSON,IGST_18_CODE))
    taxli.append(TaxCode(IGST_28_JSON,IGST_28_CODE)) 

    for busdetail in businessdetails:
      businessDetails=BusinessDetails(businessdetails[busdetail],busdetail)
  
    custom_field_list=[] #List of Custom Fields.
    for custom_field in customFields:
      custom_field_list.append(CustomField(customFields[custom_field],custom_field))  
  
    cli=[]  # List of customer objects
    for customer in customers:
        cli.append(CustomerDetails(customers[customer],custom_field_list,customer))
  
    sinvli=[] # List of sales invoice objects
    for sinvoice in sinvoices:
      sinvli.append(SalesInvoice(sinvoices[sinvoice],taxli,custom_field_list,cli,businessDetails,state_codes))
      
    self.gst_invoices=SalesInvList(sinvli).filter_inv(fm_date,to_date,inv_type)
    self.inv_type=inv_type
    
  def  gstOffline(self):
    response = HttpResponse(content_type='text/csv')
    
    if inv_type='b2b':
      response['Content-Disposition'] = 'attachment; filename="b2b.csv"'
      writer = csv.writer(response)
      for invoice in self.gst_invoices:
        for line in invoice.gst_tax_taxablevalue:
          writer.writerow([invoice.customer_gstin_no,invoice.reference,invoice.invoice_date_gst_str,invoice.totalAmount,invoice.gst_state_code,invoice.get_customfield_value('Reverse Charges'), invoice.get_customfield_value('Invoice Type'),' ',line['rate'],line['taxablevalue'] ])
    print(response)  
      
      
      
     
    
      
      









            
    
