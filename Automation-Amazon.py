
from selenium import webdriver
import unittest
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait


class AmazonTestAutomation(unittest.TestCase):
    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(chrome_options)
        self.driver.maximize_window()
        self.third_product_index = 3
        self.driver.implicitly_wait(5)
        


    def test_main(self):
        self.homepage()
        self.check_correct_amazon()
        self.search_box_text()
        self.check_cookies()
        self.go_to_second_page()
        self.verify_second_page()
        self.check_cookies()
        self.select_product()
        self.verify_product_page()
        self.add_to_cart()
        self.verify_add_to_cart()
        self.go_to_cart_page()
        self.verify_cart_page()
        self.verify_product_in_cart()
        self.delete_product()
        self.verify_deleted_product()


    def homepage(self):
        self.driver.get("https://www.amazon.com.tr")
        self.assertEqual(self.driver.current_url, "https://www.amazon.com.tr/", "Anasayfada değilsiniz")

    def check_correct_amazon(self):
        try:
            
            self.driver.find_element(By.ID, "navbar-backup-backup")

            print("Amazon'un backup sitesine yönlendirildi, test yeniden başlatılıyor.")

            self.tearDown()
            self.setUp()
            self.test_main()
        except NoSuchElementException:
            print("Doğru Amazon sitesinde devam ediliyor.")

    def search_box_text(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.check_cookies()

        try:
            search_box = WebDriverWait(self.driver, 5).until( #Element olmasına rağmen sayfa tekrar yüklendiği için "stale" hatası alıyordum
                EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))
            )
            try:
                search_box.send_keys("samsung")
            except StaleElementReferenceException:
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))
                )
                search_box.send_keys("samsung")
        except NoSuchElementException:
            self.assertTrue(False, "Search box elementi bulunamadı")

        try:
            
            search_button = self.driver.find_element(By.ID, "nav-search-submit-button")
            search_button.click()
        except NoSuchElementException:
            self.assertTrue(False, "Search button elementi bulunamadı")

        try:
            
            samsung_text_element = self.driver.find_element(By.CSS_SELECTOR, "#search .a-color-state.a-text-bold")
            self.assertEqual(samsung_text_element.text, '"samsung"', "Aramalarda samsung yok")
        except NoSuchElementException:
            self.assertTrue(False, "Samsung text elementi bulunamadı")

    def check_cookies(self):
        try:
            cookie_accept_button = self.driver.find_element(By.ID, "sp-cc-accept")
            cookie_accept_button.click()
        except NoSuchElementException:
            print("Cookie accept button elementi bulunamadı, devam ediliyor.")

    def go_to_second_page(self):
        try:
            
            go_to_second_page_button = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="2 sayfasına git"]')
            go_to_second_page_button.click()
        except NoSuchElementException:
            self.assertTrue(False, "Go to second page button elementi bulunamadı. İkinci sayfaya gidilemedi.")

    def verify_second_page(self):
        try:
            
            second_page_element = self.driver.find_element(By.CSS_SELECTOR, ".s-pagination-item.s-pagination-selected")
            self.assertEqual(second_page_element.get_attribute("aria-label"),"Sayfa 2" , "İkinci sayfada değilsiniz")
        except NoSuchElementException:
            self.assertTrue(False, "Second page elementi bulunamadı. İkinci sayfada değilsiniz.")

    def select_product(self):
        try:
            
            ad_widget_element= self.driver.find_element(By.CLASS_NAME, "_c2Itd_content_2L-a5")

            ad_widget_list_count=len(ad_widget_element.find_elements(By.CSS_SELECTOR, "li.a-carousel-card"))
            self.third_product_index += ad_widget_list_count
        except NoSuchElementException:
            self.assertTrue(False, " Advertisement widget elementi bulunamadı")

        try:
            
            third_product_element=self.driver.find_element(By.CSS_SELECTOR, 'div[role="listitem"]:nth-of-type(' + str(self.third_product_index) + ")")
            third_product_element.click()
        except NoSuchElementException:
            self.assertTrue(False, " Third product elementi bulunamadı")

    def verify_product_page(self):
        try:
            
            self.driver.find_element(By.ID, "buy-now-button")
        except NoSuchElementException:
            self.assertTrue(False, "Buy now button elementi bulunamadı. Ürün sayfasında değilsiniz")

    def add_to_cart(self):
        try:
            
            product_id_element=self.driver.find_element(By.ID, "gsod_singleOfferDisplay_Desktop")
            self.product_id = product_id_element.get_attribute("data-csa-c-asin")
        except NoSuchElementException:
            self.assertTrue(False, "Product id elementi bulunamadı. Ürün sepete eklenemedi.")

        try:
            
            add_to_cart_button=self.driver.find_element(By.ID, "add-to-cart-button")
            add_to_cart_button.click()
        except NoSuchElementException:
            self.assertTrue(False, "Add to cart button elementi bulunamadı. Ürün sepete eklenemedi.")

    def verify_add_to_cart(self):

        try:
            
            self.driver.find_element(By.ID, "NATC_SMART_WAGON_CONF_MSG_SUCCESS")
        except NoSuchElementException:
            self.assertTrue(False, "Add to cart message elementi bulunamadı. Ürün sepete eklenemedi.")

    def go_to_cart_page(self):
        try:
            
            go_to_cart_button=self.driver.find_element(By.CSS_SELECTOR, "#sw-gtc .a-button-text")
            go_to_cart_button.click()
        except NoSuchElementException:
            self.assertTrue(False, "Go to cart button elementi bulunamadı. Sepet sayfasına gidilemedi.")

    def verify_cart_page(self):
        try:
            
            verify_cart_page_element=self.driver.find_element(By.ID, "sc-active-items-header")
            self.assertEqual(verify_cart_page_element.text.strip(), "Alışveriş Sepeti", "Sepet sayfasında değilsiniz")
        except NoSuchElementException:
            self.assertTrue(False, "Verify cart page elementi bulunamadı. Sepet sayfasında değilsiniz.")

    def verify_product_in_cart(self):
        try:
            
            self.driver.find_element(By.CSS_SELECTOR, '.a-row.sc-list-item[data-asin="' + str(self.product_id) + '"]')
        except NoSuchElementException:
            self.assertTrue(False, "Ürün sepette bulunamadı")

    def delete_product(self):
        try:
            
            delete_button=self.driver.find_element(By.CLASS_NAME, 'a-size-small.sc-action-delete[data-action="delete"]')
            delete_button.click()
        except NoSuchElementException:
            self.assertTrue(False, "Delete button bulunamadı. Ürün silinemedi")

    def verify_deleted_product(self):
        try:
            
            self.driver.find_element(By.CSS_SELECTOR, '.a-row.sc-list-item[data-asin="' + str(self.product_id) + '"] .sc-list-item-removed-msg')
            self.return_to_homepage()
        except NoSuchElementException:
            self.assertTrue(False, '"Ürün silindi" elementi bulunamadı. Ürün sepette mevcut')


    def return_to_homepage(self):
        try:
            
            home_page_button=self.driver.find_element(By.ID, "nav-logo-sprites")
            home_page_button.click()
            self.assertEqual(self.driver.current_url, "https://www.amazon.com.tr/ref=nav_logo", "Ana sayfayada değilsiniz")
        except NoSuchElementException:
            self.assertTrue(False, "home_page_button bulunamadı. Ana sayfaya gidilemedi.")


