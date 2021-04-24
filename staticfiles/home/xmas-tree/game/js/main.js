function main() {
  const config = {
    parent: 'game',
    type: Phaser.AUTO,
    width: Config.CAMERA_WIDTH_PX,
    height: Config.CAMERA_HEIGHT_PX,
    physics: {
      default: 'arcade'
    },
    scene: {
      preload: preloadFn,
      create: createFn,
      update: updateFn
    }
  };
  const game = new Phaser.Game(config);
  let blockList;
  let cursorKeys;
  let directorKeys;
  let directorState;
  let gift;
  let grinch;
  let instructions;
  let puzzle;
  let dasha;
  let santa;
  let victoryCutscene;
  let world;

  function preloadFn() {
    this.load.spritesheet('girl', 'img/dasha.png', {
      frameWidth: Config.DASHA_SPRITE_WIDTH,
      frameHeight: Config.DASHA_SPRITE_HEIGHT
    });

    this.load.spritesheet('santarun', 'img/santarun.png', {
      frameWidth: Config.SANTA_RUN_SPRITE_WIDTH,
      frameHeight: Config.SANTA_RUN_SPRITE_HEIGHT
    });

    this.load.spritesheet('santadead', 'img/santadead.png', {
      frameWidth: Config.SANTA_DEAD_SPRITE_WIDTH,
      frameHeight: Config.SANTA_DEAD_SPRITE_HEIGHT
    });

    this.load.spritesheet('grinchrun', 'img/grinchrun.png', {
      frameWidth: Config.GRINCH_RUN_SPRITE_WIDTH,
      frameHeight: Config.GRINCH_RUN_SPRITE_HEIGHT
    });

    this.load.spritesheet('tree', 'img/tree.png', {
      frameWidth: Config.TREE_SPRITE_WIDTH,
      frameHeight: Config.TREE_SPRITE_HEIGHT
    });

    this.load.spritesheet('jackblink', 'img/jackblink.png', {
      frameWidth: Config.JACK_SPRITE_WIDTH,
      frameHeight: Config.JACK_SPRITE_HEIGHT
    });

    this.load.image('bookcase', 'img/bookcase.png');
    this.load.image('carpathians', 'img/carpathians.png');
    this.load.image('confetti1', 'img/confetti1.png');
    this.load.image('confetti2', 'img/confetti2.png');
    this.load.image('confetti3', 'img/confetti3.png');
    this.load.image('confetti4', 'img/confetti4.png');
    this.load.image('confetti5', 'img/confetti5.png');
    this.load.image('confetti6', 'img/confetti6.png');
    this.load.image('confetti7', 'img/confetti7.png');
    this.load.image('counter', 'img/counter.png');
    this.load.image('crate', 'img/crate.png');
    this.load.image('fireplace', 'img/fireplace.png');
    this.load.image('flowers', 'img/flowers.png');
    this.load.image('gift', 'img/gift.png');
    this.load.image('glow', 'img/glow.png');
    this.load.image('goverla', 'img/goverla.png');
    this.load.image('grinchfaint', 'img/grinchfaint.png');
    this.load.image('harry', 'img/harry.png');
    this.load.image('heart', 'img/heart.png');
    this.load.image('kyiv', 'img/kyiv.png');
    this.load.image('pathmarker', 'img/pathmarker.png');
    this.load.image('piano', 'img/piano.png');
    this.load.image('rugleft', 'img/rugleft.png');
    this.load.image('rugmiddle', 'img/rugmiddle.png');
    this.load.image('rugtop', 'img/rugtop.png');
    this.load.image('rugtopleft', 'img/rugtopleft.png');
    this.load.image('wallright', 'img/wallright.png');
    this.load.image('walltop', 'img/walltop.png');
    this.load.image('walltopright', 'img/walltopright.png');
    this.load.image('wood', 'img/wood.png');
    this.load.image('welcome', 'img/welcome.png');
    this.load.image('window', 'img/window.png');
    this.load.image('zp', 'img/zp.png');
  }

  function createFn() {
    cursorKeys = this.input.keyboard.createCursorKeys();
    directorKeys = this.input.keyboard.addKeys('space');

    directorState = new DirectorState(directorKeys);
    world = new World(this);
    grid = new Grid(this, world);
    puzzle = new Puzzle(world, grid);
    blockList = new BlockList(this, world, grid, directorState);
    santa = new Santa(this, grid, directorState);
    grinch = new Grinch(this, grid, directorState);
    dasha = new Dasha(this, world, grid, cursorKeys);
    gift = new Gift(this, grid);
    director = new Director(this, grid, puzzle, santa, grinch, gift, directorState);
    victoryCutscene = new VictoryCutscene(this, dasha, gift, directorState,
        ['confetti1', 'confetti2', 'confetti3', 'confetti4', 'confetti5', 'confetti6', 'confetti7']);
    instructions = new Instructions(this);

    this.input.keyboard.on('keydown', function(e) {
      if (e.keyCode === Config.DIRECTOR_PRODUCTION_RUNNING_KEY_CODE) {
        director.toggleProductionRunning();
      }
      if (e.keyCode === Config.RESET_KEY_CODE) {
        // resetWithPresetPuzzle(this);
      }
      if (e.keyCode === Config.TOGGLE_INSTRUCTIONS_KEY_CODE) {
        instructions.toggleVisibility();
      }
    });

    resetWithPresetPuzzle(this /* scene */);
  }

  function updateFn() {
    blockList.update(dasha.getSprite(), cursorKeys);
    // Dasha must move after checking for collisions to allow other sprites to check for overlaps on the next update.
    world.checkCollisions(dasha.getSprite());

    dasha.update();
    santa.update();
    grinch.update();
    gift.update();
    victoryCutscene.update();
  }

  function resetWithPresetPuzzle(scene) {
    if (directorState.isVictorious()) {
      // Don't reset if we're victorious.
      return;
    }
    resetPuzzle(scene, 4, 1, 6, 1, 3, 4, 40);
  }

  function resetPuzzle(scene, startY, endY, targetX, targetY, dashaX, dashaY, grinchMaxStamina) {
    world.reset();
    grid.reset(startY, endY, {x: targetX, y: targetY});
    
    const rightWallGapCenter = grid.getTileCenter(0, endY);
    world.renderRightWall(
        rightWallGapCenter.y - Config.GRID_TILE_SIZE_PX / 2,
        rightWallGapCenter.y + Config.GRID_TILE_SIZE_PX / 2);
    blockList.reset();
    blockList.addBlockInGrid(1, 2, 'crate');
    blockList.addBlockInGrid(2, 4, 'crate');
    blockList.addBlockInGrid(4, 6, 'crate');
    blockList.addBlockInGrid(7, 1, 'crate');
    blockList.addBlockInGrid(7, 2, 'crate');
    blockList.addBlockInGrid(8, 5, 'crate');
    blockList.addBlockInGrid(9, 4, 'crate');

    createBlinkAnimation(scene, 'jackBlinking');
    const jack = blockList.addBlockOffGrid(0, -1, 'jackblink', 'jackBlinking');

    santa.hide();
    grinch.reset(grinchMaxStamina);
    gift.hide();
    director.reset();
    dasha.reset(jack);

    const dashaBounds = dasha.getSprite().getBounds();
    if (world.anyObstacleInRegion(dashaBounds.centerX, dashaBounds.centerY, dashaBounds.width, dashaBounds.height)) {
      dasha.teleportTo(dashaX, dashaY);
    }
  }

  function createBlinkAnimation(scene, animationKey) {
    const frames = [];
    for (let i = 0; i < Config.JACK_BLINKING_RATIO; i++) {
      frames.push({
        key: 'jackblink',
        frame: 0
      });
    }
    frames.push({
      key: 'jackblink',
      frame: 1
    });

    scene.anims.create({
      key: 'jackBlinking',
      frames: frames,
      frameRate: Config.JACK_BLINKING_SPEED,
      repeat: -1
    });
  }
}

window.onload = main;
