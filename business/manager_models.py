import re
from dateutil import parser
from datetime import datetime
from datetime import date

B2CS_CAP=250000

#State Codes
state_codes=[
{'name':'Andaman and Nicobar Islands','codeNo':'35','codeA':'AN'},
{'name':'Andhra Pradesh','codeNo':'37','codeA':'AD'},
{'name':'Arunachal Pradesh','codeNo':'12','codeA':'AR'},
{'name':'Assam','codeNo':'18','codeA':'AS'},
{'name':'Bihar','codeNo':'10','codeA':'BR'},
{'name':'Chandigarh','codeNo':'04','codeA':'CH'},  
{'name':'Chattisgarh','codeNo':'22','codeA':'CG'},
{'name':'Dadra and Nagar Haveli','codeNo':'26','codeA':'DN'},  
{'name':'Daman and Diu','codeNo':'25','codeA':'DD'},  
{'name':'Delhi','codeNo':'07','codeA':'DL'},
{'name':'Goa','codeNo':'30','codeA':'GA'}, 
{'name':'Gujarat','codeNo':'24','codeA':'GJ'},  
{'name':'Haryana','codeNo':'06','codeA':'HR'},
{'name':'Himachal Pradesh','codeNo':'02','codeA':'HP'},
{'name':'Jammu and Kashmir','codeNo':'01','codeA':'JK'},
{'name':'Jharkhand','codeNo':'20','codeA':'JH'},
{'name':'Karnataka','codeNo':'29','codeA':'KA'},
{'name':'Kerala','codeNo':'32','codeA':'KL'},
{'name':'Lakshadweep Islands','codeNo':'31','codeA':'LD'},
{'name':'Madhya Pradesh','codeNo':'23','codeA':'MP'},
{'name':'Maharashtra','codeNo':'27','codeA':'MH'},
{'name':'Manipur','codeNo':'14','codeA':'MN'},
{'name':'Meghalaya','codeNo':'17','codeA':'ML'},
{'name':'Mizoram','codeNo':'15','codeA':'MZ'},
{'name':'Nagaland','codeNo':'13','codeA':'NL'},
{'name':'Odisha','codeNo':'21','codeA':'OD'}, 
{'name':'Pondicherry','codeNo':'34','codeA':'PY'},   
{'name':'Punjab','codeNo':'03','codeA':'PB'},
{'name':'Rajasthan','codeNo':'08','codeA':'RJ'},
{'name':'Sikkim','codeNo':'11','codeA':'SK'},
{'name':'Tamil Nadu','codeNo':'33','codeA':'TN'},
{'name':'Telangana','codeNo':'36','codeA':'TS'}, 
{'name':'Tripura','codeNo':'16','codeA':'TR'},
{'name':'Uttar Pradesh','codeNo':'09','codeA':'UP'},
{'name':'Uttarakhand','codeNo':'05','codeA':'UK' }, 
{'name':'West Bengal','codeNo':'19','codeA':'WB'},  
]


    
class CustomerDetails:
  def __init__(self,customer={},custom_field_list=None,code=None):
    customer=customer
    self.code=code
    self.custom_field_list=custom_field_list
    self.name=customer.get('Name',None)
    self.billingAddress=customer.get('BillingAddress',None)
    self.email=customer.get('Email',None)
    self.businessIdentifier=customer.get('BusinessIdentifier',None)
    self.customer_code=customer.get('Code',None)
    self.startingBalanceType=customer.get('StartingBalanceType',None)
    self.telephone=customer.get('Telephone',None)
    self.fax=customer.get('Fax',None)
    self.mobile=customer.get('Mobile',None)
    self.notes=customer.get('Notes',None)
    self.customFields=customer.get('CustomFields',None)
    self.creditLimit=customer.get('CreditLimit',None)
    self.startingBalanceType=customer.get('StartingBalanceType',None)
    
  @property
  def customer_customfield_list(self):
    li=[]
    for item in self.customFields:
      c=CustomFieldsAll(self.custom_field_list).get_custom_field(item)
      c.value=self.customFields[item]
      li.append(c)
    return li      
  
  def get_customfield_value(self,findterm):
    findterm=findterm.strip()
    pattern='.*'+findterm+'.*'
    for item in self.customer_customfield_list:
      match=re.match(pattern,item.name, re.IGNORECASE )
      if match is not None:
        return item.value
    return None

  def __str__(self):
    return self.name
  
 
