import sys

from crossword import Variable, Crossword

class Queue:
    def __init__(self, initial_list = None):
        if initial_list == None:
            self.itens = []
        else:
            self.itens = initial_list

    def empty(self):
        return len(self.itens) == 0

    def enqueue(self, item):
        self.itens.append(item)

    def dequeue(self):
        return self.itens.pop(0)
    
    def size(self):
        return len(self.itens)

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
        return self.backtrack(dict())



    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            for word in self.crossword.words.copy():
                if variable.length != len(word):
                    self.domains[variable].remove(word)
        


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get the overlaps between the variable x and y
        overlaps = self.crossword.overlaps[x,y]
        elements_to_delete = set() # Set with words that will be deleted
        revised = False # Initialize revised variable as False

        # Verify if there is an overlap
        if len(overlaps) != 0:
            # Check if for some word in x's domain if there is any word in y's domain that matches, if there is no word in y's domain that matches, then the word will be deleted from x's domain.
            for x_elem in self.domains[x]:
                delete = True
                for y_elem in self.domains[y]:
                    if x_elem[overlaps[0]] == y_elem[overlaps[1]]:
                        delete = False 
                        break
                if delete:
                    elements_to_delete.add(x_elem)
                    revised = True
            for element in elements_to_delete:
                self.domains[x].remove(element)
  
        return revised



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = Queue(initial_list = arcs) # Initialize queue

        if arcs == None:
            # If arcs argument is None, create the queue with all the arcs
            for var in self.domains:
                for neighbor in self.crossword.neighbors(var):
                    if (var, neighbor) not in queue.itens:
                        queue.enqueue((var, neighbor))

        # Enforce arc consistency 
        while not queue.empty():
            arc = queue.dequeue()
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
                for z in self.crossword.neighbors(arc[0]) - {arc[1]}:
                    queue.enqueue((z, arc[0]))
        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # The assignment is complete if each one of the variables in the crossword has an associated word
        if len(assignment.keys()) == len(self.crossword.variables):
            for value in assignment.values():
                if len(value) == 0 or type(value) != str:
                    return False
        else:
            return False

        return True



    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        keys = list(assignment.keys()) # Initialize the list with all the variables in the assignment dict

        # Check if the word is unique in the assignment dict
        for word in assignment.values():
            if list(assignment.values()).count(word) != 1:
                return False

        # Check if unary and binary constraints are satisfied
        for key in keys:
            if(key.length != len(assignment[key])):
                return False
            for neighbor in self.crossword.neighbors(key):
                if neighbor in keys:
                    i, j = self.crossword.overlaps[key,neighbor]
                    if assignment[key][i] != assignment[neighbor][j]:
                        return False
                    
        return True
            


 
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        constraint_per_word = dict() # Initialize the dict with the word as the key and the number of constraints that choosing this word generates in the crossword

        variables_to_verify = self.crossword.neighbors(var) - set(assignment.keys()) # The variables which will be verified are the variables that are neighbors and are not in the assignment

        # Given a word from y's domain, check how many constraints this choice of word makes on the variables that are neighbors
        for y_elem in self.domains[var]:
            counter = 0
            for x in variables_to_verify:
                overlaps = self.crossword.overlaps[x,var]
                for x_elem in self.domains[x]:
                    if x_elem[overlaps[0]] != y_elem[overlaps[1]]:
                        counter += 1
            constraint_per_word[y_elem] = counter

        return sorted(constraint_per_word, key = constraint_per_word.get)

        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = self.crossword.variables - assignment.keys()

        elements_in_domain_per_variable = dict()
        elements_degree_per_variable = dict()

        # Adding data to the dictionaries
        for variable in unassigned_variables:
            elements_in_domain_per_variable[variable] = len(self.domains[variable])
            elements_degree_per_variable[variable] = len(self.crossword.neighbors(variable))

        list_variables_domains = sorted(elements_in_domain_per_variable, key = elements_in_domain_per_variable.get)

        # Minimum Remaining Values
        min_domain = min(elements_in_domain_per_variable, key=elements_in_domain_per_variable.get) 

      

        # Check if there is a tie in MRV
        if list(elements_in_domain_per_variable.values()).count(elements_in_domain_per_variable[min_domain]) != 1:

            # Create the dict with the variable as the key and degree as the value, and after this use the maximum degree as a tiebreaker
            result = {key : elements_degree_per_variable[key]  for key, value in elements_in_domain_per_variable.items() if value == elements_in_domain_per_variable[min_domain]}
            
            # Check if the maximum is unique
            if list(result.values()).count(max(result.values())) == 1:
                return max(result, key=result.get)
            else:
                # Return an arbitrary variable if another tie occurs
                return list(result.keys())[0]
        
        return min_domain    
        
            



        
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Check if the assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        # If a variable is not obtained
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            if self.consistent(assignment = assignment_copy):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != None:
                    return result
                # If the var generates a failure, delete the variable
                del assignment[var]
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