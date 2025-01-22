import time

# A basic program meant to solve given sudoku puzzles.

# Prints the current board into the console.
# This will be used to show what is happening to the user.
def print_board():
    print('-------------------------------------')

    for y in range(len(board)):
        for x in range(len(board[y])):
            print( '|', end = '' )

            # Adds a bit of a checkerboard pattern, for improved readability.
            if (x < 3 or 5 < x) != (y < 3 or 5 < y):
                print( ' ', board[y][x], ' ', end = '', sep = '' )
            else:
                print( "-", board[y][x], "-", end = '', sep = '' )
        print( '|' )
        print('-------------------------------------')


# Returns True if a given group of 9 tiles
# (row, column, or 3x3 region)
# contains a given value.
def group_contains( group, n ):
    # y indicates the x-position of the column.
    # n indicates the sought value.
    for tile in group:
        if board[tile[0]][tile[1]] == n:
            return True
    return False


# Returns True if a given group
# contains a given set of tiles
# (defined by their x and y positions).
def group_contains_tiles( group, tiles ):
    for tile in tiles:
        if not group.__contains__(tile):
            return False
    return True


# Returns the 3x3 region that contains the given tile.
def get_tile_region( tile ):
    return regions[ ( int(y / 3) * 3 ) + int(x / 3) ]


# Returns True if the board has been solved correctly.
def verify_board():
    # Checks to make sure that each group follows the rules.
    for i in range(len(groups)):

        group = groups[i]
        
        for n in range(1, 10):
            if not group_contains(group, n):
                # The group doesn't contain the value,
                # meaning the board does not conform to the rules
                # and was solved incorrectly.
                return False
    return True


# Creates a new board (a double list of int values)
# using a given string.
def create_board( numbers ):
    new_board = [ [ 0 for x in range(1, 10) ] for y in range(1, 10) ]

    # Loads the board from a single giant number.
    for y in range(len(new_board)):
        for x in range(len(new_board[y])):
            new_board[y][x] = int(numbers[ (y * 9) + x ])
    

    # Goes through and replaces all '0's with ' '.
    # This makes it much easier to read if printed.
    for y in range(len(new_board)):
        for x in range(len(new_board[y])):
            if new_board[y][x] == 0:
                new_board[y][x] = ' '

    return new_board


# According to the rules of sudoku,
# in each 9-tile group of row, columns, and 3x3 regions
# there must be exactly 1 of each 1-9 value.
# As such, the program will establish those groups initially
# and apply various rules to them in order to solve the puzzle.

# Organizes the "rows" group type.
rows = [ [ [ y, x ] for x in range(9) ] for y in range(9) ]
# Organizes the "columns" group type.
columns = [ [ [ y, x ] for y in range(9) ] for x in range(9) ]

# Organizes the "regions" group type.
regions = [ [] for y in range(9) ]
current_region = 0
for region_y in range(3):
    for region_x in range(3):
        for y in range( region_y * 3, region_y * 3 + 3 ):
            for x in range( region_x * 3, region_x * 3 + 3 ):
                regions[current_region].append( [ y, x ] )
        current_region = current_region + 1

# Combines all rows, columns, and regions
# into a single list of groups.
groups = []
for group in rows:
    groups.append(group)
for group in columns:
    groups.append(group)
for group in regions:
    groups.append(group)

# These variables are explained in the "create_board" method.
board = None
restricted_values = None

confusion = 0
confusion_limit = 12

highest_confusion = 0

made_progress = False


# If true, will print out the algorithm's iterative process for each sudoku.
show_process = False
# If true, after solving a puzzle,
# will output the initial puzzle, its solution, and an approximate difficulty.
show_results = False


# Apples some basic logical rules about sudoku
# to add restricted values to some tiles,
# which will narrow down what possible values it can have.

