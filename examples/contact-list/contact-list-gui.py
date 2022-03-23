import termo
from browser import document, window
from browser.html import *


document <= STYLE("""

* {
    margin: 0px;
    box-sizing: border-box;
}

body {
    width: 100vw;
    height: 100vh;
    background-color: white;
}

table {
    width: 100%;
}

tr {
    width: 100%;
}

td {
    width: 50%;
    text-align: center;
    padding: 1em;
    color: white;
    background-color: black;
}

""")


table = TABLE()
document <= table

contact_list = termo.app.get_contact_list()

for row in contact_list:

	name = row['name']
	number = row['number']

	table <= TR([TD(name), TD(number)])
