"""
Módulo de Automação RPA (100% gratuito)
"""
import logging
from typing import Dict, Any, List, Optional
import asyncio
import os

logger = logging.getLogger(__name__)


class SeleniumBot:
    """Bot de automação usando Selenium"""

    def __init__(self):
        self.driver = None
        self.headless = os.getenv("SELENIUM_HEADLESS", "true").lower() == "true"

    async def initialize(self):
        """Inicializa o driver do Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service

            options = Options()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            self.driver = webdriver.Chrome(options=options)
            logger.info("✅ Selenium bot inicializado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Selenium: {str(e)}")
            raise

    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navega para uma URL"""
        try:
            self.driver.get(url)
            return {
                "success": True,
                "url": url,
                "title": self.driver.title
            }
        except Exception as e:
            logger.error(f"Erro na navegação: {str(e)}")
            return {"success": False, "error": str(e)}

    async def extract_text(self, selector: str) -> Dict[str, Any]:
        """Extrai texto de um elemento"""
        try:
            from selenium.webdriver.common.by import By
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return {
                "success": True,
                "text": element.text,
                "selector": selector
            }
        except Exception as e:
            logger.error(f"Erro ao extrair texto: {str(e)}")
            return {"success": False, "error": str(e)}

    async def click(self, selector: str) -> Dict[str, Any]:
        """Clica em um elemento"""
        try:
            from selenium.webdriver.common.by import By
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            element.click()
            return {
                "success": True,
                "action": "click",
                "selector": selector
            }
        except Exception as e:
            logger.error(f"Erro ao clicar: {str(e)}")
            return {"success": False, "error": str(e)}

    async def fill_input(self, selector: str, value: str) -> Dict[str, Any]:
        """Preenche um campo de input"""
        try:
            from selenium.webdriver.common.by import By
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            element.clear()
            element.send_keys(value)
            return {
                "success": True,
                "action": "fill",
                "selector": selector,
                "value": value
            }
        except Exception as e:
            logger.error(f"Erro ao preencher input: {str(e)}")
            return {"success": False, "error": str(e)}

    async def execute_script(self, script: str) -> Dict[str, Any]:
        """Executa JavaScript"""
        try:
            result = self.driver.execute_script(script)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            logger.error(f"Erro ao executar script: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_page_source(self) -> str:
        """Obtém o código fonte da página"""
        return self.driver.page_source

    async def close(self):
        """Fecha o driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium bot fechado")


class PlaywrightBot:
    """Bot de automação usando Playwright"""

    def __init__(self):
        self.browser = None
        self.page = None
        self.headless = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"

    async def initialize(self):
        """Inicializa o Playwright"""
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.page = await self.browser.new_page()
            logger.info("✅ Playwright bot inicializado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Playwright: {str(e)}")
            raise

    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navega para uma URL"""
        try:
            await self.page.goto(url)
            return {
                "success": True,
                "url": url,
                "title": await self.page.title()
            }
        except Exception as e:
            logger.error(f"Erro na navegação: {str(e)}")
            return {"success": False, "error": str(e)}

    async def extract_text(self, selector: str) -> Dict[str, Any]:
        """Extrai texto de um elemento"""
        try:
            element = await self.page.query_selector(selector)
            if element:
                text = await element.text_content()
                return {
                    "success": True,
                    "text": text,
                    "selector": selector
                }
            return {"success": False, "error": "Elemento não encontrado"}
        except Exception as e:
            logger.error(f"Erro ao extrair texto: {str(e)}")
            return {"success": False, "error": str(e)}

    async def click(self, selector: str) -> Dict[str, Any]:
        """Clica em um elemento"""
        try:
            await self.page.click(selector)
            return {
                "success": True,
                "action": "click",
                "selector": selector
            }
        except Exception as e:
            logger.error(f"Erro ao clicar: {str(e)}")
            return {"success": False, "error": str(e)}

    async def fill_input(self, selector: str, value: str) -> Dict[str, Any]:
        """Preenche um campo de input"""
        try:
            await self.page.fill(selector, value)
            return {
                "success": True,
                "action": "fill",
                "selector": selector,
                "value": value
            }
        except Exception as e:
            logger.error(f"Erro ao preencher input: {str(e)}")
            return {"success": False, "error": str(e)}

    async def execute_script(self, script: str) -> Dict[str, Any]:
        """Executa JavaScript"""
        try:
            result = await self.page.evaluate(script)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            logger.error(f"Erro ao executar script: {str(e)}")
            return {"success": False, "error": str(e)}

    async def screenshot(self, path: str = "screenshot.png") -> Dict[str, Any]:
        """Tira screenshot da página"""
        try:
            await self.page.screenshot(path=path)
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            logger.error(f"Erro ao tirar screenshot: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_page_source(self) -> str:
        """Obtém o código fonte da página"""
        return await self.page.content()

    async def close(self):
        """Fecha o browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            logger.info("Playwright bot fechado")


class GUIAutomation:
    """Automação de interface gráfica usando PyAutoGUI"""

    def __init__(self):
        import pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5

    async def click(self, x: int, y: int) -> Dict[str, Any]:
        """Clica em uma posição na tela"""
        try:
            import pyautogui
            pyautogui.click(x, y)
            return {
                "success": True,
                "action": "click",
                "position": (x, y)
            }
        except Exception as e:
            logger.error(f"Erro ao clicar: {str(e)}")
            return {"success": False, "error": str(e)}

    async def type_text(self, text: str) -> Dict[str, Any]:
        """Digita texto"""
        try:
            import pyautogui
            pyautogui.typewrite(text)
            return {
                "success": True,
                "action": "type",
                "text": text
            }
        except Exception as e:
            logger.error(f"Erro ao digitar: {str(e)}")
            return {"success": False, "error": str(e)}

    async def press_key(self, key: str) -> Dict[str, Any]:
        """Pressiona uma tecla"""
        try:
            import pyautogui
            pyautogui.press(key)
            return {
                "success": True,
                "action": "keypress",
                "key": key
            }
        except Exception as e:
            logger.error(f"Erro ao pressionar tecla: {str(e)}")
            return {"success": False, "error": str(e)}

    async def screenshot(self, path: str = "screenshot.png") -> Dict[str, Any]:
        """Tira screenshot da tela"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            logger.error(f"Erro ao tirar screenshot: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_screen_size(self) -> Dict[str, Any]:
        """Obtém o tamanho da tela"""
        try:
            import pyautogui
            width, height = pyautogui.size()
            return {
                "success": True,
                "width": width,
                "height": height
            }
        except Exception as e:
            logger.error(f"Erro ao obter tamanho da tela: {str(e)}")
            return {"success": False, "error": str(e)}