# Takes in a "recursion" value as well;
# each time the method calls itself,
# the recursion value will be 1 lower,
# and it will not call itself anymore if the recursion is 0.
# This helps to decrease the time it takes,
# and prevents it from exceeding the recursion limit.
def process_board(recursion):

    global board
    global restricted_values
    global confusion
    global confusion_limit

    global made_progress

    if confusion == 0 or confusion == confusion_limit:

        # Rule 1:
        # A tile cannot contain a value
        # that already exists in the same row, column, or 3x3 group.

        # Look at how neat and simple this is!
        for group in groups:
            for tile in group:
                if board[tile[0]][tile[1]] == ' ':
                    for n in range(1, 10):
                        if group_contains(group, n):        
                            if not restricted_values[tile[0]][tile[1]].__contains__(n):
                                restricted_values[tile[0]][tile[1]].append(n)
                                made_progress = True

    if confusion == 1 or confusion == confusion_limit:

        # Rule 2:
        # if, in a given group,
        # there is only 1 space that can legally contain a given value,
        # then that value must be placed in that space.

        # For each group.
        for group in groups:
            # Establishes values that are present in the group.
            # These values do not need to be evaluated.
            values_present = []
            for tile in group:
                value = board[tile[0]][tile[1]]
                if value != ' ' and not values_present.__contains__(value):
                    values_present.append(value)
            
            # For each value from 1-9.
            for n in range(1, 10):
                # Determines all empty spaces in the group that could possibly contain this value.
                possible_spaces = []

                for tile in group:
                    value = board[tile[0]][tile[1]]
                    if value == ' ' and not restricted_values[tile[0]][tile[1]].__contains__(n):
                        possible_spaces.append( tile )

                
                # If there is only 1 space, then that tile must have this value.
                if len(possible_spaces) == 1:
                    chosen_tile = possible_spaces[0]

                    restricted_values[chosen_tile[0]][chosen_tile[1]] = []
                    for m in range(1, 10):
                        if m != n:
                            restricted_values[chosen_tile[0]][chosen_tile[1]].append(m)

                    # Then updates all other tiles in the same group, adding this value as a restricted value.
                    for tile in group:
                        # Excludes the nominated tile.
                        if [tile[0], tile[1]] != [chosen_tile[0], chosen_tile[1]] and not restricted_values[tile[0]][tile[1]].__contains__(n):
                            restricted_values[tile[0]][tile[1]].append(n)

                            made_progress = True


    if confusion == 2 or confusion == confusion_limit:

        # Rule 3 and 4:
        # If it is determined that, within a group (row, column, region),
        # there are only 2 or 3 empty tiles that can legally contain a particular value,
        # and they all overlap a group of a different type (row, column, region),
        # it can be inferred that no other tile in that row/column can contain that value.
        
        # Should compare all group types with other group types.
        # Except for rows with columns.
        # They only ever intersect at a single point.
        
        # For each group.
        # Assesses group A to find all empty tiles that can contain a value.
        # If all such tiles intersect with a second group (group B),
        # then for each other tile in group B, adds that value to the tile's restricted values.
        for group in groups:
            # For each 1-9 value.
            for n in range(1, 10):
                # Determines tiles that can legally have that value.
                possible_tiles = []

                # Checks each tile in the group.
                # If the tile is empty and can contain the current value,
                # it is added to the list of possible tiles.
                for tile in group:
                    value = board[tile[0]][tile[1]]
                    if value == ' ' and not restricted_values[tile[0]][tile[1]].__contains__(n):
                        possible_tiles.append( tile )
                

                # If there are 2-3 possible tiles, then proceeds to see if they intersect with another group (of a different type).
                # If there's only 1 possible tile, then it will already be given that value, because of Rule 2, so no further steps are needed.
                # If there are more than 3 possible tiles, then those tiles can't all possibly intersect with another group.
                        
                if len(possible_tiles) == 2 or len(possible_tiles) == 3:
                    # Figures out if all of the tiles intersect with a different group type.
                    # To do this, finds another group that intersects with the first tile.
                    # Then checks if all tiles intersect with that group.
                    overlap_group = None

                    # Checks if all tiles are in the same row, or column, or region as the first tile,
                    # and that it's a different group than the one currently being evaluated.
                    if group != rows[tile[0]] and group_contains_tiles( rows[tile[0]], possible_tiles ):
                        # Tiles share same row.
                        overlap_group = rows[tile[0]]
                    elif group != columns[tile[1]] and group_contains_tiles( columns[tile[1]], possible_tiles ):
                        # Tiles share same column.
                        overlap_group = columns[tile[1]]
                    else:
                        region = get_tile_region(possible_tiles[0])
                        if group != region and group_contains_tiles( region, possible_tiles ):
                            # Tiles share same column.
                            overlap_group = region
                    
                    if not overlap_group == None:

                        # The possible tiles overlap with another group.
                        # meaning no other tile in that other group can have the evaluated value.

                        # Goes through every other tile in the group,
                        # setting its restricted values to be the current value.

                        for tile in overlap_group:
                            # Ensures that this tile isn't one of the possible tiles.
                            if not possible_tiles.__contains__(tile) and board[tile[0]][tile[1]] == ' ' and not restricted_values[tile[0]][tile[1]].__contains__(n):
                                
                                restricted_values[tile[0]][tile[1]].append(n)
                        
                                made_progress = True
    
    
    if confusion == 3 or confusion == confusion_limit:
        # Rule 5:
        # If in a given row, column, or group,
        # there are n tiles, which share between them a number of values equal to n,
        # those values being ones that no other tiles in that row, column, or group can contain,
        # then those tiles cannot contain any other value,
        # and thus can have those values restricted for them.

        # For each group.
        for group in groups:

            # This tracks the sets of tiles that can contain a value.
            # Index 0 of this list tracks all tiles that can contain a 1,
            # Index 1 counts tiles that can contain a 2, etc.
            # It's a bit confusing that they're offset, but that's how lists work I guess.
            sets = [[] for i in range(9)]

            # For each 1-9 value.
            for n in range(1, 10):
                for tile in group:
                    if board[tile[0]][tile[1]] == ' ' and not restricted_values[tile[0]][tile[1]].__contains__(n):
                        sets[n - 1].append( tile )
            
            # Now that the sets are established,
            # determines if there are any matching sets.
            # For each set, establishes its length.
            # Now if there are n sets, each of length n, that contain the same tiles,
            # then this rule applies.
            
            # Goes through each set.
            # Adds its own index number (+1) to a list.
            # That set will compare itself to other sets.
            # If it finds a set that has the exact same tiles as itself, will add that set's index number (+1) to a list.
            # If the length of that list reaches the set's length, then that means that according to rule 5,
            # those tiles cannot be anything except for any of the values in the list.
            # As such, will set their restricted values to be every other value.
                        
            # The last set in the list will have already been compared with every other,
            # so there's no point in analyzing it.
            for i in range(len(sets) - 1):

                current_set = sets[i]

                # If the length of the set is one,
                # that means that that there is only 1 tile that can have that value.
                # But according to Rule 2, that tile already will have every other value as restricted.
                # So nothing needs to be done.
                if len(current_set) > 1:

                    # Tracks what values are in the current set of tiles,
                    # which of course includes the set's initial value.
                    set_values = [ i + 1 ]

                    # Goes through later sets and compares them to self.
                    # Doesn't need to go to earlier sets, because those sets would've already compared themselves to this one.

                    for j in range( i + 1, len(sets) ):
                        if current_set == sets[j]:
                            # Matching set found.
                            set_values.append( j + 1 )
                            # Also erases the set, it won't be needed again.
                            sets[j] = []

                    # If the length of set_values equals the length of the set,
                    # applies Rule 5 by setting the set's restricted tiles to be every other value
                    # not included in set_values.
                    
                    if len(set_values) == len(current_set):
                        # The length of values contained by each tile in the current set
                        # exactly matches the number of tiles.
                        # That means that each tile must occupy one of those values,
                        # and thus cannot occupy any others.

                        # Sets list of restricted values to be given to all tiles in set.
                        non_set_values = []
                        for n in range(1, 10):
                            if not set_values.__contains__(n):
                                non_set_values.append(n)

                        # Gives the set of restricted values to all tiles in set.
                        for tile in current_set:
                            for n in non_set_values:
                                if not restricted_values[tile[0]][tile[1]].__contains__(n):
                                    restricted_values[tile[0]][tile[1]].append(n)
                        
                                    made_progress = True
                            
    
    if confusion == 4 or confusion == confusion_limit:
        # Rule 6:
        # If, within a row, column, or group,
        # there are n number of tiles, each of which can only contain
        # n possible values, and this set of values is the same among
        # all of these tiles, then not only can those tiles not have any other value,
        # but no other tile can have those values.
              
        # For each group.
        for group in groups:
            # Tries to match tiles with other ones that have the exact same restricted values.
            # (Same as having the same allowed values, which is what we're doing)

            for i in range(len(group)):
                tile = group[i]

                if board[tile[0]][tile[1]] == ' ':
                    # Tracks all tiles that match with this one,
                    # including this one.
                    matching_tiles = [ tile ]

                    # Only compares itself to tiles later in the array,
                    # since it will have already been compared to earlier ones.
                    for j in range( i + 1, len(group) ):
                        tile2 = group[j]
                        if board[tile2[0]][tile2[1]] == ' ' and restricted_values[tile[0]][tile[1]] == restricted_values[tile2[0]][tile2[1]]:
                            matching_tiles.append( tile2 )
                    
                    # If the list of matching tiles is as long as the list of permitted values
                    # (just 9 - length of restricted values),
                    # then no other tiles within the row can be that value.
                    if len(matching_tiles) == 9 - len(restricted_values[tile[0]][tile[1]]):
                        
                        # Goes through each other tile in the group,
                        # adding the unrestricted values to those tile's restricted values.
                        for n in range( 1, 10 ):
                            if not restricted_values[tile[0]][tile[1]].__contains__(n):
                                # This value can only exist within the matching tiles,
                                # meaning it should be restricted for all other tiles.
                                for tile2 in group:
                                    # Ensures that it is not one of the matching tiles.
                                    if not matching_tiles.__contains__( tile2 ) and not restricted_values[tile2[0]][tile2[1]].__contains__(n):
                                        restricted_values[tile2[0]][tile2[1]].append(n)
                        
                                        made_progress = True


    if made_progress == False and confusion >= 5 and recursion > 0:
        # Rule 7:
        # If any value that a given empty tile A could contain
        # would inevitably lead to a given tile B having the same value,
        # then that tile B must have that value.

        # Copies the current board and stores it here.
        # Because it will be creating hypothetical boards that aren't necessarily correct,
        # it will need a way to revert the changes.
        previous_board = []
        for row in board:
            previous_board.append( row.copy() )

        previous_restricted_values = [ [ [] for i in range(1, 10) ] for j in range(1, 10) ]
        for y in range(len(restricted_values)):
            for x in range(len(restricted_values[y])):
                previous_restricted_values[y][x] = restricted_values[y][x].copy()

        previous_confusion = confusion

        # Tracks if, throughout this process,
        # any progress was made.
        # The original made_progress can't be used,
        # since it will have its value overwritten while simulating hypothetical values.
        made_progress2 = False

        # For each tile that has 2-3 possible values.
        for y in range(len(board)):
            for x in range(len(board[y])):
                # Only checks tiles with a specific number of unrestricted values,
                # which increases as confusion increases.
                # This is done to save time;
                # a tile with fewer possible values is far more likely to lead to a conclusive result.

                unrestricted_values_target = previous_confusion - 3
                
                if made_progress2 == False and board[y][x] == ' ' and 9 - len(restricted_values[y][x]) == unrestricted_values_target:
                    # For each possible value that this tile can have,
                    # sets the tile to be that value,
                    # then evaluates the board for a while.

                    hypothetical_boards = []
                    hypothetical_restricted_value_sets = []

                    for n in range(1, 10):

                        if not restricted_values[y][x].__contains__(n):
                            # The tile might contain this value, so puts the value in that tile, and just sees what happens I guess.

                            board[y][x] = n

                            confusion = 0

                            # Evaluates the hypothetical board for a while until it gets confused.
                            while confusion <= confusion_limit:

                                process_board(recursion - 1)

                                place_values( False, False )
                                made_progress = False

                            hypothetical_boards.append(board)
                            hypothetical_restricted_value_sets.append(restricted_values)
                            
                            # Resets the board and restricted values to how they were previously.
                            board = []
                            for row in previous_board:
                                board.append( row.copy() )
                            
                            restricted_values = [ [ [] for i in range(1, 10) ] for j in range(1, 10) ]
                            for y2 in range(len(previous_restricted_values)):
                                for x2 in range(len(previous_restricted_values[y2])):
                                    restricted_values[y2][x2] = previous_restricted_values[y2][x2].copy()

                    confusion = previous_confusion

                    # For each tile that was previously empty,
                    # evaluates it in all new board configurations.
                    # If it has the same value for each of those,
                    # then it must be that value.

                    for y2 in range(len(board)):
                        for x2 in range(len(board[y2])):
                            if board[y2][x2] == ' ':
                                # I don't think that this can be optimized in any significant capacity.

                                # Tile was previously empty.
                                # Now gets all values that it was given in the hypothetical boards.
                                # If they're all the same, then it must be given that value, for reals.
                                
                                hypothetical_values = []
                                for hypothetical_board in hypothetical_boards:
                                    
                                    hypothetical_values.append( hypothetical_board[y2][x2] )
                                
                                values_conclusive = True

                                for value in hypothetical_values:
                                    if value == ' ' or not value == hypothetical_values[0]:
                                        values_conclusive = False
                                        break

                                if values_conclusive:
                                    # Regardless of the values that the first tile can have,
                                    # tile B will always have a certain value.
                                    # Thus, tile B must have that value.

                                    # So sets all other values to be restricted for it.
                                    for n in range ( 1, 10 ):
                                        if not n == hypothetical_values[0] and not restricted_values[y2][x2].__contains__(n):
                                            restricted_values[y2][x2].append(n)

                                    # This seems to have helped.
                                    made_progress2 = True


                    # Rule 8:
                    # If a tile being given a value would necessarily to the board being illogical,
                    # then the tile cannot have that value.

                    # Looks at all of the hypothetical boards.
                    # If the board is found to not make sense
                    # (any tile has 9 restrictions),
                    # then the current tile cannot have the value it has in this board.

                    for i in range(len(hypothetical_boards)):

                        hypothetical_board = hypothetical_boards[i]
                        hypothetical_restricted_values = hypothetical_restricted_value_sets[i]

                        for y2 in range(len(hypothetical_restricted_values)):
                            for x2 in range(len(hypothetical_restricted_values[y2])):
                                if hypothetical_board[y2][x2] == ' ' and len(hypothetical_restricted_values[y2][x2]) == 9:
                                    # This tile has 9 restricted values,
                                    # therefore the board is illogical,
                                    # therefore the currently evaluated tile
                                    # cannot have the tested value.

                                    tested_value = hypothetical_board[y][x]
                                    if not restricted_values[y][x].__contains__(tested_value):
                                        restricted_values[y][x].append(tested_value)

                                    made_progress2 = True
                    
                    # Resets previous lists to reflect new changes,
                    # in case there were any.
                    previous_restricted_values = [ [ [] for i in range(1, 10) ] for j in range(1, 10) ]
                    for y2 in range(len(restricted_values)):
                        for x2 in range(len(restricted_values[y2])):
                            previous_restricted_values[y2][x2] = restricted_values[y2][x2].copy()

                    # If a value was found,
                    # then exits rule 7/8 code,
                    # so that it can attempt the other rules first.
                    # Because it's likely that the other rules will be able to do some work from there.

        board = previous_board
        restricted_values = previous_restricted_values
        confusion = previous_confusion

        if made_progress2:
            made_progress = True


