from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg_1_statement = parse_input("fact: on ?disk peg1")
        peg_1_disks_list = self.kb.kb_ask(peg_1_statement)  
        p1_list =[]        
        peg_1_tuple = ()
        if peg_1_disks_list == False:
            peg_1_tuple = ()
        else:
            for i in peg_1_disks_list:
                if i.bindings_dict["?disk"] == "disk1":
                    p1_list.append(1)
                elif i.bindings_dict["?disk"] == "disk2":
                    p1_list.append(2)
                elif i.bindings_dict["?disk"] == "disk3":
                    p1_list.append(3)
                elif i.bindings_dict["?disk"] == "disk4":
                    p1_list.append(4)
                elif i.bindings_dict["?disk"] == "disk5":
                    p1_list.append(5)
        p1_list.sort()
        peg_1_tuple = tuple(p1_list)

        peg_2_statement = parse_input("fact: on ?disk peg2")
        peg_2_disks_list = self.kb.kb_ask(peg_2_statement)  
        p2_list =[]        
        peg_2_tuple = ()
        if peg_2_disks_list == False:
            peg_2_tuple = ()
        else:
            for i in peg_2_disks_list:
                if i.bindings_dict["?disk"] == "disk1":
                    p2_list.append(1)
                elif i.bindings_dict["?disk"] == "disk2":
                    p2_list.append(2)
                elif i.bindings_dict["?disk"] == "disk3":
                    p2_list.append(3)
                elif i.bindings_dict["?disk"] == "disk4":
                    p2_list.append(4)
                elif i.bindings_dict["?disk"] == "disk5":
                    p2_list.append(5)
        p2_list.sort()
        peg_2_tuple = tuple(p2_list)

        peg_3_statement = parse_input("fact: on ?disk peg3")
        peg_3_disks_list = self.kb.kb_ask(peg_3_statement)  
        p3_list =[]        
        peg_3_tuple = ()
        if peg_3_disks_list == False:
            peg_3_tuple = ()
        else:
            for i in peg_3_disks_list:
                if i.bindings_dict["?disk"] == "disk1":
                    p3_list.append(1)
                elif i.bindings_dict["?disk"] == "disk2":
                    p3_list.append(2)
                elif i.bindings_dict["?disk"] == "disk3":
                    p3_list.append(3)
                elif i.bindings_dict["?disk"] == "disk4":
                    p3_list.append(4)
                elif i.bindings_dict["?disk"] == "disk5":
                    p3_list.append(5)
        p3_list.sort()
        peg_3_tuple = tuple(p3_list)

        return (peg_1_tuple, peg_2_tuple, peg_3_tuple)

            



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk = str(movable_statement.terms[0])
        start_peg = str(movable_statement.terms[1])
        end_peg = str(movable_statement.terms[2])
        new_top_disk = ""
        end_top_disk = ""

        # Disk is no longer on the start peg
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + start_peg + ")"))

        # Disk is no longer the top of the start peg
        self.kb.kb_retract(parse_input("fact: (topStack " + disk + " " + start_peg + ")"))

        # Finding the new top disk 
        new_top = self.kb.kb_ask(parse_input("fact: (onTop " + disk + " ?newTop)"))
        if new_top:
            new_top_disk = new_top[0].bindings_dict["?newTop"]

            # The new top disk is asserted for the start peg
            self.kb.kb_assert(parse_input("fact: (topStack " + new_top_disk + " " + start_peg + ")"))

            # The original disk is no longer on top of the new top disk
            self.kb.kb_retract(parse_input("fact: (onTop " + disk + " " + new_top_disk + ")"))
        else:

            # If there was no other disk, start peg is now empty
            self.kb.kb_assert(parse_input("fact: (isEmpty " + start_peg + ")"))

        # If the end peg has a disk
        end_top = self.kb.kb_ask(parse_input("fact: (topStack ?endTopDisk " + end_peg + ")"))
        if end_top:
            end_top_disk = end_top[0].bindings_dict["?endTopDisk"]

            # End pegs current top disk is no longer top
            self.kb.kb_retract(parse_input("fact: (topStack " + end_top_disk + " " + end_peg + ")"))

            # The disk is now on top of the former top disk on the end peg
            self.kb.kb_assert(parse_input("fact: (onTop " + disk + " " + end_top_disk + ")"))

            # Disk is now the top of the end peg
            self.kb.kb_assert(parse_input("fact: (topStack " + disk + " " + end_peg + ")"))

            # Disk is now on the end peg
            self.kb.kb_assert(parse_input("fact: (on " + disk + " " + end_peg + ")"))


        else:
            # End peg is no longer empty
            self.kb.kb_retract(parse_input("fact: (isEmpty " + end_peg + ")"))

            # Disk is now on the end peg
            self.kb.kb_assert(parse_input("fact: (on " + disk + " " + end_peg + ")"))

            # Disk is now the top of the end peg
            self.kb.kb_assert(parse_input("fact: (topStack " + disk + " " + end_peg + ")"))


        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        

        row_1 = []
        row_2 = []
        row_3 = []


        row_1.append(self.kb.kb_ask(parse_input("fact: location ?tile pos1 pos1"))[0].bindings_dict["?tile"])
        row_1.append(self.kb.kb_ask(parse_input("fact: location ?tile pos2 pos1"))[0].bindings_dict["?tile"])
        row_1.append(self.kb.kb_ask(parse_input("fact: location ?tile pos3 pos1"))[0].bindings_dict["?tile"])

        row_2.append(self.kb.kb_ask(parse_input("fact: location ?tile pos1 pos2"))[0].bindings_dict["?tile"])
        row_2.append(self.kb.kb_ask(parse_input("fact: location ?tile pos2 pos2"))[0].bindings_dict["?tile"])
        row_2.append(self.kb.kb_ask(parse_input("fact: location ?tile pos3 pos2"))[0].bindings_dict["?tile"])

        row_3.append(self.kb.kb_ask(parse_input("fact: location ?tile pos1 pos3"))[0].bindings_dict["?tile"])
        row_3.append(self.kb.kb_ask(parse_input("fact: location ?tile pos2 pos3"))[0].bindings_dict["?tile"])
        row_3.append(self.kb.kb_ask(parse_input("fact: location ?tile pos3 pos3"))[0].bindings_dict["?tile"])

        transformDict = {
            "tile1": 1,
            "tile2": 2,
            "tile3": 3,
            "tile4": 4,
            "tile5": 5,
            "tile6": 6,
            "tile7": 7,
            "tile8": 8,
            "tile9": 9,
            "emptyTile": -1
        }

        x = lambda a : transformDict[a]

        r1 = list(map(x, row_1))
        r2 = list(map(x, row_2))
        r3 = list(map(x, row_3))

        return (tuple(r1), tuple(r2), tuple(r3))

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        tile = str(movable_statement.terms[0])
        start_x = str(movable_statement.terms[1])
        start_y = str(movable_statement.terms[2])
        end_x = str(movable_statement.terms[3])
        end_y = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (location emptyTile " + end_x + " " + end_y + ")"))
        self.kb.kb_retract(parse_input("fact: (location " + tile + " " + start_x + " " + start_y + ")"))

        self.kb.kb_assert(parse_input("fact: (location " + tile + " " + end_x + " " + end_y + ")"))
        self.kb.kb_assert(parse_input("fact: (location emptyTile " + start_x + " " + start_y + ")"))



        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
