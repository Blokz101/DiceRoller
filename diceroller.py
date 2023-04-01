from functools import lru_cache

from rich.table import Table
from rich.text import Text
from rich import box

import re
import random






class DiceRoller:  
    
    def __init__(self, input: str) -> None:
        
        self.rawinput: str = input
        
        self.status: Text = None
        
        self.rolls: list[int] = []
        self.probability: float = -1
        self.betterProbability: float = -1
        self.worseProbability: float = -1
        
        self.rollTable: Table = Table(box = box.SIMPLE_HEAD, show_footer = True)
        self.stasticsTable: Table = Table(box = box.SIMPLE_HEAD)
        self.finalTable: Table = Table(box = box.SIMPLE_HEAD, show_footer = True)
        
        numDice, diceMax, modifier = DiceRoller.__readDiceSyntax(self.rawinput)
        self.__rollDice(numDice, diceMax, modifier)
        
        
        
            
            
    def __rollDice(self, numDice: int, diceMax: int, modifier: int) -> tuple:

            # Print the roll status
            self.status = Text.assemble(
                ("Rolling ", "bold white"),
                ("{0} D{1}".format(numDice, diceMax), "bold dark_magenta"),
                (" with ", "bold white"),
                ("{0:+} modifier".format(modifier), "bold dark_magenta")
            )
            
            # Define the roll table
            self.rollTable.add_column("Roll #", no_wrap = True, width = 10)
            self.rollTable.add_column("Value", no_wrap = True, width = 10)
            self.rollTable.add_column("Total", no_wrap = True, width = 10)
            
            # Roll and sum the dice
            diceSum: int = 0
            for index in range(numDice):
                
                diceRoll: int = random.randint(1, diceMax)
                diceSum += diceRoll
                
                self.rolls.append(diceRoll)
                
                self.rollTable.add_row(
                    "Roll {0}".format(index), 
                    "[{1}]{0}[/{1}]".format(
                        round(diceRoll, 4), 
                        DiceRoller.__conditionalFormat(diceRoll, diceMax, 1)
                    ),
                    str(diceSum)
                )
            self.rollTable.columns[2].footer = str(diceSum)
            
            # Define the statsitcs table
            self.stasticsTable.add_column("Roll Stastics", no_wrap = True, width = 23)
            self.stasticsTable.add_column("", no_wrap = True, width = 10)
            
            # Calculate the statsitcs for the roll
            self.stasticsTable.add_row(
                "Roll Max", 
                str(round( numDice * diceMax, 4 ))
            )
            
            self.stasticsTable.add_row(
                "Roll Mean", 
                str(round( ((diceMax + 1) / 2) * numDice, 4 ))
            )
            
            self.stasticsTable.add_row(
                "Roll Min",
                str(round( numDice, 4 ))
            )
            
            probability: float = DiceRoller.sumProbability(diceSum, numDice, diceMax) * 100
            self.stasticsTable.add_row(
                "Probability = X",
                str(round( probability, 4 ))
            )
            
            worseProbability: float = DiceRoller.sumAndBelowProbability(diceSum - 1, numDice, diceMax) * 100
            self.stasticsTable.add_row(
                "Probability < X",
                str(round( worseProbability, 4 ))
            )
            
            betterProbability: float = DiceRoller.sumAndAboveProbability(diceSum + 1, numDice, diceMax) * 100
            self.stasticsTable.add_row(
                "Probability > X",
                str(round( betterProbability, 4 ))
            ) 
            
            # Define the final numbers table
            self.finalTable.add_column("Final Numbers", no_wrap = True, width = 23, footer = "Final Total")
            self.finalTable.add_column("", no_wrap = True, width = 10)
                
            # Add values
            self.finalTable.add_row("Dice Sum", str( diceSum ))
            self.finalTable.add_row("Modifier", "{:+}".format(modifier))
            self.finalTable.columns[1].footer = str(diceSum + modifier)
    
    
    
    @classmethod
    def __readDiceSyntax(cls, rawInput: str) -> tuple:
        
        # Match format d20
        if re.fullmatch("d\d+", rawInput):
            
            return 1, int(rawInput[1:]), 0
        
        # Match format 4d20
        if re.fullmatch("\d+d\d+", rawInput):
            inputs: list = re.split("d", rawInput)
            inputs = [int(num) for num in inputs]
            return inputs[0], inputs[1], 0
        
        # Match format d20+5
        if re.fullmatch("d\d+(\+|\-)\d+", rawInput):
            inputs: list = re.split("d|\+|\-", rawInput[1:])
            inputs = [int(num) for num in inputs]
            if "+" in rawInput: 
                return 1, inputs[0], inputs[1]
            if "-" in rawInput:
                return 1, inputs[0], -inputs[1]
        
        # Match format 4d20+5
        if re.fullmatch("\d+d\d+(\+|\-)\d+", rawInput):
            inputs: list = re.split("d|\+|\-", rawInput)
            inputs = [int(num) for num in inputs]
            if "+" in rawInput: 
                return inputs[0], inputs[1], inputs[2]
            if "-" in rawInput:
                return inputs[0], inputs[1], -inputs[2]
    
        # Raise a value error if the arguments are not valid 
        raise ValueError("Illegal dice syntax: {0}".format(rawInput))
                
                
                
    @classmethod
    def __conditionalFormat(cls, value: float, maxValue: float, minValue: float) -> str:
        
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
    