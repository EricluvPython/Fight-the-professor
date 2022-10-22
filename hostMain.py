from host import *

wnd = tkinter.Tk()
wnd.geometry("800x600")
wnd.title("Fight the Professor!")
#wnd.resizable(0,0)
loginGUIObj = loginGUI(wnd)
wnd.mainloop()