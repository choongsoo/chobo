# a variation of intrographics based on PyGame

import traceback
import math
import os.path

class system:
    def __init__(self):
        self.window = None

    @staticmethod
    def extra(command):
        system.error("Call to " + command + " has too many arguments.")

    @staticmethod
    def missing(command):
        system.error("Call to " + command + " doesn't have enough arguments.")

    @staticmethod
    def invalid(argument, value):
        system.error("Invalid " + argument + ": " + str(value))

    @staticmethod
    def immutable(attribute, item):
        system.error("The " + attribute + " of the " + item + " is read-only.")

    @staticmethod
    def error(message):
        print("An error occurred here:")
        for location in reversed(traceback.format_stack()):
            if "chobo.py" not in location:
                print(location, message)
                quit()

# singleton
sys = system()

# check dependency
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
try:
    import pygame
except ImportError:
    system.error("Module \"chobo\" requires module \"PyGame\"")

# default DEBUG is on
DEBUG = True

pygame.init()
pygame.font.init()
pygame.mixer.init()

class window:
    """Simple graphical display."""

    def __init__(self, width=None, height=None, *extra):
        command = "chobo.window(width, height)"

        # Argument existence
        if len(extra) > 0:
            system.extra(command)
            return
        if width is None or height is None:
            system.missing(command)
            return

        if sys.window is not None:
            system.error("You can create only one window.")

        # Argument types
        try:
            width, height = int(width), int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            system.invalid("window dimensions", (width, height))
            return

        self.width = width
        self.height = height

        self.background = [255, 255, 255]

        self.clock = pygame.time.Clock()

        self.fps = 200
        self.tick = 0

        self.shapes = []

        self.timerFunctions = {}

        self.keyFunctions = []

        self.mouseClickFunctions = {}
        self.mouseDragFunctions = {}
        self.mouseDown = {}

        sys.window = self

    def onTimer(self, interval=None, timerFunc=None, *extra):
        """Add a function on a timer"""
        command = "window.onTimer(interval,function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if timerFunc is None or interval is None:
            system.missing(command)
            return
        if interval < 1000 / self.fps:
            system.invalid("interval",interval)
            return

        if interval not in self.timerFunctions:
            self.timerFunctions[interval] = {"lastRun":self.tick, "functions":[]}
        if timerFunc not in self.timerFunctions[interval]["functions"]:
            self.timerFunctions[interval]["functions"].append(timerFunc)

    def offTimer(self, timerFunc=None, *extra):
        """Remove a function on a timer"""
        command = "window.offTimer(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if timerFunc is None:
            system.missing(command)
            return

        for interval in self.timerFunctions:
            if timerFunc in self.timerFunctions[interval]["functions"]:
                self.timerFunctions[interval]["functions"].remove(timerFunc)

    def onMouseClick(self, buttonID, clickFunc, *extra):
        """Assign a function to handle mouse button clicks."""
        command = "window.onMouseClick(buttonID, function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if clickFunc is None:
            system.missing(command)
            return
        try:
            buttonID = int(buttonID)
        except:
            system.invalid("buttonID", buttonID)
            return
        if buttonID < 1 or buttonID > 5:
            system.invalid("buttonID", buttonID)
            return

        if buttonID not in self.mouseClickFunctions:
            self.mouseClickFunctions[buttonID] = []

        if clickFunc not in self.mouseClickFunctions[buttonID]:
            self.mouseClickFunctions[buttonID].append(clickFunc)

    def offMouseClick(self, buttonID, clickFunc, *extra):
        """Unassign a function to handle mouse button clicks."""
        command = "window.offMouseClick(buttonID, function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if clickFunc is None:
            system.missing(command)
            return
        try:
            buttonID = int(buttonID)
        except:
            system.invalid("buttonID", buttonID)
            return
        if buttonID < 1 or buttonID > 5:
            system.invalid("buttonID", buttonID)
            return

        if clickFunc in self.mouseClickFunctions.get(buttonID, []):
            self.mouseClickFunctions[buttonID].remove(clickFunc)

    def onMouseDrag(self, buttonID, dragFunc, *extra):
        """Assign a function to handle mouse drags."""
        command = "window.onMouseDrag(buttonID, function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if dragFunc is None:
            system.missing(command)
            return
        try:
            buttonID = int(buttonID)
        except:
            system.invalid("buttonID", buttonID)
            return
        if buttonID < 1 or buttonID > 5:
            system.invalid("buttonID", buttonID)
            return

        if buttonID not in self.mouseDragFunctions:
            self.mouseDragFunctions[buttonID] = []

        if dragFunc not in self.mouseDragFunctions[buttonID]:
            self.mouseDragFunctions[buttonID].append(dragFunc)

    def offMouseDrag(self, buttonID, dragFunc, *extra):
        """Unassign a function to handle mouse drags."""
        command = "window.offMouseDrag(buttonID, function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if dragFunc is None:
            system.missing(command)
            return
        try:
            buttonID = int(buttonID)
        except:
            system.invalid("buttonID", buttonID)
            return
        if buttonID < 1 or buttonID > 5:
            system.invalid("buttonID", buttonID)
            return

        if dragFunc in self.mouseDragFunctions.get(buttonID, []):
            self.mouseDragFunctions[buttonID].remove(dragFunc)

    def translateKey(self, key):
        return pygame.key.name(key)

    def open(self, title="chobo", *extra):
        """Make the window visible."""
        command = "window.open(title?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(title)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and pygame.key.get_focused():
                    pressedKey = self.translateKey(event.key)
                    if DEBUG:
                        print(pressedKey)
                    if len(self.keyFunctions) > 0:
                        for aFunction in self.keyFunctions:
                            aFunction(pressedKey)
                elif pygame.mouse.get_focused():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouseDown[event.button] = True
                        clickFunctions = self.mouseClickFunctions.get(event.button, [])
                        x, y = event.pos
                        if DEBUG:
                            print(event.button, (x, y))
                        for aFunction in clickFunctions:
                            aFunction(x, y)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouseDown[event.button] = False
                    elif event.type == pygame.MOUSEMOTION:
                        for mouseButton in dict(self.mouseDragFunctions):
                            if self.mouseDown.get(mouseButton, False):
                                dragFunctions = self.mouseDragFunctions.get(mouseButton, [])
                                x, y = event.pos
                                for aFunction in dragFunctions[:]:
                                    aFunction(x, y)

            # refresh drawing

            # set the background color
            self.screen.fill(self.background)

            # draw all the shapes
            for aShape in self.shapes:
                aShape.__draw__()


            # force an update
            pygame.display.flip()

            #iwait for the interval
            self.tick += self.clock.tick(self.fps)

            # call all the timer functions
            for interval in dict(self.timerFunctions):
                if self.tick - self.timerFunctions[interval]["lastRun"] > interval:
                    self.timerFunctions[interval]["lastRun"] = self.tick
                    for aFunction in self.timerFunctions[interval]["functions"][:]:
                        aFunction()

        pygame.quit()

    def onKeyPress(self, keyFunc=None, *extra):
        """Assign a function to handle key presses."""
        command = "window.onKeyPress(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if keyFunc is None:
            system.missing(command)
            return

        if keyFunc not in self.keyFunctions:
            self.keyFunctions.append(keyFunc)

    def offKeyPress(self, keyFunc=None, *extra):
        """Unassign a function to handle mouse drags."""
        command = "window.offKeyPress(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if keyFunc is None:
            system.missing(command)
            return

        if keyFunc in self.keyFunctions:
            self.keyFunctions.remove(keyFunc)

    def fill(self, color=None, *extra):
        """Give the window a background color."""
        command = "window.fill(color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if color is None:
            return system.missing(command)

        self.background = color

    def polygon(self, *points):
        """Draw and return a polygon shape."""
        command = "window.polygon( (x1,y1), (x2,y2), (x3,y3), ...)"

        # Argument existence
        if len(points) < 3:
            return system.missing(command)

        # Argument types
        pointlist = []
        for point in points:
            try:
                (x, y) = tuple(point)
                x = int(x)
                y = int(y)
                pointlist.append((x, y))
            except:
                return system.invalid("(x,y) point", point)

        shape = polygon(tuple(pointlist))
        self.shapes.append(shape)
        return shape

    def line(self, *points):
        """Draw and return a line shape."""
        command = "window.line( (x1, y1), (x2, y2), ...)"

        # Argument existence
        if len(points) < 2:
            return system.missing(command)

        # Argument types
        pointlist = []
        for point in points:
            try:
                (x, y) = tuple(point)
                x = int(x)
                y = int(y)
                pointlist.append((x, y))
            except:
                return system.invalid("(x, y) point", point)

        shape = lines(tuple(pointlist))
        self.shapes.append(shape)
        return shape

    def rectangle(self, pos=None, width=None, height=None, *extra):
        """Draw and return a rectangle shape."""
        command = "window.rectangle( (x,y), width, height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            if len(pos) > 2:
                return system.invalid("rectangle location", pos)
            x = pos[0]
            y = pos[1]
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("rectangle location", pos)

        try:
            width, height = int(width), int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("rectangle dimensions", (width, height))

        shape = rectangle(x, y, width, height)
        self.shapes.append(shape)
        return shape

    def oval(self, pos=None, width=None, height=None, *extra):
        """Draw and return an oval shape."""
        command = "window.oval( (x,y),width,height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("oval location", pos)

        try:
            width = int(width)
            height = int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("oval dimensions", (width, height))

        shape = oval(x, y, width, height)
        self.shapes.append(shape)
        return shape

    def arc(self, pos=None, width=None, height=None, beginAngle=None, arcAngle=None, *extra):
        """Draw and return an arc shape."""
        command = "window.arc( (x,y),width,height, beginAngle, arcAngle)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or width is None or height is None or beginAngle is None or arcAngle is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("arc location", (x, y))

        try:
            width = int(width)
            height = int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("arc dimensions", (width, height))

        try:
            beginAngle = int(beginAngle) % 360
            arcAngle = int(arcAngle) % 360


        except ValueError:
            return system.invalid("arc angles", (beginAngle, arcAngle))

        shape = arc(x, y, width, height, beginAngle, arcAngle)
        self.shapes.append(shape)
        return shape

    def text(self, pos=None, message=None, *extra):
        """Draw and return a text shape."""
        command = "window.text( (x,y), message)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or message is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("text location", (x, y))

        shape = text(x, y, str(message))
        self.shapes.append(shape)
        return shape

    def image(self, pos=None, filename=None, *extra):
        """Draw and return an image shape."""
        command = "window.image(x,y,filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or filename is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("image location", (x, y))

        shape = image(x, y, str(filename))
        self.shapes.append(shape)
        return shape

    def emptyimage(self, pos=None, width=None, height=None, *extra):
        """Draw and return an empty image shape."""
        command = "window.emptyimage(width,height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("image location", (x, y))

        try:
            width = int(width)
            height = int(height)
        except ValueError:
            return system.invalid("image width and height", (width, height))

        shape = emptyimage(x, y, width, height)
        self.shapes.append(shape)
        return shape

    def soundfx(self, filename=None, *extra):
        """Set and return the audio object."""
        command = "window.soundfx(filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if filename is None:
            return system.missing(command)

        # Argument types
        filename = filename.strip()

        if not os.path.isfile(filename):
            return system.invalid("file not found", filename)

        audioObject = soundfx(filename)
        return audioObject

    def music(self, filename=None, *extra):
        """Set and return the music object."""
        command = "window.music(filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if filename is None:
            return system.missing(command)

        # Argument types
        filename = filename.strip()

        if not os.path.isfile(filename):
            return system.invalid("file not found", filename)

        audioObject = music(filename)
        return audioObject

    def remove(self, shape=None):
        """Remove a shape from the window."""
        command = "window.remove(shape)"

        # Argument existence
        if shape is None:
            return system.missing(command)
        if not isinstance(shape, windowshape):
            return system.invalid("shape", shape)

        self.shapes.remove(shape)

    def ovalPoint(self, pos=None, width=None, height=None, angle=None, *extra):
        """Compute a point at an angle on an oval with the given position, width, and height."""
        command = "ovalPoint(centerPosition, width, height, angle)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or width is None or height is None or angle is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("invalid location", pos)

        try:
            width = max(1, int(width / 2))
            if width <= 0:
                raise ValueError
        except ValueError:
            return system.invalid("invalid width", width)

        try:
            height = max(1, int(height / 2))
            if height <= 0:
                raise ValueError
        except ValueError:
            return system.invalid("invalid height", height)

        try:
            angle = float(angle)
        except ValueError:
            return system.invalid("invalid angle", angle)

        # convert from degrees to radians
        angle = math.radians(angle)

        return (x + width * math.sin(angle) + width, y - height * math.cos(angle) + height)

