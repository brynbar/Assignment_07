#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BDunbar, 2020-Feb-29, Modified code, completed the Assignment 06 TODO'S
# DKlos, 2020-Mar-2, Refactored add_cd
# BDunbar, 2020-Mar-5, Modified code, Added structured error handling and usage of binary data for Assignment 07
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Processing CD information: adding or deleting cd entries"""  
    
    @staticmethod
    def add_cd(cd_id, cd_title, cd_artist, table):
        """Function to add cd entries to the inventory

        Args:
            cd_id (string): ID for the cd
            cd_title (string): Title of the new CD
            cd_artist (string): Artist of the new CD
            table (list of dict): a list of dictionaries (2D structure) for the cd inventory

        Returns:
            table (list of dict): a list of dictionaries (2D structure) for the cd inventory, after data has been added
        """
        # 3.3.2 Add item to the table
        dicRow = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        table.append(dicRow)
        return table

    @staticmethod
    def remove_cd(table, cd_id):
        """Function to remove cd entries from the inventory

        Args:
            table (list of dict): a list of dictionaries (2D structure) for the cd inventory
            cd_id: the ID of the cd to be removed

        Returns:
            table (list of dict): a list of dictionaries (2D structure) for the cd inventory after, data has been removed
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == cd_id:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return table

class FileProcessor:
    """Processing the data to and from text file"""

    #TODOne - Unpickle Data that is read from CD Inventory binary file
    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        """
        
        try:
            table.clear() # clears existing data and allows to load from file
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile)
        except FileNotFoundError:
            print("The file {} could not be loaded, because it could not be found.\n".format(file_name))
        
        return table

    #TODOne - Pickle the CD Inventory Data
    @staticmethod
    def write_file(file_name, table):
        """Function to write data to the CD Inventory file, saving the data to the file
        
        Args:
            file_name: name of file that the data is saved to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        objFile = open(strFileName, 'wb')
        pickle.dump(table, objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice


    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def get_cd_info():
        """Gets information for a new cd entry
        
        Args:
            None.
            
        Returns:
            item_id (string): ID for the cd
            item_title (string): Title of the new CD
            item_artist (string): Artist of the new CD
        """
        # TODOne - Add Structured Error Handling
        item_id = input('Enter ID: ').strip()
        while True:
            try:
                int(item_id)
                break
            except ValueError:
                item_id = input('\nOops! That is not a number. Please enter a numeric ID: ').strip()
            
        item_title = input('What is the CD\'s title? ').strip()
        item_artist = input('What is the Artist\'s name? ').strip()
        return item_id, item_title, item_artist

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...\n')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.3 process add a CD
    elif strChoice == 'a':
        # # 3.3.1 Ask user for new ID, CD Title and Artist
        lstTbl = DataProcessor.add_cd(*IO.get_cd_info(), lstTbl)

        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        # TODOne - Add Structured Error Handling
        intIDDel = input('Which ID would you like to delete? ').strip()
        while True:
            try:
                int(intIDDel)
                break
            except ValueError:
                intIDDel = input('\nOops! That is not a number. Please enter a numeric ID: ').strip()
                
        # 3.5.2 search thru table and delete CD
        lstTbl = DataProcessor.remove_cd(lstTbl, intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
