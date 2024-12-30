from django.contrib import admin
from testapp.models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from usermanagementapp.models import *




# Register your models here.
# class DoctorTableAdmin(admin.ModelAdmin):
#     list_display=['doctor_id']
# admin.site.register(DoctorTable,DoctorTableAdmin)

class HospitalMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'hospital_name', 'status']
admin.site.register(HospitalMaster, HospitalMasterAdmin)


class BranchMasterAdminResource(resources.ModelResource):
    class Meta:
        model = BranchMaster
        import_id_fields = ['branch_id']
class BranchMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['group_id', 'branch_name']
    resource_class = BranchMasterAdminResource
admin.site.register(BranchMaster, BranchMasterAdmin)


class GroupMasterAdminResource(resources.ModelResource):
    class Meta:
        model = GroupMaster
        import_id_fields = ['group_id']


class GroupMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['group_id', 'group_name']
    resource_class = GroupMasterAdminResource


admin.site.register(GroupMaster, GroupMasterAdmin)


class TitleMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', ]


admin.site.register(TitleMaster, TitleMasterAdmin)

class HolidayMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', ]
admin.site.register(HolidayMaster, HolidayMasterAdmin)

class DoctorScheduleTableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id','select_doctor']
admin.site.register(DoctorScheduleTable, DoctorScheduleTableAdmin)

class GenderMaterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id','Gender']
admin.site.register(GenderMater, GenderMaterAdmin)

class DistrictMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id','district']
admin.site.register(DistrictMaster, DistrictMasterAdmin)

class CountryMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','country']
admin.site.register(CountryMaster, CountryMasterAdmin)

class CityMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','city']
admin.site.register(CityMaster, CityMasterAdmin)

class MostCommonDocumentTypeMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','document_type']
admin.site.register(MostCommonDocumentTypeMaster, MostCommonDocumentTypeMasterAdmin)

class MaritalStatusMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','marital_status']
admin.site.register(MaritalStatusMaster, MaritalStatusMasterAdmin)

class RelationMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','relation_name']
admin.site.register(RelationMaster, RelationMasterAdmin)

# Service Master===========
class ServiceCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','service_category']
admin.site.register(ServiceCategory, ServiceCategoryAdmin)

class ServiceSubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','service_sub_category']
admin.site.register(ServiceSubCategory,ServiceSubCategoryAdmin)
class ServiceDepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','service_department']
admin.site.register(ServiceDepartment, ServiceDepartmentAdmin)

class ServiceSubDepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','service_sub_department']
admin.site.register(ServiceSubDepartment,ServiceSubDepartmentAdmin)

class ServiceMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','service_name','Charges','service_department']
admin.site.register(ServiceMaster,ServiceMasterAdmin)

class TariffMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','tariff_name']
admin.site.register(TariffMaster,TariffMasterAdmin)

class DesignationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','designation']
admin.site.register(Designation,DesignationAdmin)

class CorporateMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','corporate_Name']
admin.site.register(CorporateMaster,CorporateMasterAdmin)

class BillingGroupAdminResource(resources.ModelResource):
    class Meta:
        model = BillingGroup
        import_id_fields = ['billing_group_id']
class BillingGroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['billing_group_id', 'billing_group']
    resource_class = BillingGroupAdminResource
admin.site.register(BillingGroup, BillingGroupAdmin)

class WardTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','type']
admin.site.register(WardType,WardTypeAdmin)
class WardCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','category']
admin.site.register(WardCategory,WardCategoryAdmin)
class TariffChargeMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','tariff']
admin.site.register(TariffChargeMaster,TariffChargeMasterAdmin)

class BillingGroupTariffLinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','Tariff','Billing_Group_Name']
admin.site.register(BillingGroupTariffLink,BillingGroupTariffLinkAdmin)

class BillingGroupCorporateMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','Corporate_Name','Biiling_Group']
admin.site.register(BillingGroupCorporateMaster,BillingGroupCorporateMasterAdmin)


