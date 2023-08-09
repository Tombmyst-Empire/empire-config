from pygments.style import Style
from pygments.token import Comment, Keyword, Name, Number, Operator, String


class EmPygments(Style):
    background_color = "#111"
    default_style = ""
    styles = {
        Comment: "italic #767676",
        Keyword: "bold #cb06bd",
        Name: "#b3b3b3",
        Name.Function: "#a800ff",
        Name.Function.Magic: "#ff0092",
        Name.Class: "bold #e89f00",
        Name.Builtin.Pseudo: "bold #2aff3a",
        Name.Decorator: "#9e700c",
        Name.Exception: "#bf857d",
        String: "#00a700",
        Number: "#f00",
        Operator: "bold",
    }
