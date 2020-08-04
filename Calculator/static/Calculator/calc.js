var buttons = document.getElementsByTagName("button")
var back = document.getElementById("backslash")
var clear = document.getElementById("clear")
var equal = document.getElementById("equal")
var screen = document.getElementById("screen")
var base_respone = "http://localhost:8080/Calculator/";


var exprisson = []

var temp = []
for (let i = 0; i < buttons.length; ++i)
    temp.push(buttons[i])
buttons = temp

function isLetter(str) {
    return str.match(/[a-z]/i);
}

function screen_out() {

    let output = ""
    exprisson.forEach(el => output += el)
    screen.value = output

}

function generate_output() {

    let xhttp = new XMLHttpRequest()

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            output = JSON.parse(this.responseText).result
            exprisson = []
            exprisson.push(output)
            screen_out()
        } else {

            exprisson = ['Error']
            screen_out()
        }
    };

    let exp = ""
    let replaced_expression = exprisson.map(el => { //  sending / to server cause error as the / mess with pathing, solved by replacing / with @ and converting it back in server
        if (el == '/') return '@'
        else return el
    })
    replaced_expression.forEach(el => exp += el)
    xhttp.open('GET', base_respone + exp + '/calculate')
    xhttp.send()


}


equal.onclick = generate_output


back.onclick = () => {
        exprisson.pop();
        screen_out()
    } // delete an element from the end of the expression

clear.onclick = () => {
        exprisson = [];
        screen_out()
    } // clear the expression

buttons = buttons.filter(btn => btn.value != "<=" && btn.value != "clear" && btn.value != "=")




for (let i = 0; i < buttons.length; ++i)
    buttons[i].onclick = function(event) {

        //append a value to expression
        let txt = this.value
        if (isLetter(txt[0]) && txt != "pi" && txt != 'e') txt += '(' // if txt is a function append a "(" to the end of it
        exprisson.push(txt)
        screen_out()
    }