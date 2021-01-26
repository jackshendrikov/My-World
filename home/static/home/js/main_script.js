'use strict';

// Helper function
function addListenerToElement (element, eventType, listener) {
  element.addEventListener(eventType, listener)
}

// Add "active" class to clicked element, remove it from siblings and toggle show in sub-menus
function toggleActiveClass () {
  let parentElement = this.parentNode;
  let siblings = parentElement.parentNode.children;
  let dropDown = this.nextElementSibling;

  for (const value of siblings) {
    if (value.classList.contains('menu-item-active')) {
      value.classList.remove('menu-item-active')
    }
  }
  if (!parentElement.classList.contains('menu-item-active')) {
    parentElement.classList.add('menu-item-active')
  }
  if (dropDown !== null) {
    dropDown.classList.toggle('sub-menu-show')
  }
}

// Close the open dropdow clicking everywhere
function closeDropdown (event) {
  let dropDownShow = document.getElementsByClassName('sub-menu-show')[0];

  if (dropDownShow !== undefined && dropDownShow.previousElementSibling !== event.target) {
    dropDownShow.classList.remove('sub-menu-show')
  }
}

// Toggle animated menu opening in mobile view, dynamically based on menu items quantity
function toggleNav () {
  const navBar = this.parentNode.nextElementSibling;
  const menuItem = document.getElementsByClassName('menu-item');
  const menuItemHeight = menuItem[0].offsetHeight;
  const menuItemLength = menuItem.length;
  const menuHeight = menuItemHeight * menuItemLength;

  navBar.classList.toggle('menu-open');

  if (navBar.classList.contains('menu-open')) {
    navBar.animate([{ height: '0' }, { height: menuHeight + 'px' }], {
      duration: 500,
      easing: 'ease-in-out'
    })
  } else {
    navBar.animate([{ height: menuHeight + 'px' }, { height: '0' }], {
      duration: 500,
      easing: 'ease-in-out'
    })
  }
}

let menuItems = document.querySelectorAll('.menu-item-link');
let toggleButton = document.getElementById('toggle-nav');

for (const value of menuItems) {
  addListenerToElement(value, 'click', toggleActiveClass)
}

addListenerToElement(window, 'mouseup', closeDropdown);
addListenerToElement(toggleButton, 'click', toggleNav);

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
