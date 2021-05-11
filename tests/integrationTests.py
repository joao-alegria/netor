import pytest
from selenium import webdriver
import time
import os

@pytest.fixture()
def driver():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    broswer = webdriver.Firefox(options=fireFoxOptions, executable_path="tests/geckodriver")
    yield broswer
    broswer.close()

@pytest.fixture
def admin(driver):
    driver.get('http://localhost:4200/login')
    driver.find_element_by_id('inputUsername').send_keys("admin")
    driver.find_element_by_id('inputPassword').send_keys("admin")
    driver.find_element_by_id('submitLogin').click()
    assert driver.find_element_by_id('welcomeUser').text == "Welcome Back,\nadmin"

@pytest.fixture
def user(driver):
    driver.get('http://localhost:4200/login')
    driver.find_element_by_id('inputUsername').send_keys("user")
    driver.find_element_by_id('inputPassword').send_keys("user")
    driver.find_element_by_id('submitLogin').click()
    assert driver.find_element_by_id('welcomeUser').text == "Welcome Back,\nuser"

def test_getDefaultGroups(driver, admin):
    driver.find_element_by_id('adminTenantTab').click()
    elements=driver.find_elements_by_tag_name('h3')
    assert len(elements)==2
    assert elements[0].text=="Group: admin"
    assert elements[1].text=="Group: user"

def test_createNewGroup(driver, admin):
    driver.find_element_by_id('adminTenantTab').click()
    driver.find_element_by_id('CreateGroup').click()
    driver.find_element_by_id('groupName').send_keys("seleniumTest")
    driver.find_element_by_id('confirmCreateNewGroup').click()
    elements=driver.find_elements_by_tag_name('h3')
    assert len(elements)==3
    assert elements[2].text=="Group: seleniumTest"

def test_deleteExistingGroup(driver, admin):
    driver.find_element_by_id('adminTenantTab').click()
    elements=driver.find_elements_by_tag_name('h3')
    assert len(elements)==3
    assert elements[2].text=="Group: seleniumTest"
    driver.find_element_by_id('seleniumTest').click()
    driver.find_element_by_id('deleteGroup').click()
    time.sleep(2)
    driver.find_element_by_id('confirmAction').click()
    elements=driver.find_elements_by_tag_name('h3')
    assert len(elements)==2

def test_getDefaultTenants(driver, admin):
    driver.find_element_by_id('adminTenantTab').click()
    adminGroup=driver.find_element_by_id('admin')
    adminTenants=adminGroup.find_elements_by_class_name("groupName")
    assert len(adminTenants)==1
    assert adminTenants[0].text=="admin"
    userGroup=driver.find_element_by_id('user')
    userTenants=userGroup.find_elements_by_class_name("groupName")
    assert len(userTenants)==1
    assert userTenants[0].text=="user"

def test_createNewTenant(driver, admin):
    driver.find_element_by_id('adminTenantTab').click()
    driver.find_element_by_id('user').click()
    driver.find_element_by_id('addTenant').click()  
    driver.find_element_by_id('inputUsername').send_keys("testUser")
    driver.find_element_by_id('inputPassword').send_keys("testUser")
    driver.find_element_by_id('inputPasswordConfirm').send_keys("testUser")
    driver.find_element_by_id('submitNewTenant').click()
    userGroup=driver.find_element_by_id('user')
    tenants=userGroup.find_elements_by_class_name("groupName")
    assert len(tenants)==2
    assert tenants[1].text=="testUser"

def test_deleteExistingTenant(driver, admin):
    driver.find_element_by_id('adminTenantTab').click()
    userGroup=driver.find_element_by_id('user')
    tenants=userGroup.find_elements_by_class_name("groupName")
    assert len(tenants)==2
    assert tenants[1].text=="testUser"
    tenants[1].click()
    driver.find_element_by_id('deleteTenant').click()

def test_getPreloadedDDomain(driver, admin):
    driver.find_element_by_id('adminDomainTab').click()
    elements=driver.find_elements_by_class_name('DOMAIN')
    assert len(elements)==1
    titles=driver.find_elements_by_tag_name('h3')
    assert len(titles)==1
    assert titles[0].text=="ITAV"

def test_createNewDDomain(driver, admin):
    driver.find_element_by_id('adminDomainTab').click()
    driver.find_element_by_id('OnboardDomain').click()
    driver.find_element_by_id('domainId').send_keys("testDomain")
    driver.find_element_by_id('domainName').send_keys("testDomain")
    driver.find_element_by_id('domainDescription').send_keys("testDomain")
    driver.find_element_by_id('domainAdmin').send_keys("testAdmin")
    driver.find_element_by_id('domainStatus').send_keys("ACTIVE")
    driver.find_element_by_id('domainInterUrl').send_keys("localhost")
    driver.find_element_by_id('domainInterPort').send_keys("1234")

    driver.find_element_by_id('domainLayerId0').send_keys("OSM")
    driver.find_element_by_id('domainLayerDriverType0').send_keys("OSM_NFVO")
    driver.find_element_by_id('domainLayerOsmNfvoUsername0').send_keys("admin")
    driver.find_element_by_id('domainLayerOsmNfvoPassword0').send_keys("admin")
    driver.find_element_by_id('domainLayerOsmNfvoProject0').send_keys("admin")

    driver.find_element_by_id('onboardNst').click()

    elements=driver.find_elements_by_class_name('DOMAIN')
    assert len(elements)==2
    titles=driver.find_elements_by_tag_name('h3')
    assert len(titles)==2
    assert titles[1].text=="testDomain"

