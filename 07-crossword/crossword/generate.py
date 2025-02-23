import copy
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        #print(self.domains)
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        domains=copy.deepcopy(self.domains)
        for var,words in domains.items():
            for word in words:
                if var.length != len(word):
                    self.domains[var].remove(word)
        #print(self.domains)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        domins_copy=copy.deepcopy(self.domains)
        
        result=False
        i,j = self.crossword.overlaps[x,y]
        if i:
            for x_word in domins_copy[x]:
                matched=False
                for y_word in domins_copy[y]:
                    if x_word[i] == y_word[j]:
                        matched=True
                
                if matched ==False:
                    if x_word in self.domains[x]:
                        self.domains[x].remove(x_word)
                        
        return result

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        domains=copy.deepcopy(self.domains)
        # check if arcs is none
        if arcs == None:
            que=list()
            for X in domains:
                for Y in self.crossword.neighbors(X):
                    if self.crossword.overlaps[X,Y] is not None:
                        que.append((X,Y))
        while len(que) != 0:
            x,y=que.pop()
            if self.revise(x,y):
                # domain of x is empty
                if len(self.domains[x]) == 0 :
                    return False
                for neighbour in self.crossword.neighbors(x):
                    if neighbour != y:
                        que.append((neighbour, x))
            return True

        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment)==len(self.domains):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        result=True
        # check that all value is distinct
        for v1 in assignment:
            for v2 in assignment:
                if (v1 != v2) and (assignment[v1]== assignment[v2]):
                    result=False
        # check the length of the word  
        for var in assignment:
            if var.length != len(assignment[var]):
                result=False
        
        # check the overlap between var
        for var in assignment:
            for ovar in self.crossword.neighbors(var):
                if ovar in assignment:
                    i,j=self.crossword.overlaps[var,ovar]
                    if assignment[var][i] != assignment[ovar][j]:
                        result=False
        
        return result


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values=list()
        for x in self.domains[var]:
            if x not in assignment.values():
                values.append(x)

        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        vars=list()
        for var in self.domains:
            if var not in assignment:
                vars.append((var,len(self.domains[var]),len(self.crossword.neighbors(var))))

        
        def heursitc(item):
            return -item[2], item[1]
        
        sort_vars=sorted(vars,key=heursitc)
        
        return sort_vars[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # self.print(assignment)
        # print(self.domains)
        # print('-'*20)
        if len(assignment) == len(self.domains):
            return assignment
        var=self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            
            assignment_copy=copy.deepcopy(assignment)
            assignment_copy[var]=value
            if self.consistent(assignment_copy):
                res=self.backtrack(assignment_copy)
                if res != None:
                    return res
                
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