class SupplierDetails:
  def __init__(self,supplier={}):
    supplier=supplier
    self.name=supplier.get('Name',None)
    self.email=supplier.get('Email',None)
    self.telephone=supplier.get('Telephone',None)
    self.fax=supplier.get('Fax',None)
    self.mobile=supplier.get('Mobile',None)
    self.notes=supplier.get('Notes',None)
    self.address=supplier.get('Address',None)
    self.customFields=supplier.get('CustomFields',None)
    self.code=supplier.get('Code',None)
    self.creditLimit=supplier.get('CreditLimit',None)
    
  def __str__(self):
    return self.name

class SalesInvoice:
   def __init__(self,salesinv={},taxli=None,custom_field_list=None,customer_obj_list=None,businessDetails=None,state_codes=state_codes,):
      salesinv=salesinv
      self.businessDetails=businessDetails
      self.state_codes=state_codes
      self.customer_obj_list=customer_obj_list
      self.custom_field_list=custom_field_list
      self.taxli=taxli
      self.issueDate=salesinv.get('IssueDate',None)
      self.reference=salesinv.get('Reference',None)
      self.to=salesinv.get('To',None)
      self.billingAddress=salesinv.get('BillingAddress',None)
      self.lines=salesinv.get('Lines',None)
      self.dueDate=salesinv.get('DueDate',None)
      self.discount=salesinv.get('Discount',None)
      self.amountsIncludeTax=salesinv.get('AmountsIncludeTax',None)
      self.roundingMethod=salesinv.get('RoundingMethod',None)
      self.dueDateType=salesinv.get('DueDateType',None)
      self.dueDateDays=salesinv.get('DueDateDays',None)
      self.latePaymentFees=salesinv.get('LatePaymentFees',None)
      self.latePaymentFeesPercentage=salesinv.get('LatePaymentFeesPercentage',None)
      self.rounding=salesinv.get('Rounding',None)
      self.customFields=salesinv.get('CustomFields',None)
   
      
   def __str__(self):
      return self.reference
   
   @property 
   def lines_list(self):
      lines_list=[]
      for line in self.lines:
        lines_list.append(SalesInvLine(line,self.amountsIncludeTax,self.taxli,self.custom_field_list))
      return lines_list
   
   @property 
   def gst_inv_type(self):
      ''' Returns type of Invoice as per GST Format'''
      if self.customer_gstin_no is not None:
        return "b2b"
      else:
        if self.gst_intrastate is True:
          return "b2cs"
        else :
          if  self.totalAmount > B2CS_CAP:
            return "b2cl"
          else:
            return "b2cs"
          
   @property
   def gst_state_code(self):
      if self.customer_gstin_no is None:
        return None
      customer_state_code=self.customer_gstin_no[:2]
      for state in self.state_codes:
        if state['codeNo']==customer_state_code:
          return"%s-%s" % (state['codeNo'],state['name'])
   
   @property
   def own_gstin(self):
      return self.businessDetails.businessIdentifier
    
   
   @property
   def gst_intrastate(self):
      ''' Returns True or False if GST is from One State to Another'''
      if self.customer_gstin_no is not None:
        if self.own_gstin[:2]==self.customer_gstin_no[:2]:
          return True
        else:
          return False
      else:
        None
        
          
      
   @property
   def totalAmount(self):
      ''' Sum of Invoice Lines for (amt_aft_discount + tax.val for each tax from tax_val_list'''
      totalAmount=0
      if self.amountsIncludeTax is None:  
        for invLine in self.lines_list:
          if invLine.qty is not None:
            totalAmount+=(invLine.amt_aft_discount*invLine.qty)
          else:
            totalAmount+=invLine.amt_aft_discount
          for taxobj in invLine.tax_val_list:
            totalAmount+=taxobj.value
      else:
        for invLine in self.lines_list:
          if invLine.qty is not None:
            totalAmount+=(invLine.amt_aft_discount*invLine.qty)
          else:
            totalAmount+=invLine.amt_aft_discount
      return totalAmount
   
   @property
   def customer_gstin_no(self):
      ''' Return customer GSTIN No'''
      customer=CustomersAll(self.customer_obj_list).get_customer(self.to)
      if customer.businessIdentifier!="":
        return customer.businessIdentifier
      else :
        None
        
   @property
   def invoice_pydatetime(self):
      ''' Return invoice date in Python date time format for searching'''
      dt=parser.parse(self.issueDate)
      return dt
   
   @property
   def invoice_date_gst_str(self):
      ''' Return Invoice Date in GST Format'''
      dt=self.invoice_pydatetime
      return dt.strftime('%d-%b-%y')
   
   @property
   def gst_tax_taxablevalue(self):
      ''' Returns a list containing dicts with tax rate and taxable value.
          after totaling the taxable value for similar tax rate.
      '''
      li=[]
      for invoiceline in self.lines_list:
        if invoiceline.tax_rate!=0:
          li.append({'rate':invoiceline.tax_rate,'taxablevalue':invoiceline.taxableValue}) #Need to check for zero gst if taxablevalue is zero or invoice value.
        else :
          li.append({'rate':invoiceline.tax_rate,'taxablevalue':0})   
      nli=[]
      for item in li:
        if len(nli)==0:
          nli.append(item)
        else:
          x=0 # Assume item in li not in nli
          for obj in nli:
            if obj['rate']==item['rate']:
              obj['taxablevalue']+=item['taxablevalue']
              x=1   # Item in li found in nli with same tax rate, hence value added. 
          if x!=1:  # Item in li does not match any tax rate in nli. Apped item to nli.
            nli.append(item)
      return nli
          
   @property
   def salesinv_customfield_list(self):
      li=[]
      for item in self.customFields:
        c=CustomFieldsAll(self.custom_field_list).get_custom_field(item)
        c.value=self.customFields[item]
        li.append(c)
      return li
    
    
   def get_customfield_value(self,findterm):
      findterm=findterm.strip()
      pattern='.*'+findterm+'.*'
      for item in self.salesinv_customfield_list:
        match=re.match(pattern,item.name, re.IGNORECASE )
        if match is not None:
          return item.value
      return None   
      
