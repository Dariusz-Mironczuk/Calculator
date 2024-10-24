import customtkinter as ctk
import darkdetect
from settings import *
from buttons import Button, NumButton, MathButton
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color= (WHITE, BLACK))

        #Display info
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        middle_screen_width = int((screen_width / 2) - (APP_SIZE[0] / 2))
        middle_sceen_height = int((screen_height / 2) - (APP_SIZE[1] / 2))

        #Setup
        ctk.set_appearance_mode(f'{'dark' if is_dark else 'light'}')
        self.title('')
        self.iconbitmap('empty.ico')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{middle_screen_width}+{middle_sceen_height}')
        self.resizable(False, False)
        self.title_bar_color(is_dark)
        
        #Grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight= 1, uniform= 'a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight= 1, uniform= 'a')

        #Data
        self.result_string = ctk.StringVar(value= '0') 
        self.formula_string = ctk.StringVar(value= '')
        self.display_nums = []
        self.full_operation = []

        #Widgets
        self.create_widgets()


        #Security check
        self.bind('<Escape>', lambda event: self.quit())

        #Run / Main loop
        self.mainloop()

    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMW_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMW_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def create_widgets(self):

        #Fonts
        main_font = ctk.CTkFont(family= FONT, size= NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family= FONT, size= OUTPUT_FONT_SIZE)

        #Output Labels
        OutputLabel(self, 0, 'e', main_font, self.formula_string)  #Formula
        OutputLabel(self, 1, 'e', result_font, self.result_string) #Result

        #Clear button (AC)
        Button(self,
               function = self.clear,
               text = OPERATORS['clear']['text'],
               row = OPERATORS['clear']['row'],
               column = OPERATORS['clear']['col'],
               font = main_font)
        
        #Persentage button
        Button(self,
               function = self.percent,
               text = OPERATORS['percent']['text'],
               row = OPERATORS['percent']['row'],
               column = OPERATORS['percent']['col'],
               font = main_font)
        
        #Invert button
        Button(self,
               function = self.invert,
               text = OPERATORS['invert']['text'],
               row = OPERATORS['invert']['row'],
               column = OPERATORS['invert']['col'],
               font = main_font)
        
        #Number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
               parent = self,
               function = self.num_press,
               text = num,
               row = data['row'],
               column = data['col'],
               font = main_font,
               span = data['span'])
            
        #Math buttons
        for operator, data in MATH_POSITIONS.items():
            MathButton(
               parent = self,
               function = self.math_press,
               text = data['character'],
               operator = operator,
               row = data['row'],
               column = data['col'],
               font = main_font)

    def math_press(self, value):
        current_number = ''.join(self.display_nums)
        
        if current_number:
            self.full_operation.append(current_number)

            if value != '=':
                #Update data
                self.full_operation.append(value)
                self.display_nums.clear()

                #Update output
                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))

            else:
                formula = ' '.join(self.full_operation)
                result = eval(formula)

                #Formating the result
                if isinstance(result, float):
                    
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 4)
                        
                #Update data
                self.full_operation.clear()
                self.display_nums = [str(result)]

                self.result_string.set(result)
                self.formula_string.set(formula)

    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number)

    def clear(self):
        self.result_string.set(0)
        self.formula_string.set('')
        self.display_nums.clear()
        self.full_operation.clear()

    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent_number = current_number / 100

            self.display_nums = list(str(percent_number))
            self.result_string.set(''.join(self.display_nums))

    def invert(self):
        current_number = ''.join(self.display_nums)
        if current_number:

            if float(current_number) > 0:
                self.display_nums.insert(0, '-')
            else:
                del self.display_nums[0]

            self.result_string.set(''.join(self.display_nums))

class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, placement, font, textvariable):
        super().__init__(master= parent, font= font, textvariable = textvariable)

        self.grid(row = row, column = 0, columnspan = 4, sticky = placement, padx = 10)

if __name__ == '__main__':
    calculator = Calculator(True)