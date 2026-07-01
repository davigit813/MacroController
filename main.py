import time
import threading
import json
import os
from medules.autoclicker import thread_lclick, thread_rclick

class MacroController:
    def __init__(self):
        self.module_states = {}
        self.currently_in_foreground = True
        self.currently_in_menu = False
        self.running = True
        self.arquivo_config = "config.json"

    def start_autoclick(self, cps=8, randomize=2, shake=0, blockhit=0, hold=True, bblock=False, button="left"):
        self.module_states["autoclick"] = True
        thread_lclick(
            self,
            module="autoclick",
            slider=cps,
            randomize=randomize,
            shake=shake,
            blockhit=blockhit,
            hold=hold,
            bblock=bblock,
            button=button
        )
        print(f"✅ Autoclick ATIVADO! CPS: {cps}")

    def start_fastplace(self, cps=8, randomize=2, shake=0, hold=True, eat=False, button="right"):
        self.module_states["fastplace"] = True
        thread_rclick(
            self,
            module="fastplace",
            slider=cps,
            randomize=randomize,
            shake=shake,
            hold=hold,
            eat=eat,
            button=button
        )
        print(f"✅ FastPlace ATIVADO! CPS: {cps}")

    def stop_autoclick(self):
        self.module_states["autoclick"] = False
        print("🔴 Autoclick DESATIVADO!")

    def stop_fastplace(self):
        self.module_states["fastplace"] = False
        print("🔴 FastPlace DESATIVADO!")

    def ler_comando(self):
        if os.path.exists(self.arquivo_config):
            with open(self.arquivo_config, 'r') as f:
                try:
                    dados = json.load(f)
                    return dados
                except:
                    return None
        return None

    def limpar_comando(self):
        if os.path.exists(self.arquivo_config):
            os.remove(self.arquivo_config)

    def executar(self):
        print("🎯 MacroController Python aguardando comandos...")
        
        while self.running:
            comando = self.ler_comando()
            
            if comando:
                acao = comando.get("acao", "")
                tipo = comando.get("tipo", "autoclick")
                
                if acao == "ativar":
                    cps = comando.get("cps", 8)
                    randomize = comando.get("randomize", 2)
                    shake = comando.get("shake", 0)
                    blockhit = comando.get("blockhit", 0)
                    hold = comando.get("hold", True)
                    bblock = comando.get("bblock", False)
                    
                    if tipo == "autoclick":
                        self.start_autoclick(cps, randomize, shake, blockhit, hold, bblock, "left")
                    elif tipo == "fastplace":
                        self.start_fastplace(cps, randomize, shake, hold, False, "right")
                    
                    self.limpar_comando()
                    
                elif acao == "desativar":
                    if tipo == "autoclick":
                        self.stop_autoclick()
                    elif tipo == "fastplace":
                        self.stop_fastplace()
                    self.limpar_comando()
                    
                elif acao == "sair":
                    self.running = False
                    self.stop_autoclick()
                    self.stop_fastplace()
                    self.limpar_comando()
                    print("👋 Encerrando...")
                    break
            
            time.sleep(0.5)

if __name__ == "__main__":
    controller = MacroController()
    controller.executar()
