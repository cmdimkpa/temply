#! /usr/bin/env python2

# temply -- a class-based HTML templating system :: write HTML page as a list of objects

global DEFAULT_STYLES, COLORS, BASE_TABLE_STYLE

def customize(original_text,revisions={}):
    for revision in revisions:
        original_text = original_text.replace(revision,revisions[revision])
    return original_text

def pop(pagelist=[]):
    # generate HTML string for entire page
    return "".join(map(lambda x:x.render(),pagelist))

def itemize(dict=[]):
    itemized = ""
    for key in dict:
        unit = '%s="%s" ' % (str(key),str(dict[key]))
        itemized+=unit
    return itemized[:-1]

def extrude(tag_type,data=[]):
    return map(lambda x:x.render(),[basicTag(tag_type,point) for point in data])

class basicTag:
    def __init__(self,tag,inner=None):
        self.tag = tag
        self.inner = inner
        self.html = "<%s>%s</%s>" % (tag,inner,tag)
    def update(self,tag,renders=[]):
        def splice(renders):
            mashup = ""
            for render in renders:
                mashup+=render
            return mashup
        self.html = "<%s>%s</%s>" % (tag,splice(renders),tag)

    def render(self,copies=1):
        this_render = ""
        for i in range(copies):
            this_render+=self.html
        return this_render

class dataTag(basicTag):
    def __init__(self,tag,tag_data,inner=None,terminates=True):
        self.tag = tag
        self.tag_data = tag_data
        self.inner = inner
        self.terminates = terminates
        if self.terminates:
            self.html = "<%s %s>%s</%s>" % (tag,itemize(tag_data),inner,tag)
        else:
            self.html = "<%s %s>" % (tag,itemize(tag_data))
    def update(self,tag,tag_data,renders=[]):
        def splice(renders):
            mashup = ""
            for render in renders:
                mashup+=render
            return mashup
        if self.terminates:
            self.html = "<%s %s>%s</%s>" % (tag,itemize(tag_data),splice(renders),tag)
        else:
            self.html = "<%s %s>" % (tag,itemize(tag_data))

class ListBlock:
    def __init__(self,list_data):
        self.list_data = list_data
        self.list = basicTag("ul")
        self.build()
    def build(self):
        self.list.update("ul",extrude("li",self.list_data))
    def render(self,copies=1):
        return self.list.render(copies)

class Table:
    def __init__(self,data={}):
        self.data = data
        self.table = dataTag("table",{"id":"TABLE_ID"})
        self.build()
    update = __init__
    def build(self):
        table_runner = ""
        min_size = min([len(self.data[header]) for header in self.data])
        copy = {}
        for header in self.data:
            copy[header] = self.data[header][:min_size]
        self.data = copy; del copy
        header_row = basicTag("tr")
        header_row.update("tr",extrude("td",[header for header in self.data]))
        table_runner+=header_row.render()
        for row in range(min_size):
            data_row = basicTag("tr")
            data_row.update("tr",extrude("td",[self.data[header][row] for header in self.data]))
            table_runner+=data_row.render()
        self.table.update("table",{"id":"TABLE_ID"},[table_runner])
    def render(self,copies=1):
        return self.table.render(copies)


class Page:
    def __init__(self):
        self.generics = {"html":basicTag("html"),"head":basicTag("head"),"body":basicTag("body")}
        self.head = []
        self.body = []
        self.page = [self.generics["html"]]
    def update_head(self,head):
        self.head = head
    def update_body(self,body):
        self.body = body
    def build(self):
        self.generics["head"].update("head",[pop(self.head)])
        self.generics["body"].update("body",[pop(self.body)])
        self.generics["html"].update("html",[self.generics["head"].render(),self.generics["body"].render()])
        self.page = [self.generics["html"]]
    def render(self):
        return pop(self.page)