# Using the restricted values,
# determines what empty tiles to fill in values for.

# The change_difficulty variable is used to determine whether or not 
# the program should update the highest_confusion value.

# This is because when this function is called in the rule 7/8 section,
# it is guaranteed to have its confusion reach 10 at some point while evaluating the hypothetical boards,
# so that should not affect the highest_confusion value or else it would not be accurate.

def place_values( show_process, change_difficulty ):

    global confusion
    global confusion_limit
    global highest_confusion
    global made_progress

    # Assigns values to tiles based on the tile's restricted values.
    for y in range(len(board)):
        for x in range(len(board[y])):
            # If the tile has 8 restricted values, then it can be solved,
            # because only 1 value can possibly remain.
            if board[y][x] == ' ' and len(restricted_values[y][x]) == 8:

                # Finds value not included in restricted values,
                # and gives the tile that value.
                for n in range( 1, 10 ):
                    if not restricted_values[y][x].__contains__(n):
                        board[y][x] = n
                        
                        made_progress = True

                        if show_process:
                            print( 'Placed value ', n, ' in tile (', x, ',', y, ')', sep='' )

                        break
    
    # If the program has not made any progress in solving the puzzle,
    # the confusion counter will increase,
    # so that it will try more complex solving methods in the next iteration.

    # Or, if it did make progress,
    # its confusion will return to 0,
    # so that it may now apply the faster rules with the newly-gathered information.
    if not made_progress:
        confusion = confusion + 1
    else:
        confusion = 0

    if change_difficulty and confusion > highest_confusion and confusion <= confusion_limit:
        highest_confusion = confusion

