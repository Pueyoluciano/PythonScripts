import Tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

canvas.create_circle(100, 120, 50, fill="#0F0")

root.wm_title("Circlulos")
root.mainloop()