COLORS = {'AliceBlue': '#F0F8FF', 'Crimson': '#E238EC', 'Tron Blue': '#7DFDFE', 'Coral Blue': '#AFDCEC', 'Red Fox': '#C35817', 'Grayish Turquoise': '#5E7D7E', 'Vampire Gray': '#565051', 'Iceberg': '#56A5EC', 'Lemon Chiffon': '#FFF8C6', 'Green Peas': '#89C35C', 'Plum': '#B93B8F', 'Purple Flower': '#A74AC7', 'Blush Pink': '#E6A9EC', 'Copper': '#B87333', 'Red Wine': '#990012', 'Jade Green': '#5EFB6E', 'Midnight': '#2B1B17', 'Dark Orchid': '#7D1B7E', 'Jeans Blue': '#A0CFEC', 'Sage Green': '#848b79', 'Bright Neon Pink': '#F433FF', 'Cotton Candy': '#FCDFFF', 'Plum Velvet': '#7D0552', 'Black Cat': '#413839', 'Jungle Green': '#347C2C', 'Red': '#FF0000', 'Charcoal': '#34282C', 'Light Salmon': '#F9966B', 'Mango Orange': '#FF8040', 'Algae Green': '#64E986', 'Kelly Green': '#4CC552', 'Army Brown': '#827B60', 'Sea Turtle Green': '#438D80', 'Neon Pink': '#F535AA', 'Green': '#00FF00', 'Azure': '#F0FFFF', 'Medium Sea Green': '#306754', 'Rust': '#C36241', 'Orange Gold': '#D4A017', 'Green Apple': '#4CC417', 'Dimorphotheca Magenta': '#E3319D', 'Hot Pink': '#F660AB', 'BlanchedAlmond': '#FFEBCD', 'Oak Brown': '#806517', 'Slime Green': '#BCE954', 'Dark Orange': '#F88017', 'Pumpkin Orange': '#F87217', 'Velvet Maroon': '#7E354D', 'Blue Lagoon': '#8EEBEC', 'Medium Turquoise': '#48CCCD', 'Blush Red': '#E56E94', 'Viola Purple': '#7E587E', 'Blue Koi': '#659EC7', 'Pine Green': '#387C44', 'Zombie Green': '#54C571', 'Dark Forest Green': '#254117', 'Black Cow': '#4C4646', 'Heliotrope Purple': '#D462FF', 'Iridium': '#3D3C3A', 'Mint green': '#98FF98', 'Caramel': '#C68E17', 'Slate Gray': '#657383', 'Green Yellow': '#B1FB17', 'Lawn Green': '#87F717', 'Tulip Pink': '#C25A7C', 'Indigo': '#4B0082', 'Rosy Brown': '#B38481', 'Dark Violet': '#842DCE', 'Purple Jam': '#6A287E', 'Denim Dark Blue': '#151B8D', 'Flamingo Pink': '#F9A7B0', 'Sea Blue': '#C2DFFF', 'Pink Cupcake': '#E45E9D', 'Yellow Green': '#52D017', 'Pale Violet Red': '#D16587', 'Cookie Brown': '#C7A317', 'Fire Engine Red': '#F62817', 'Mustard': '#FFDB58', 'BurlyWood': '#DEB887', 'Pink Rose': '#E7A1B0', 'Frog Green': '#99C68E', 'Medium Forest Green': '#347235', 'Bullet Shell': '#AF9B60', 'Wisteria Purple': '#C6AEC7', 'Purple Dragon': '#C38EC7', 'Cranberry': '#9F000F', 'Sun Yellow': '#FFE87C', 'Light Pink': '#FAAFBA', 'Columbia Blue': '#87AFC7', 'Crystal Blue': '#5CB3FF', 'Purple Mimosa': '#9E7BFF', 'Blue Zircon': '#57FEFF', 'Purple': '#8E35EF', 'Stoplight Go Green': '#57E964', 'Halloween Orange': '#E66C2C', 'White': '#FFFFFF', 'Ruby Red': '#F62217', 'Medium Aquamarine': '#348781', 'Salad Green': '#A1C935', 'Northern Lights Blue': '#78C7C7', 'Rubber Ducky Yellow': '#FFD801', 'Tangerine': '#E78A61', 'Blue Hosta': '#77BFC7', 'Dark Goldenrod': '#AF7817', 'Lavender Pinocchio': '#EBDDE2', 'Blue Orchid': '#1F45FC', 'Gunmetal': '#2C3539', 'Carbon Gray': '#625D5D', 'Pig Pink': '#FDD7E4', 'Metallic Silver': '#BCC6CC', 'Pastel Blue': '#B4CFEC', 'Green Thumb': '#B5EAAA', 'Gray Cloud': '#B6B6B4', 'Rogue Pink': '#C12869', 'Yellow': '#FFFF00', 'Platinum': '#E5E4E2', 'Green Onion': '#6AA121', 'Rose': '#E8ADAA', 'Blue green': '#7BCCB5', 'Chartreuse': '#8AFB17', 'Black Eel': '#463E3F', 'Sedona': '#CC6600', 'Beetle Green': '#4C787E', 'Harvest Gold': '#EDE275', 'Khaki Rose': '#C5908E', 'Blue Dress': '#157DEC', 'Navy Blue': '#000080', 'Forest Green': '#4E9258', 'Light Sky Blue': '#82CAFA', 'Beige': '#F5F5DC', 'Magenta': '#FF00FF', 'Cornflower Blue': '#6495ED', 'Dark Slate Grey': '#25383C', 'Cobalt Blue': '#0020C2', 'Gray Dolphin': '#5C5858', 'Parchment': '#FFFFC2', 'Bright Gold': '#FDD017', 'Sapphire Blue': '#2554C7', 'Black': '#000000', 'Marble Blue': '#566D7E', 'Sandy Brown': '#EE9A4D', 'Bashful Pink': '#C25283', 'Greenish Blue': '#307D7E', 'Light Slate Gray': '#6D7B8D', 'Pink Daisy': '#E799A3', 'Gray Goose': '#D1D0CE', 'Goldenrod': '#EDDA74', 'Avocado Green': '#B2C248', 'Cinnamon': '#C58917', 'Eggplant': '#614051', 'Light Blue': '#ADDFFF', 'Taupe': '#483C32', 'Purple Daffodil': '#B041FF', 'Corn Yellow': '#FFF380', 'Misty Rose': '#FBBBB9', 'Ash Gray': '#666362', 'Iguana Green': '#9CB071', 'Glacial Blue Ice': '#368BC1', 'Watermelon Pink': '#FC6C85', 'Peach': '#FFE5B4', 'Golden brown': '#EAC117', 'Sangria': '#7E3817', 'Medium Violet Red': '#CA226B', 'Saffron': '#FBB917', 'Love Red': '#E41B17', 'Blue Eyes': '#1569C7', 'Blue Whale': '#342D7E', 'Oil': '#3B3131', 'Valentine Red': '#E55451', 'Construction Cone Orange': '#F87431', 'Macaw Blue Green': '#43BFC7', 'Green Snake': '#6CBB3C', 'Desert Sand': '#EDC9AF', 'Mahogany': '#C04000', 'Maroon': '#810541', 'Mocha': '#493D26', 'Pink Bow': '#C48189', 'Lime Green': '#41A317', 'Cornsilk': '#FFF8DC', 'Cloudy Gray': '#6D6968', 'Papaya Orange': '#E56717', 'Macaroni and Cheese': '#F2BB66', 'Light Cyan': '#E0FFFF', 'Dollar Bill Green': '#85BB65', 'Bronze': '#CD7F32', 'Ginger Brown': '#C9BE62', 'Battleship Gray': '#848482', 'Royal Blue': '#2B60DE', 'Dark Sea Green': '#8BB381', 'Venom Green': '#728C00', 'Rosy Finch': '#7F4E52', 'Fern Green': '#667C26', 'Camouflage Green': '#78866B', 'Mauve': '#E0B0FF', 'Blonde': '#FBF6D9', 'Denim Blue': '#79BAEC', 'Ocean Blue': '#2B65EC', 'Sea Green': '#4E8975', 'Mist Blue': '#646D7E', 'Purple Haze': '#4E387E', 'Lovely Purple': '#7F38EC', 'Jet Gray': '#616D7E', 'Chestnut': '#954535', 'Water': '#EBF4FA', 'Pink Bubble Gum': '#FFDFDD', 'Brass': '#B5A642', 'Cadillac Pink': '#E38AAE', 'Jellyfish': '#46C7C7', 'Pink Lemonade': '#E4287C', 'Aztech Purple': '#893BFF', 'Steel Blue': '#4863A0', 'Sand': '#C2B280', 'Blueberry Blue': '#0041C2', 'Purple Iris': '#571B7E', 'Violet Red': '#F6358A', 'Hummingbird Green': '#7FE817', 'Violet': '#8D38C9', 'Blossom Pink': '#F9B7FF', 'Cyan Opaque': '#92C7C7', 'Teal': '#008080', 'Lavender blue': '#E3E4FA', 'Blue Jay': '#2B547E', 'Pearl': '#FDEEF4', 'Light Steel Blue': '#728FCE', 'Brown Sugar': '#E2A76F', 'Rose Gold': '#ECC5C0', 'Deep Peach': '#FFCBA4', 'Blue Diamond': '#4EE2EC', 'Tiger Orange': '#C88141', 'Shamrock Green': '#347C17', 'Sunrise Orange': '#E67451', 'Vanilla': '#F3E5AB', 'Night': '#0C090A', 'Burnt Pink': '#C12267', 'Plum Pie': '#7D0541', 'Puce': '#7F5A58', 'Bean Red': '#F75D59', 'Sepia': '#7F462C', 'Bee Yellow': '#E9AB17', 'Sienna': '#8A4117', 'Lipstick Pink': '#C48793', 'Seaweed Green': '#437C17', 'Day Sky Blue': '#82CAFF', 'Purple Sage Bush': '#7A5DC7', 'Emerald Green': '#5FFB17', 'Wood': '#966F33', 'Periwinkle': '#E9CFEC', 'Light Slate Blue': '#736AFF', 'Aquamarine': '#7FFFD4', 'Shocking Orange': '#E55B3C', 'Light Aquamarine': '#93FFE8', 'Orange Salmon': '#C47451', 'Butterfly Blue': '#38ACEC', 'Lava Red': '#E42217', 'Tan Brown': '#ECE5B6', 'Blue Ivy': '#3090C7', 'Deep Pink': '#F52887', 'Blood Red': '#7E3517', 'Coral': '#FF7F50', 'Khaki': '#ADA96E', 'Pistachio Green': '#9DC209', 'Light Jade': '#C3FDB8', 'Jasmine Purple': '#A23BEC', 'Tyrian Purple': '#C45AEC', 'Pink': '#FAAFBE', 'Alien Green': '#6CC417', 'Dark Salmon': '#E18B6B', 'Burgundy': '#8C001A', 'Dodger Blue': '#1589FF', 'Milk White': '#FEFCFF', 'Windows Blue': '#357EC7', 'Cantaloupe': '#FFA62F', 'Tiffany Blue': '#81D8D0', 'Chocolate': '#C85A17', 'Dark Slate Blue': '#2B3856', 'Nebula Green': '#59E817', 'Slate Blue': '#737CA1', 'Gray Wolf': '#504A4B', 'Silk Blue': '#488AC7', 'Medium Orchid': '#B048B5', 'Electric Blue': '#9AFEFF', 'Clover Green': '#3EA055', 'Medium Purple': '#8467D7', 'Spring Green': '#4AA02C', 'Light Coral': '#E77471', 'Midnight Blue': '#151B54', 'Chestnut Red': '#C34A2C', 'Scarlet': '#FF2400', 'Red Dirt': '#7F5217', 'Medium Spring Green': '#348017', 'Chilli Pepper': '#C11B17', 'Sandstone': '#786D5F', 'Fall Leaf Brown': '#C8B560', 'Basket Ball Orange': '#F88158', 'Champagne': '#F7E7CE', 'Coffee': '#6F4E37', 'School Bus Yellow': '#E8A317', 'Dark Turquoise': '#3B9C9C', 'Gray': '#736F6E', 'Moccasin': '#827839', 'Blue Ribbon': '#306EFF', 'Sky Blue': '#6698FF', 'AntiqueWhite': '#FAEBD7', 'Camel brown': '#C19A6B', 'Purple Amethyst': '#6C2DC7', 'Ferrari Red': '#F70D1A', 'Light Sea Green': '#3EA99F', 'Cherry Red': '#C24641', 'Grape': '#5E5A80', 'Light Slate': '#CCFFFF', 'Baby Blue': '#95B9C7', 'Lapis Blue': '#15317E', 'Turquoise': '#43C6DB', 'Dragon Green': '#6AFB92', 'Brown Bear': '#835C3B', 'Tea Green': '#CCFB5D', 'Dark Carnation Pink': '#C12283', 'Lilac': '#C8A2C8', 'SeaShell': '#FFF5EE', 'Beer': '#FBB117', 'Smokey Gray': '#726E6D', 'Grapefruit': '#DC381F', 'Thistle': '#D2B9D3', 'Robin Egg Blue': '#BDEDFF', 'Celeste': '#50EBEC', 'Cream': '#FFFFCC', 'Blue Gray': '#98AFC7', 'Carnation Pink': '#F778A1', 'Granite': '#837E7C', 'Dull Purple': '#7F525D', 'Blue Angel': '#B7CEEC', 'Hazel Green': '#617C58', 'Crocus Purple': '#9172EC', 'Purple Monster': '#461B7E', 'Pale Blue Lily': '#CFECEC', 'Cyan or Aqua': '#00FFFF', 'Earth Blue': '#0000A0', 'Firebrick': '#800517', 'Blue Lotus': '#6960EC', 'Deep Sky Blue': '#3BB9FF', 'Powder Blue': '#C6DEFF', 'Plum Purple': '#583759'}

