from DiceRoller import DiceRoller
from ShortcutManager import ShortcutManager

from rich.console import Console

import os
import re

if os.name == "posix":
    import readline
elif os.name == "nt":
    import pyreadline3
else:
    raise OSError("Operating System is not compatable")






class DndAssistant:
    
    
    
    def __init__(self):
        
        self.console: Console = Console()
        self.shortcuts: ShortcutManager = ShortcutManager("shortcuts.csv")
        
        
    
    def main(self) -> None:
        
        
        while True:
            
            # Get the next input from the user
            self.console.rule(style = "bold dark_magenta")
            line: str = input(">>> ")
            
            # Quit if the input is q
            if re.fullmatch("exit|q|stop", line):
                break
            
            
            if re.fullmatch("(\d+)?d\d+((\+|\-|\/)\d+)?", line):
                self.rollDice(line)
                continue
            
            if self.shortcuts.match(line):
                self.rollDice(self.shortcuts.getShortcut(line))
                continue
            
            
            self.console.print("Input not valid", style = "red")
        
        
        
    def rollDice(self, line:str) -> None:
        
        roll: DiceRoller = DiceRoller(line)
                
        self.console.line()
        self.console.print(roll.status)
        self.console.print(roll.rollTable)
        self.console.print(roll.stasticsTable)
        self.console.print(roll.finalTable)
        
        
        
if __name__ == "__main__":
    DndAssistant().main()