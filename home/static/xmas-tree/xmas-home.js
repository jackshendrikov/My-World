let greeting = [
    'printf("{0}");',
    'cout << "{0}" << endl;',
    'WriteLn("{0}");',
    'System.out.println( "{0}" );',
    'print "{0}"',
    'fmt.Println("{0}");',
    'echo "{0}"',
    'say "{0}"',
    'print("{0}");',
    '(print "{0}")',
    'PRINT "{0}"',
    '<%= "{0}" %>',
    'System.Console.WriteLine("{0}");',
    'console.log("{0}");',
    'document.write("{0}")',
];

let year = new Date().getFullYear() + 1;
let str = ["Merry Christmas!", "Happy New Year!", "Hello " + year + "!"];

if (!String.prototype.format) {
    String.prototype.format = function() {
        let args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ?
                args[number] :
                match;
        });
    };
}

function transform(element, value) {
    element.style.WebkitTransform = value;
    element.style.MozTransform = value;
    element.style.msTransform = value;
    element.style.OTransform = value;
    element.style.transform = value;
}

function getRandom(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}


let div;

function createBranch(width, height) {
    div = document.createElement('button');

    let s = greeting[getRandom(0, greeting.length - 1)].format(str[getRandom(0, str.length - 1)]);

    let text = document.createTextNode(s);

    div.setAttribute("id", "branch");
    div.setAttribute("class", "christmas");

    div.appendChild(text);

    div.style.width = width + 'px';
    div.style.height = height + 'px';
    let green = 75 + Math.ceil(Math.random() * 200);
    let other = Math.ceil(Math.random() * 50);
    div.style.backgroundColor = "rgba(" + other + "," + green + "," + other + ", 1)";
    div.onclick = function() {
        window.open(links[getRandom(0, links.length - 1)], "_self")
    };
    return div;
}


let width = 500;
let height = 600;
let tree = document.getElementById("tree");
tree.style.width = width + 'px';
tree.style.height = height + 'px';

for (let i = 0; i < 350; i++) {
    let top_margin = 70;
    let x = width / 2;
    let y = Math.round(Math.random() * height) + top_margin;
    let rx = 0;
    let ry = Math.random() * 360;
    let rz = Math.random() * 3;
    let elementWidth = 15 + (((y - top_margin) / height) * width / 1.8);
    let elementHeight = 26;

    div = createBranch(elementWidth, elementHeight);

    transform(div, 'translate3d(' + x + 'px, ' + y + 'px, 0px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) rotateZ(' + rz + 'deg)');
    tree.appendChild(div);
}

let items = [], point = document.querySelector('svg').createSVGPoint();

function getCoordinates(e, svg) {
  point.x = e.clientX;
  point.y = e.clientY;
  return point.matrixTransform(svg.getScreenCTM().inverse());
}

function changeColor(e) {
  document.body.className = e.currentTarget.className;
}

function Item(config) {
  Object.keys(config).forEach(function (item) {this[item] = config[item];}, this);
  this.el.addEventListener('mousemove', this.mouseMoveHandler.bind(this));
  this.el.addEventListener('touchmove', this.touchMoveHandler.bind(this));
}

Item.prototype = {
  update: function update(c) {
    this.clip.setAttribute('cx', c.x);
    this.clip.setAttribute('cy', c.y);
  },
  mouseMoveHandler: function mouseMoveHandler(e) {
    this.update(getCoordinates(e, this.svg));
  },
  touchMoveHandler: function touchMoveHandler(e) {
    e.preventDefault();
    let touch = e.targetTouches[0];
    if (touch) return this.update(getCoordinates(touch, this.svg));
  }
};

[].slice.call(document.querySelectorAll('.item'), 0).forEach(function (item, index) {
  items.push(new Item({
    el: item,
    svg: item.querySelector('svg'),
    clip: document.querySelector('#clip-'+index+' circle'),
  }));
});

[].slice.call(document.querySelectorAll('button'), 0).forEach(function (button) {
  button.addEventListener('click', changeColor);
});