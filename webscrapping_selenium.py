#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 18:20:43 2019

@author: viniciussaurin
"""

from selenium import webdriver
from time import sleep
import pandas as pd

path = '/chromedriver'
path_excel = '/RN.xls'


class ChromeAuto:
    def __init__(self):
        self.driver_path = path
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=Perfil')
        self.chrome = webdriver.Chrome(
                self.driver_path,
                options=self.options
        )
    def acessa(self, site):
        self.chrome.get(site)
    
    def scrapping_head(self):
        tr_elements = self.chrome.find_elements_by_xpath('//tr/th')
        col=[]
        i=0        
        for t in tr_elements:
            i += 1
            name=t.text
            print(f'{i}:{name}')
            col.append(name)
        return col
    
        
    
    def scrapping_body(self):
        td_elements = self.chrome.find_elements_by_xpath('//tr/td')
        tr_elements = self.chrome.find_elements_by_xpath('//tbody/tr')
        qtd_td_por_tr = int(len(td_elements)/len(tr_elements))
        col = []
        temp = []
        for k in range(len(tr_elements)):
            for j in range(qtd_td_por_tr):
                data = td_elements[k * qtd_td_por_tr + j].text
                temp.append(data)
            col.append(temp)
            temp = []
        
        return col
    
    def clicar_proxima_pagina(self):
        try:
            btn_proxima_pg = self.chrome.find_element_by_link_text('próxima')
            btn_proxima_pg.click()
            return True
        except Exception as e:
            print('Erro ao clicar em Próxima página:', e)
            return False
        
        
    def sair(self):
        self.chrome.quit()


if __name__ == '__main__':
    chrome = ChromeAuto()
    acessa = chrome.acessa('http://servicos.searh.rn.gov.br/searh/Remuneracao/RemuneracaoPorId/17301247?MesAno=10%2F2019')
    head = chrome.scrapping_head()
    retorno_px_pg = True
    i = 0
    body=pd.DataFrame(columns=head)
    while retorno_px_pg:
        temp = pd.DataFrame.from_records(data=chrome.scrapping_body(), columns=head)
        body = body.append(temp)
        print(i)
        i+=1
        retorno_px_pg = chrome.clicar_proxima_pagina()
    sleep(2)
    chrome.sair()
    body.to_excel(path_excel, index=False)