class DoctorTableAdminResource(resources.ModelResource):
    class Meta:
        model = DoctorTable
        import_id_fields = ['doctor_name']
class DoctorTableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['doctor_id', 'doctor_name']
    resource_class = DoctorTableAdminResource
admin.site.register(DoctorTable, DoctorTableAdmin)

class PatientsRegistrationsAllInOneAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['id', 'location']
admin.site.register(PatientsRegistrationsAllInOne, PatientsRegistrationsAllInOneAdmin)

class OpdBillingTemperAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['uhid', 'visit_no','service_name','rate']
admin.site.register(OpdBillingTemper, OpdBillingTemperAdmin)

class OpdBillingMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this code is for our own primary key
    '''
    list_display = ['uhid','visit_no','bill_no','bill_date_time','lou_no','claim_no','claim_status','checklist_status','department','doctor_name']
admin.site.register(OpdBillingMain, OpdBillingMainAdmin)

admin.site.register(RoomNumber)
admin.site.register(TokenMasterConf)
# class OpdBillingTemp(models.Model):
#     list_display = ['extra_fields']
admin.site.register(OpdBillingTemp)
# admin.site.register(LabResultEntry)
admin.site.register(CreateUser)

class LabResultEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['test_id','profile_name','service_name','profile_id']
admin.site.register(LabResultEntry, LabResultEntryAdmin)

class Service_TestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['test_name']
admin.site.register(Service_Test, Service_TestAdmin)

class ServiceTest_recordsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['test_name']
admin.site.register(ServiceTest_records, ServiceTest_recordsAdmin)

class ServiceTestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['test_name']
admin.site.register(ServiceTest, ServiceTestAdmin)

class VendorMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['vendor_name','created_at','updated_at']
admin.site.register(VendorMaster, VendorMasterAdmin)


class Validation_recordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'PTID','uhid']
admin.site.register(Validation_record, Validation_recordAdmin)

class SampleCollectedAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'PTID','uhid','profile_name','outsource']
admin.site.register(SampleCollected, SampleCollectedAdmin)

class Inventory_ItemMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','item_name']
admin.site.register(Inventory_ItemMaster, Inventory_ItemMasterAdmin)

class Refered_by_MasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['Staff_name']
admin.site.register(Refered_by_Master, Refered_by_MasterAdmin)

class ItemCategoryMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_category']
admin.site.register(ItemCategoryMaster, ItemCategoryMasterAdmin)

class ItemsubcategoryMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['itemsubcategory']
admin.site.register(ItemsubcategoryMaster, ItemsubcategoryMasterAdmin)

class ItemUnitMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['unit']
admin.site.register(ItemUnitMaster, ItemUnitMasterAdmin)

class PackagigMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_packing']
admin.site.register(PackagigMaster, PackagigMasterAdmin)

class ProfileServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['profile_id','profile_name']
admin.site.register(ProfileService, ProfileServiceAdmin)

class PurchaseOrder_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['PO_id']
admin.site.register(PurchaseOrder_Parent, PurchaseOrder_ParentAdmin)

class PurchaseOrder_TempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_ID']
admin.site.register(PurchaseOrder_Temp, PurchaseOrder_TempAdmin)

class PurchaseOrder_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['PO_Id','item_id']
admin.site.register(PurchaseOrder_Child, PurchaseOrder_ChildAdmin)

class StockEntry_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['GRN_id']
admin.site.register(StockEntry_Parent, StockEntry_ParentAdmin)

class StockEntry_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['GRN_id']
admin.site.register(StockEntry_Child, StockEntry_ChildAdmin)

class Stock_BatchWiseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['GRN_id']
admin.site.register(Stock_BatchWise, Stock_BatchWiseAdmin)

class Vendor_PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['vendor_payment_no']
admin.site.register(Vendor_Payment, Vendor_PaymentAdmin)

class Material_Intent_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['intent_id']
admin.site.register(Material_Intent_Parent, Material_Intent_ParentAdmin)

class Material_Intent_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['intent_id']
admin.site.register(Material_Intent_Child, Material_Intent_ChildAdmin)

class Item_Issue_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_issue_no']
admin.site.register(Item_Issue_Parent, Item_Issue_ParentAdmin)

class Item_Issue_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_issue_no']
admin.site.register(Item_Issue_Child, Item_Issue_ChildAdmin)

class Item_Return_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_return_no']
admin.site.register(Item_Return_Parent, Item_Return_ParentAdmin)

class Item_return_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_return_no']
admin.site.register(Item_return_Child, Item_return_ChildAdmin)

class Item_Return_Supplier_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['supplier_return_no']
admin.site.register(Item_Return_Supplier_Parent, Item_Return_Supplier_ParentAdmin)

class Item_Return_Supplier_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['supplier_return_no']
admin.site.register(Item_Return_Supplier_Child, Item_Return_Supplier_ChildAdmin)

class Purchase_Intent_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['intent_id']
admin.site.register(Purchase_Intent_Parent, Purchase_Intent_ParentAdmin)

class Stock_BatchWise_MainstoreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_issue_no','item_id']
admin.site.register(Stock_BatchWise_Mainstore, Stock_BatchWise_MainstoreAdmin)

class Stock_BatchWise_SubstoreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_issue_no','item_id']
admin.site.register(Stock_BatchWise_Substore, Stock_BatchWise_SubstoreAdmin)

class Item_Issue_ToSubStore_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_issue_no']
admin.site.register(Item_Issue_ToSubStore_Parent, Item_Issue_ToSubStore_ParentAdmin)

class Item_Issue_ToSubStore_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_issue_no']
admin.site.register(Item_Issue_ToSubStore_Child, Item_Issue_ToSubStore_ChildAdmin)

class Item_Return_ToCPC_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['return_no']
admin.site.register(Item_Return_ToCPC_Child, Item_Return_ToCPC_ChildAdmin)

class MakeItem_return_ToCPC_TempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_id']
admin.site.register(MakeItem_return_ToCPC_Temp, MakeItem_return_ToCPC_TempAdmin)

class ProfileMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','profile_name','profile_amount']
admin.site.register(ProfileMaster, ProfileMasterAdmin)


class PatientVisitMainsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid','visit_id', 'visit_type','location']
admin.site.register(PatientVisitMains, PatientVisitMainsAdmin)

# class ProfileChargeMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ['profile_id','profile_charge', 'tariff_id','ipd_opd']
# admin.site.register(ProfileChargeMaster, ProfileChargeMasterAdmin)

# class ServiceChargeMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ['id','service_id','ward_category','service_category','service_charge', 'tariff_id','ipd_opd']
# admin.site.register(ServiceChargeMaster, ServiceChargeMasterAdmin)

class CreditAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['bill_no', 'uhid','visit_no']
admin.site.register(Credit, CreditAdmin)

class Insurance_Checklist_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_no']
admin.site.register(Insurance_Checklist_Parent, Insurance_Checklist_ParentAdmin)

class Insurance_Checklist_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['checklist_no']
admin.site.register(Insurance_Checklist_Child, Insurance_Checklist_ChildAdmin)

class OpdPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid','visit_id','bill_id','mode_type']
admin.site.register(OpdPayment, OpdPaymentAdmin)

class OpdBillingSubAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid','visit_no','bill_no','unit','service_id']
admin.site.register(OpdBillingSub, OpdBillingSubAdmin)

class PS_CounterSale_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','uhid','visit_id']
admin.site.register(PS_CounterSale_Parent,PS_CounterSale_ParentAdmin)

class PS_CounterSale_childAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_id']
admin.site.register(PS_CounterSale_child,PS_CounterSale_childAdmin)

class PS_sales_return_ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','sales_return_id','item_id']
admin.site.register(PS_sales_return_Child,PS_sales_return_ChildAdmin)

class PS_sales_return_ParentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','sales_no','sales_return_id']
admin.site.register(PS_sales_return_Parent,PS_sales_return_ParentAdmin)

class Department_ConsumptionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_id','consumption_No']
admin.site.register(Department_Consumption,Department_ConsumptionAdmin)

class PS_CounterSale_TempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_id']
admin.site.register(PS_CounterSale_Temp,PS_CounterSale_TempAdmin)

class Generic_MasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['generic_name']
admin.site.register(Generic_Master,Generic_MasterAdmin)

class Estimate_bill_subAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','uhid','name','billing_group']
admin.site.register(Estimate_bill_sub,Estimate_bill_subAdmin)

class Temp_AccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','uhid','visit_id']
admin.site.register(Temp_Access,Temp_AccessAdmin)

class Permanent_AccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','uhid','visit_id']
admin.site.register(Permanent_Access,Permanent_AccessAdmin)

class MakeItem_return_TempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['item_id']
admin.site.register(MakeItem_return_Temp,MakeItem_return_TempAdmin)

class PS_Sales_Payement_DetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['sale_date','op_sale_no']
admin.site.register(PS_Sales_Payement_Detail,PS_Sales_Payement_DetailAdmin)

class StoreMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','store_name']
admin.site.register(StoreMaster,StoreMasterAdmin)

#-===================== 05\06\2023 ============================
class OpdPackageService_tempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','service_name']
admin.site.register(OpdPackageService_temp,OpdPackageService_tempAdmin)

class OpdPackageServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','package_name','service_name','profile_name']
admin.site.register(OpdPackageService,OpdPackageServiceAdmin)

class OpdPackageService_mainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id']
admin.site.register(OpdPackageService_main,OpdPackageService_mainAdmin)

# class PackageChargeMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ['id','tariff_id','package_id','package_charge','ward_type','ward_category']
# admin.site.register(PackageChargeMaster,PackageChargeMasterAdmin)

class PostEquip_preparationMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','post_equip_name','description']
admin.site.register(PostEquip_preparationMaster,PostEquip_preparationMasterAdmin)

admin.site.register(ScreenAccess)

class OpdPackageMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','package_name','package_amount']
admin.site.register(OpdPackageMaster,OpdPackageMasterAdmin)

class PendingInvestigation_mainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','PTID','test_id','uhid','visit_no','bill_no','profile_name','date_time','department','sub_department']
admin.site.register(PendingInvestigation_main,PendingInvestigation_mainAdmin)

class SampleCollectionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'PTID','test_id','lab_service_name']
admin.site.register(SampleCollection, SampleCollectionAdmin)
class Investigation_mainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uhid','admission_ID','investigation_id','service_name']

class BedChargeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'ward_type','ward_cat','bed_no','bed_charge']
admin.site.register(BedCharge, BedChargeAdmin)

class DialysisScheduleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'schedule_id','uhid','department','sub_dept','shifting_date','shift_id']
admin.site.register(DialysisSchedule, DialysisScheduleAdmin)

# Clinical Management
#=================== For Clinical Management 24/08/2023 =========================
class VitalSignAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uhid','bill_id','visit_id','bmi']
admin.site.register(VitalSign, VitalSignAdmin)

class PreMedicineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid','visit_id','bill_id','medicine','dosage']
admin.site.register(PreMedicine,PreMedicineAdmin)

class DiagnosisMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'diagnosis_id','diagnosis_name','icd_10_code','icd_11_code']
admin.site.register(DiagnosisMaster,DiagnosisMasterAdmin)

class HistoryAndExaminationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uhid','bill_id','visit_id',]
admin.site.register(HistoryAndExamination,HistoryAndExaminationAdmin)

class InvestigationProcedureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id','investigation_and_procedure']
admin.site.register(InvestigationProcedure, InvestigationProcedureAdmin)

class AdviceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(Advice, AdviceAdmin)

class PresentingComplaintAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(PresentingComplaint, PresentingComplaintAdmin)

class DiagnosisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(Diagnosis, DiagnosisAdmin)

class PresentingComplaintTempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(PresentingComplaintTemp, PresentingComplaintTempAdmin)

class PresentingComplaintSubAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(PresentingComplaintSub, PresentingComplaintSubAdmin)

class DiagnosisTempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(DiagnosisTemp, DiagnosisTempAdmin)

class DiagnosisSubAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(DiagnosisSub, DiagnosisSubAdmin)

class InvestigationProcedureTempAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(InvestigationProcedureTemp,InvestigationProcedureTempAdmin)

class InvestigationProcedureSubAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'bill_id','visit_id',]
admin.site.register(InvestigationProcedureSub,InvestigationProcedureSubAdmin)

class MedicalCertificatesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['mc_templates', 'authorize_dr','finalized',]
admin.site.register(MedicalCertificates,MedicalCertificatesAdmin)
#=========================== END Clinical Management ==============================

class BookedAppointmentsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['admin', 'patient_id','first_name','patient_appointment_date','patient_appointment_id']
admin.site.register(BookedAppointments,BookedAppointmentsAdmin)

#======================== Nephrology 24/08/2023 ==========================
class PrescriptionDialysisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','uhid','visit_id']
admin.site.register(PrescriptionDialysis,PrescriptionDialysisAdmin)

class PreDialysisAssessmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(PreDialysisAssessment,PreDialysisAssessmentAdmin)

class PreEquipPreparationPreDialysisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(PreEquipPreparationPreDialysis,PreEquipPreparationPreDialysisAdmin)

class Pre_Dialysis_DetailsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(Pre_Dialysis_Details,Pre_Dialysis_DetailsAdmin)

class AddDrugs_DialysisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(AddDrugs_Dialysis,AddDrugs_DialysisAdmin)

class Post_Dialysis_DetailsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(Post_Dialysis_Details,Post_Dialysis_DetailsAdmin)

class IntraDialysisPerHourInputAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(IntraDialysisPerHourInput,IntraDialysisPerHourInputAdmin)

class IntraDialysisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(IntraDialysis,IntraDialysisAdmin)

class PostEquip_preparationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(PostEquip_preparation,PostEquip_preparationAdmin)

class SessionNoteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(SessionNote,SessionNoteAdmin)

class Chemotherapy_treatment_sheetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'patient_name',]
admin.site.register(Chemotherapy_treatment_sheet,Chemotherapy_treatment_sheetAdmin)

class PostDialysisDischargeSheetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['uhid', 'visit_id',]
admin.site.register(PostDialysisDischargeSheet,PostDialysisDischargeSheetAdmin)
class LabResultEntry_recordsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['PTID', 'test_id',]
admin.site.register(LabResultEntry_records,LabResultEntry_recordsAdmin)

class PatientRegistrationMainsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uhid',]
admin.site.register(PatientRegistrationMains,PatientRegistrationMainsAdmin)

class PatientRegistrationSubAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uhid',]
admin.site.register(PatientRegistrationSub,PatientRegistrationSubAdmin)

class PatientBillingInfosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uhid',]
admin.site.register(PatientBillingInfos,PatientBillingInfosAdmin)



class AvailabilityIntradayScheduleMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','doctor_id','time_slot_id']
admin.site.register(AvailabilityIntradayScheduleMaster,AvailabilityIntradayScheduleMasterAdmin)

class CentralisedAdminViewAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','Token_Issued']
admin.site.register(CentralisedAdminView,CentralisedAdminViewAdmin)

class OPDBillDiscountRemarkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['authorised_by','bill_no','remark','created_at','created_by']
admin.site.register(OPDBillDiscountRemark,OPDBillDiscountRemarkAdmin)

class CancelBillRemarkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['bill_no','reason','created_by','location']
admin.site.register(CancelBillRemark, CancelBillRemarkAdmin)
class AuthorizedPersonAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['auth_name','department']
admin.site.register(AuthorizedPerson, AuthorizedPersonAdmin)