class windowshape:
    def __init__(self):
        self.rect = None

    def getRect(self):
        return self.rect

    def overlaps(self, shape=None, *extra):
        """Check if this shape overlaps another."""
        command = self.__class__.__name__ + ".overlaps(shape)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if shape is None:
            return system.missing(command)

        # Argument types
        if not isinstance(shape, windowshape):
            return system.invalid("shape", shape)

        if self.rect is None or shape.getRect() is None:
            return system.error("at least one of the shapes is not added to the window")

        return self.rect.colliderect(shape.getRect())


# A shape specified by a list of points.
class listshape(windowshape):
    def __init__(self, points):
        super().__init__()
        self.configure(points)

    # Update the shape location.
    def configure(self, points):
        self.points = points
        self.x = min(x for (x,y) in points)
        self.y = min(y for (x,y) in points)
        self.__dict__["left"] = min(x for (x,y) in points)
        self.__dict__["top"] = min(y for (x,y) in points)
        self.__dict__["right"] = max(x for (x,y) in points)
        self.__dict__["bottom"] = max(y for (x,y) in points)
        self.__dict__["width"] = self.__dict__["right"] - self.__dict__["left"]
        self.__dict__["height"] = self.__dict__["bottom"] - self.__dict__["top"]
        self.rect = pygame.Rect(self.x, self.y, self.__dict__["width"], self.__dict__["height"])

    def rotate(self, angle):
        angle = math.radians(angle)

        cx = self.__dict__["left"] + self.__dict__["width"] / 2
        cy = self.__dict__["top"] + self.__dict__["height"] / 2

        newPoints = []
        for index in range(len(self.points)):
            x, y = self.points[index]
            dx = x - cx
            dy = y - cy
            newx = dx * math.cos(angle) - dy * math.sin(angle)
            newy = dy * math.cos(angle) + dx * math.sin(angle)

            newx += cx
            newy += cy
            newPoints.append((newx, newy))
        self.configure(newPoints)

    def fill(self, color=None, *extra):
        """Change the color of this shape."""
        command = self.__class__.__name__ + ".fill(color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if color is None:
            return system.missing(command)

        self.__dict__["fillColor"] = color

    def move(self, dx=None, dy=None, *extra):
        """Move this shape."""
        command = self.__class__.__name__ + ".move(dx,dy)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if dx is None or dy is None:
            return system.missing(command)

        # Argument types
        try:
            dx = int(dx)
            dy = int(dy)
        except ValueError:
            return system.invalid("movement vector", (dx,dy))

        self.configure(tuple(map(lambda p: (p[0] + dx,p[1] + dy), self.points)))

    def relocate(self, pos=None, *extra):
        """Change the location of this shape."""
        command = self.__class__.__name__ + ".relocate(x,y)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            sx, sy = self.__dict__["left"], self.__dict__["top"]
            dx = int(x) - sx
            dy = int(y) - sy
        except ValueError:
            return system.invalid("new location", pos)

        self.move(dx, dy)

    def scale(self, horizonScale=None, verticalScale=None, *extra):
        """Scale this shape by the given horizontal and vertical scale."""
        command = self.__class__.__name__ + ".scale(horizonScale,verticalScale)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if horizonScale is None or verticalScale is None:
            return system.missing(command)

        newPoints = []
        for index in range(len(self.points)):
            x, y = self.points[index]
            dx = x - self.__dict__["left"]
            dy = y - self.__dict__["top"]
            newx = dx * horizonScale
            newy = dy * verticalScale

            newx += self.__dict__["left"]
            newy += self.__dict__["top"]
            newPoints.append((newx, newy))
        self.configure(newPoints)

