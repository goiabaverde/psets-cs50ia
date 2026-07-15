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
        self.mines_cells = set()
        if self.count == len(self.cells):
            self.mines_cells = self.cells
        return self.mines_cells


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        self.safes_cells = set()
        if self.count == 0:
            self.safes_cells = self.cells
        return self.safes_cells




    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        cell_in = False

        if cell in self.cells:
            cell_to_remove = cell
            self.count -= 1
            cell_in = True


        if cell_in:
            self.cells.remove(cell_to_remove)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        cell_in = False

        if cell in self.cells:
            cell_to_remove = cell
            cell_in = True

        if cell_in:
            self.cells.remove(cell_to_remove)


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
        def clean_knowledge(self):
            """
            Removes sentences from knowledge where the set of cells is empty, deleting useless sentences.
            """
            sentences_to_remove = []
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    sentences_to_remove.append(sentence)
            for sentence in sentences_to_remove:
                self.knowledge.remove(sentence)

        def infere_knowledge(self):
            """
            Performs all possible inferences given the current knowledge.
            """
            # As long as some inference is made, the loop will continue.
            infered = True
            while infered:
                infered = False
                for sentence in self.knowledge:
                    # Get the safe cells
                    if sentence.count == 0 and len(sentence.cells) != 0:
                        cells_to_update = set()
                        for cell in sentence.cells:
                            cells_to_update.add(cell)
                        for cell in cells_to_update:
                            self.mark_safe(cell)
                        infered = True
                    # Get the cells which have mines
                    elif sentence.count == len(sentence.cells) and len(sentence.cells) != 0:
                        cells_to_update = set()
                        for cell in sentence.cells:
                            cells_to_update.add(cell)
                        for cell in cells_to_update:
                            self.mark_mine(cell)
                        infered = True

                    # Add sentences based on subsets of the cells
                    for i in range(len(self.knowledge)):
                        for j in  range(len(self.knowledge)):
                            if j != i:
                                if self.knowledge[j].cells.issubset(self.knowledge[i].cells):
                                    new_sentence = Sentence(self.knowledge[i].cells - self.knowledge[j].cells, self.knowledge[i].count - self.knowledge[j].count)
                                    if new_sentence not in self.knowledge and len(self.knowledge[i].cells - self.knowledge[j].cells) != 0:
                                        self.knowledge.append(new_sentence)
                                        infered = True
                clean_knowledge(self)

        # Add the cell to the moves made and mark the cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Create a new sentence. If the set of cells is not empty and isn't already in the knowledge, it will be added to the knowledge.
        cells = set()
        known_mines_counter = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) != cell:
                    if 0 <= i < self.height and 0 <= j < self.width:
                        # If we know that some cell is a mine, the new sentence count will be updated.
                        if (i,j) in self.mines:
                            known_mines_counter += 1
                        # Add cells that we do not have any information about.
                        elif (i,j) not in self.safes and (i,j) not in self.mines:
                            cells.add((i,j))

        if Sentence(cells, count) not in self.knowledge and len(cells) != 0:
            self.knowledge.append(Sentence(cells, count - known_mines_counter))

        infere_knowledge(self)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) != 0:
            for safe_cell in self.safes:
                if safe_cell not in self.moves_made:
                    return safe_cell
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = []

        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    moves.append((i,j))
        if len(moves) != 0:
            move = moves[random.randint(0, len(moves) - 1)]
            self.moves_made.add(move)
            return move
        return None