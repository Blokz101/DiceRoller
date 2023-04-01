from functools import lru_cache

from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme
from rich import print as rprint

import math
import re
import random
import os

if os.name == "posix":
    import readline
elif os.name == "nt":
    import pyreadline3
else:
    raise OSError("Operating System is not compatable")



class DiceRoller:
    
    inputPatternRegEx: str = "\d+d\d+((\+|\-)\d+)?"
    
    
    
    def __init__(self) -> None:
        
        self.console = Console()
        
    
    
    def main(self):
        
        while True:
            
            # Get the next input from the user
            self.console.rule(style = "bold dark_magenta")
            line: str = input(">>> ")
            
            # Quit if the input is q
            if re.fullmatch("exit|q|stop", line):
                break
        
            # Check if the input is valid
            if not re.fullmatch(DiceRoller.inputPatternRegEx, line):
                self.console.print("Input not valid", style = "")
                continue
            
            # Split input into numbers
            inputs: list[int] = [int(num) for num in re.findall("\d+", line)]
            
            # Set the added modifier boolean
            addedModifier: bool = (len(inputs) == 3)
            
            #Set the modifier to 0 if there is none given
            if not addedModifier:
                inputs.append(0)
            
            # Negate the modifier if it should be negative
            if addedModifier and "-" in line:
                inputs[2] *= -1
            
            self.rollDice(inputs[0], inputs[1], inputs[2])
            
            
            
    def rollDice(self, numDice: int, diceMax: int, modifier: int) -> None:
        
            # Print the roll status
            self.console.print("\nRolling [variable]{0}[/variable] [variable]D{1}[/variable] with [variable]{2:+}[/variable] modifier".format(
                numDice,
                diceMax,
                modifier
            ), style = "white bold")  
            
            # Define the roll table
            rollTable: Table = Table(box = box.SIMPLE_HEAD, show_footer = True)
            rollTable.add_column("Roll #", no_wrap = True, width = 10)
            rollTable.add_column("Value", no_wrap = True, width = 10)
            rollTable.add_column("Total", no_wrap = True, width = 10)
            
            # Roll and sum the dice
            diceSum: int = 0
            for index in range(numDice):
                
                diceRoll: int = random.randint(1, diceMax)
                diceSum += diceRoll
                
                rollTable.add_row(
                    "Roll {0}".format(index), 
                    "[{1}]{0}[/{1}]".format(
                        round(diceRoll, 4), 
                        DiceRoller.conditionalFormat(diceRoll, diceMax, 1)
                    ),
                    str(diceSum)
                )
                
            # Print the table
            rollTable.columns[2].footer = str(diceSum)
            self.console.print(rollTable)
            
            # Define the statsitcs table
            stasticsTable: Table = Table(box = box.SIMPLE_HEAD)
            stasticsTable.add_column("Roll Stastics", no_wrap = True, width = 23)
            stasticsTable.add_column("", no_wrap = True, width = 10)
            
            # Calculate the statsitcs for the roll
            stasticsTable.add_row(
                "Roll Max", 
                str(round( numDice * diceMax, 4 ))
            )
            
            stasticsTable.add_row(
                "Roll Mean", 
                str(round( ((diceMax + 1) / 2) * numDice, 4 ))
            )
            
            stasticsTable.add_row(
                "Roll Min",
                str(round( numDice, 4 ))
            )
            
            probability: float = DiceRoller.sumProbability(diceSum, numDice, diceMax) * 100
            stasticsTable.add_row(
                "Probability = X",
                str(round( probability, 4 ))
            )
            
            worseProbability: float = DiceRoller.sumAndBelowProbability(diceSum - 1, numDice, diceMax) * 100
            stasticsTable.add_row(
                "Probability < X",
                str(round( worseProbability, 4 ))
            )
            
            betterProbability: float = DiceRoller.sumAndAboveProbability(diceSum + 1, numDice, diceMax) * 100
            stasticsTable.add_row(
                "Probability > X",
                str(round( betterProbability, 4 ))
            )
            
            # Print the table
            self.console.print(stasticsTable)   
            
            # Define the final numbers table
            finalTable: Table = Table(box = box.SIMPLE_HEAD, show_footer = True)  
            finalTable.add_column("Final Numbers", no_wrap = True, width = 23, footer = "Final Total")
            finalTable.add_column("", no_wrap = True, width = 10)
                
            # Add values
            finalTable.add_row("Dice Sum", str( diceSum ))
            finalTable.add_row("Modifier", "{:+}".format(modifier))
            
            # Print table
            finalTable.columns[1].footer = str(diceSum + modifier)
            self.console.print(finalTable)
                
                
                
    @classmethod
    def conditionalFormat(cls, value: float, maxValue: float, minValue: float) -> str:
        
        offsetValue: float = value - minValue
        offsetMax: float = maxValue - minValue
        
        if offsetValue >= 3/4 * offsetMax:
            return "green4"
        
        if offsetValue >= 1/4 * offsetMax:
            return "dark_orange"
        
        return "red1".format(value)
    
    
    
    @classmethod
    def sumProbability(cls, total: int, numDice: int, diceMax: int) -> float:
        
        return DiceRoller.__sumsForTotal(total, numDice, diceMax) / diceMax**numDice
    
    
    
    @classmethod
    def sumAndAboveProbability(cls, total: int, numDice: int, diceMax: int) -> float:
        
        if total == numDice * diceMax:
            return DiceRoller.sumProbability(numDice, numDice, diceMax)
        
        if total > diceMax * numDice:
            return 0
        
        return DiceRoller.sumProbability(total, numDice, diceMax) + DiceRoller.sumAndAboveProbability(total + 1, numDice, diceMax)
    
    
    
    @classmethod
    def sumAndBelowProbability(cls, total: int, numDice: int, diceMax: int) -> float:
        
        if total == numDice:
            return DiceRoller.sumProbability(numDice, numDice, diceMax)
        
        if total < numDice:
            return 0
        
        return DiceRoller.sumProbability(total, numDice, diceMax) + DiceRoller.sumAndBelowProbability(total - 1, numDice, diceMax)
    
    
    
    @classmethod
    @lru_cache(None)
    def __sumsForTotal(cls, total: int, numDice: int, diceMax: int) -> int:
        
        if not numDice:
            return not total
        
        return sum( DiceRoller.__sumsForTotal( total - die, numDice - 1, diceMax) for die in range(1, diceMax + 1) )
        
        
        
    
    

if __name__ == "__main__":
    DiceRoller().main()