# Solves a given puzzle and returns the solution.
def solve_board( start_board_string ):

    global board
    global restricted_values
    global confusion
    global confusion_limit
    global highest_confusion
    global made_progress

    # Tracks how many iterations of the while-loop have occurred.
    iteration = 1

    # Creates a new board using the given string.
    board = create_board(start_board_string)

    # This will track the current restricted values
    # that each tile has been determined to have.
    # This is how the program is able to narrow down what each empty tile can be,
    # so that it can solve the puzzle.
    restricted_values = [[ [] for x in range(1, 10)] for y in range(1, 10)]

    # The confusion value tracks if the AI has been stumped and does not know how to advance.
    # Whenever the AI gets through a whole iteration without making any progress
    # (meaning it was not able to establish a new value or a new restricted value for any tile),
    # its confusion will go up by 1.

    # The more confused the AI gets, the more complex its strategies will be.
    # This means that when the sudoku is easier,
    # it will not waste time with unnecessarily complex strategies.
    confusion = 0

    # Also tracks the highest that confusion ever gets.
    # This allows the AI to give a vaguely accurate difficulty rating.
    highest_confusion = 0

    if show_process:
        print( 'Starting board' )
        print_board()

    while not verify_board() and confusion < confusion_limit:
        # For each iteration,
        # tracks if the program made any progress in solving the puzzle.
        made_progress = False

        if show_process:
            print()
            print( 'Beginning iteration #', iteration )
            print( 'confusion: ', confusion, '/', confusion_limit, sep = '' )

        process_board(3)

        place_values( show_process, True )
        
        if show_process:
            # For debug purposes,
            # sets any empty tile with exactly 7 restricted values as '?'.
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x] == ' ' and len(restricted_values[y][x]) == 7:
                        board[y][x] = '?'

            # If confusion isn't 0, that means no changes were made,
            # so it's not necessary to redraw the board.
            if confusion == 0:
                print_board()

            # Un-question-marks board.
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x] == '?' or board[y][x] == 0:
                        board[y][x] = ' '
            
            iteration = iteration + 1

    verification = verify_board()

    
    # Must convert solution to a single 81-digit string.
    final_board_string = ''
    if verification:
        for row in board:
            for tile in row:
                final_board_string = final_board_string + str(tile)
    else:
        # The board was not solved properly,
        # so returns just a question mark.

        # Given the high effectiveness of this program,
        # it's likely that either the sudoku wasn't solable in the first place,
        # it has multiple possible solutions (which shouldn't be the case),
        # or it requires an absurd amount of brute force to solve.
        final_board_string = '?'

    if show_results:
        # If show_results is true,
        # prints the puzzle and the solution.
        print()
        print( 'puzzle:   ', start_board_string )
        print( 'solution: ', final_board_string )
        difficulty_rating = 'very hard'
        if highest_confusion <= 1:
            difficulty_rating = 'very easy'
        elif highest_confusion == 2:
            difficulty_rating = 'easy'
        elif highest_confusion == 3:
            difficulty_rating = 'medium'
        elif highest_confusion == 4:
            difficulty_rating = 'hard'

        print( 'difficuly: ', highest_confusion, '/', confusion_limit, ' (', difficulty_rating, ')', sep='' )
        print()
        print()

    return final_board_string

