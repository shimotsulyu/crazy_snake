import pyautogui
import time
import yaml
import asyncio

stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
persist = c["counter"]["persist"]
time_persist = c["intervals"]["time_persist"]
delay = c["intervals"]["btn_delay"]
long_delay = c["intervals"]["btn_long_delay"]
interval = c["intervals"]["farm_cicle"]
confidence = c["percents"]["confidence"]

def click(target, confidence=confidence, stopOnFail=True):
    _click = pyautogui.locateCenterOnScreen(f'images/{target}.png', confidence=confidence)
    print(f"Procurando {target}")
    if _click is None:
        for i in range(persist):
            _click = pyautogui.locateCenterOnScreen(f'images/{target}.png', confidence=confidence)
            time.sleep(time_persist)
            if _click is not None: break
            if i == persist - 1 and stopOnFail is True:
                print("Target não encontrado. Resetando sistema")
                main()
    time.sleep(delay)
    pyautogui.click(_click)
    time.sleep(1)
    if pyautogui.locateCenterOnScreen(f'images/{target}.png', confidence=confidence) is not None:
        pyautogui.click(_click)
    print(f"  Clicou! {_click}")

def sensor_click(target):
    encerrou = pyautogui.locateOnScreen(f'images/{target}.png')
    if (encerrou is not None):
        click(f'{target}')
        return True

async def circle_walk():
    keys = [
        ['w','a'],
        ['d','w'],
        ['s','d'],
        ['a','s']
    ]
    while True:
        for k in keys:
            await asyncio.sleep(0)
            pyautogui.keyDown(k[0])
            pyautogui.keyUp(k[1])

async def finished(loop):
    print('Verificando se bateu')
    hit = sensor_click('pular')
    if (hit):
        finish = sensor_click('mais_uma_rodada')
        if (finish):
            loop.close()
            return start()
    finish = sensor_click('mais_uma_rodada')
    if (finish):
        loop.close()
        return start()

async def main(loop):
    print("**BOT STARTED**")
    click('btn_modo_sem_fim')
    click('clique_iniciar')
    time.sleep(2)
    f1 = loop.create_task(circle_walk())
    while True:
        f2 = loop.create_task(finished(loop))
        await asyncio.wait([f2])
        #time.sleep(10)

def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()

if __name__ == '__main__':
    confirm = pyautogui.confirm('Deseja iniciar o Bot?')
    if (confirm=="OK"):
        start()