class lines(listshape):
    """A line shape."""
    def __init__(self, points):
        super().__init__(points)
        self.__dict__["color"] = (0, 0, 0)
        self.__dict__["fillColor"] = None
        self.__dict__["borderWidth"] = 1

    def fill(self, color=None, *extra):
        """Change the color of this line."""
        command = "line.border(width,color?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if color is None:
            return system.missing(command)

        # Argument types
        self.__dict__["color"] = color

    def border(self, width=None, *extra):
        """Change the border width of this line."""
        command = "line.border(width)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if width is None:
            return system.missing(command)

        # Argument types
        try:
            width = int(width)
            if width < 1:
                raise ValueError
        except ValueError:
            return system.invalid("border width", width)

        self.__dict__["borderWidth"] = width

    def __draw__(self, enclosed=False):
#        points = [(int(p[0]), int(p[1])) for p in self.points]
#        pygame.draw.polygon(sys.window.screen, self.__dict__["fillColor"], points, 0)
        if self.__dict__["borderWidth"] > 0:
            pygame.draw.lines(sys.window.screen, self.__dict__["color"], enclosed, self.points, self.__dict__["borderWidth"])

class polygon(lines):
    """A polygon shape."""
    def __init__(self, points):
        super().__init__(points)

    def fill(self, color=None, *extra):
        """Change the color of this shape."""
        command = self.__class__.__name__ + ".fill(color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if color is None:
            return system.missing(command)

        self.__dict__["fillColor"] = color

    def border(self, width=None, color=(0, 0, 0), *extra):
        """Change the border around this polygon."""
        command = "polygon.border(width,color?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if width is None:
            return system.missing(command)

        # Argument types
        try:
            width = int(width)
            if width < 0:
                raise ValueError
        except ValueError:
            return system.invalid("border width", width)

        self.__dict__["borderWidth"] = width
        self.__dict__["color"] = color

    def __draw__(self):
        if self.__dict__["fillColor"] is not None:
            pygame.draw.polygon(sys.window.screen, self.__dict__["fillColor"], self.points, 0)

        super().__draw__(enclosed=True)

