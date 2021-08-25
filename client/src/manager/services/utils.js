export function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

export function isColorValid(color) {
    return color.slice(0,1) === "#" && (color.length === 4 || color.length === 7) && color.slice(1).split("").map(char => '0123456789ABCDEF'.includes(char.toUpperCase()))
}