# Will solve a certain range of puzzles,
# given the starting index and the number of puzzles.
def solve_from_puzzles_file( start_index, puzzle_quota, write_to_file ):
    if puzzle_quota < 1:
        return

    # Times the process.
    from datetime import datetime
    start_time = datetime.now()

    if write_to_file:
        # Gets the last line of the solutions file,
        # so that it can add another enter to the end of the file,
        # 1n case it was mistakenly deleted by the user.
        solutions = open( 'solutions.txt', 'r' )
        last_line = '\n'
        for line in solutions:
            last_line = line
        solutions.close()

        # If True,
        # that means there isn't an empty line at the end like there should be,
        # so adds an enter to the file later.
        # This isn't strictly necessary, but it's probably worth doing
        # as it decreases the chance of the user accidentally breaking something.
        missing_enter = ( not last_line[len(last_line) - 1] == '\n' )


        # Loads the solutions file again,
        # this time being able to write to it.
        solutions = open( 'solutions.txt', 'a' )

        if missing_enter:
            # Adds enter to the end of the file,
            # to prevent possible formatting issues.
            solutions.write( '\n' )


    # Goes through the puzzles file in a linear manner
    # and skips all puzzles before the starting index.
    puzzles = open( 'diabolical.txt', 'r' )

    for i in range( 0, start_index ):
        puzzles.readline()

    # Tracks the number of puzzles attempted,
    # and the number of puzzles solved.
    tried_count = 0
    solved_count = 0

    print()
    print( 'Starting at line:', start_index )
    print( 'Puzzles to solve:', puzzle_quota )
    print()
    print( 'Solving...' )
    print()

    for i in range(0, puzzle_quota):

        line = puzzles.readline()

        if line == '':
            # If the line is empty,
            # then the end of the file was reached.
            print( 'Reached end of file' )
            break

        tried_count = tried_count + 1

        # Tokenizes the string, so that it can access the puzzle.

        sorted = line.split()
        solution = solve_board( sorted[1] )


        # If write_to_file is true,
        # adds a line to the end of the solutions text file.
        if write_to_file:
            new_line = sorted[0] + ' ' + solution + '  ' + sorted[2] + '\n'
            solutions.write( new_line )

        if not solution == '?':
            solved_count = solved_count + 1


    puzzles.close()
    if write_to_file:
        solutions.close()

    print( 'Solving complete' )
    if tried_count > 0:
        print( 'Successfully solved ', solved_count, '/', tried_count, ' correctly', sep='' )
        if write_to_file:
            print( 'Solutions were written to solutions file.' )
    else:
        print( 'Solved 0 puzzles?' )
    print()

    end_time = datetime.now()

    # Prints the total time taken for all puzzles,
    # and the average time per puzzle.
    print( 'Time taken:', ( end_time - start_time ) )
    print( 'Avg time per sudoku:', ( ( end_time - start_time ) / tried_count ) )
    print()


