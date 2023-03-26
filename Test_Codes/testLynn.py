from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from Test_Data.data import Login_Data
from Test_Locators.locators import Login_Locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pytest

class Test_Lynn:

    # booting function for running the pytest testcases
    @pytest.fixture

    def boot(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        wait = WebDriverWait(self.driver, 10)
        yield
        #self.driver.close()

    def test_login(self, boot):
        self.driver.implicitly_wait(5)
        self.driver.get(Login_Data().url)
        self.driver.maximize_window()
        self.driver.find_element(by=By.NAME, value=Login_Locators().username_locator).send_keys(Login_Data().username)
        self.driver.find_element(by=By.NAME, value=Login_Locators().password_locator).send_keys(Login_Data().password)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().submit_locator).click()
        assert self.driver.title =='OrangeHRM'
        print("LOGIN SUCCESS : Logged in with the Username {a} & {b}".format(a=Login_Data().username, b=Login_Data().password))

    def test_search_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        search_flag = self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator_home_page)
        if(search_flag.is_displayed()):
            print("Search TextBox is displayed on Homepage")
        else:
            print("Search TextBox is not present")
        options_list = self.driver.find_elements(by=By.CSS_SELECTOR, value='li.oxd-main-menu-item-wrapper')
        if (len(options_list) != 0):
            print("The Menu options are displayed on the Admin Page")
        for items in options_list:
            print(items.text)
        populate_locator = self.driver.find_element(by=By.XPATH, value='//span[@class="oxd-text oxd-text--span oxd-main-menu-item--name"]')
        sleep(5)
        search_input_box = self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator_input)
        sleep(2)
        if(search_input_box.send_keys("Ad") or populate_locator.text == 'Admin'):
            print("Admin tab is displayed")

    def test_page_headers_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.LINK_TEXT, value='Admin').click()
        self.driver.find_element(by=By.CLASS_NAME, value=Login_Locators().page_header_dropdown_locator).click()
        print("Clicked User Mgmnt dropdown")
        self.driver.find_element(by=By.LINK_TEXT, value='Users').click()
        print("Clicked Users")
        user_role = self.driver.find_element(by=By.XPATH, value=Login_Locators().user_role_locator)
        if(user_role.is_displayed()):
            print("User Role Dropdown is displayed on Admin Page")
        else:
            print("user Role Dropdown is not displayed on Admin Page")

        status = self.driver.find_element(by=By.XPATH, value=Login_Locators().status_locator)
        if(status.is_displayed()):
            print("Status Dropdown is displayed on Admin Page")
        else:
            print("Status Dropdown is not displayed on Admin Page")

        self.driver.find_element(by=By.XPATH, value=Login_Locators().user_role_dropdown).click()
        user_list = self.driver.find_elements(by=By.XPATH, value=Login_Locators().user_role_dropdown)
        print("Size of user dropdown list : ", len(user_list))
        for items in user_list:
            print(items.text)
        sleep(5)

        self.driver.find_element(by=By.XPATH, value=Login_Locators().status_dropdown).click()
        status_list = self.driver.find_elements(by=By.XPATH, value=Login_Locators().status_dropdown)
        print("Size of status dropdown list : ", len(status_list))
        for items in status_list:
            print(items.text)

    def test_add_employee_add_personal_details(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().add_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().toggle_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_username_locator).send_keys(Login_Data().pim_username)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_password_locator).send_keys(Login_Data().pim_password)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_confirm_password_locator).send_keys(Login_Data().pim_confirm_password)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_enabled_radio_button).click()
        self.driver.find_element(by=By.NAME, value=Login_Locators().pim_firstname_locator).send_keys(Login_Data().pim_firstname)
        self.driver.find_element(by=By.NAME, value=Login_Locators().pim_lastname_locator).send_keys(Login_Data().pim_lastname)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_save_locator).click()
        print("Successfully added employee details..")
        sleep(5)

        print("After Employee Creation URL : ", self.driver.current_url)

        add_employee_url = 'https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee'
        if(self.driver.current_url != add_employee_url):
            print("Successfully navigated to Employee List page")
        else:
            print("Failed to navigate to Employee List page")
        sleep(5)
        
        emp_list_tabs = self.driver.find_elements(by=By.CSS_SELECTOR, value='a.orangehrm-tabs-item')
        print("Size of Employee List Tabs : ", len(emp_list_tabs))
        for items in emp_list_tabs:
            print(items.text)
        if(len(emp_list_tabs) != 0):
            print("All the tabs are present in the Employee List Page")
        else:
            print("Tabs are not present in the Employee List Page")

        # entering personal details
        self.driver.find_element(by=By.XPATH, value=Login_Locators().nickname_locator).send_keys(Login_Data().nickname)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().otherid_locator).send_keys(Login_Data().otherid)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().license_num_locator).send_keys(Login_Data().license_num)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().license_exp_date_locator).send_keys(Login_Data().lic_exp_date)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().ssn_num_locator).send_keys(Login_Data().ssn_num)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().sin_num_locator).send_keys(Login_Data().sin_num)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().nationality_locator).click()
        nationality_dropdown_list = self.driver.find_elements(by=By.XPATH, value=Login_Locators().nationality_locator)

        self.driver.find_element(by=By.XPATH, value=Login_Locators().marital_status_locator).click()
        marital_dropdown_list = self.driver.find_elements(by=By.XPATH, value=Login_Locators().marital_status_locator)
        for i in marital_dropdown_list:
            print(i.text)
            if i.text == 'Married':
                i.click()

        self.driver.find_element(by=By.XPATH, value=Login_Locators().nationality_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().dob_locator).send_keys(Login_Data().date_of_birth)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().gender_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().mil_serv_locator).send_keys(Login_Data().mil_service)
        self.driver.execute_script("window.scrollTo(0, 300)")
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_save_locator).click()
        
    def test_emp_contact_details_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()

        self.driver.find_element(by=By.XPATH, value=Login_Locators().contact_tab_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().street1_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().street1_locator).send_keys(Login_Data().street1)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().street2_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().street2_locator).send_keys(Login_Data().street2)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().city_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().city_locator).send_keys(Login_Data().city)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().state_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().state_locator).send_keys(Login_Data().state)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().zip_code_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().zip_code_locator).send_keys(Login_Data().zipcode)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().home_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().home_locator).send_keys(Login_Data().home)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().mobile_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().mobile_locator).send_keys(Login_Data().mobile)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().work_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().work_locator).send_keys(Login_Data().work)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().work_email_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().work_email_locator).send_keys(Login_Data().work_email)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().other_email_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().other_email_locator).send_keys(Login_Data().other_email)
        bool_save = self.driver.find_element(by=By.XPATH, value=Login_Locators().contact_save_locator).is_displayed()
        if bool_save:
            sleep(3)
            self.driver.find_element(by=By.XPATH, value=Login_Locators().contact_save_locator).click()
    
    def test_emp_emergency_contact_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()

        self.driver.find_element(by=By.XPATH, value=Login_Locators().emergency_contact_locator).click()
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().add_emergency_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().name_emergency_locator).send_keys(Login_Data().name_emergency)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().relationship_locator).send_keys(Login_Data().relationship)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().home_tel_emergency_locator).send_keys(Login_Data().home_tel_emergency)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().mobile_emergency_locator).send_keys(Login_Data().mobile_emergency)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().work_tel_emergency_locator).send_keys(Login_Data().work_tel_emergency)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emergency_save_locator).click()
    
    def test_emp_dependent_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()

        self.driver.find_element(by=By.XPATH, value=Login_Locators().dependents_tab_locator).click()
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().add_dependents_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().dependent_name_locator).send_keys(Login_Data().dependent_name)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().dependent_relationship_locator).send_keys(Login_Data().dependent_relationship)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().dependent_dob_locator).send_keys(Login_Data().dependent_dob)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().dependents_save_locator).click()

    def test_emp_job_details_validation(self, boot):
        self.driver.implicitly_wait(5)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().job_tab_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().job_date_locator).send_keys(Login_Data().job_date)
        sleep(6)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().toggle_emp_contract_locator).click()
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().contract_start_date_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().contract_start_date_locator).send_keys(Login_Data().contract_start_date)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().contract_end_date_locator).clear()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().contract_end_date_locator).send_keys(Login_Data().contract_end_date)
        self.driver.execute_script("window.scrollTo(0, 300)")
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().job_save_locator).click()
    

    def test_emp_termination_validation(self, boot):
        self.driver.implicitly_wait(5)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().job_tab_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_terminate_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().termination_date_locator).send_keys(Login_Data().termination_date)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().termination_reason_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().termination_reason_locator).send_keys(Login_Data().termination_reason)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().termination_save_locator).click()
    
    def test_emp_salary_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().salary_tab_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().add_salary_details_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().salary_component_locator).send_keys(Login_Data().salary_component)
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().currency_locator).send_keys(Login_Data().currency)
        sleep(4)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().amount_locator).send_keys(Login_Data().amount)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().toggle_deposit_locator).click()
        sleep(3)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().account_number_locator).send_keys(Login_Data().account_number)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().rounting_number_locator).send_keys(Login_Data().routing_number)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().amount_toggle_deposit_locator).send_keys(Login_Data().amount_toggle_deposit)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().account_type_locator).send_keys(Login_Data().account_type)
        self.driver.execute_script("window.scrollTo(0, 200)")
        sleep(4)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().toggle_deposit_save_locator).click()
    

    def test_emp_tax_validation(self, boot):
        self.driver.implicitly_wait(10)
        self.test_login(self)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().pim_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().emp_name_locator).send_keys(Login_Data().emp_name_search)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().search_locator).click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().edit_emp_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().tax_exemptions_locator).click()
        self.driver.find_element(by=By.XPATH, value=Login_Locators().status_tax_locator).send_keys(Login_Data().status_federal_tax)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().state_income_tax_locator).send_keys(Login_Data().status_income_tax)
        self.driver.find_element(by=By.XPATH, value=Login_Locators().tax_exemptions_save_locator).click()








































































        








































    





























        
        
        













































                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 

        


















