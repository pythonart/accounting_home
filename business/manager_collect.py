from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL
from business.manager_models import *

m=manager_object(ROOT_URL,USER_NAME,business='Demo Company Indian GST')

sinvoices=m.get_sales_invoices()
tcodes=m.get_taxCodes()
customers=m.get_customers()
customFields=m.get_customfields()
businessdetails=m.get_businessdetails()
#suppliers=m.get_suppliers()

taxli=[] #List of TaxCode objects
for tax in tcodes:
  taxli.append(TaxCode(tcodes[tax],tax))


custom_field_list=[] #List of Custom Fields.
for custom_field in customFields:
  custom_field_list.append(CustomField(customFields[custom_field],custom_field))  
  
cli=[]  # List of customer objects
for customer in customers:
  cli.append(CustomerDetails(customers[customer],custom_field_list,customer))
  
sinvli=[] # List of sales invoice objects
for sinvoice in sinvoices:
  sinvli.append(SalesInvoice(sinvoices[sinvoice],taxli,custom_field_list,cli))


for busdetail in businessdetails:
  businessDetails=BusinessDetails(businessdetails[busdetail],busdetail)



            
    