class SalesInvLine:
   ''' A Object to store each line of a tax invoice. taxli is a list of all TaxCode objects'''
   def __init__(self,line,amountsIncludeTax=None,taxli=None,custom_field_list=None):
      self.custom_field_list=custom_field_list
      self.taxli=taxli #list of all taxobjects
      self.amountsIncludeTax=amountsIncludeTax
      self.description=line.get('Description',None)
      self.account=line.get('Account',None)
      self.taxCode=line.get('TaxCode','69831b78-192c-4715-9129-9aafa64ccaa3') #If not tax assign GST zero
      self.qty=line.get('Qty',None)
      self.item=line.get('Item',None)
      self.amount=line.get('Amount',None)
      self.discount=line.get('Discount',None)
      self.trackingCode=line.get('TrackingCode',None)
      self.customFields=line.get('CustomFields',None)
      
   @property
   def taxableValue(self):
      ''' Returns the taxable value depending of if tax is included or not.'''
      if self.tax_val_list is None:
        return 0
      if self.amountsIncludeTax is None:
        if self.qty is not None:
          return (self.amt_aft_discount*self.qty)
        else:
          return self.amt_aft_discount
      else:
        taxobj=TaxCodesAll(self.taxli).get_tax_code(self.taxCode)
        if taxobj.taxcomp_list_tax_rate_total !=0:
          amt_before_tax=self.amt_aft_discount / (((taxobj.taxcomp_list_tax_rate_total)/100) + 1)
        else :
          amt_before_tax=self.amt_aft_discount
        if self.qty is not None:  
          return (amt_before_tax*self.qty)
        else :
          return amt_before_tax
      
   @property
   def amt_aft_discount(self):
      ''' Returns the amount after discount is applied. Per UNIT
      Note: When tax is included the unit rate shown in Invoice line amount is wrong.
      E.G self.amount=100 Rs , tax applied multi rate 6% (5.23 Rs) and 3% (2.61 Rs) , Total tax 7.84 Rs, Discount 5% Rs 5,
      Total Bill Amount after Tax is 95 Rs. Hence Actual Unit Price is 91.7 Rs After 5 Rs dicount its 87.15, Plus Tax 7.84
      will give 95 Rs. There for the unit price is 91.7 Rs. Taxable Value is 87.15 Rs. 
      '''
      if self.discount is not None:
        return int(self.amount) -  ((int(self.amount)*int(self.discount))/100 )
      else :
        if self.amount is not None:
          return int(self.amount)
        else:
          return 0
  
   @property
   def tax_val_list(self):
      '''Contains a list of InvoiceTaxValue objects. They contain The tax value after rate
      is applied on the taxable amount. 
      taxobj contains a TaxCode object for the taxcode in the invoice line.
      A check is made to see if its a Multi Rate TaxCode.
      Qty is Multiplied here.
      '''
      li=[]
      if self.taxCode is None:
        return None
      taxobj=TaxCodesAll(self.taxli).get_tax_code(self.taxCode)
      if self.amountsIncludeTax is None : # if Amounts Do not Include Tax 
        if taxobj.taxcomp_exists is True: #If Multiple tax rates exist store value of each rate in a list and return it.
          for item in taxobj.taxcomp_list:
            t=InvoiceTaxValue()
            if item.rate ==0:   #For zero GST
              t.value=0
            else :
              t.value=((self.amt_aft_discount*item.rate)/100)*self.qty
            t.name=item.name
            t.rate=item.rate
            li.append(t)
        else:                             # if only single tax rate exists, take the value from TaxCode object and store it in list and return
            t=InvoiceTaxValue()
            if taxobj.rate==0:  #For zero GST
              t.value=0
            else :  
              t.value=((self.amt_aft_discount*taxobj.rate)/100)*self.qty
            t.name=taxobj.name
            t.rate=taxobj.rate
            li.append(t)
      else:#if Amounts  Include Tax then.
          if taxobj.taxcomp_list_tax_rate_total !=0:
            amt_before_tax=self.amt_aft_discount / (((taxobj.taxcomp_list_tax_rate_total)/100) + 1)
          else :
            amt_before_tax=self.amt_aft_discount
          taxVal=self.amt_aft_discount-amt_before_tax
          if taxobj.taxcomp_exists is True:    # if Multiple Tax Rates exisit
            for item in taxobj.taxcomp_list:
              t=InvoiceTaxValue()
              if item.rate==0:
                t.value=0
              else:  
                t.value=((amt_before_tax*item.rate)/100)*self.qty
              t.name=item.name
              t.rate=item.rate
              li.append(t)
          else:
              t=InvoiceTaxValue()               #if Only Single tax rate exists.
              if taxobj.rate==0:
                t.value=0
              else:  
                t.value=((amt_before_tax*taxobj.rate)/100)*self.qty
              t.name=taxobj.name
              t.rate=taxobj.rate
              li.append(t)
      return li
   
   @property
   def tax_rate(self):
      rate=0
      if self.tax_val_list is None:
        return 0
      for tax in self.tax_val_list:
        rate+=tax.rate
      return rate
   
   @property
   def tax_name(self):
      if self.tax_val_list is None:
        return "No Tax Applied"
      taxobj=TaxCodesAll(self.taxli).get_tax_code(self.taxCode)
      return taxobj.name
      
   
   @property
   def salvesInvLine_customfield_list(self):
      li=[]
      for item in self.customFields:
        c=CustomFieldsAll(self.custom_field_list).get_custom_field(item)
        c.value=self.customFields[item]
        li.append(c)
      return li      
    
   def get_customfield_value(self,findterm):
      findterm=findterm.strip()
      pattern='.*'+findterm+'.*'
      for item in self.salvesInvLine_customfield_list:
        match=re.match(pattern,item.name, re.IGNORECASE )
        if match is not None:
          return item.value
      return None    
          
   def __str__(self):
      return self.description
    
  
    
