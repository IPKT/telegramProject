from selenium import webdriver
from selenium.webdriver.common.by import By

# Setup WebDriver
driver = webdriver.Chrome()

# Buka halaman web
username = 'bawil3@wrs.id'
password = 'bawil3'
driver.get("http://202.90.199.203:3000/login")

driver.find_element("name", "user").send_keys(username)
driver.find_element("name", "password").send_keys(password)
driver.find_element(By.CLASS_NAME,"css-6ntnx5-button").click()
# Temukan panel berdasarkan kelas
panels = driver.find_elements(By.ID, 'panel-class')

# Cetak teks dari setiap panel
for panel in panels:
    text = panel.text
    print(text)
    print(panels)
# Tutup browser
driver.quit()
