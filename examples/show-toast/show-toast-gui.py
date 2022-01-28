import termo
from browser import document
from browser.html import STYLE, INPUT, BUTTON


document <= STYLE('''

body {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background-color: #F5F5DC;
}

input {
    width: 100%;
    height: 25vh;
    text-align: center;
    margin-bottom: 10px;
}

button {
   min-height: 60vh;
}

''')


input_text = INPUT(type='text', placeholder='text to show in a toast')
button_show = BUTTON('SHOW TOAST', style=dict(width='100%', height='90%'))

document <= input_text + button_show

input_text.focus()


def on_click(e):
    termo.app.show_toast(input_text.value if input_text.value else input_text.placeholder)
    input_text.value = ''
    input_text.focus()

button_show.bind('click', on_click)
