import re
from peewee import *

teleos_db = MySQLDatabase(None)

def get_teleos_db():
    return teleos_db

DeferredClient = DeferredRelation()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = teleos_db

class Abbreviations(BaseModel):
    abbreviation = CharField(db_column='Abbreviation', primary_key=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    full_text = CharField(db_column='Full_text', null=True)
    practitioner = IntegerField(db_column='Practitioner_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'abbreviations'

class AccessRestriction(BaseModel):
    access_restriction = PrimaryKeyField(db_column='Access_restriction_ID')
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    program_to_restrict = CharField(db_column='Program_to_restrict', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    user_class = IntegerField(db_column='User_class_ID', null=True)

    class Meta:
        db_table = 'access_restriction'

class AccountsCategory(BaseModel):
    accounts_category = PrimaryKeyField(db_column='Accounts_category_ID')
    accounts_category_number = CharField(db_column='Accounts_category_number', null=True, unique=True)
    accounts_category_text = CharField(db_column='Accounts_category_text', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'accounts_category'

RE_ANIMAL_CLEAN_NAME = re.compile('^([a-zA-Z 0-9]+)')

class Animal(BaseModel):
    animal = PrimaryKeyField(db_column='Animal_ID')
    name = CharField(db_column='Animal_name', index=True, null=True)
    breed = CharField(db_column='Breed', null=True)
    client = ForeignKeyField(DeferredClient, related_name='clients', db_column='Client_ID', index=True, null=True)
    colour = CharField(db_column='Colour', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date_of_birth = DateTimeField(db_column='Date_of_birth', null=True)
    deceased = IntegerField(db_column='Deceased')
    height = DecimalField(db_column='Height', null=True)
    identity_number = CharField(db_column='Identity_number', index=True, null=True)
    inpatient = IntegerField(db_column='Inpatient')
    insurance_co = CharField(db_column='Insurance_Co', index=True, null=True)
    insurance_expiry_date = DateTimeField(db_column='Insurance_expiry_date', null=True)
    insurance_policy_number = CharField(db_column='Insurance_policy_number', index=True, null=True)
    markings = CharField(db_column='Markings', null=True)
    movedaway = IntegerField(db_column='MovedAway', null=True)
    neutered = IntegerField(db_column='Neutered')
    notes = CharField(db_column='Notes', null=True)
    operation = IntegerField(db_column='Operation_ID', null=True)
    other_1 = CharField(db_column='Other_1', index=True, null=True)
    other_2 = CharField(db_column='Other_2', null=True)
    other_3 = CharField(db_column='Other_3', null=True)
    other_4 = CharField(db_column='Other_4', null=True)
    other_5 = CharField(db_column='Other_5', null=True)
    overnight_charge = DecimalField(db_column='Overnight_charge', null=True)
    sensitive_notes = CharField(db_column='Sensitive_notes', null=True)
    sex = CharField(db_column='Sex', null=True)
    species = CharField(db_column='Species', null=True)
    ts = DateTimeField(db_column='TS')
    warning_or_status_1 = CharField(db_column='Warning_or_status_1', null=True)
    warning_or_status_2 = CharField(db_column='Warning_or_status_2', null=True)
    warning_or_status_3 = CharField(db_column='Warning_or_status_3', null=True)
    weight = DecimalField(db_column='Weight', null=True)

    def is_male(self):
        return self.sex == 'M' or self.sex == 'X'

    def get_clean_name(self):
        m = RE_ANIMAL_CLEAN_NAME.match(self.name)
        return m.group(1).strip()

    class Meta:
        db_table = 'animal'

class AnimalInsuranceDetails(BaseModel):
    animal = IntegerField(db_column='Animal_ID', null=True, unique=True)
    animal_insurance = PrimaryKeyField(db_column='Animal_insurance_ID')
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    exclusions = CharField(db_column='Exclusions', null=True)
    inception_date = DateTimeField(db_column='Inception_date', null=True)
    policy_excess = CharField(db_column='Policy_excess', null=True)
    policy_limit = DecimalField(db_column='Policy_limit', null=True)
    policy_type_text = CharField(db_column='Policy_type_text', index=True, null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'animal_insurance_details'

class Animalnotes(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    animalnoteid = PrimaryKeyField(db_column='AnimalNoteID')
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    lastedited = DateTimeField(db_column='LastEdited', index=True, null=True)
    practitionerid = IntegerField(db_column='PractitionerID', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', index=True, null=True)
    typeid = IntegerField(db_column='TypeID', null=True)

    class Meta:
        db_table = 'animalnotes'

class Animalstableyard(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    animalstableyardid = PrimaryKeyField(db_column='AnimalStableyardID')
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    stableyardid = IntegerField(db_column='StableyardID', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'animalstableyard'

class Appointmentnotifications(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    appointmentnotificationid = PrimaryKeyField(db_column='AppointmentNotificationID')
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    mobilenumber = CharField(db_column='MobileNumber', null=True)
    noticeperiod = IntegerField(db_column='NoticePeriod', null=True)
    notificationtext = CharField(db_column='NotificationText', null=True)
    slotid = IntegerField(db_column='SlotID', null=True, unique=True)
    status = CharField(db_column='Status', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'appointmentnotifications'

class Appointmentnotificationtext(BaseModel):
    appointmentnotificationtextid = PrimaryKeyField(db_column='AppointmentNotificationTextID')
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    ts = DateTimeField(db_column='TS', null=True)
    text = CharField(db_column='Text', null=True)
    title = CharField(db_column='Title', null=True)

    class Meta:
        db_table = 'appointmentnotificationtext'

class ApptTrigger(BaseModel):
    appointment_trigger = PrimaryKeyField(db_column='Appointment_trigger_ID')
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    diary = IntegerField(db_column='Diary_ID', null=True)
    how_soon = IntegerField(db_column='How_soon', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'appt_trigger'

class Archived(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', index=True, null=True)
    amount_in_currency = DecimalField(db_column='Amount_in_currency', null=True)
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    client_department = IntegerField(db_column='Client_department_ID', index=True, null=True)
    currency_abbreviation = CharField(db_column='Currency_abbreviation', null=True)
    date_entered = DateTimeField(db_column='Date_entered', index=True, null=True)
    details = CharField(db_column='Details', index=True, null=True)
    entered_by = IntegerField(db_column='Entered_by', null=True)
    invoice_date = DateTimeField(db_column='Invoice_date', index=True, null=True)
    invoiced = IntegerField(db_column='Invoiced')
    multiplication = FloatField(db_column='Multiplication', null=True)
    net_value = DecimalField(db_column='Net_value', null=True)
    paid = IntegerField(db_column='Paid')
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_or_procedure = CharField(db_column='Stock_or_Procedure', null=True)
    time_entered = DateTimeField(db_column='Time_entered', null=True)
    transaction = PrimaryKeyField(db_column='Transaction_ID')
    vat_amount = DecimalField(db_column='VAT_amount', null=True)
    vat_percentage = FloatField(db_column='VAT_percentage', null=True)
    work_done_by = IntegerField(db_column='Work_done_by', index=True, null=True)

    class Meta:
        db_table = 'archived'

class AuditTrail(BaseModel):
    audit_trail = PrimaryKeyField(db_column='Audit_trail_ID')
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    number = IntegerField(db_column='Number', null=True)
    spare_1 = CharField(db_column='Spare_1', null=True)
    spare_2 = IntegerField(db_column='Spare_2', null=True)
    ts = DateTimeField(db_column='TS')
    tax_point = DateTimeField(db_column='Tax_point', null=True)
    transaction = IntegerField(db_column='Transaction_ID', index=True, null=True)
    type = IntegerField(db_column='Type', null=True)

    class Meta:
        db_table = 'audit_trail'

class Breed(BaseModel):
    average_height_f = CharField(db_column='Average_height_F', null=True)
    average_height_m = CharField(db_column='Average_height_M', null=True)
    average_weight_f = CharField(db_column='Average_weight_F', null=True)
    average_weight_m = CharField(db_column='Average_weight_M', null=True)
    breed = PrimaryKeyField(db_column='Breed_ID')
    breed_text = CharField(db_column='Breed_text', null=True, unique=True)
    colours = CharField(db_column='Colours', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    idexxbreedid = IntegerField(db_column='IdexxBreedID', null=True)
    information1 = CharField(db_column='Information1', null=True)
    information2 = CharField(db_column='Information2', null=True)
    information3 = CharField(db_column='Information3', null=True)
    information4 = CharField(db_column='Information4', null=True)
    information5 = CharField(db_column='Information5', null=True)
    markings = CharField(db_column='Markings', null=True)
    picture = CharField(db_column='Picture', null=True)
    species = CharField(db_column='Species', null=True)
    subtype = CharField(db_column='Subtype', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'breed'

class Business(BaseModel):
    address_1 = CharField(db_column='Address_1', null=True)
    address_2 = CharField(db_column='Address_2', null=True)
    address_3 = CharField(db_column='Address_3', null=True)
    address_4 = CharField(db_column='Address_4', null=True)
    billing_terms = CharField(db_column='Billing_Terms', null=True)
    business = PrimaryKeyField(db_column='Business_ID')
    business_name = CharField(db_column='Business_Name', null=True)
    contact_name = CharField(db_column='Contact_Name', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    delivery_charge = DecimalField(db_column='Delivery_Charge', null=True)
    email_address = CharField(db_column='Email_Address', null=True)
    fax_number = CharField(db_column='Fax_Number', null=True)
    house_number = CharField(db_column='House_Number', null=True)
    isreferringpractice = IntegerField(db_column='IsReferringPractice', null=True)
    modem_number = CharField(db_column='Modem_Number', null=True)
    notes = CharField(db_column='Notes', null=True)
    postcode = CharField(db_column='Postcode', null=True)
    ts = DateTimeField(db_column='TS')
    telephone_number = CharField(db_column='Telephone_Number', null=True)
    website_url = CharField(db_column='Website_URL', null=True)

    class Meta:
        db_table = 'business'

class Cardterminalconfig(BaseModel):
    cardterminalid = PrimaryKeyField(db_column='CardTerminalID')
    ipaddress = CharField(db_column='IPAddress', null=True, unique=True)
    sitelocation = CharField(db_column='SiteLocation', null=True)
    terminalidentifier = CharField(db_column='TerminalIdentifier', null=True, unique=True)

    class Meta:
        db_table = 'cardterminalconfig'

class Client(BaseModel):
    address_1 = CharField(db_column='Address_1', index=True, null=True)
    address_2 = CharField(db_column='Address_2', index=True, null=True)
    address_3 = CharField(db_column='Address_3', index=True, null=True)
    address_4 = CharField(db_column='Address_4', index=True, null=True)
    bill_type = CharField(db_column='Bill_type', null=True)
    billing_terms = CharField(db_column='Billing_terms', null=True)
    client = PrimaryKeyField(db_column='Client_ID')
    client_department = IntegerField(db_column='Client_department_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    credit_limit = DecimalField(db_column='Credit_limit', null=True)
    email_address = CharField(db_column='Email_address', null=True)
    first_name_or_initials = CharField(db_column='First_name_or_initials', null=True)
    first_name_or_initials_2 = CharField(db_column='First_name_or_initials_2', null=True)
    first_registered = DateTimeField(db_column='First_registered', null=True)
    global_discount = FloatField(db_column='Global_discount', null=True)
    home_text = CharField(db_column='Home_text', null=True)
    home_text_2 = CharField(db_column='Home_text_2', null=True)
    house_number = CharField(db_column='House_number', index=True, null=True)
    last_visit = DateTimeField(db_column='Last_visit', null=True)
    map_reference = CharField(db_column='Map_reference', null=True)
    mileage = IntegerField(db_column='Mileage', null=True)
    mobile_text = CharField(db_column='Mobile_text', null=True)
    movedaway = IntegerField(db_column='MovedAway', null=True)
    next_appointment_date = DateTimeField(db_column='Next_appointment_date', null=True)
    next_appointment_diary_no = IntegerField(db_column='Next_appointment_diary_no', null=True)
    next_appointment_time = DateTimeField(db_column='Next_appointment_time', null=True)
    notes = CharField(db_column='Notes', null=True)
    other_1 = CharField(db_column='Other_1', index=True, null=True)
    other_2 = CharField(db_column='Other_2', index=True, null=True)
    other_3 = CharField(db_column='Other_3', null=True)
    other_4 = CharField(db_column='Other_4', null=True)
    other_5 = CharField(db_column='Other_5', null=True)
    other_address_1 = CharField(db_column='Other_Address_1', index=True, null=True)
    other_address_2 = CharField(db_column='Other_Address_2', null=True)
    other_address_3 = CharField(db_column='Other_Address_3', null=True)
    other_address_4 = CharField(db_column='Other_Address_4', null=True)
    other_housenumber = CharField(db_column='Other_Housenumber', null=True)
    other_postcode = CharField(db_column='Other_Postcode', index=True, null=True)
    phone_home = CharField(db_column='Phone_home', index=True, null=True)
    phone_home_2 = CharField(db_column='Phone_home_2', null=True)
    phone_mobile = CharField(db_column='Phone_mobile', index=True, null=True)
    phone_work = CharField(db_column='Phone_work', index=True, null=True)
    postcode = CharField(db_column='Postcode', index=True, null=True)
    referringpracticeid = IntegerField(db_column='ReferringPracticeID', null=True)
    referringvetid = IntegerField(db_column='ReferringVetID', null=True)
    send_this_run = IntegerField(db_column='Send_this_run')
    sensitive_notes = CharField(db_column='Sensitive_notes', null=True)
    surname = CharField(db_column='Surname', index=True, null=True)
    surname_2 = CharField(db_column='Surname_2', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    thirdpartyoptout = IntegerField(db_column='ThirdPartyOptOut', null=True)
    title = CharField(db_column='Title', null=True)
    title_2 = CharField(db_column='Title_2', null=True)
    usual_branch = IntegerField(db_column='Usual_branch', null=True)
    usual_vet_1 = CharField(db_column='Usual_vet_1', null=True)
    usual_vet_2 = CharField(db_column='Usual_vet_2', null=True)
    warning_or_status_1 = CharField(db_column='Warning_or_status_1', null=True)
    warning_or_status_2 = CharField(db_column='Warning_or_status_2', null=True)
    warning_or_status_3 = CharField(db_column='Warning_or_status_3', null=True)
    which_billing_address = CharField(db_column='Which_billing_address', null=True)
    which_recall_address = CharField(db_column='Which_recall_address', null=True)
    work_text = CharField(db_column='Work_text', null=True)

    def get_intl_mobile(self):
        mob = self.phone_mobile.strip()
        if mob is None or len(mob) == 0:
            raise KeyError('No mobile number')

        mob = "".join(mob.split(' '))
        if mob[0] == '0':
            mob = "44" + mob[1:]
        elif mob[0] == '7':
            mob = "44" + mob

        return mob

    class Meta:
        db_table = 'client'

class ClientDepartment(BaseModel):
    client_department = PrimaryKeyField(db_column='Client_department_ID')
    client_department_number = CharField(db_column='Client_department_number', null=True, unique=True)
    client_department_text = CharField(db_column='Client_department_text', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    default_telephone_number = CharField(db_column='Default_telephone_number', null=True)
    next_purchase_order_number = IntegerField(db_column='Next_Purchase_Order_Number', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'client_department'

class Clientadditionalcontactnum(BaseModel):
    caption = CharField(db_column='Caption', null=True)
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    contactid = PrimaryKeyField(db_column='ContactID')
    lastedited = DateTimeField(db_column='LastEdited', null=True)
    number = CharField(db_column='Number', null=True)

    class Meta:
        db_table = 'clientadditionalcontactnum'

class ClientBalance(BaseModel):
    balance = DecimalField(db_column='Balance', null=True)
    clientbalanceid = PrimaryKeyField(db_column='ClientBalanceID')
    client = ForeignKeyField(Client, db_column='ClientID', index=True, null=True)
    insurance_balance = DecimalField(db_column='InsuranceBalance', null=True)
    php_balance = DecimalField(db_column='PHPBalance', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'clientbalance'

class Clientstableyard(BaseModel):
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    clientstableyardid = PrimaryKeyField(db_column='ClientStableyardID')
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    stableyardid = IntegerField(db_column='StableyardID', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'clientstableyard'

class Colour(BaseModel):
    colour = PrimaryKeyField(db_column='Colour_ID')
    colour_text = CharField(db_column='Colour_text', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'colour'

class Currency(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    currency_abbreviation = CharField(db_column='Currency_abbreviation', primary_key=True)
    currency_text = CharField(db_column='Currency_text', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'currency'

class Databaseversion(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    databaseversionid = PrimaryKeyField(db_column='DatabaseVersionID')
    ts = DateTimeField(db_column='TS', null=True)
    version = IntegerField(db_column='Version', index=True, null=True)

    class Meta:
        db_table = 'databaseversion'

class Deletions(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    deleteid = PrimaryKeyField(db_column='DeleteID')
    ts = DateTimeField(db_column='TS')
    tableid = IntegerField(db_column='TableID')
    tablename = CharField(db_column='TableName', null=True)

    class Meta:
        db_table = 'deletions'

class Diary(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    defaultnotificationtext = IntegerField(db_column='DefaultNotificationText', null=True)
    diary = PrimaryKeyField(db_column='Diary_ID')
    diary_name = CharField(db_column='Diary_name', null=True, unique=True)
    diary_type = CharField(db_column='Diary_type', null=True)
    slots_profile_fri = CharField(db_column='Slots_profile_Fri', null=True)
    slots_profile_mon = CharField(db_column='Slots_profile_Mon', null=True)
    slots_profile_sat = CharField(db_column='Slots_profile_Sat', null=True)
    slots_profile_sun = CharField(db_column='Slots_profile_Sun', null=True)
    slots_profile_thu = CharField(db_column='Slots_profile_Thu', null=True)
    slots_profile_tue = CharField(db_column='Slots_profile_Tue', null=True)
    slots_profile_wed = CharField(db_column='Slots_profile_Wed', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'diary'

class DocumentationTrigger(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    documentation_trigger = PrimaryKeyField(db_column='Documentation_trigger_ID')
    file_to_print = CharField(db_column='File_to_print', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    stockorprocedure = CharField(db_column='StockorProcedure', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'documentation_trigger'

class Dosage(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    dosage_or_warning = PrimaryKeyField(db_column='Dosage_or_warning_ID')
    dosage_or_warning_abbrev = CharField(db_column='Dosage_or_warning_abbrev', null=True, unique=True)
    dosage_or_warning_text = CharField(db_column='Dosage_or_warning_text', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'dosage'

class DrugCategory(BaseModel):
    drug_category = PrimaryKeyField(db_column='Drug_category')
    drug_category_abbreviation = CharField(db_column='Drug_category_abbreviation', null=True)
    drug_category_full_text = CharField(db_column='Drug_category_full_text', null=True)

    class Meta:
        db_table = 'drug_category'

class DrugLocation(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    drug_location = PrimaryKeyField(db_column='Drug_location_ID')
    drug_location_text = CharField(db_column='Drug_location_text', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'drug_location'

class DrugLocationAbbreviation(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    drug_location_abbreviation = CharField(db_column='Drug_Location_Abbreviation', index=True, null=True)
    drug_location = PrimaryKeyField(db_column='Drug_Location_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'drug_location_abbreviation'

class Edits(BaseModel):
    editid = PrimaryKeyField(db_column='EditID')
    tableid = IntegerField(db_column='TableID')
    tablename = CharField(db_column='TableName', null=True)

    class Meta:
        db_table = 'edits'

class Errors(BaseModel):
    additionaldetails = CharField(db_column='AdditionalDetails', null=True)
    errordate = DateTimeField(db_column='ErrorDate', null=True)
    errordescription = CharField(db_column='ErrorDescription', null=True)
    errorid = PrimaryKeyField(db_column='ErrorID')
    practitionerinitials = CharField(db_column='PractitionerInitials', null=True)
    runningquery = CharField(db_column='RunningQuery', null=True)
    sectionref = CharField(db_column='SectionRef', null=True)
    source = CharField(db_column='Source', null=True)
    sourceversion = CharField(db_column='SourceVersion', null=True)
    stacktrace = CharField(db_column='StackTrace', null=True)
    workstation = CharField(db_column='Workstation', null=True)
    workstationfolder = CharField(db_column='WorkstationFolder', null=True)

    class Meta:
        db_table = 'errors'

class Estimate(BaseModel):
    amount = DecimalField(db_column='Amount', null=True)
    animal = IntegerField(db_column='Animal_ID', null=True)
    client = IntegerField(db_column='Client_ID', null=True)
    date = DateTimeField(db_column='Date', index=True, null=True)
    description = CharField(db_column='Description', null=True)
    estimate = PrimaryKeyField(db_column='Estimate_ID')
    file_contained_in = CharField(db_column='File_contained_in', null=True)

    class Meta:
        db_table = 'estimate'

class ExplicitDosage(BaseModel):
    dosagemessage = TextField(db_column='DosageMessage', null=True)
    explicitdosageid = PrimaryKeyField(db_column='ExplicitDosageID')
    species = IntegerField(db_column='Species', null=True)
    speciesid = IntegerField(db_column='SpeciesID', null=True)
    stockid = IntegerField(db_column='StockID', null=True)
    warningmessage = TextField(db_column='WarningMessage', null=True)

    class Meta:
        db_table = 'explicit_dosage'

class FieldChangeTrigger(BaseModel):
    client_or_animal = CharField(db_column='Client_or_animal', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    field_change_trigger = PrimaryKeyField(db_column='Field_change_trigger')
    field_to_change = CharField(db_column='Field_to_change', null=True)
    new_value = CharField(db_column='New_value', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'field_change_trigger'

class FieldChangeTriggerCopy(BaseModel):
    client_or_animal = CharField(db_column='Client_or_animal', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    field_change_trigger = PrimaryKeyField(db_column='Field_change_trigger')
    field_to_change = CharField(db_column='Field_to_change', null=True)
    new_value = CharField(db_column='New_value', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'field_change_trigger_copy'

class HospitalEntries(BaseModel):
    admitted_by = IntegerField(db_column='Admitted_by_ID', null=True)
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    cancellation_reason = CharField(db_column='Cancellation_Reason', null=True)
    cancelled = IntegerField(db_column='Cancelled')
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    communication = TextField(db_column='Communication', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date_admitted = DateTimeField(db_column='Date_Admitted', null=True)
    date_discharged = DateTimeField(db_column='Date_discharged', null=True)
    discharge_details = TextField(db_column='Discharge_Details', null=True)
    inpatient = IntegerField(db_column='Inpatient', index=True)
    list = IntegerField(db_column='List_ID', index=True, null=True)
    notes = TextField(db_column='Notes', null=True)
    nurse = IntegerField(db_column='Nurse_ID', null=True)
    operation = PrimaryKeyField(db_column='Operation_ID')
    phone_special = CharField(db_column='Phone_Special', null=True)
    reason_for_admittal = CharField(db_column='Reason_for_admittal', null=True)
    status = CharField(db_column='Status', null=True)
    ts = DateTimeField(db_column='TS')
    under_care_of = IntegerField(db_column='Under_care_of_ID', null=True)

    class Meta:
        db_table = 'hospital_entries'

class HospitalSheet(BaseModel):
    appetite = CharField(db_column='Appetite', null=True)
    comments = CharField(db_column='Comments', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date = DateTimeField(db_column='Date', null=True)
    drink = CharField(db_column='Drink', null=True)
    entry = PrimaryKeyField(db_column='Entry_ID')
    medication = IntegerField(db_column='Medication_ID', index=True, null=True)
    medication_administered = IntegerField(db_column='Medication_administered')
    medication_date = DateTimeField(db_column='Medication_date', null=True)
    medication_freehand = CharField(db_column='Medication_freehand', null=True)
    medication_quantity = FloatField(db_column='Medication_quantity', null=True)
    medication_type = CharField(db_column='Medication_type', null=True)
    motions = CharField(db_column='Motions', null=True)
    operation = IntegerField(db_column='Operation_ID', index=True, null=True)
    pulse = CharField(db_column='Pulse', null=True)
    respiration = CharField(db_column='Respiration', null=True)
    ts = DateTimeField(db_column='TS')
    temp = FloatField(db_column='Temp', null=True)
    urine = CharField(db_column='Urine', null=True)
    user = IntegerField(db_column='User_ID', index=True, null=True)
    vomiting = CharField(db_column='Vomiting', null=True)

    class Meta:
        db_table = 'hospital_sheet'

class Idexxbreedlist(BaseModel):
    code = CharField(db_column='Code', index=True, null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    idexxbreedlistid = PrimaryKeyField(db_column='IdexxBreedListID')
    name = CharField(db_column='Name', null=True)
    speciescode = CharField(db_column='SpeciesCode', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'idexxbreedlist'

class Idexxpendingtests(BaseModel):
    animalid = IntegerField(db_column='AnimalID', null=True)
    clientid = IntegerField(db_column='ClientID', null=True)
    idexxpendingtestid = PrimaryKeyField(db_column='IdexxPendingTestID')
    ordernumber = CharField(db_column='OrderNumber', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)
    transactionid = IntegerField(db_column='TransactionID', index=True, null=True)

    class Meta:
        db_table = 'idexxpendingtests'

class Idexxreferenceversion(BaseModel):
    idexxreferenceversionid = PrimaryKeyField(db_column='IdexxReferenceVersionID')
    name = CharField(db_column='Name', null=True)
    ts = DateTimeField(db_column='TS', null=True)
    version = CharField(db_column='Version', null=True)

    class Meta:
        db_table = 'idexxreferenceversion'

class Idexxspecieslist(BaseModel):
    code = CharField(db_column='Code', index=True, null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    idexxspecieslistid = PrimaryKeyField(db_column='IdexxSpeciesListID')
    name = CharField(db_column='Name', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'idexxspecieslist'

class Idexxtestlist(BaseModel):
    addon = IntegerField(db_column='AddOn', null=True)
    allowsaddons = IntegerField(db_column='AllowsAddOns', null=True)
    allowsbatch = IntegerField(db_column='AllowsBatch', null=True)
    code = CharField(db_column='Code', index=True, null=True)
    currencycode = CharField(db_column='CurrencyCode', null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    idexxtestlistid = PrimaryKeyField(db_column='IdexxTestListID')
    listprice = DecimalField(db_column='ListPrice', null=True)
    name = CharField(db_column='Name', null=True)
    specimen = CharField(db_column='Specimen', null=True)
    ts = DateTimeField(db_column='TS', null=True)
    turnaround = CharField(db_column='Turnaround', null=True)

    class Meta:
        db_table = 'idexxtestlist'

class Idexxtestlistlinks(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    feemarkup = DecimalField(db_column='FeeMarkup', null=True)
    idexxtestlistid = IntegerField(db_column='IdexxTestListID', index=True, null=True)
    idexxtestlistlinkid = PrimaryKeyField(db_column='IdexxTestListLinkID')
    percentagemarkup = FloatField(db_column='PercentageMarkup', null=True)
    procedureid = IntegerField(db_column='ProcedureID', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'idexxtestlistlinks'

class IncludedStock(BaseModel):
    add_price = IntegerField(db_column='Add_price')
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    destock = IntegerField(db_column='Destock')
    included_stock_instance = PrimaryKeyField(db_column='Included_stock_instance_ID')
    multiplier = IntegerField(db_column='Multiplier', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    stock_item = IntegerField(db_column='Stock_item', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'included_stock'

class Insurance(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    insurance = PrimaryKeyField(db_column='Insurance_ID')
    insurance_co_name = CharField(db_column='Insurance_co_name', null=True, unique=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'insurance'

class InsuranceClaims(BaseModel):
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    completed = DateTimeField(db_column='Completed', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date_entered = DateTimeField(db_column='Date_entered', null=True)
    insurance_guid = CharField(db_column='Insurance_GUID', primary_key=True)
    notes = CharField(db_column='Notes', null=True)
    practitioner = IntegerField(db_column='Practitioner_ID', index=True, null=True)
    query_guid = CharField(db_column='Query_GUID', null=True, unique=True)
    recipient_guid = CharField(db_column='Recipient_GUID', index=True, null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'insurance_claims'

class InsuranceConditions(BaseModel):
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    claim_date = DateTimeField(db_column='Claim_date', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    description = CharField(db_column='Description', null=True)
    insurance_condition = PrimaryKeyField(db_column='Insurance_condition_ID')
    ts = DateTimeField(db_column='TS')
    total_ex_vat = DecimalField(db_column='Total_ex_VAT', null=True)
    total_incl_vat = DecimalField(db_column='Total_incl_VAT', null=True)
    treatment_date_from = DateTimeField(db_column='Treatment_date_from', null=True)
    treatment_date_to = DateTimeField(db_column='Treatment_date_to', null=True)
    vat = DecimalField(db_column='VAT', null=True)

    class Meta:
        db_table = 'insurance_conditions'

class InsurancePolicyType(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    insurance = IntegerField(db_column='Insurance_ID', index=True, null=True)
    policy_type = PrimaryKeyField(db_column='Policy_type_ID')
    policy_type_text = CharField(db_column='Policy_type_text', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'insurance_policy_type'

class Invoicecheck(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', index=True, null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    enddate = DateTimeField(db_column='EndDate', index=True, null=True)
    invoicecheckid = PrimaryKeyField(db_column='InvoiceCheckID')
    startdate = DateTimeField(db_column='StartDate', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'invoicecheck'

class Invoicelinks(BaseModel):
    amount = DecimalField(db_column='Amount', null=True)
    animalid = IntegerField(db_column='AnimalID', null=True)
    clientid = IntegerField(db_column='ClientID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    invoicelineid = IntegerField(db_column='InvoiceLineID', index=True, null=True)
    invoicelinkid = PrimaryKeyField(db_column='InvoiceLinkID')
    ts = DateTimeField(db_column='TS', null=True)
    transactionid = IntegerField(db_column='TransactionID', index=True, null=True)
    transactiontype = IntegerField(db_column='TransactionType', null=True)

    class Meta:
        db_table = 'invoicelinks'

class Invoices(BaseModel):
    client = IntegerField(db_column='Client_ID', index=True)
    invoice_date = DateTimeField(db_column='Invoice_Date', index=True, null=True)
    invoice = PrimaryKeyField(db_column='Invoice_ID')
    invoice_number = IntegerField(db_column='Invoice_Number', unique=True)
    parent_invoice_line = IntegerField(db_column='Parent_Invoice_Line_ID', index=True)
    practitioner = IntegerField(db_column='Practitioner_ID', index=True)

    class Meta:
        db_table = 'invoices'

class Kennel(BaseModel):
    amount_per_day = DecimalField(db_column='Amount_per_day', null=True)
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    arrival_date = DateTimeField(db_column='Arrival_date', index=True, null=True)
    boarding_tariff = CharField(db_column='Boarding_tariff', null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    current_status = CharField(db_column='Current_status', index=True, null=True)
    departure_date = DateTimeField(db_column='Departure_date', index=True, null=True)
    extra_notes_1 = CharField(db_column='Extra_notes_1', null=True)
    extra_notes_2 = CharField(db_column='Extra_notes_2', null=True)
    extra_notes_3 = CharField(db_column='Extra_notes_3', null=True)
    extra_work_1_status = CharField(db_column='Extra_work_1_status', null=True)
    extra_work_2_status = CharField(db_column='Extra_work_2_status', null=True)
    extra_work_3_status = CharField(db_column='Extra_work_3_status', null=True)
    extra_work_4_status = CharField(db_column='Extra_work_4_status', null=True)
    kennel = PrimaryKeyField(db_column='Kennel_ID')
    last_intrac = DateTimeField(db_column='Last_Intrac', null=True)
    last_booster = DateTimeField(db_column='Last_booster', null=True)
    moves_required = CharField(db_column='Moves_required', null=True)
    permanent_notes = CharField(db_column='Permanent_notes', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'kennel'

class KennelHistory(BaseModel):
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date = DateTimeField(db_column='Date', null=True)
    entered_by = IntegerField(db_column='Entered_by', null=True)
    kennel = IntegerField(db_column='Kennel_ID', index=True, null=True)
    kennel_history = PrimaryKeyField(db_column='Kennel_history_ID')
    notes = CharField(db_column='Notes', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'kennel_history'

class Labels(BaseModel):
    action1 = CharField(db_column='Action1', null=True)
    action1practitioner = CharField(db_column='Action1Practitioner', null=True)
    action2 = CharField(db_column='Action2', null=True)
    action2practitioner = CharField(db_column='Action2Practitioner', null=True)
    action3 = CharField(db_column='Action3', null=True)
    action3practitioner = CharField(db_column='Action3Practitioner', null=True)
    animal = CharField(db_column='Animal', null=True)
    client = CharField(db_column='Client', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date = CharField(db_column='Date', null=True)
    dosewarn1 = CharField(db_column='DoseWarn1', null=True)
    dosewarn2 = CharField(db_column='DoseWarn2', null=True)
    dosewarn3 = CharField(db_column='DoseWarn3', null=True)
    dosewarn4 = CharField(db_column='DoseWarn4', null=True)
    drug = CharField(db_column='Drug', null=True)
    labelid = PrimaryKeyField(db_column='LabelID')
    numberoflabels = IntegerField(db_column='NumberOfLabels', null=True)
    quantity = CharField(db_column='Quantity', null=True)
    rcvsnumber = CharField(db_column='RCVSnumber', null=True)
    ts = DateTimeField(db_column='TS')
    transactionid = IntegerField(db_column='TransactionID', null=True)

    class Meta:
        db_table = 'labels'

class LogInvoicerun(BaseModel):
    billingparameters = TextField(db_column='BillingParameters', null=True)
    clientdepartment = IntegerField(db_column='ClientDepartment', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    endinginvoicenumber = IntegerField(db_column='EndingInvoiceNumber', null=True)
    endingstatementnumber = IntegerField(db_column='EndingStatementNumber', null=True)
    invoicerunid = PrimaryKeyField(db_column='InvoiceRunID')
    practitionerinitials = CharField(db_column='PractitionerInitials', null=True)
    runendtime = DateTimeField(db_column='RunEndTime', null=True)
    runstarttime = DateTimeField(db_column='RunStartTime', null=True)
    startinginvoicenumber = IntegerField(db_column='StartingInvoiceNumber', null=True)
    startingstatementnumber = IntegerField(db_column='StartingStatementNumber', null=True)
    ts = DateTimeField(db_column='TS', null=True)
    workstationfolder = CharField(db_column='WorkstationFolder', null=True)

    class Meta:
        db_table = 'log_invoicerun'

class Macrov1(BaseModel):
    command = CharField(db_column='Command', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    description = CharField(db_column='Description', null=True)
    macro = PrimaryKeyField(db_column='Macro_ID')
    procedure = IntegerField(db_column='Procedure_ID', index=True, null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'macrov1'

class Macrov2(BaseModel):
    ask = IntegerField(db_column='Ask', null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    free = IntegerField(db_column='Free', null=True)
    groupid = IntegerField(db_column='GroupID', index=True, null=True)
    itemreference = CharField(db_column='ItemReference', null=True)
    itemtype = CharField(db_column='ItemType', null=True)
    lineindex = FloatField(db_column='LineIndex', null=True)
    macrolineid = PrimaryKeyField(db_column='MacroLineID')
    mult = IntegerField(db_column='Mult', null=True)
    procedureid = IntegerField(db_column='ProcedureID', index=True, null=True)
    quantity = FloatField(db_column='Quantity', null=True)
    singleselection = IntegerField(db_column='SingleSelection', null=True)
    ts = DateTimeField(db_column='TS')
    xfercosttoprocedure = IntegerField(db_column='XferCostToProcedure', null=True)

    class Meta:
        db_table = 'macrov2'

class Manufacturer(BaseModel):
    address_1 = CharField(db_column='Address_1', null=True)
    address_2 = CharField(db_column='Address_2', null=True)
    address_3 = CharField(db_column='Address_3', null=True)
    address_4 = CharField(db_column='Address_4', null=True)
    billing_terms = CharField(db_column='Billing_Terms', null=True)
    contact_name = CharField(db_column='Contact_Name', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    delivery_charge = DecimalField(db_column='Delivery_Charge', null=True)
    email_address = CharField(db_column='Email_Address', null=True)
    fax_number = CharField(db_column='Fax_Number', null=True)
    house_number = CharField(db_column='House_Number', null=True)
    manufacturer = PrimaryKeyField(db_column='Manufacturer_ID')
    manufacturer_name = CharField(db_column='Manufacturer_Name', null=True)
    modem_number = CharField(db_column='Modem_Number', null=True)
    notes = TextField(db_column='Notes', null=True)
    postcode = CharField(db_column='Postcode', null=True)
    ts = DateTimeField(db_column='TS')
    telephone_number = CharField(db_column='Telephone_Number', null=True)
    website_url = CharField(db_column='Website_URL', null=True)

    class Meta:
        db_table = 'manufacturer'

class Memos(BaseModel):
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    client_or_animal = CharField(db_column='Client_or_Animal', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date = DateTimeField(db_column='Date', null=True)
    memo = PrimaryKeyField(db_column='Memo_ID')
    memo_text = CharField(db_column='Memo_text', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'memos'

class NewBatchNumbers(BaseModel):
    amount_remaining = FloatField(db_column='Amount_remaining', null=True)
    batch = PrimaryKeyField(db_column='Batch_ID')
    batch_number = CharField(db_column='Batch_number', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    drug_location = IntegerField(db_column='Drug_location_ID', null=True)
    expiry_date = DateTimeField(db_column='Expiry_date', index=True, null=True)
    last_used = DateTimeField(db_column='Last_used', index=True, null=True)
    stock = IntegerField(db_column='Stock_ID', index=True, null=True)
    supplier = IntegerField(db_column='Supplier_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'new_batch_numbers'

class NotesTrigger(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    multiplication_factor = IntegerField(db_column='Multiplication_factor', null=True)
    notes_trigger = PrimaryKeyField(db_column='Notes_trigger_ID')
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', null=True)

    class Meta:
        db_table = 'notes_trigger'

class Oldstuff(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', index=True, null=True)
    amount_in_currency = DecimalField(db_column='Amount_in_currency', null=True)
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    client_department = IntegerField(db_column='Client_department_ID', index=True, null=True)
    currency_abbreviation = CharField(db_column='Currency_abbreviation', null=True)
    date_entered = DateTimeField(db_column='Date_entered', index=True, null=True)
    details = CharField(db_column='Details', index=True, null=True)
    entered_by = IntegerField(db_column='Entered_by', null=True)
    invoice_date = DateTimeField(db_column='Invoice_date', index=True, null=True)
    invoiced = IntegerField(db_column='Invoiced')
    multiplication = FloatField(db_column='Multiplication', null=True)
    net_value = DecimalField(db_column='Net_value', null=True)
    paid = IntegerField(db_column='Paid')
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_or_procedure = CharField(db_column='Stock_or_Procedure', null=True)
    time_entered = DateTimeField(db_column='Time_entered', null=True)
    transaction = PrimaryKeyField(db_column='Transaction_ID')
    vat_amount = DecimalField(db_column='VAT_amount', null=True)
    vat_percentage = FloatField(db_column='VAT_percentage', null=True)
    work_done_by = IntegerField(db_column='Work_done_by', index=True, null=True)

    class Meta:
        db_table = 'oldstuff'

class Onpaymentdiscounts(BaseModel):
    animalid = IntegerField(db_column='AnimalID', null=True)
    clientid = IntegerField(db_column='ClientID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    discountid = IntegerField(db_column='DiscountID', index=True, null=True)
    discountpercentage = IntegerField(db_column='DiscountPercentage', null=True)
    netamount = DecimalField(db_column='NetAmount', null=True)
    onpaymentdiscountid = PrimaryKeyField(db_column='OnPaymentDiscountID')
    ts = DateTimeField(db_column='TS', null=True)
    totalamount = DecimalField(db_column='TotalAmount', null=True)
    transactionid = IntegerField(db_column='TransactionID', index=True, null=True)
    vatamount = DecimalField(db_column='VATAmount', null=True)

    class Meta:
        db_table = 'onpaymentdiscounts'

class Operations(BaseModel):
    animal = IntegerField(db_column='Animal_ID', null=True)
    client = IntegerField(db_column='Client_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    details = CharField(db_column='Details', null=True)
    op_date = DateTimeField(db_column='Op_date', null=True)
    op_time = DateTimeField(db_column='Op_time', null=True)
    operation = PrimaryKeyField(db_column='Operation_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'operations'

class OrderNumber(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date_purchased = DateTimeField(db_column='Date_purchased', null=True)
    order_number = PrimaryKeyField(db_column='Order_number_ID')
    purchase_order_number = CharField(db_column='Purchase_Order_Number', null=True)
    supplier = IntegerField(db_column='Supplier_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'order_number'

class PaymentType(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    payment_text = CharField(db_column='Payment_text', null=True)
    payment_type = PrimaryKeyField(db_column='Payment_type_ID')
    surchargedepts = CharField(db_column='SurchargeDepts', null=True)
    surchargeiflessthan = DecimalField(db_column='SurchargeIfLessThan', null=True)
    surchargeifmorethan = DecimalField(db_column='SurchargeIfMoreThan', null=True)
    surchargepercentage = IntegerField(db_column='SurchargePercentage', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'payment_type'

class Paymentallocations(BaseModel):
    amount = DecimalField(db_column='Amount', null=True)
    animalid = IntegerField(db_column='AnimalID', null=True)
    clientid = IntegerField(db_column='ClientID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    paymentallocationid = PrimaryKeyField(db_column='PaymentAllocationID')
    paymentid = IntegerField(db_column='PaymentID', index=True, null=True)
    receiptid = IntegerField(db_column='ReceiptID', null=True)
    ts = DateTimeField(db_column='TS', null=True)
    transactionid = IntegerField(db_column='TransactionID', index=True, null=True)

    class Meta:
        db_table = 'paymentallocations'

class Pdfs(BaseModel):
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    dateprinted = DateTimeField(db_column='DatePrinted', null=True)
    date_created = DateTimeField(db_column='Date_created', null=True)
    date_sent = DateTimeField(db_column='Date_sent', null=True)
    email_address = CharField(db_column='Email_address', null=True)
    filename = CharField(db_column='Filename', null=True)
    invoice_number = CharField(db_column='Invoice_number', null=True)
    pdf = PrimaryKeyField(db_column='PDF_ID')
    printed = IntegerField(db_column='Printed')
    status = CharField(db_column='Status', null=True)
    ts = DateTimeField(db_column='TS')
    transactionid = IntegerField(db_column='TransactionID', null=True)
    type = CharField(db_column='Type', null=True)

    class Meta:
        db_table = 'pdfs'

class PhpInstance(BaseModel):
    active = IntegerField(db_column='Active')
    animal = ForeignKeyField(Animal, db_column='Animal_ID', index=True, null=True)
    client = ForeignKeyField(Client, db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    lastedited = DateTimeField(db_column='LastEdited', null=True)
    lasteditedby = CharField(db_column='LastEditedBy', null=True)
    notes = CharField(db_column='Notes', null=True)
    php_procedure = IntegerField(db_column='PHP_Procedure_ID', index=True, null=True)
    php_instance = PrimaryKeyField(db_column='PHP_instance_ID')
    plan_end_date = DateTimeField(db_column='Plan_end_date', index=True, null=True)
    plan_start_date = DateTimeField(db_column='Plan_start_date', index=True, null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'php_instance'

class Phpallocations(BaseModel):
    allowed = FloatField(db_column='Allowed', null=True)
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    groupid = IntegerField(db_column='GroupID', index=True, null=True)
    had = FloatField(db_column='Had', null=True)
    itemref = CharField(db_column='ItemRef', null=True)
    itemtype = CharField(db_column='ItemType', null=True)
    lastedited = DateTimeField(db_column='LastEdited', null=True)
    lasteditedby = IntegerField(db_column='LastEditedBy', null=True)
    phpallocationid = PrimaryKeyField(db_column='PHPAllocationID')
    phpinstanceid = IntegerField(db_column='PHPInstanceID', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'phpallocations'

class Postcode(BaseModel):
    county = CharField(db_column='County', null=True)
    locality = CharField(db_column='Locality', null=True)
    postcode = CharField(db_column='Postcode', primary_key=True)
    posttown = CharField(db_column='Posttown', null=True)
    street = CharField(db_column='Street', null=True)
    street_numbers = TextField(db_column='Street_numbers', null=True)

    class Meta:
        db_table = 'postcode'

class Practitioner(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    password = CharField(db_column='Password', index=True, null=True)
    practitioner = PrimaryKeyField(db_column='Practitioner_ID')
    practitioner_full_name = CharField(db_column='Practitioner_full_name', null=True)
    practitioner_initials = CharField(db_column='Practitioner_initials', null=True, unique=True)
    rcvsnumber = IntegerField(db_column='RCVSnumber', null=True)
    ts = DateTimeField(db_column='TS')
    user_class = IntegerField(db_column='User_class_ID', null=True)
    vetformularykey = CharField(db_column='VetFormularyKey', null=True)

    class Meta:
        db_table = 'practitioner'

class Prescription(BaseModel):
    animal = IntegerField(db_column='Animal_ID', null=True)
    client = IntegerField(db_column='Client_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    details = CharField(db_column='Details', null=True)
    expiry_date = DateTimeField(db_column='Expiry_date', null=True)
    last_edited_date = DateTimeField(db_column='Last_edited_date', null=True)
    last_edited_initials = CharField(db_column='Last_edited_initials', null=True)
    prescription = PrimaryKeyField(db_column='Prescription_ID')
    repeats_allowed = IntegerField(db_column='Repeats_allowed', null=True)
    repeats_had = IntegerField(db_column='Repeats_had', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'prescription'

class PrescriptionHistory(BaseModel):
    animal = IntegerField(db_column='Animal_ID', null=True)
    client = IntegerField(db_column='Client_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date = DateTimeField(db_column='Date', null=True)
    initials = CharField(db_column='Initials', null=True)
    prescription = IntegerField(db_column='Prescription_ID', index=True, null=True)
    prescription_history = PrimaryKeyField(db_column='Prescription_history_ID')
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', null=True)

    class Meta:
        db_table = 'prescription_history'

class PrescriptionLine(BaseModel):
    animal = IntegerField(db_column='Animal_ID', null=True)
    client = IntegerField(db_column='Client_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    dosage = CharField(db_column='Dosage', null=True)
    prescription = IntegerField(db_column='Prescription_ID', index=True, null=True)
    prescription_line = PrimaryKeyField(db_column='Prescription_line_ID')
    quantity = FloatField(db_column='Quantity', null=True)
    substock = IntegerField(db_column='Substock_ID', null=True)
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', null=True)
    warning1 = CharField(db_column='Warning1', null=True)
    warning2 = CharField(db_column='Warning2', null=True)
    warning3 = CharField(db_column='Warning3', null=True)

    class Meta:
        db_table = 'prescription_line'

class PriceBand(BaseModel):
    band_finish = IntegerField(db_column='Band_finish', null=True)
    band_start = IntegerField(db_column='Band_start', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    each_or_flat = CharField(db_column='Each_or_flat', null=True)
    price = DecimalField(db_column='Price', null=True)
    price_band = PrimaryKeyField(db_column='Price_band_ID')
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'price_band'

class Procedure(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    force_weight_entry = IntegerField(db_column='Force_weight_entry')
    price_each = DecimalField(db_column='Price_each', null=True)
    procedure = PrimaryKeyField(db_column='Procedure_ID')
    procedure_ref = CharField(db_column='Procedure_ref', null=True, unique=True)
    procedure_text = CharField(db_column='Procedure_text', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    transaction_text = CharField(db_column='Transaction_text', null=True)
    vat_rate = CharField(db_column='VAT_Rate', null=True)

    class Meta:
        db_table = 'procedure'

class ProcedureCopy(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    force_weight_entry = IntegerField(db_column='Force_weight_entry')
    price_each = DecimalField(db_column='Price_each', null=True)
    procedure = PrimaryKeyField(db_column='Procedure_ID')
    procedure_ref = CharField(db_column='Procedure_ref', null=True, unique=True)
    procedure_text = CharField(db_column='Procedure_text', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    transaction_text = CharField(db_column='Transaction_text', null=True)
    vat_rate = CharField(db_column='VAT_Rate', null=True)

    class Meta:
        db_table = 'procedure_copy'

class Protocol(BaseModel):
    description = CharField(db_column='Description', null=True)
    protocol = PrimaryKeyField(db_column='Protocol_ID')

    class Meta:
        db_table = 'protocol'

class ProtocolQuestion(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    freehand_or_what = CharField(db_column='Freehand_or_what', null=True)
    macro = IntegerField(db_column='Macro_ID', null=True)
    preceding_or_surrounding_text = CharField(db_column='Preceding_or_surrounding_text', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    protocol = IntegerField(db_column='Protocol_ID', index=True, null=True)
    protocol_question = PrimaryKeyField(db_column='Protocol_question_ID')
    question_text = CharField(db_column='Question_text', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'protocol_question'

class RecallInstance(BaseModel):
    animal = ForeignKeyField(Animal, db_column='Animal_ID', index=True, null=True)
    client = ForeignKeyField(Client, db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    method = CharField(db_column='Method', null=True)
    recall_due_on = DateTimeField(db_column='Recall_due_on', index=True, null=True)
    recall_entered_on = DateTimeField(db_column='Recall_entered_on', index=True, null=True)
    recall_instance = PrimaryKeyField(db_column='Recall_instance_ID')
    recall_type = IntegerField(db_column='Recall_type_ID', null=True)
    remindercounter = DecimalField(db_column='ReminderCounter', null=True)
    remindercreated = DateTimeField(db_column='ReminderCreated', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'recall_instance'

class RecallInstanceCopy(BaseModel):
    animal = IntegerField(db_column='Animal_ID', index=True, null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    method = CharField(db_column='Method', null=True)
    recall_due_on = DateTimeField(db_column='Recall_due_on', index=True, null=True)
    recall_entered_on = DateTimeField(db_column='Recall_entered_on', index=True, null=True)
    recall_instance = PrimaryKeyField(db_column='Recall_instance_ID')
    recall_type = IntegerField(db_column='Recall_type_ID', null=True)
    remindercounter = DecimalField(db_column='ReminderCounter', null=True)
    remindercreated = DateTimeField(db_column='ReminderCreated', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'recall_instance_copy'

class RecallTrigger(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    recall_trigger = PrimaryKeyField(db_column='Recall_trigger')
    recall_type = IntegerField(db_column='Recall_type_ID', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'recall_trigger'

class RecallType(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    file_to_use_1st_reminder = CharField(db_column='File_to_use_1st_reminder', null=True)
    file_to_use_2nd_reminder = CharField(db_column='File_to_use_2nd_reminder', null=True)
    file_to_use_3rd_reminder = CharField(db_column='File_to_use_3rd_reminder', null=True)
    next_recall_type = IntegerField(db_column='Next_recall_type', null=True)
    recall_interval = IntegerField(db_column='Recall_interval', null=True)
    recall_text = CharField(db_column='Recall_text', index=True, null=True)
    recall_type = PrimaryKeyField(db_column='Recall_type_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'recall_type'

class Referringvet(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    referringpracticeid = IntegerField(db_column='ReferringPracticeID', index=True, null=True)
    referringvetid = PrimaryKeyField(db_column='ReferringVetID')
    ts = DateTimeField(db_column='TS', null=True)
    vetname = CharField(db_column='VetName', null=True)

    class Meta:
        db_table = 'referringvet'

class Reminderinstance(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    interval = IntegerField(db_column='Interval', index=True, null=True)
    mobilenumber = CharField(db_column='MobileNumber', null=True)
    reminderdueon = DateTimeField(db_column='ReminderDueOn', index=True, null=True)
    reminderformat = IntegerField(db_column='ReminderFormat', null=True)
    reminderinstanceid = PrimaryKeyField(db_column='ReminderInstanceID')
    remindertypeid = IntegerField(db_column='ReminderTypeID', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'reminderinstance'

class Remindertrigger(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    itemid = IntegerField(db_column='ItemID', null=True)
    remindertriggerid = PrimaryKeyField(db_column='ReminderTriggerID')
    remindertypeid = IntegerField(db_column='ReminderTypeID', null=True)
    stockorprocedure = CharField(db_column='StockorProcedure', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'remindertrigger'

class Remindertype(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    details = CharField(db_column='Details', null=True)
    export = IntegerField(db_column='Export', null=True)
    recallstoreplace = CharField(db_column='RecallsToReplace', null=True)
    remindertypeid = PrimaryKeyField(db_column='ReminderTypeID')
    ts = DateTimeField(db_column='TS', null=True)
    typetext = CharField(db_column='TypeText', null=True, unique=True)

    class Meta:
        db_table = 'remindertype'

class Savsnetpending(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    details = TextField(db_column='Details', null=True)
    savsnetpendingid = PrimaryKeyField(db_column='SAVSNETPendingID')
    ts = DateTimeField(db_column='TS')
    type = CharField(db_column='Type', index=True, null=True)
    userid = IntegerField(db_column='UserID', index=True, null=True)

    class Meta:
        db_table = 'savsnetpending'

class Savsnetsettings(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    postcode = CharField(db_column='PostCode', null=True)
    practiceid = CharField(db_column='PracticeID', null=True)
    savsnetsettingsid = PrimaryKeyField(db_column='SAVSNETSettingsID')
    sitelocation = CharField(db_column='SiteLocation', null=True, unique=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'savsnetsettings'

class Savsnetsurveylog(BaseModel):
    animalid = IntegerField(db_column='AnimalID', index=True, null=True)
    consultdate = DateTimeField(db_column='ConsultDate', index=True, null=True)
    consultguid = CharField(db_column='ConsultGUID', index=True, null=True)
    savsnetsurveylogid = PrimaryKeyField(db_column='SAVSNETSurveyLogID')
    ts = DateTimeField(db_column='TS')
    userid = IntegerField(db_column='UserID', index=True, null=True)

    class Meta:
        db_table = 'savsnetsurveylog'

class SeasonalVariations(BaseModel):
    drug_location = IntegerField(db_column='Drug_location_ID', index=True, null=True)
    season_begin = DateTimeField(db_column='Season_begin', null=True)
    season_end = DateTimeField(db_column='Season_end', null=True)
    seasonal_minimum = FloatField(db_column='Seasonal_minimum', null=True)
    seasonal_variations = PrimaryKeyField(db_column='Seasonal_variations_ID')
    stock = IntegerField(db_column='Stock_ID', index=True, null=True)

    class Meta:
        db_table = 'seasonal_variations'

class Slot(BaseModel):
    animal = IntegerField(db_column='Animal_ID', null=True)
    arrived_at = DateTimeField(db_column='Arrived_at', null=True)
    client = IntegerField(db_column='Client_ID', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    current_status = CharField(db_column='Current_status', index=True, null=True)
    instance_number = IntegerField(db_column='Instance_number', null=True)
    other_notes = CharField(db_column='Other_notes', null=True)
    page = IntegerField(db_column='Page_ID', null=True)
    reason = CharField(db_column='Reason', null=True)
    slot = PrimaryKeyField(db_column='Slot_ID')
    ts = DateTimeField(db_column='TS')
    time_label = DateTimeField(db_column='Time_label', index=True, null=True)
    vet_to_see = CharField(db_column='Vet_to_see', index=True, null=True)

    class Meta:
        db_table = 'slot'

class SmsLog(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    date = DateTimeField(db_column='Date', null=True)
    destination = CharField(db_column='Destination', null=True)
    from_ = CharField(db_column='From', null=True)
    message = CharField(db_column='Message', null=True)
    message_id = PrimaryKeyField(db_column='Message_ID')
    status = CharField(db_column='Status', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'sms_log'

class SpecialPriceGroupClients(BaseModel):
    client = IntegerField(db_column='Client_ID', null=True)
    special_price_group_clients = PrimaryKeyField(db_column='Special_price_group_clients_ID')
    special_price_groups = IntegerField(db_column='Special_price_groups_ID', null=True)

    class Meta:
        db_table = 'special_price_group_clients'

class SpecialPriceGroups(BaseModel):
    description = CharField(db_column='Description', null=True)
    special_price_groups = PrimaryKeyField(db_column='Special_price_groups_ID')

    class Meta:
        db_table = 'special_price_groups'

class SpecialPrices(BaseModel):
    allow_fees = IntegerField(db_column='Allow_fees', null=True)
    amount_1 = DecimalField(db_column='Amount_1', null=True)
    amount_2 = FloatField(db_column='Amount_2', null=True)
    behaviour = CharField(db_column='Behaviour', null=True)
    client = IntegerField(db_column='Client_ID', index=True, null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    expiry_date = DateTimeField(db_column='Expiry_date', null=True)
    special_price_group = IntegerField(db_column='Special_price_group', null=True)
    special_prices = PrimaryKeyField(db_column='Special_prices_ID')
    stock = IntegerField(db_column='Stock_ID', index=True, null=True)
    stock_or_procedure = CharField(db_column='Stock_or_procedure', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'special_prices'

class Species(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    idexxspeciesid = IntegerField(db_column='IdexxSpeciesID', null=True)
    species = PrimaryKeyField(db_column='Species_ID')
    species_text = CharField(db_column='Species_text', null=True, unique=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'species'

class Stableyard(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    stableyardaddress1 = CharField(db_column='StableyardAddress1', null=True)
    stableyardaddress2 = CharField(db_column='StableyardAddress2', null=True)
    stableyardaddress3 = CharField(db_column='StableyardAddress3', null=True)
    stableyardaddress4 = CharField(db_column='StableyardAddress4', null=True)
    stableyardhousename = CharField(db_column='StableyardHousename', null=True)
    stableyardhowtogetthere = CharField(db_column='StableyardHowToGetThere', null=True)
    stableyardid = PrimaryKeyField(db_column='StableyardID')
    stableyardinitials = CharField(db_column='StableyardInitials', null=True)
    stableyardpostcode = CharField(db_column='StableyardPostcode', null=True)
    stableyardpriceband = CharField(db_column='StableyardPriceBand', null=True)
    stableyardspare1 = CharField(db_column='StableyardSpare1', null=True)
    stableyardspare2 = CharField(db_column='StableyardSpare2', null=True)
    stableyardspare3 = CharField(db_column='StableyardSpare3', null=True)
    stableyardspare4 = CharField(db_column='StableyardSpare4', null=True)
    stableyardsurname = CharField(db_column='StableyardSurname', null=True)
    stableyardtitle = CharField(db_column='StableyardTitle', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'stableyard'

class Statementaddress(BaseModel):
    animalid = IntegerField(db_column='AnimalID', null=True)
    clientid = IntegerField(db_column='ClientID', index=True, null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    statementaddress1 = CharField(db_column='StatementAddress1', null=True)
    statementaddress2 = CharField(db_column='StatementAddress2', null=True)
    statementaddress3 = CharField(db_column='StatementAddress3', null=True)
    statementaddress4 = CharField(db_column='StatementAddress4', null=True)
    statementaddressid = PrimaryKeyField(db_column='StatementAddressID')
    statementhousename = CharField(db_column='StatementHousename', null=True)
    statementinitials = CharField(db_column='StatementInitials', null=True)
    statementpercentage = FloatField(db_column='StatementPercentage', null=True)
    statementpostcode = CharField(db_column='StatementPostcode', null=True)
    statementspare1 = CharField(db_column='StatementSpare1', null=True)
    statementspare2 = CharField(db_column='StatementSpare2', null=True)
    statementspare3 = CharField(db_column='StatementSpare3', null=True)
    statementspare4 = CharField(db_column='StatementSpare4', null=True)
    statementsurname = CharField(db_column='StatementSurname', null=True)
    statementtitle = CharField(db_column='StatementTitle', null=True)
    ts = DateTimeField(db_column='TS', null=True)

    class Meta:
        db_table = 'statementaddress'

class Stock(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', null=True)
    actual_rounded_price = DecimalField(db_column='Actual_rounded_price', null=True)
    alt_ordering_stock = IntegerField(db_column='Alt_Ordering_Stock_ID', null=True)
    bar_code = CharField(db_column='Bar_code', index=True, null=True)
    block_ordering = IntegerField(db_column='Block_Ordering')
    block_reason = CharField(db_column='Block_Reason', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    discount_from_net = FloatField(db_column='Discount_from_net', null=True)
    discount_to_selling = FloatField(db_column='Discount_to_selling', null=True)
    dosage_message = CharField(db_column='Dosage_message', null=True)
    drug_category = IntegerField(db_column='Drug_category', null=True)
    drug_data = CharField(db_column='Drug_data', null=True)
    label_text = CharField(db_column='Label_text', null=True)
    last_updated = DateTimeField(db_column='Last_updated', null=True)
    last_updated_initials = CharField(db_column='Last_updated_initials', null=True)
    manufacturer = IntegerField(db_column='Manufacturer_ID', null=True)
    markup_to_rrp = FloatField(db_column='Markup_to_RRP', null=True)
    markup_to_rrp_2 = FloatField(db_column='Markup_to_RRP_2', null=True)
    markup_to_rrp_3 = FloatField(db_column='Markup_to_RRP_3', null=True)
    net_net_specials_discount = FloatField(db_column='Net_net_Specials_Discount', null=True)
    net_net_suppliers_discount = FloatField(db_column='Net_net_Suppliers_Discount', null=True)
    net_net_price = FloatField(db_column='Net_net_price', null=True)
    pack_cost = DecimalField(db_column='Pack_cost', null=True)
    pack_cost_2 = DecimalField(db_column='Pack_cost_2', null=True)
    pack_cost_3 = DecimalField(db_column='Pack_cost_3', null=True)
    primary_supplier = IntegerField(db_column='Primary_Supplier', null=True)
    spx = IntegerField(db_column='SPX')
    season_begin_month = IntegerField(db_column='Season_begin_month', null=True)
    season_end_month = IntegerField(db_column='Season_end_month', null=True)
    stock = PrimaryKeyField(db_column='Stock_ID')
    stock_description = CharField(db_column='Stock_description', index=True, null=True)
    stock_reference = CharField(db_column='Stock_reference', null=True, unique=True)
    supplier = IntegerField(db_column='Supplier_ID', null=True)
    supplier_id_2 = IntegerField(db_column='Supplier_ID_2', null=True)
    supplier_id_3 = IntegerField(db_column='Supplier_ID_3', null=True)
    supplier_reference = CharField(db_column='Supplier_reference', index=True, null=True)
    supplier_reference_2 = CharField(db_column='Supplier_reference_2', index=True, null=True)
    supplier_reference_3 = CharField(db_column='Supplier_reference_3', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    transaction_text = CharField(db_column='Transaction_text', index=True, null=True)
    units_per_pack = CharField(db_column='Units_per_pack', null=True)
    update_prices = IntegerField(db_column='Update_Prices', null=True)
    use_net_net_pricing = IntegerField(db_column='Use_net_net_pricing')
    vat_rate = CharField(db_column='VAT_Rate', null=True)
    warning_message = CharField(db_column='Warning_message', null=True)

    class Meta:
        db_table = 'stock'

class StockCategory(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    stock_category = PrimaryKeyField(db_column='Stock_category')
    stock_category_abbreviation = CharField(db_column='Stock_category_abbreviation', index=True, null=True)
    stock_category_full_text = CharField(db_column='Stock_category_full_text', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'stock_category'

class StockCopy230217(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', null=True)
    actual_rounded_price = DecimalField(db_column='Actual_rounded_price', null=True)
    alt_ordering_stock = IntegerField(db_column='Alt_Ordering_Stock_ID', null=True)
    bar_code = CharField(db_column='Bar_code', index=True, null=True)
    block_ordering = IntegerField(db_column='Block_Ordering')
    block_reason = CharField(db_column='Block_Reason', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    discount_from_net = FloatField(db_column='Discount_from_net', null=True)
    discount_to_selling = FloatField(db_column='Discount_to_selling', null=True)
    dosage_message = CharField(db_column='Dosage_message', null=True)
    drug_category = IntegerField(db_column='Drug_category', null=True)
    drug_data = CharField(db_column='Drug_data', null=True)
    label_text = CharField(db_column='Label_text', null=True)
    last_updated = DateTimeField(db_column='Last_updated', null=True)
    last_updated_initials = CharField(db_column='Last_updated_initials', null=True)
    manufacturer = IntegerField(db_column='Manufacturer_ID', null=True)
    markup_to_rrp = FloatField(db_column='Markup_to_RRP', null=True)
    markup_to_rrp_2 = FloatField(db_column='Markup_to_RRP_2', null=True)
    markup_to_rrp_3 = FloatField(db_column='Markup_to_RRP_3', null=True)
    net_net_specials_discount = FloatField(db_column='Net_net_Specials_Discount', null=True)
    net_net_suppliers_discount = FloatField(db_column='Net_net_Suppliers_Discount', null=True)
    net_net_price = FloatField(db_column='Net_net_price', null=True)
    pack_cost = DecimalField(db_column='Pack_cost', null=True)
    pack_cost_2 = DecimalField(db_column='Pack_cost_2', null=True)
    pack_cost_3 = DecimalField(db_column='Pack_cost_3', null=True)
    primary_supplier = IntegerField(db_column='Primary_Supplier', null=True)
    spx = IntegerField(db_column='SPX')
    season_begin_month = IntegerField(db_column='Season_begin_month', null=True)
    season_end_month = IntegerField(db_column='Season_end_month', null=True)
    stock = PrimaryKeyField(db_column='Stock_ID')
    stock_description = CharField(db_column='Stock_description', index=True, null=True)
    stock_reference = CharField(db_column='Stock_reference', null=True, unique=True)
    supplier = IntegerField(db_column='Supplier_ID', null=True)
    supplier_id_2 = IntegerField(db_column='Supplier_ID_2', null=True)
    supplier_id_3 = IntegerField(db_column='Supplier_ID_3', null=True)
    supplier_reference = CharField(db_column='Supplier_reference', index=True, null=True)
    supplier_reference_2 = CharField(db_column='Supplier_reference_2', index=True, null=True)
    supplier_reference_3 = CharField(db_column='Supplier_reference_3', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    transaction_text = CharField(db_column='Transaction_text', index=True, null=True)
    units_per_pack = CharField(db_column='Units_per_pack', null=True)
    update_prices = IntegerField(db_column='Update_Prices', null=True)
    use_net_net_pricing = IntegerField(db_column='Use_net_net_pricing')
    vat_rate = CharField(db_column='VAT_Rate', null=True)
    warning_message = CharField(db_column='Warning_message', null=True)

    class Meta:
        db_table = 'stock_copy_23-02-17'

class StockHolding(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    drug_location = IntegerField(db_column='Drug_location_ID', index=True, null=True)
    reorder_multiple = IntegerField(db_column='Reorder_multiple', null=True)
    seasonal_minimum = IntegerField(db_column='Seasonal_minimum', null=True)
    stock = IntegerField(db_column='Stock_ID', index=True, null=True)
    stock_holding = PrimaryKeyField(db_column='Stock_holding_ID')
    stock_level = FloatField(db_column='Stock_level', null=True)
    stock_minimum = IntegerField(db_column='Stock_minimum', null=True)
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'stock_holding'

class StockOrders(BaseModel):
    arrived = IntegerField(db_column='Arrived', null=True)
    branch = IntegerField(db_column='Branch', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    on_order = IntegerField(db_column='On_order', null=True)
    order_date = DateTimeField(db_column='Order_date', null=True)
    order_number = IntegerField(db_column='Order_number_ID', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_order = PrimaryKeyField(db_column='Stock_order_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'stock_orders'

class StockPurchases(BaseModel):
    amount_paid = DecimalField(db_column='Amount_Paid', null=True)
    branch = IntegerField(db_column='Branch', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    invoice_number = CharField(db_column='Invoice_number', null=True)
    invoice_number_id = CharField(db_column='Invoice_number_ID', null=True)
    order_number = IntegerField(db_column='Order_number_ID', null=True)
    quantity = IntegerField(db_column='Quantity', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_or_substock = CharField(db_column='Stock_or_substock', null=True)
    stock_purchase = PrimaryKeyField(db_column='Stock_purchase_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'stock_purchases'

class StockRecall(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    recall_type = IntegerField(db_column='Recall_type_ID', null=True)
    stock = IntegerField(db_column='Stock_ID', index=True, null=True)
    stock_recall = PrimaryKeyField(db_column='Stock_recall_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'stock_recall'

class StockSubitem(BaseModel):
    add_flat_fee = IntegerField(db_column='Add_flat_fee')
    code = CharField(db_column='Code', null=True, unique=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    dispensing_fee = DecimalField(db_column='Dispensing_fee', null=True)
    multiply_divide_factor = FloatField(db_column='Multiply_divide_factor', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_subitem = PrimaryKeyField(db_column='Stock_subitem_ID')
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', index=True, null=True)
    unit_price = DecimalField(db_column='Unit_price', null=True)

    class Meta:
        db_table = 'stock_subitem'

class StockSubitem220217(BaseModel):
    add_flat_fee = IntegerField(db_column='Add_flat_fee')
    code = CharField(db_column='Code', null=True, unique=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    dispensing_fee = DecimalField(db_column='Dispensing_fee', null=True)
    multiply_divide_factor = FloatField(db_column='Multiply_divide_factor', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_subitem = PrimaryKeyField(db_column='Stock_subitem_ID')
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', index=True, null=True)
    unit_price = DecimalField(db_column='Unit_price', null=True)

    class Meta:
        db_table = 'stock_subitem_22-02-17'

class StockSubitemCopy230217(BaseModel):
    add_flat_fee = IntegerField(db_column='Add_flat_fee')
    code = CharField(db_column='Code', null=True, unique=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    dispensing_fee = DecimalField(db_column='Dispensing_fee', null=True)
    multiply_divide_factor = FloatField(db_column='Multiply_divide_factor', null=True)
    stock = IntegerField(db_column='Stock_ID', null=True)
    stock_subitem = PrimaryKeyField(db_column='Stock_subitem_ID')
    ts = DateTimeField(db_column='TS')
    text = CharField(db_column='Text', index=True, null=True)
    unit_price = DecimalField(db_column='Unit_price', null=True)

    class Meta:
        db_table = 'stock_subitem_copy_23-02-17'

class StockSubitemMarkup(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    markup_to_rrp = FloatField(db_column='Markup_to_RRP', null=True)
    stock = IntegerField(db_column='Stock_ID', index=True, null=True)
    stock_subitem = IntegerField(db_column='Stock_Subitem_ID', index=True, null=True)
    stock_subitem_markup = PrimaryKeyField(db_column='Stock_Subitem_Markup_ID')
    ts = DateTimeField(db_column='TS')

    class Meta:
        db_table = 'stock_subitem_markup'

class Stockactivesubstancelinks(BaseModel):
    activesubstanceid = IntegerField(db_column='ActiveSubstanceID', null=True)
    activesubstancelinkid = PrimaryKeyField(db_column='ActiveSubstanceLinkID')
    stockid = IntegerField(db_column='StockID', null=True)

    class Meta:
        db_table = 'stockactivesubstancelinks'

class Stockactivesubstances(BaseModel):
    activesubstanceid = PrimaryKeyField(db_column='ActiveSubstanceID')
    activesubstancename = CharField(db_column='ActiveSubstanceName', null=True)
    activesubstancenumber = CharField(db_column='ActiveSubstanceNumber', null=True)

    class Meta:
        db_table = 'stockactivesubstances'

class Supplier(BaseModel):
    address_1 = CharField(db_column='Address_1', null=True)
    address_2 = CharField(db_column='Address_2', null=True)
    address_3 = CharField(db_column='Address_3', null=True)
    address_4 = CharField(db_column='Address_4', null=True)
    billing_terms = CharField(db_column='Billing_terms', null=True)
    contact_name = CharField(db_column='Contact_Name', null=True)
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    delivery_charge = DecimalField(db_column='Delivery_Charge', null=True)
    email_address = CharField(db_column='Email_address', null=True)
    fax_number = CharField(db_column='Fax_number', null=True)
    house_number = CharField(db_column='House_Number', null=True)
    modem_number = CharField(db_column='Modem_number', null=True)
    notes = CharField(db_column='Notes', null=True)
    postcode = CharField(db_column='Postcode', null=True)
    supplier = PrimaryKeyField(db_column='Supplier_ID')
    supplier_name = CharField(db_column='Supplier_name', null=True)
    ts = DateTimeField(db_column='TS')
    telephone_number = CharField(db_column='Telephone_number', null=True)
    website_url = CharField(db_column='Website_URL', null=True)

    class Meta:
        db_table = 'supplier'

class Title(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    id = PrimaryKeyField(db_column='ID')
    ts = DateTimeField(db_column='TS')
    title = CharField(db_column='Title', null=True)

    class Meta:
        db_table = 'title'

class Transactions(BaseModel):
    accounts_category = IntegerField(db_column='Accounts_category_ID', index=True, null=True)
    amount_in_currency = DecimalField(db_column='Amount_in_currency', null=True)
    animal = ForeignKeyField(Animal, related_name='an_transactions', db_column='Animal_ID', index=True, null=True)
    client = ForeignKeyField(Client, related_name='cl_transactions', db_column='Client_ID', index=True, null=True)
    client_department = IntegerField(db_column='Client_department_ID', index=True, null=True)
    createdby = ForeignKeyField(Practitioner, related_name='trx_created', db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    currency_abbreviation = CharField(db_column='Currency_abbreviation', null=True)
    date_entered = DateTimeField(db_column='Date_entered', index=True, null=True)
    details = CharField(db_column='Details', index=True, null=True)
    entered_by = ForeignKeyField(Practitioner, related_name='trx_enterred', db_column='Entered_by', null=True)
    invoice_date = DateTimeField(db_column='Invoice_date', index=True, null=True)
    invoiced = IntegerField(db_column='Invoiced')
    multiplication = FloatField(db_column='Multiplication', null=True)
    net_value = DecimalField(db_column='Net_value', null=True)
    paid = IntegerField(db_column='Paid')
    procedure = ForeignKeyField(Procedure, db_column='Procedure_ID', null=True)
    stock = ForeignKeyField(Stock, db_column='Stock_ID', index=True, null=True)
    stock_or_procedure = CharField(db_column='Stock_or_Procedure', null=True)
    ts = DateTimeField(db_column='TS')
    time_entered = DateTimeField(db_column='Time_entered', null=True)
    transaction = PrimaryKeyField(db_column='Transaction_ID')
    vat_amount = DecimalField(db_column='VAT_amount', null=True)
    vat_percentage = FloatField(db_column='VAT_percentage', null=True)
    work_done_by = ForeignKeyField(Practitioner, related_name='trx_worked', db_column='Work_done_by', index=True, null=True)

    class Meta:
        db_table = 'transactions'

class Twins(BaseModel):
    primary_client = IntegerField(db_column='Primary_client_ID', index=True, null=True)
    secondary_client = IntegerField(db_column='Secondary_client_ID', index=True, null=True)
    twin = PrimaryKeyField(db_column='Twin_ID')

    class Meta:
        db_table = 'twins'

class Uitelworkentry(BaseModel):
    button = CharField(db_column='Button', null=True)
    buttonhash = CharField(db_column='ButtonHash', null=True)
    columnsizes = CharField(db_column='ColumnSizes', null=True)
    formsize = CharField(db_column='FormSize', null=True)
    maximised = IntegerField(db_column='Maximised', null=True)
    phpinfopanelsize = IntegerField(db_column='PHPinfoPanelSize', null=True)
    practitionerid = IntegerField(db_column='PractitionerID', null=True)
    sortonfiltertext = IntegerField(db_column='SortOnFilterText', null=True)
    uiid = PrimaryKeyField(db_column='UIid')
    workstation = CharField(db_column='Workstation', null=True)

    class Meta:
        db_table = 'uitelworkentry'
        indexes = (
            (('workstation', 'practitionerid', 'button'), True),
        )

class UserClass(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    default_channel = IntegerField(db_column='Default_channel', null=True)
    default_window_size = IntegerField(db_column='Default_window_size', null=True)
    ts = DateTimeField(db_column='TS')
    user_class = PrimaryKeyField(db_column='User_class_ID')
    user_class_name = CharField(db_column='User_class_name', null=True)

    class Meta:
        db_table = 'user_class'

class UserGroupMembers(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    practitioner = IntegerField(db_column='Practitioner_ID', index=True, null=True)
    ts = DateTimeField(db_column='TS')
    user_group = IntegerField(db_column='User_group_ID', index=True, null=True)
    user_group_members = PrimaryKeyField(db_column='User_group_members')

    class Meta:
        db_table = 'user_group_members'

class UserGroups(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    ts = DateTimeField(db_column='TS')
    user_group = PrimaryKeyField(db_column='User_group_ID')
    user_group_name = CharField(db_column='User_group_name', null=True, unique=True)

    class Meta:
        db_table = 'user_groups'

class VatRate(BaseModel):
    createdby = IntegerField(db_column='CreatedBy', null=True)
    createdon = DateTimeField(db_column='CreatedOn', null=True)
    percentage = FloatField(db_column='Percentage', null=True)
    rate_description = CharField(db_column='Rate_description', null=True)
    ts = DateTimeField(db_column='TS')
    vat_rate = CharField(db_column='VAT_Rate', primary_key=True)

    class Meta:
        db_table = 'vat_rate'

class Version(BaseModel):
    forbuild = CharField(db_column='ForBuild', null=True)
    lastchecked = DateTimeField(db_column='LastChecked', null=True)
    otherstuff = CharField(db_column='OtherStuff', null=True)
    versionid = PrimaryKeyField(db_column='VersionID')

    class Meta:
        db_table = 'version'

class Vetconnectsettings(BaseModel):
    accounttype = CharField(db_column='AccountType', null=True)
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    labaccountid = CharField(db_column='LabAccountID', null=True)
    password = CharField(db_column='Password', null=True)
    practicecountrycode = CharField(db_column='PracticeCountryCode', null=True)
    sitelocation = CharField(db_column='SiteLocation', index=True, null=True)
    ts = DateTimeField(db_column='TS', null=True)
    username = CharField(db_column='Username', null=True)
    vetconnectsettingsid = PrimaryKeyField(db_column='VetConnectSettingsID')

    class Meta:
        db_table = 'vetconnectsettings'

class Visiocareconsultsettings(BaseModel):
    datecreated = DateTimeField(db_column='DateCreated', null=True)
    password = CharField(db_column='Password', null=True)
    redirectpath = CharField(db_column='RedirectPath', null=True)
    ts = DateTimeField(db_column='TS', null=True)
    username = CharField(db_column='Username', null=True)
    visiocareconsultsettingsid = PrimaryKeyField(db_column='VisioCareConsultSettingsID')
    workstation = CharField(db_column='Workstation', unique=True)

    class Meta:
        db_table = 'visiocareconsultsettings'

class VisitSheet(BaseModel):
    visit_sheet = PrimaryKeyField(db_column='Visit_sheet_ID')
    visit_sheet_description = CharField(db_column='Visit_sheet_description', null=True)

    class Meta:
        db_table = 'visit_sheet'

class VisitSheetEntry(BaseModel):
    procedure = IntegerField(db_column='Procedure_ID', null=True)
    visit_sheet = IntegerField(db_column='Visit_sheet_ID', null=True)
    visit_sheet_entry = PrimaryKeyField(db_column='Visit_sheet_entry_ID')

    class Meta:
        db_table = 'visit_sheet_entry'


DeferredClient.set_model(Client)