class rectangle(polygon):
    """A polygon shape."""
    def __init__(self, x, y, width, height):
        points = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        super().__init__(points)

class arc(polygon):
    """An arc shape."""

    def __init__(self, x, y, width, height, beginAngle, arcAngle):
#        self.id = canvas.create_oval(0, 0, 0, 0, width=1)
        points = []

        a = max(1, int(width / 2))
        b = max(1, int(height / 2))

        arcAngle %= 360

        if arcAngle == 0:
            arcAngle = 360
        else:
            points.append((x + a, y + b))

        for i in range(beginAngle, beginAngle + arcAngle + 1):
            points.append(sys.window.ovalPoint( (x, y), width, height, i))

        # points = [(v + x + a, w + y + b) for (v, w) in points]

        super().__init__(points)

class oval(arc):
    """An oval shape."""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 0, 360)

# A shape specified by a single point.
class pointshape(windowshape):
    def __init__(self, x, y):
        super().__init__()
        self.configure(x, y)

    # Update the shape location.
    def configure(self, x, y):
        self.x = x
        self.y = y
        self.__dict__["left"] = x
        self.__dict__["top"] = y
        self.__dict__["right"] = x
        self.__dict__["bottom"] = y
        self.__dict__["width"] = 0
        self.__dict__["height"] = 0

    def move(self, dx=None, dy=None, *extra):
        """Move this shape."""
        command = self.__class__.__name__ + ".move(dx,dy)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if dx is None or dy is None:
            return system.missing(command)

        # Argument types
        try:
            dx = int(dx)
            dy = int(dy)
        except ValueError:
            return system.invalid("movement vector", (dx,dy))

        self.configure(self.x + dx, self.y + dy)

    def relocate(self, pos=None, *extra):
        """Change the location of this shape."""
        command = self.__class__.__name__ + ".relocate(x,y)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("new location", pos)

        self.configure(x, y)

