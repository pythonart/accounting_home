from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL
from business.manager_models import *
from business.inbuilt_tax_codes import *

Class gst_business:
  def __init__(self,business,fm_date,to_date,inv_type):
    m=manager_object(ROOT_URL,USER_NAME,business='Demo Company Indian GST')
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
      
      









            
    
