function snowfall() {
    let xmasSet = document.getElementById("xmas-version");
    xmasSet.style.display = "none";

    let defaultSet = document.getElementById("default-version");
    defaultSet.style.display = "inline";

    // Only supported in IE8+
    if ($.browser.msie && parseInt($.browser.version) < 8) return;

    // -------------------------------
    // --- Configuration variables ---
    // -------------------------------

    // How many frames per second?  More => smoother but more processor intensive
    let fps = 40;

    // How often should flakes be added?  Every 10 frames by default.  Greater => fewer flakes
    let addNewFlakesEveryNFrames = 10;

    // How many flakes should be added each time?  Greater => more flakes, more processor intensive
    let newFlakesToAdd = 3;

    // Controls the speed; 0.7 provides a nice speed
    let speedControl = 0.7;

    // -------------------------------
    // -------------------------------
    // -------------------------------

    // Holder variables
    let flakes = [];
    let additionCounter = 0;

    // The flake creator function
    function createFlake(curX, curY) {

        // How unique should each flake be?  These values specify max unique speed and wiggle/drift
        let maxSpeedOffset = 2;
        let maxWiggleOffset = 10;

        // How big should the flakes be?
        let minSize = 5;
        let maxSize = 15;

        // How much drifting/wiggling should be allowed in the downward path?
        let minWiggle = 10;
        let maxWiggle = 40;

        let sizePercent = Math.random();
        let size = Math.floor(sizePercent * (maxSize - minSize) + minSize);
        let opacity = 0.3 + Math.random() * 0.7;
        if ($.browser.msie && parseInt($.browser.version) < 10) //disable transparency on old IE to make rendering easier
            opacity = undefined;
        let color = '#9CF';

        // Create a unique speed offset, so each flake falls at a unique rate
        let speedOffset = Math.floor(Math.random() * maxSpeedOffset);

        // Create a unique wiggle amount based on size (bigger = more wiggle/drift)
        let wiggle = minWiggle + (maxWiggleOffset * Math.random()) + (maxWiggle - minWiggle) * sizePercent;

        let flake = $('<div class="snowflake">').text(' ').css({
            position: 'fixed',
            left: curX,
            top: curY,
            zIndex: 1000000,
            width: size,
            height: size,
            opacity: opacity,
            borderRadius: size / 2,
            '-moz-border-radius': size / 2,
            '-webkit-border-radius': size / 2,
            backgroundColor: color
        }).appendTo('body');

        let flakeObj = {
            size: size,
            sizePercent: sizePercent,
            homeX: curX,
            curX: curX,
            curY: curY,
            flake: flake,
            uniqueSpeedOffset: speedOffset,
            wiggle: wiggle,
            wiggleCounter: Math.floor(100 * Math.random())
        };
        flakes.push(flakeObj);

        return flakeObj;
    }

    // Create the sin table to save processing power later
    let sinTable = [];
    for (let i = 0; i < 100; i++) {
        let sin = Math.sin((i / 100) * Math.PI * 2);
        sinTable.push(sin);
    }

    // Track where the mouse is, so we can move flakes away from it
    let mouseX = -200;
    let mouseY = -200;
    let $w = $(window);
    $(document).mousemove(function(e) {
        mouseX = e.pageX - $w.scrollLeft();
        mouseY = e.pageY - $w.scrollTop();
    });

    function onEnterFrame() {
        // Update existing flakes
        let winH = $w.height();
        for (let i = flakes.length - 1; i > -1; i--) {
            let flakeObj = flakes[i];
            let flake = flakeObj.flake;
            let speed = 2 + (1 - flakeObj.sizePercent) * 5 + flakeObj.uniqueSpeedOffset; // bigger = slower to fall
            speed *= speedControl; // apply the speed control
            let curY = flakeObj.curY;
            let newY = curY + speed;

            let wiggleCounter = flakeObj.wiggleCounter = (++flakeObj.wiggleCounter % 100);
            let sin = sinTable[wiggleCounter];
            let wiggle = flakeObj.wiggle * sin;
            let newX = flakeObj.homeX + wiggle;

            // If we're close to the mouse, force out of the way
            let mouseXDist = Math.abs(mouseX - newX);
            let mouseYDist = Math.abs(mouseY - newY);
            let influenceArea = 150;
            if (mouseXDist < influenceArea && mouseYDist < influenceArea) {
                let maxForce = 10;
                let dist = Math.sqrt(mouseXDist * mouseXDist + mouseYDist * mouseYDist);
                if (dist < influenceArea) {
                    let influence = maxForce * (1 - (dist / influenceArea));
                    if (mouseY > newY) {
                        newY -= influence;
                        if (mouseX < newX) flakeObj.homeX += influence;
                        else flakeObj.homeX -= influence;
                    }
                    else newY += influence;
                }
            }

            flakeObj.curY = newY;
            flakeObj.curX = newX;
            flake.css({
                top: newY,
                left: newX
            });

            // Destroy flake if it has gone out of view by 100
            if (newY > winH + 100) {
                flake.remove();
                flakeObj.flake = null;
                flakes.splice(i, 1);
            }
        }

        // Add any new flakes
        if (++additionCounter % addNewFlakesEveryNFrames === 0) {
            additionCounter = 0;

            let minX = -100;
            let maxX = $(window).width() + 100;
            let homeY = -100;
            for (let i = 0; i < newFlakesToAdd; i++) {
                let curX = minX + Math.floor(Math.random() * (maxX - minX));
                let curY = homeY + Math.floor(100 * Math.random());
                createFlake(curX, curY);
            }
        }
    }

    // Start the animation based on the requested frames per second
    let timerID = setInterval(onEnterFrame, 1000 / fps);

    $("#default-version").click(function() {
        clearInterval(timerID);
        [...document.getElementsByClassName("snowflake")].map(n => n && n.remove());
        defaultSet.style.display = "none";
        xmasSet.style.display = "inline";
    });
}