class image(pointshape):
    """A image."""

    def __init__(self, x, y, filename=None):
        if filename is not None:
            self.img = pygame.image.load(filename)
            self.original = pygame.image.load(filename)
        super().__init__(x, y)
        self.rotation = 0

    # Update the shape location.
    def configure(self, x, y):
        self.x = x
        self.y = y
        self.__dict__["left"] = x
        self.__dict__["top"] = y
        self.__dict__["width"] = self.img.get_width()
        self.__dict__["height"] = self.img.get_height()
        self.__dict__["right"] = x + self.img.get_width()
        self.__dict__["bottom"] = y + self.img.get_height()
        self.__dict__["rect"] = self.getRect()

    def rotate(self, angle):
        if angle == 0:
            return
        self.rotation += angle
        del self.img
        self.img = pygame.transform.rotate(self.original, -self.rotation)
        x = self.x + self.__dict__["width"] / 2 - self.img.get_width() / 2
        y = self.y + self.__dict__["height"] / 2 - self.img.get_height() / 2
        self.configure(x, y)

    def getColor(self, pos=None, *extra):
        """Retrieve the (r,g,b) color at pixel x,y of the image."""
        command = "image.getColor( (x,y) )"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None:
            return system.missing(command)

        # Argument types
        try:
            x, y = pos
            if x < 0 or x >= self.original.get_width():
                raise ValueError
            if y < 0 or y >= self.original.get_height():
                raise ValueError
        except ValueError:
            return system.invalid("image pixel", pos)

        return self.original.get_at( (x, y) )[:3]

    def setColor(self, pos=None, color=None, *extra):
        """Change the (r,g,b) color at pixel x,y of the image."""
        command = "image.setColor( (x,y), color )"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if pos is None or color is None:
            return system.missing(command)

        # Argument types
        try:
            if len(pos) > 2:
                return system.invalid("image pixel", pos)
            x = int(pos[0])
            y = int(pos[1])
            if x < 0 or x >= self.original.get_width():
                raise ValueError
            if y < 0 or y >= self.original.get_height():
                raise ValueError
        except ValueError:
            return system.invalid("image pixel", pos)

        try:
            r, g, b = color
        except:
            return system.invalid("color", color)
        self.original.set_at( (x, y), (r, g, b, 255))

        self.img = self.original
        self.rotate(self.rotation)

    def saveAs(self, filename=None, *extra):
        """Save this image to a file."""
        command = "image.saveAs(filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if filename is None:
            return system.missing(command)

        pygame.image.save(self.img, str(filename))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def __draw__(self):
        self.rect = sys.window.screen.blit(self.img, self.getRect())


