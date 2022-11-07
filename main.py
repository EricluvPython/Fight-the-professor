import tkinter
import tkinter.font as font
import host
import client
import single
from GameEngine import Game


def goMulti(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("Fight the Professor!")
    mainframe = tkinter.Frame(wnd)
    mainframe.pack()
    lab = tkinter.Label(
        mainframe, text="Choose whether you're a\n host or a client:\n")
    lab['font'] = font.Font(size=20)
    lab.pack()
    btn1 = tkinter.Button(mainframe, text="Play as host",
                          width=18, height=5, command=lambda: goHost(wnd))
    btn1['font'] = font.Font(size=14)
    btn1.pack()
    btn2 = tkinter.Button(mainframe, text="Play as client",
                          width=18, height=5, command=lambda: goClient(wnd))
    btn2['font'] = font.Font(size=14)
    btn2.pack()
    wnd.mainloop()


def goHost(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("Fight the Professor!")
    #wnd.resizable(0, 0)
    loginGUIObj = host.loginGUI(wnd)
    wnd.mainloop()


def goClient(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("Fight the Professor!")
    wnd.resizable(0, 0)
    loginGUIObj = client.loginGUI(wnd)
    wnd.mainloop()


def goSolo(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("Fight the Professor!")
    wnd.resizable(0, 0)
    game = Game('human', 'AI1', 'AI2')
    singleGUIObj = single.singleGUI(game)
    wnd.mainloop()


def goHome(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("Fight the Professor!")
    mainframe = tkinter.Frame(wnd)
    mainframe.pack()
    titleLab = tkinter.Label(mainframe, text="Fight the Professor!")
    titleLab['font'] = font.Font(size=24, weight='bold', slant='italic')
    titleLab.pack()
    lab = tkinter.Label(mainframe, text="Choose the game mode:\n")
    lab['font'] = font.Font(size=20)
    lab.pack()
    btn1 = tkinter.Button(mainframe, text="Multiplayer",
                          height=5, width=15, command=lambda: goMulti(wnd))
    btn1['font'] = font.Font(size=14)
    btn1.pack()
    btn2 = tkinter.Button(mainframe, text="Single Player",
                          height=5, width=15, command=lambda: goSolo(wnd))
    btn2['font'] = font.Font(size=14)
    btn2.pack()
    wnd.mainloop()


if __name__ == '__main__':
    goHome()
