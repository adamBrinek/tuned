
#Importin tuned modules
import tuned.logs
import tuned.consts as consts

ACK = True
NACK = False

log = tuned.logs.get()


class Autoswitch(object, ):
    def __init__(self):
        self._switching = False

        self._type = ""
        self._insert_fifo = []
        self._semaphore = False
        self._status = True
        self.tab_1 = []

#    def __init_tab__(self):
        #tady si nainicializuju tabulku
        #v Application.py

    def set_switching(self,conf):
        if conf == 'True':
            self._switching = True
        else:
            self._switching = False
    
    def set_type(self,switch_type):
        self._type = switch_type

    def status(self):
        #vratim jestli mam v konfiguraku povoleno meneni
        return self._switching

    def type(self):
        return self._type


    def change(self, code_name):
        #zkontrolovat jestli je code name v tabulce
        if self.check_tab(code_name):
            return True
        else:
            return False

    def check_tab(self,code_name):
        for item in self.tab_1:
            if code_name in item:
                return True
        return False

#Ladici fce
    #vypisu si tabulku do logu
    def write_tab(self):
        for item in self.tab_1:
            log.info(item)



#    def check_code_name(self, code_name):
        #pokud je code_name v seznamu tak vrat True jinak False
#        try:
#            FIFO.index(code_name)
#        except ValueError:
#            return False
#        return True


#    def add_code_name(self, code_name):
        #pridam code_name do seznamu
#        self.recalculate()

#    def remove_code_name(self, code_name):
        #odstranim code_name ze seznamu
#        self.recalculate()

#    def recalculate(self):
        #provedl jsem nejakou zmenu v seznamu tak ji prepocitam a pokud je potreba tak zmenim profil


#    def quit(self, code_name):
        #posilam code name pluginu co uz konci a tim padem si ho vyradim z LIFO a pokud se to zmeni tak prepocitam
#        return ACK
