import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells)==self.count:
            return self.cells
        
        return None
        
                

        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        return None

        
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1




    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark cell al move that has been make
        
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.safes.add(cell)
        # 3) add a new sentence to the AI's knowledge base
        #        based on the value of `cell` and `count`

        arr_cells=self.around_cells(cell)
        copy_count=copy.deepcopy(count)
        cells=set()
        for c in arr_cells:
            if c in self.safes:
                copy_count-=1
            elif c not in self.safes | self.mines:
                cells.add(c)

        # add new sentance fo knowledge
        st=Sentence(cells,count)
        if len(st.cells)>0:
            self.knowledge.append(st)
            # print(f'add new sentence to knowldge {st}')
        
        # print(f"knowldge: ")
        # for sen in self.knowledge:
        #     print(sen)

        
        # 4) mark any additional cells as safe or as mines
        #        if it can be concluded based on the AI's knowledge base
        self.check_knowldge()
        print('-'*20)
        print(f'safe node after check{self.safes}')
        
        


        # 5) add any new sentences to the AI's knowledge base
        #        if they can be inferred from existing knowledge
        self.extra_sent()
        print('-'*20)
        print(f'safe node after extra{self.safes}')


        

    def check_knowldge(self):
        # make deepcopy of knoledge to perform on it
        copy_know=copy.deepcopy(self.knowledge)
        for sent in copy_know:
            # if sentence is empy remove form knowledge
            if len(sent.cells)==0:
                try:
                    self.knowledge.remove(sent)
                except ValueError:
                    pass
            #print(f'current sentence cells{sent.cells}')
            mines = sent.known_mines()
            safes = sent.known_safes()
            #print(f"return cells {safes}")
            # add all mine to self.mine
            if mines:
                for mine in mines:
                    print('-'*20)
                    print(f'mark {mine} as mine')
                    print('-'*20)
                    self.mark_mine(mine)
                    self.check_knowldge()
            
            # add all safe to self.safes
            if safes:
                for safe in safes:
                    print('-'*20)
                    print(f'mark {safe} as safe')
                    print('-'*20)
                    self.mark_safe(safe)
                    self.check_knowldge()    

    def around_cells(self,cell):
        a_cells=set()
        # loop over all cells around wanted cell
        for i in range(cell[0]-1,cell[0]+2):
            for j in range(cell[1]-1,cell[1]+2):
                # ignore cell itself
                if (i,j)==cell:
                    continue
                elif 0<=i<self.height and 0<=j<self.width:
                    a_cells.add((i,j))
        
        return a_cells
    
    def extra_sent(self):
        # loop on knowldge to check if any one 
        # is sub set on another one
        for sent1 in self.knowledge:
            for sent2 in self.knowledge:
                if sent1.cells.issubset(sent2.cells):
                    new_cell=sent2.cells - sent1.cells
                    new_count=sent2.count - sent1.count
                    new_sent=Sentence(new_cell,new_count)
                    mines=new_sent.known_mines()
                    safes=new_sent.known_safes()

                    if mines:
                        for mine in mines:
                            self.mark_mine(mine)
                    if safes:
                        for safe in safes:
                            self.mark_safe(safe)

        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made|self.mines:
                print('='*20)
                print(f'current AI move {cell}')
                print('='*20)
                return cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        maxmoves = self.width * self.height

        while maxmoves > 0:
            maxmoves -= 1

            row = random.randrange(self.height)
            column = random.randrange(self.width)

            if (row, column) not in self.moves_made | self.mines:
                print('='*20)
                print(f'current random move {(row,column)}')
                print('='*20)
                return (row, column)

        return None
