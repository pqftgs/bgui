from .widget import Widget, BGUI_DEFAULT, BGUI_NO_THEME, BGUI_CENTERED, BGUI_CLIP
from .frame import Frame
from .label import Label
from .frame_button import FrameButton
from .utils import scalar, clamp


class ScrollFrame(Widget):
    """A clickable frame-based button"""
    theme_sections = 'FrameButton'
    theme_options = {
            'Color': (0.4, 0.4, 0.4, 1),
            'BorderSize': 1,
            'BorderColor': (0, 0, 0, 1),
            'LabelSubTheme': '',
            }

    def __init__(self, parent, name=None, base_color=None, text="", font=None,
                pt_size=None, aspect=None, size=[1, 1], pos=[0, 0], sub_theme='', options=BGUI_DEFAULT):
        """
        :param parent: the widget's parent
        :param name: the name of the widget
        :param base_color: the color of the button
        :param text: the text to display (this can be changed later via the text property)
        :param font: the font to use
        :param pt_size: the point size of the text to draw (defaults to 30 if None)
        :param aspect: constrain the widget size to a specified aspect ratio
        :param size: a tuple containing the width and height
        :param pos: a tuple containing the x and y position
        :param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
        :param options: various other options
        """

        Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)
        self.xdiff = 0
        border_size = 0.05
        border_color = [(0.0, 0.0, 0.0, 1.0) for i in range(4)]
        client_color = [(0.0, 0.0, 1.0, 1.0) for i in range(4)]
        border_colors = []

        for i in range(8):
            border_colors.append([((i*0.1), (i*0.1), (i*0.1), 0.5) for b in range(4)])
        self.container = Frame(self, size=[1, 1], pos=[0, 0], options=BGUI_NO_THEME)

        #plain borders
        self.border_top = Frame(self.container, size=[1-(border_size*2), border_size], pos=[border_size, 1-border_size], options=BGUI_NO_THEME)
        self.border_bottom = Frame(self.container, size=[1-(border_size*2), border_size], pos=[border_size, 0], options=BGUI_NO_THEME)
        self.border_left = Frame(self.container, size=[border_size, 1], pos=[0, 0], options=BGUI_NO_THEME)
        self.border_right = Frame(self.container, size=[border_size, 1], pos=[1-border_size, 0], options=BGUI_NO_THEME)
        self.border_bottom_left = Frame(self.container, size=[border_size, border_size], pos=[0, 0], options=BGUI_NO_THEME)
        self.border_top_left = Frame(self.container, size=[border_size, border_size], pos=[0, 1-border_size], options=BGUI_NO_THEME)
        self.border_top_right = Frame(self.container, size=[border_size, border_size], pos=[1-border_size, 1-border_size], options=BGUI_NO_THEME)
        self.border_bottom_right = Frame(self.container, size=[border_size, border_size], pos=[1-border_size, 0], options=BGUI_NO_THEME)

        self.border_top.colors = border_colors[0]
        self.border_bottom.colors = border_colors[1]
        self.border_left.colors = border_colors[2]
        self.border_right.colors = border_colors[3]
        self.border_bottom_left.colors = border_colors[4]
        self.border_top_left.colors = border_colors[5]
        self.border_top_right.colors = border_colors[6]
        self.border_bottom_right.colors = border_colors[7]

        #viewport
        self.view = Frame(self.container, size=[1-(border_size*2), 1-(border_size*2)], pos=[0, 0], options=BGUI_NO_THEME | BGUI_CENTERED | BGUI_CLIP)

        #scrollable client
        #self.client = Frame(self.view, name='client', size=[2, 2], pos=[0, 0], options=BGUI_NO_THEME)
        self.client = Frame(self.view, name='client', size=[2, 2], pos=[0, 0], options=BGUI_NO_THEME)
        self.client.colors = client_color

        #frame title
        self.title = Label(self.border_top, text=text, font=font, pt_size=pt_size, pos=[0, 0], sub_theme=self.theme['LabelSubTheme'], options=BGUI_DEFAULT | BGUI_CENTERED)

        #scrollbars
        self.horizontal_scrollbar = FrameButton(self.border_bottom, text='', size=[1, 1], pos=[0, 0], options = BGUI_DEFAULT)
        self.update_horizontal_scrollbar_size()
        self.horizontal_scrollbar.on_click = self._horizontal_scrollbar_click
        self.horizontal_scrollbar.on_active = self._horizontal_scrollbar_active

    def _horizontal_scrollbar_click(self, widget):
        self.xdiff = self.system.cursor_pos[0]-self.horizontal_scrollbar.position[0]

    def _horizontal_scrollbar_active(self, widget):
        minX = self.horizontal_scrollbar.parent.position[0]
        #print ("SIZE")
        #print (self.horizontal_scrollbar.parent.size[0])
        maxX = (self.horizontal_scrollbar.parent.position[0]+(self.horizontal_scrollbar.parent.size[0]/self._base_size[0]))- (self.horizontal_scrollbar.size[0]/self._base_size[0])
        cursor = self.system.cursor_pos[0]-self.xdiff
        #print('xdiff', self.xdiff)
        #print('original cursor', self.system.cursor_pos[0])
        #print('cursor', cursor)
        #print('minX',minX)
        #print('maxX',maxX)
        x1 = scalar(cursor, maxX, minX)
        #print (x1)
        #print('clamp max', (1/self.horizontal_scrollbar.parent.size[0])*(self.horizontal_scrollbar.size[0]))
        x2 = clamp(x1, 0, (1/self.horizontal_scrollbar.parent.size[0])*(self.horizontal_scrollbar.size[0]))#-self.horizontal_scrollbar.pos[0])
        new_pos = [x2, 0]
        #print(x1, x2)
        self.horizontal_scrollbar.position = new_pos
        self.client.position = [x2*-1, 0]
        # if not base_color:
            # base_color = self.theme['Color']
        # self.base_color = base_color
        # self.frame.border = self.theme['BorderSize']
        # self.frame.border_color = self.theme['BorderColor']

        # self.light = [
            # self.base_color[0] + 0.15,
            # self.base_color[1] + 0.15,
            # self.base_color[2] + 0.15,
            # self.base_color[3]]
        # self.dark = [
            # self.base_color[0] - 0.15,
            # self.base_color[1] - 0.15,
            # self.base_color[2] - 0.15,
            # self.base_color[3]]
        # self.frame.colors = [self.dark, self.dark, self.light, self.light]

    # @property
    # def text(self):
        # return self.label.text

    # @text.setter
    # def text(self, value):
        # self.label.text = value

    # @property
    # def color(self):
        # return self.base_color

    # @color.setter
    # def color(self, value):
        # self.base_color = value
        # self.light = [
            # self.base_color[0] + 0.15,
            # self.base_color[1] + 0.15,
            # self.base_color[2] + 0.15,
            # self.base_color[3]]
        # self.dark = [
            # self.base_color[0] - 0.15,
            # self.base_color[1] - 0.15,
            # self.base_color[2] - 0.15,
            # self.base_color[3]]
        # self.frame.colors = [self.dark, self.dark, self.light, self.light]

    # def _handle_hover(self):
        # light = self.light[:]
        # dark = self.dark[:]

        # Lighten button when hovered over.
        # for n in range(3):
            # light[n] += .1
            # dark[n] += .1
        # self.frame.colors = [dark, dark, light, light]

    # def _handle_active(self):
        # light = self.light[:]
        # dark = self.dark[:]

        # Darken button when clicked.
        # for n in range(3):
            # light[n] -= .1
            # dark[n] -= .1
        # self.frame.colors = [light, light, dark, dark]
    def update_horizontal_scrollbar_size(self):
        #print(self.size)
        #print(self._base_size)
        relative_normalized_size = 1/((1/self.view.size[0])*next(iter (self.view.children.values())).size[0])
        self.horizontal_scrollbar.size = [relative_normalized_size, 1]
    def _update_client(self):
        max_size = [0.0, 0.0]
        min_size = [0.0, 0.0]
        first = True
        for child in self.client.children.values():
            pos = child.position
            size = child.size
            if first:
                max_size[0] = pos[0]+size[0]
                max_size[1] = pos[1]+size[1]
                min_size[0] = pos[0]
                min_size[1] = pos[1]
            else:
                max_size[0] = max(pos[0]+size[0], max_size[0])
                max_size[1] = max(pos[1]+size[1], max_size[1])
                min_size[0] = min(pos[0], min_size[0])
                min_size[1] = min(pos[1], min_size[1])
        client_size = self.client.size
        self.client.size = [(1/(self.view.size[0]+self.view.position[0]))*(client_size[0]*(max_size[0]/client_size[0])), (1/(self.view.size[1]+self.view.position[1]))*(client_size[1]*(max_size[1]/client_size[1]))]

    def _draw(self):
        """Draw the button"""

        # Draw the children before drawing an additional outline
        Widget._draw(self)