class TaxCode:
   def __init__(self,tax,code):
      ''' Stores a TaxCode and its data  Fields, code,name,components (for Multiple Rate Tax)
      taxRate (Stating its a CustomRate),taxRateType (Stating MultiRate ), Tax account code
      '''
      self.code=code
      self.name=tax.get('Name',None)
      self.components=tax.get('Components',None)
      self.taxRate=tax.get('TaxRate',None)
      self.taxRateType=tax.get('TaxRateType',None)
      self.rate_check=tax.get('Rate',None)
      self.account=tax.get('Account',None)
      self.rate=self.gstexempt()
   
   def gstexempt(self):
        if self.rate_check==None and self.taxcomp_exists==False:
            rate=0.0
            return rate
        if self.rate_check==None and self.taxcomp_exists==True:
            rate=None
            return rate
        else:
            rate=tax.get('Rate',None)
            return rate
   
   @property  
   def taxcomp_list(self):
      ''' Returns a list of Tax Component Objects for a TaxCode if Multi Rate Tax is used.
      else returs None.
      '''
      taxcomp_list=[]
      if self.taxcomp_exists is True:
        for taxcomp in self.components:
          taxcomp_list.append(TaxCodeComponent(taxcomp))
        return taxcomp_list
      else :
        return None
    
   @property
   def taxcomp_list_tax_rate_total(self):
      ''' Sum of the rate of the individual tax components in a TaxCode
      Also checks if Tax Component existis. If it does add all the tax rates
      from each component. Else since a single tax rate is applicable
      returns the tax rate from TaxCode.
      '''
      totalTax=0
      if self.taxcomp_exists is True:
        for taxcomp in self.taxcomp_list:
          totalTax += taxcomp.rate
      else:
        totalTax=self.rate
      return totalTax
   
   @property
   def taxcomp_exists(self):
      ''' Check if Tax Components exist, If inbuilt taxes are used they will contain a list with empty dicts 
      as below
      "Components": [
      {},
      {}
                 ]
      Even if the tax is not a MultipleRate TaxCode object blank components are generated. Hence
      we use Rate in the TaxCode object. If no rate exisits its a MultipleComponent Tax and will return True.
      '''
      if self.rate_check is not None:
        return False
      else:
        for item in self.components:
            value=False
            if len(item) > 0 and ( item.get('Rate',None) is not None) :
                value=True
                break
        return value        
            
               
    
    
    
   def __str__(self):
      return self.name
  
