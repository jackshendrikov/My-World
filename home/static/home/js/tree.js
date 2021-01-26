MorphSVGPlugin.convertToPath('polygon');

const xmlns = "http://www.w3.org/2000/svg", xlinkns = "http://www.w3.org/1999/xlink";

select = function(s) {
    return document.querySelector(s);
    },
    selectAll = function(s) {
    return document.querySelectorAll(s);
    },
    pContainer = select('.pContainer'),
    mainSVG = select('.mainSVG'),
    star = select('#star'),
    sparkle = select('.sparkle'),
    tree = select('#tree'),
    showParticle = true,
    // particleColorArray = ['#69D2E7', '#A7DBD8', '#E0E4CC', '#F38630', '#FA6900'],
    // particleColorArray = ['#7FBBEF','#D5780F','#381502','#FDED56','#7D1607','#F0C495','#C2293B','#53AB61','#343DE1','#FCD422'],
    particleColorArray = ['#FFFCF9', '#339B8B', '#B74551','#C89568','#CC9966', '#336666', '#669966', '#CC9966', '#CC3333', '#339B8B', '#B74551'],
    // particleColorArray = ['#E8F6F8', '#ACE8F8', '#F6FBFE','#A2CBDC','#B74551', '#5DBA72', '#910B28', '#910B28', '#446D39'],
    particleTypeArray = ['#star','#circ','#cross','#heart'],
    particleTypeArray = ['#star'],
    particlePool = [],
    particleCount = 0,
    numParticles = 250

TweenMax.set('svg', {
    visibility: 'visible'
})

TweenMax.set(sparkle, {
	transformOrigin:'50% 50%',
	y:-100
})

let treePath = MorphSVGPlugin.pathDataToBezier(select('.treePath').getAttribute('d'), {
  offsetX: 0,
  offsetY: 0
});

let treeBottomPath = MorphSVGPlugin.pathDataToBezier(select('.treeBottomPath').getAttribute('d'), {
  offsetX: 0,
  offsetY: 0
});

//console.log(starPath.length)
let mainTl = new TimelineMax({delay: 10, repeat: -1}), starTl;

// mainTl.seek(100).timeScale(1.82)

function randomBetween(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

function flicker(p){
    //console.log("flivker")
    TweenMax.killTweensOf(p, {opacity:true});
    TweenMax.fromTo(p, 0.07,{
        alpha:1
    }, {
        alpha:Math.random(),
        //ease: RoughEase.ease.config({ template: Power0.easeNone, strength: 3, points: 6, taper: "both", randomize: true, clamp: false}),
        repeat:-1
    })
}

function createParticles() {
    // var step = numParticles/starPath.length;
    // console.log(starPath.length)
    let i = numParticles, p, particleTl, step = numParticles / treePath.length, pos;
    while (--i > -1) {
        p = select(particleTypeArray[i%particleTypeArray.length]).cloneNode(true);
        mainSVG.appendChild(p);
        p.setAttribute('fill', particleColorArray[i % particleColorArray.length]);
        p.setAttribute('class', "particle");
        particlePool.push(p);
        //hide them initially
        TweenMax.set(p, {
            x:-100,
            y:-100,
            transformOrigin:'50% 50%'
        })
    }
}

function getScale(){
  return randomBetween(5, 20) / 10;
}

function playParticle(p){
    if(!showParticle){return};
    var p = particlePool[particleCount]
    TweenMax.set(p, {
        //attr:{
            x: pContainer._gsTransform.x,
            y: pContainer._gsTransform.y,
            scale:getScale()
    });

    let tl = new TimelineMax();
    tl.to(p, randomBetween(10, 60)/10, {
        physics2D: {
            velocity: randomBetween(-13, 16),
            angle:randomBetween(-180, 180),
            gravity:randomBetween(-13, 44)
        },

        scale:0,
        rotation:randomBetween(-123,360),
        //skewY:(Math.random() * 180),
        ease: Power1.easeOut,
        onStart:flicker,
        onStartParams:[p],
        //repeat:-1,
        onRepeat: function(p) {
            TweenMax.set(p, {
                scale:getScale()
            })
        },
        onRepeatParams: [p]
    });

    //particlePool[particleCount].play();
    particleCount++;
    //mainTl.add(tl, i / 1.3)
    particleCount = (particleCount >=numParticles) ? 0 : particleCount
}

function drawStar(){
    starTl = new TimelineMax({onUpdate:playParticle})
    starTl.to([pContainer, sparkle], 6, {
        bezier: {
            type: "cubic",
            values: treePath,
            autoRotate: false
        },
        ease: Linear.easeNone
    })
        .to([pContainer, sparkle], 1, {
            onStart:function(){showParticle = false},
            x:treeBottomPath[0].x,
            y:treeBottomPath[0].y
        })
        .to([pContainer, sparkle], 2, {
            onStart:function(){showParticle = true},
            bezier: {
                type: "cubic",
                values: treeBottomPath,
                autoRotate: false
            },
            ease: Linear.easeNone
        },'-=0')
.from('.treeBottomMask', 2, {
    drawSVG:'0% 0%',
    stroke:'#FFF',
    ease:Linear.easeNone
},'-=2')
  //TweenMax.staggerTo(particlePool, 2, {})
}

function textAnim(){}

createParticles();
drawStar();
//ScrubGSAPTimeline(mainTl)

mainTl.staggerFrom(['.treePathMask','.treePotMask','.treeBottomMask'], 6, {
    drawSVG:'0% 0%',
    stroke:'#FFF',
    cycle:{
        duration:[6, 1,2]
    },
    ease:Linear.easeNone
},6)

    .from('.treeStar', 3, {
        //skewY:270,
        scaleY:0,
        scaleX:0.15,
        transformOrigin:'50% 50%',
        ease:Elastic.easeOut.config(1,0.5)
    },'-=4')

    .to(['.treeStarOutline', '.messageText'], 1, {
        alpha:1,
        ease:RoughEase.ease.config({ template:  Power0.easeNone, strength: 2, points: 16, taper: "none", randomize: true, clamp: false})
    },'-=3')

    .to(sparkle, 3, {
        alpha:0,
        ease:RoughEase.ease.config({ template:  Power0.easeNone, strength: 2, points: 100, taper: "both", randomize: true, clamp: false})
    },'-=5')

    .to('.whole', 2, {
        alpha:0,
        ease:Sine.easeIn
    },'+=2')

mainTl.add(starTl, 0)
TweenMax.globalTimeScale(1.3);
//ScrubGSAPTimeline(mainTl)