let artwork;
let colorArray;

function degrees_to_radians(degrees) {
	let pi = Math.PI;
	return degrees * (pi / 180);
}

function setup() {
	createCanvas(windowWidth, windowHeight);
	artwork = new Artwork();
	artwork.createNew(50, 10, 20);
}

function mousePressed() {
	setup();
}

function draw() {
	background(0, 0, 0);
	artwork.display();
}

function windowResized() {
	waitress = millis() + 2000;
	if (fullscreen()) {
		resizeCanvas(displayWidth, displayHeight);
	} else {
		resizeCanvas(windowWidth, windowHeight);
	}
	showing = true;
	setup();
}

class Artwork {
	constructor() {
		this.rings = [];
		this.centerRadius;
		this.baseBandSize;

		this.rotationRate = 10;
		this.rotationIndex = 0;
	}

	createNew(numberOfRings, centerRadius, baseBandSize) {
		this.centerRadius = centerRadius;
		this.baseBandSize = baseBandSize;

		for (let i = 0; i < numberOfRings; i++) {
			this.rings.push(
				new Ring(
					i,
					i,
					this.baseBandSize,
					this.centerRadius,
					color(random(0, 256), random(0, 256), random(0, 256)),
					color(random(0, 256), random(0, 256), random(0, 256))
				)
			);
		}
	}

	display() {
		_.forEach(this.rings, (r) => r.display());
	}
}

class Ring {
	constructor(
		id,
		layer,
		baseBandSize,
		centerRadius,
		ringTriangleColor,
		ringOuter
	) {
		this.id = id;
		this.layer = layer;
		this.baseBandSize = baseBandSize;
		this.centerRadius = centerRadius;
		this.ringTriangleColor = ringTriangleColor;
		this.ringOuter = ringOuter;
		this.innerRadius = this.centerRadius + this.layer * this.baseBandSize;
		this.outerRadius = this.innerRadius + this.baseBandSize;
		this.angle = 0;
		this.rateOfChange = 0.25;
		this.directionClockwise = this.layer % 2;

		this.inverseDensity = 3;
		this.maxRotations = 360 / this.inverseDensity;
		this.angleFind = 360 / this.maxRotations;
		this.tick = [];
		this.tickMax = [];
		this.tickMin = [];
		this.ticksTarget = [];

		this.tick.length = this.maxRotations;
		this.tickMax.length = this.maxRotations;
		this.tickMin.length = this.maxRotations;
		this.ticksTarget.length = this.maxRotations;

		this.rateOfTickChange = 0.5;
		for (let i = 0; i < this.maxRotations; i++) {
			this.tick[i] = 0;

			let r1 = random(this.innerRadius, this.outerRadius);
			let r2 = random(this.innerRadius, this.outerRadius);

			this.tickMax[i] = r2 > r1 ? r2 : r1;
			this.tickMin[i] = r2 > r1 ? r1 : r2;
			this.ticksTarget[i] = 0;
		}
	}

	display() {
		noFill();
		strokeWeight(1);
		this.drawBands();
		this.drawTicTockBand();
	}

	drawBands() {
		stroke(this.ringOuter);
		ellipse(windowWidth / 2, windowHeight / 2, this.outerRadius * 2);
	}

	drawTicTockBand() {
		if (this.directionClockwise) {
			this.angle = (this.angle + this.rateOfChange) % 360;
		} else {
			this.angle = (this.angle - this.rateOfChange) % 360;
		}

		for (let i = 0; i < this.maxRotations; i++) {
			this.drawTick((this.angle + i * this.angleFind) % 360, this.angleFind, i);
		}
	}

	drawTick(topAngle, angleFind, index) {
		let point1 = this.findPointByAngleAndCircle(topAngle, this.innerRadius);

		if (this.ticksTarget[index] === 0) {
			this.tick[index] = this.tickMin[index];
			this.ticksTarget[index] = this.tickMax[index];
		}

		if (this.tick[index] >= this.tickMax[index]) {
			this.ticksTarget[index] = this.tickMin[index];
		}

		if (this.tick[index] <= this.tickMin[index]) {
			this.ticksTarget[index] = this.tickMax[index];
		}

		if (this.ticksTarget[index] > this.tick[index]) {
			this.tick[index] += this.rateOfTickChange;
		} else {
			this.tick[index] -= this.rateOfTickChange;
		}

		let point2 = this.findPointByAngleAndCircle(topAngle, this.tick[index]);

		line(point1.x, point1.y, point2.x, point2.y);
	}

	findPointByAngleAndCircle(a, r) {
		let x = windowWidth / 2 + r * cos(degrees_to_radians(a));
		let y = windowHeight / 2 + r * sin(degrees_to_radians(a));

		return { x: x, y: y };
	}
}