class emptyimage(image):
    """An empty image."""

    def __init__(self, x, y, width, height):
        self.img = pygame.Surface( (width, height) )
        self.original =  pygame.Surface( (width, height) )

        super().__init__(x, y)

class text(pointshape):
    """A text label."""

    def __init__(self, x, y, message):
        super().__init__(x, y)
        self.message = message
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        self.color = (0, 0, 0)
        self.__render__()

    def format(self, font=None, size=None, color=(0,0,0), *extra):
        command = "text.format(font, size, color?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if font is None or size is None:
            return sys.missing(command)

        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.__render__()

    def rewrite(self, message, *extra):
        command = "text.rewrite(message)"
        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        self.message = message
        self.__render__()

    def __render__(self):
        self.text = self.font.render(self.message, True, self.color)

    def __draw__(self):
        self.rect = sys.window.screen.blit(self.text, (self.x, self.y))

class soundfx():
    """A sound FX object"""

    def __init__(self, filename):
        self.soundfx = pygame.mixer.Sound(filename)

    def play(self):
        self.soundfx.play()

class music():
    """A music object"""
    __currentMusic = None

    def __init__(self, filename):
        self.music = filename
        self.volume = pygame.mixer.music.get_volume()
        self.playing = False

    def play(self):
        if music.__currentMusic is not self:
            if music.__currentMusic is not None:
                music.__currentMusic.playing = False
            try:
                pygame.mixer.music.unload() # works only with Pygame 2.0+
            except:
                pass
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(self.volume)
            music.__currentMusic = self
            self.playing = True
        pygame.mixer.music.play()

    def stop(self):
        if music.__currentMusic is self:
            pygame.mixer.music.stop()
            self.playing = False

    def pause(self):
        if music.__currentMusic is self:
            pygame.mixer.music.pause()
            self.playing = False

    def unpause(self):
        if music.__currentMusic is self:
            pygame.mixer.music.unpause()
            self.playing = True

    def isPlaying(self):
        if music.__currentMusic is self:
            if pygame.mixer.music.get_busy():
                return self.playing
        return False

    def setVolume(self, volume):
        if volume < 0 or volume > 1.0:
            return system.invalid("volume", volume)
        self.volume = volume
        if music.__currentMusic is self:
            pygame.mixer.music.set_volume(self.volume)

    def getVolume(self):
        return self.volume


