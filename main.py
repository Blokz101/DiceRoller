from DiceRoller import DiceRoller

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
        
        
    
    def main(self) -> None:
        
        
        while True:
            
            # Get the next input from the user
            self.console.rule(style = "bold dark_magenta")
            line: str = input(">>> ")
            
            # Quit if the input is q
            if re.fullmatch("exit|q|stop", line):
                break
            
            
            if re.fullmatch("(\d+)?d\d+((\+|\-)\d+)?", line):
                roll: DiceRoller = DiceRoller(line)
                
                self.console.line()
                self.console.print(roll.status)
                self.console.print(roll.rollTable)
                self.console.print(roll.stasticsTable)
                self.console.print(roll.finalTable)
                
                continue
            
            
            self.console.print("Input not valid", style = "red")
        
        
        
        
        
        
if __name__ == "__main__":
    DndAssistant().main()