BASE_TABLE_STYLE = '#TABLE_ID {font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;border-collapse: collapse;width: 100%;}#TABLE_ID td, #TABLE_ID th {border: 1px;solid #ddd;padding: 8px;}#TABLE_ID tr:nth-child(even){background-color: #f2f2f2;}#TABLE_ID tr:hover {background-color: #ddd;}#TABLE_ID th {padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: TABLE_COLOR;color: white;}'

DEFAULT_STYLES = {
    "auto":[
        dataTag("meta",{"charset":"utf-8"},terminates=False),
        dataTag("meta",{"viewport":"width=device-width, initial-scale=1"},terminates=False),
        dataTag("link",{"href":"https://www.w3schools.com/w3css/4/w3.css","rel":"stylesheet"},terminates=False),
        dataTag("link",{"href":"https://fonts.googleapis.com/css?family=Lato","rel":"stylesheet"},terminates=False),
        dataTag("link",{"href":"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css","rel":"stylesheet"},terminates=False),
        basicTag("style",customize(BASE_TABLE_STYLE,{"TABLE_COLOR":COLORS["Purple"]}))
    ]
}

page = Page()

head = DEFAULT_STYLES["auto"]

body = [
    # header
    basicTag("h1","A paragraph about me"),
    # paragraph
    basicTag("p","I'm from Nigeria."),
    # list
    ListBlock(["Born in 1986","Loves Math","Degree in Mechanical Engineering"]),
    #table
    Table(
        {
            "Name":["John Elumelu","Cynthia Obiazor","Tobi Kamson"],
            "Department":["Mathematics","Civil Engineering","English"],
            "Age":[22,19,24],
            "Sex":["Male","Female","Male"]
        }
    ),
]
page.update_head(head)
page.update_body(body)
page.build()
print page.render()
