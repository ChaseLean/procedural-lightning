from tkinter import Tk, Canvas
from pygame import mixer
from random import random, choice
from math import sin, cos, pi, exp


class Lightning:
    def __init__(self, strength, x, y, slant=0, branch=False, master=None):
        self.master = master
        self.path = [[x, y]]

        for i in range(1, 500):

            radius = 5 * random()
            angle = ((120 * random() - 60) + 20 * slant) * pi / 180

            x_new, y_new = self.rotate(self.path[i - 1][0], self.path[i - 1][1], radius, angle)
            self.path.append([x_new, y_new])

            branch_slant = choice([-1.5, -1, 1, 1.5])
            if not branch:
                if random() < 0.01 - len(self.path) / 30000:
                    slant += branch_slant
                if slant and random() < 0.01 * abs(slant):
                    slant /= 3
                if random() < 0.075 and y_new < 175:
                    Lightning(strength / 2, x_new, y_new, slant + branch_slant, True, self.master)

            if branch:
                if strength >= 1:
                    if 1000 * random() < len(self.path):
                        Lightning(strength - strength / 5, x_new, y_new, slant - branch_slant, True, self.master)
                        Lightning(strength - strength / 2, x_new, y_new, slant + branch_slant, True, self.master)
                        break
                    elif random() < 0.025:
                        strength -= strength / 5
                elif 5000 * random() < 1 + 4 * len(self.path):
                    break

            if y_new > 350:
                Reflection(x_new - 5, y_new + 3, 0, strength, slant, self.master)
                break

        alpha = abs(-(exp(-strength) - 1))
        self.bolt = self.master.create_line(self.path, fill=transparency(self.master, alpha), width=strength, smooth=True)
        self.master.after(50, lambda: self.fade(alpha - 0.3 / (strength + 1)))

    def fade(self, alpha):
        if alpha <= 0.1:
            self.master.delete(self.bolt)
            return
        self.master.itemconfig(self.bolt, fill=transparency(self.master, alpha))
        self.master.after(75, lambda: self.fade(alpha))
        alpha = 0.75 * alpha

    def rotate(self, x, y, radius, angle):
        x_prime = - radius * sin(angle)
        y_prime = radius * cos(angle)
        return x + x_prime, y + y_prime


class Reflection:
    def __init__(self, x, y, count, strength, slant, master=None):
        self.master = master
        self.total_ref = 40

        alpha = 0.4 * (strength + 10) / 16 * (self.total_ref - count / 2) / self.total_ref
        opacity = transparency(self.master, alpha)

        self.reflection = self.master.create_line(0, 0, min(20, 4 * strength) + 0.3 * count, 0, fill=opacity, width=min(4, strength))
        self.master.move(self.reflection, x + (0.5 * slant * count) + count * (random() - 0.5), y + 4 * count)
        self.fade(alpha, 0)

        if count < self.total_ref:
            count += 1
            Reflection(x, y, count, strength, slant, self.master)

    def fade(self, alpha, frame):
        if frame > 4:
            self.master.delete(self.reflection)
            return
        self.master.itemconfig(self.reflection, fill=transparency(self.master, alpha))
        self.master.after(100, lambda: self.fade(alpha * 0.9, frame + 1))


def transparency(c, alpha):
    background = int(c['background'].strip('gray')) / 100
    opacity = int((alpha + (1 - alpha) * background) * 100)
    opacity_string = 'gray' + str(opacity)
    return opacity_string


def main():
    def summon_lightning(event):
        canvas.itemconfig(instructions, state="hidden")
        strength = exp(2 * random())
        x_position = 600 * random() + 200
        y_position = -100
        Lightning(strength, x_position, y_position, 0, False, canvas)
        thunder.set_volume(strength / 7)
        thunder.play()

    root = Tk()
    root.geometry("1000x500")
    root.title("Lightning Generator")
    canvas = Canvas(root, width=1000, height=500)
    canvas.configure(bg="gray0")
    canvas.pack()

    mixer.init()
    thunder = mixer.Sound("Files\\thunder.mp3")
    root.bind("<Button-1>", summon_lightning)
    instructions = canvas.create_text(500, 200, text="Click anywhere on the screen\nto summon a bolt of lightning.",
                                      font=('Corbel', 20), fill="white")
    root.mainloop()


if __name__ == '__main__':
    main()