def test_deleteExistingDDomain(driver, admin):
    driver.find_element_by_id('adminDomainTab').click()
    elements=driver.find_elements_by_class_name('DOMAIN')
    assert len(elements)==2
    titles=driver.find_elements_by_tag_name('h3')
    assert len(titles)==2
    assert titles[1].text=="testDomain"
    elements[1].click()
    driver.find_element_by_id('deleteDomain').click()
    driver.find_element_by_id('confirmAction').click()

    elements=driver.find_elements_by_class_name('DOMAIN')
    assert len(elements)==1
    titles=driver.find_elements_by_tag_name('h3')
    assert len(titles)==1
    assert titles[0].text=="ITAV"

def test_createNewBlueprint(driver, admin):
    driver.find_element_by_id('adminBlueprintTab').click()
    driver.find_element_by_id('onboardNewVSB').click()
    driver.find_element_by_id("vsbDrop").send_keys(os.path.abspath("tests/entities/vsb.json"))
    driver.find_element_by_id("nstDrop").send_keys(os.path.abspath("tests/entities/nstExternalNSST.json"))
    driver.find_element_by_id("ruleNstId0").send_keys("interdomain_e2e_nstNST")
    driver.find_element_by_id("ruleNSDid0").send_keys("interdomain_slice_nsd")
    driver.find_element_by_id("ruleNSDversion0").send_keys("1.0")
    driver.find_element_by_id("ruleNSflavourid0").send_keys("interdomain_df")
    driver.find_element_by_id("ruleinstlevelid0").send_keys("intedomain_il")

    driver.find_element_by_id("ruleparamid0_0").send_keys("peers")
    driver.find_element_by_id("ruleparammin0_0").send_keys("1")
    driver.find_element_by_id("ruleparammax0_0").send_keys("10")

    driver.find_element_by_id("onboardVsb").click()
    elements=driver.find_elements_by_class_name('VSB')
    assert len(elements)==1

def test_createNewDescriptor(driver, user):
    driver.find_element_by_id('tenantBlueprintTab').click()
    elements=driver.find_elements_by_class_name('VSB')
    elements[0].click()
    driver.find_element_by_id("createDescriptor").click()
    driver.find_element_by_id("name").send_keys("seleniumVsdTest")  
    driver.find_element_by_id("version").send_keys("1.0")
    driver.find_element_by_id("sliceServiceType").send_keys("EMBB")
    driver.find_element_by_id("isPublic").click()
    driver.find_element_by_id("Peers").send_keys("5")
    driver.find_element_by_id("sliceServiceDomain").send_keys("ITAV")
    driver.find_element_by_id("sliceType").send_keys("EMBB")
    driver.find_element_by_id("priority").send_keys("MEDIUM")
    driver.find_element_by_id("submitNewDescriptor").click()
    driver.find_element_by_id('tenantDescriptorTab').click()
    elements=driver.find_elements_by_class_name('VSD')
    assert len(elements)==1

def test_createNewVSI(driver, user):
    driver.find_element_by_id('tenantDescriptorTab').click()
    elements=driver.find_elements_by_class_name('VSD')
    assert len(elements)==1
    elements[0].click()
    driver.find_element_by_id('instantiateVSI').click()
    driver.find_element_by_id('vsiId').send_keys("portalTest")
    driver.find_element_by_id('name').send_keys("portalTest")
    driver.find_element_by_id('description').send_keys("portalTest")
    driver.find_element_by_id('domainId').send_keys("ITAV")
    driver.find_element_by_id('submitNewVS').click()

    driver.find_element_by_id('tenantVsiTab').click()
    elements=driver.find_elements_by_class_name('VSI')
    assert len(elements)==1

def test_deleteExistingVSI(driver, user):
    driver.find_element_by_id('tenantVsiTab').click()
    elements=driver.find_elements_by_class_name('VSI')
    assert len(elements)==1
    elements[0].click()
    driver.find_element_by_id('removeVSI').click()
    driver.find_element_by_id('confirmAction').click()
    elements=driver.find_elements_by_class_name('VSI')
    assert len(elements)==0

def test_deleteExistingDescriptor(driver, user):
    driver.find_element_by_id('tenantDescriptorTab').click()
    elements=driver.find_elements_by_class_name('VSD')
    assert len(elements)==1
    elements[0].click()
    driver.find_element_by_id("deleteVSD").click()
    driver.find_element_by_id('confirmAction').click()
    elements=driver.find_elements_by_class_name('VSD')
    assert len(elements)==0

def test_deleteExistingBlueprint(driver, admin):
    driver.find_element_by_id('adminBlueprintTab').click()
    elements=driver.find_elements_by_class_name('VSB')
    assert len(elements)==1
    elements[0].click()
    driver.find_element_by_id("deleteVSB").click()
    driver.find_element_by_id('confirmAction').click()
    elements=driver.find_elements_by_class_name('VSB')
    assert len(elements)==0

def test_deleteExistingNST(driver, admin):
    driver.find_element_by_id('adminTemplateTab').click()
    elements=driver.find_elements_by_class_name('NST')
    assert len(elements)==1
    elements[0].click()
    driver.find_element_by_id("deleteNST").click()
    driver.find_element_by_id('confirmAction').click()
    elements=driver.find_elements_by_class_name('NST')
    assert len(elements)==0