print()
print( "Welcome to Blaykron's Epic Sudoku Algorithm!" )
print()

# Gets user input to determine action.
# Will continue running until the user ends the program.
running = True

while running:

    # Resets whether the process and results should be shown.
    show_process = False
    show_results = False

    input1 = ''
    input_is_valid = False
    while not input_is_valid:
        print( "Please select a command:" )
        print( "1. Input custom sudoku, 2. Solve specified puzzles from file, 3. Proceed through entire file, 4. Quit" )
        input1 = input()
        print()

        if not input1.isdigit():
            print( 'That is not an integer.' )
        elif int(input1) < 0 or int(input1) > 4:
            print( 'That is out of range.' )
        else:
            input_is_valid = True

  
    if input1 == '1':

        # Solves custom puzzle.

        input2 = ''
        input_is_valid = False
        while not input_is_valid:
            print( 'Please input a sudoku (must be 81 digits, containing numbers from 0-9 inclusive).' )
            print( 'Ensure that the sudoku is actually solvable and has exactly 1 possible solution.' )
            input2 = input()
            print()

            if len(input2) != 81:
                print( 'Input is not of correct length.' )
            else:

                input_is_valid = True
                # Checks that each character is an integer from 0-9.
                for char in input2:
                    

                    if char.isdigit() and int(char) >= 0 and int(char) <= 9:
                        # All is well.
                        pass
                    else:
                        print( 'Must only contain values from 0-9.' )
                        input_is_valid = False
                        break
        
        # The inputted sudoku is a valid sudoku puzzle.
        # (that doesn't necessarily mean it's solvable...)

        print( 'Lastly: do you want to see the process?' )

        
        show_results = True

        input3 = ''
        input_is_valid = False
        while not input_is_valid:
            print( '1. Show only results, 2. Show full process' )
            input3 = input()
            print()
            if not input3.isdigit():
                print( 'That is not an integer.' )
            elif int(input3) < 0 or int(input3) > 2:
                print( 'That is out of range.' )
            else:
                input_is_valid = True
        if input3 == '2':
            # Shows only results.
            show_process = True

        
        # Times the process.
        from datetime import datetime
        start_time = datetime.now()
        
        solve_board( input2 )
        
        end_time = datetime.now()
        print( 'Time taken:', ( end_time - start_time ) )
        print()

  
    elif input1 == '2':

        # Solves puzzles without writing them to file.

        print( 'The text file contains 119681 puzzles.' )
        print( 'Specify the starting index, and how many puzzles to solve from there.' )
        
        input2 = ''
        input_is_valid = False
        while not input_is_valid:
            print( 'First, please state the starting puzzle index (0-119680).' )
            input2 = input()
            print()
            if not input2.isdigit():
                print( 'That is not an integer.' )
            elif int(input2) < 0 or int(input2) > 119680:
                print( 'That is out of range.' )
            else:
                input_is_valid = True
        
        # Now has starting position.
        start_index = int(input2)

        input3 = ''
        input_is_valid = False
        while not input_is_valid:
            print( 'Next, please state number of puzzles to be completed (1-', (119681 - start_index), ').', sep='' )
            input3 = input()
            print()
            if not input3.isdigit():
                print( 'That is not an integer.' )
            elif int(input3) < 0 or int(input3) > (119681 - start_index):
                print( 'That is out of range.' )
            else:
                input_is_valid = True
        
        # Will solve this many puzzles, including the one at the starting position.
        puzzle_quota = int(input3)

        
        print( 'Lastly: do you want to see the process?' )

        input4 = ''
        input_is_valid = False
        while not input_is_valid:
            print( '1. Do not show, 2. Show only results, 3. Show full process for each puzzle' )
            input4 = input()
            print()
            if not input4.isdigit():
                print( 'That is not an integer.' )
            elif int(input4) < 0 or int(input4) > 3:
                print( 'That is out of range.' )
            else:
                input_is_valid = True
        if input4 == '2':
            # Shows only results.
            show_results = True
        elif input4 == '3':
            # Shows process and results.
            show_process = True
            show_results = True

        # Solves specified range of puzzles.
        solve_from_puzzles_file( start_index, puzzle_quota, False )

  
    elif input1 == '3':

        # Solves puzzles and writes them to file,
        # if there's space.

        print( 'Will find where the solutions text file left off,' )
        print( 'and will solve from there,')
        print( 'adding the solutions to the solutions text file.')


        # Will start solving puzzles where the solutions text file left off.
        solutions = open( 'solutions.txt', 'r' )
        
        start_index = 0
        last_line = '\n'
        for line in solutions:
            start_index = start_index + 1
            last_line = line
        
        solutions.close()

        if start_index == 119681:
            # The solutions file is full, so this action cannot be taken.
            print()
            print( 'The solutions text file is full; no more puzzles remain to be solved.' )
        else:
            input2 = ''
            input_is_valid = False
            while not input_is_valid:
                print( 'Please state number of puzzles to be completed (1-', (119681 - start_index), ').', sep='' )
                input2 = input()
                if not input2.isdigit():
                    print( 'That is not an integer.' )
                elif int(input2) < 0 or int(input2) > (119681 - start_index):
                    print( 'That is out of range.' )
                else:
                    input_is_valid = True
        
            puzzle_quota = int(input2)

            
            print( 'Lastly: do you want to see the process?' )

            input3 = ''
            input_is_valid = False
            while not input_is_valid:
                print( '1. Do not show, 2. Show only results, 3. Show full process for each puzzle' )
                input3 = input()
                print()
                if not input3.isdigit():
                    print( 'That is not an integer.' )
                elif int(input3) < 0 or int(input3) > 3:
                    print( 'That is out of range.' )
                else:
                    input_is_valid = True
            if input3 == '2':
                # Shows only results.
                show_results = True
            elif input3 == '3':
                # Shows process and results.
                show_process = True
                show_results = True

            # Solves specified range of puzzles,
            # writing the solutions to the attached file.
            solve_from_puzzles_file( start_index, puzzle_quota, True )

  
    elif input1 == '4':
        print( 'Are you sure?' )

    # Asks the user if they want to do something else,
    # or quit the program.
    input5 = ''
    input_is_valid = False
    while not input_is_valid:
        print( '1. Return to menu, 2. Quit program' )
        input5 = input()
        print()
        if not input5.isdigit():
            print( 'That is not an integer.' )
        elif int(input5) < 0 or int(input5) > 2:
            print( 'That is out of range.' )
        else:
            input_is_valid = True
    
    if input5 == '2':
        # Quits the program.

        running = False

        print( 'Thanks for using the program.' )
        print()