class TaxCodeComponent:
   ''' An Object to Store Tax components when MultipleRate Tax is used'''
   def __init__(self,taxcomp):
      self.name=taxcomp.get('Name',None)
      self.rate=taxcomp.get('Rate',None)
      self.account=taxcomp.get('Account',None)
    
   def __str__(self):
      return self.name
    

class TaxCodesAll:
  '''Stores A List of all TaxCode objsts when they are provided'''
  def __init__(self,taxli):
    self.tax_code_list=taxli    
  
  def get_tax_code(self,taxcode):
    ''' Returns a TaxCode object when a taxcode string is provided'''
    for item in self.tax_code_list:
      if item.code == taxcode:
        return item
        break
    return None
    
class InvoiceTaxValue:
  ''' Stors the Tax Name, Rate and Value of the tax applied on the Taxable Amount '''
  def __int__(self,value=None,name=None,rate=None):
    self.name=name
    self.value=value
    self.rate=rate
    
  def __str__(self):
    return self.name+' '+str(self.rate)
  
  
class CustomField:
  ''' Stores information of a custom Field'''
  def __init__(self,customfield={},code=None):
    self.code=code
    self.name=customfield.get('Name',None)
    self.value=None
    self.type=customfield.get('Type',None)
    self.FieldType=customfield.get('Type',None)
    self.dropdownvalues=customfield.get('DropdownValues',None)
    
  def __str__(self):
    return self.name
    
class CustomFieldsAll:
  ''' Stores a list of custom field objects. Returns a custom
  custom field when code is supplied
  '''
  def __init__(self,custom_field_list):
    self.custom_field_list=custom_field_list
    
  def get_custom_field(self,code):
    for item in self.custom_field_list:
      if item.code==code:
        return item
        break
    return None
  
class CustomersAll:
  ''' Contains a list of all Customer Objects'''
  def __init__(self,customer_obj_list):
    self.customers=customer_obj_list
    
  def get_customer(self,code):
    for item in self.customers:
        if item.code==code:
          return item
    return None

  
class BusinessDetails:
  '''Own Business Details'''
  
  def __init__(self,businessdetails={},code=None):
    self.code=code
    self.businessName=businessdetails.get('BusinessName',None)
    self.businessContactInformation=businessdetails.get('BusinessContactInformation',None)
    self.businessIdentifier=businessdetails.get('BusinessIdentifier',None)
    
    
class SalesInvList:
  ''' A list of sales invoices searchable by dates'''
  def __init__(self,sinvli):
    self.sinvli=sinvli
    
  def filter_inv(self,from_date,to_date,inv_type):
    #from_date and to_date Format should be (YYYY,M,DD)
    retli=[]
    fm_date=datetime.strptime(from_date,'%d/%m/%Y')
    to_date=datetime.strptime(to_date,'%d/%m/%Y')
    for inv in self.sinvli:
      if inv.invoice_pydatetime >= fm_date and inv.invoice_pydatetime <= to_date and inv.gst_inv_type==inv_type:
        retli.append(inv)
    return retli
        
class B2CLS_Output:
  ''' Input will be a SalesInvList filtered for Date and Inv Type containing only b2cls '''
  def __init__(self,retli):
    self.retli=retli
    
  def b2cl_str(self):
    li=[{'rate':k,'taxablevalue':0} for k in range(1,28)]
    for invoice in self.retli:
      for line in invoice.gst_tax_taxablevalue:
        for tax in li:
          if tax['rate']==line['rate']:
            tax['taxablevalue']+=line['taxablevalue']
    nli=[]
    for item in li:
      if item['taxablevalue']!=0:
        nli.append(item)
    return nli
        
          
      
      
       
    

            
          
        
      
    
  
