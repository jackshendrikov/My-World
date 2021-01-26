class World {
  constructor(scene) {
    this.scene_ = scene;
    this.nonResettableObstacles_ = [];
    this.obstacleSprites_ = [];
    this.nonBlockingObstacleSprites_ = [];

    scene.physics.world.setBounds(0, 0, Config.WORLD_WIDTH_PX, Config.WORLD_HEIGHT_PX);

    // Render the floor.
    const floor = scene.add.tileSprite(Config.WORLD_WIDTH_PX / 2, Config.WORLD_HEIGHT_PX / 2,
        Config.WORLD_WIDTH_PX, Config.WORLD_HEIGHT_PX, 'wood');
    floor.depth = Depths.FLOOR;

    this.renderWalls_();

    this.renderObjects_();
  }

  reset() {
    this.obstacleSprites_ = [];
    this.nonBlockingObstacleSprites_ = [];
  }

  renderWalls_() {
    const topWall = this.scene_.physics.add.existing(
        this.scene_.add.tileSprite(Config.WORLD_WIDTH_PX / 2, Config.WORLD_WALL_TOP_HEIGHT_PX / 2,
            Config.WORLD_WIDTH_PX, Config.WORLD_WALL_TOP_HEIGHT_PX, 'walltop'),
        true /* static */);
    topWall.depth = Depths.FLOOR;

    const topRightWall = this.scene_.physics.add.sprite(
        Config.WORLD_WIDTH_PX - Config.WORLD_WALL_TOP_RIGHT_WIDTH_PX / 2,
        Config.WORLD_WALL_TOP_RIGHT_HEIGHT_PX / 2,
        'walltopright');
    topRightWall.depth = Depths.FLOOR;
    topRightWall.setImmovable(true);

    const topLeftWall = this.scene_.physics.add.sprite(
        Config.WORLD_WALL_TOP_RIGHT_WIDTH_PX / 2,
        Config.WORLD_WALL_TOP_RIGHT_HEIGHT_PX / 2,
        'walltopright');
    topLeftWall.depth = Depths.FLOOR;
    topLeftWall.setImmovable(true);
    topLeftWall.flipX = -1;

    const leftWall = this.scene_.physics.add.existing(
        this.scene_.add.tileSprite(
            Config.WORLD_WALL_SIDE_WIDTH_PX / 2,
            (Config.WORLD_HEIGHT_PX + Config.WORLD_WALL_TOP_RIGHT_HEIGHT_PX) / 2,
            Config.WORLD_WALL_SIDE_WIDTH_PX,
            Config.WORLD_HEIGHT_PX - Config.WORLD_WALL_TOP_RIGHT_HEIGHT_PX,
            'wallright'),
        true /* static */);
    leftWall.depth = Depths.FLOOR;
    leftWall.flipX = -1;
    
    this.addNonResettableObstacleSprite_(topWall);
    this.addNonResettableObstacleSprite_(topRightWall);
    this.addNonResettableObstacleSprite_(topLeftWall);
    this.addNonResettableObstacleSprite_(leftWall);
  }

  renderRightWall(gapTopY, gapBottomY) {
    const rightWallTop = this.scene_.physics.add.existing(
        this.scene_.add.tileSprite(
            Config.WORLD_WIDTH_PX - Config.WORLD_WALL_SIDE_WIDTH_PX / 2,
            (gapTopY + Config.WORLD_WALL_TOP_RIGHT_HEIGHT_PX) / 2,
            Config.WORLD_WALL_SIDE_WIDTH_PX,
            gapTopY - Config.WORLD_WALL_TOP_RIGHT_HEIGHT_PX,
            'wallright'),
        true /* static */);
    rightWallTop.depth = Depths.FLOOR;

    const rightWallBottom = this.scene_.physics.add.existing(
        this.scene_.add.tileSprite(
            Config.WORLD_WIDTH_PX - Config.WORLD_WALL_SIDE_WIDTH_PX / 2,
            (Config.WORLD_HEIGHT_PX + gapBottomY) / 2,
            Config.WORLD_WALL_SIDE_WIDTH_PX,
            Config.WORLD_HEIGHT_PX - gapBottomY,
            'wallright'),
        true /* static */);
    rightWallBottom.depth = Depths.FLOOR;

    this.addObstacleSprite(rightWallTop);
    this.addObstacleSprite(rightWallBottom);
  }

  renderObjects_() {
    const pianoWidth = Config.WORLD_PIANO_WIDTH_PX * Config.WORLD_PIANO_SCALE;
    const pianoHeight = Config.WORLD_PIANO_HEIGHT_PX * Config.WORLD_PIANO_SCALE;
    const piano = this.scene_.physics.add.sprite(Config.WORLD_WALL_SIDE_WIDTH_PX + pianoWidth / 2, 200, 'piano');
    piano.displayWidth = pianoWidth;
    piano.displayHeight = pianoHeight;
    piano.depth = Depths.OBJECTS;
    piano.setImmovable(true);

    const bookcaseWidth = Config.WORLD_BOOKCASE_WIDTH_PX * Config.WORLD_BOOKCASE_SCALE;
    const bookcaseHeight = Config.WORLD_BOOKCASE_HEIGHT_PX * Config.WORLD_BOOKCASE_SCALE;
    const bookcase = this.scene_.physics.add.sprite(Config.WORLD_WIDTH_PX - Config.WORLD_WALL_SIDE_WIDTH_PX - bookcaseWidth / 2,
        100,
        'bookcase');
    bookcase.displayWidth = bookcaseWidth;
    bookcase.displayHeight = bookcaseHeight;
    bookcase.depth = Depths.OBJECTS;
    bookcase.setImmovable(true);

    const flowers = this.scene_.physics.add.sprite(
        bookcase.x - bookcase.displayWidth / 2 - Config.WORLD_FLOWERS_WIDTH_PX / 2 - 10,
        bookcase.y + bookcase.displayHeight / 2 - Config.WORLD_FLOWERS_HEIGHT_PX / 2,
        'flowers');
    flowers.depth = Depths.OBJECTS;
    flowers.setImmovable(true);

    const counter = this.scene_.physics.add.sprite(310, 140, 'counter');
    counter.depth = Depths.OBJECTS_IN_FRONT;
    const counterObstacle = this.scene_.physics.add.sprite(counter.x,
        counter.y + Config.WORLD_BEHIND_COUNTER_HEIGHT_PX / 2,
        'crate');
    counterObstacle.alpha = 0;
    counterObstacle.displayWidth = counter.displayWidth;
    counterObstacle.displayHeight = counter.displayHeight - Config.WORLD_BEHIND_COUNTER_HEIGHT_PX;
    counterObstacle.setImmovable(true);

    const snowWindow = this.scene_.add.sprite(counter.x, Config.WORLD_WALL_TOP_HEIGHT_PX / 2, 'window');
    snowWindow.depth = Depths.OBJECTS;

    const zp = this.scene_.add.sprite(counter.x - 83, Config.WORLD_WALL_TOP_HEIGHT_PX / 2, 'zp');
    zp.depth = Depths.OBJECTS;

    const harry = this.scene_.add.sprite(counter.x - 148, Config.WORLD_WALL_TOP_HEIGHT_PX / 2, 'harry');
    harry.depth = Depths.OBJECTS;

    const carpathians = this.scene_.add.sprite(79, Config.WORLD_WALL_TOP_HEIGHT_PX / 2, 'carpathians');
    carpathians.depth = Depths.OBJECTS;

    const kyiv = this.scene_.add.sprite(counter.x + 87, Config.WORLD_WALL_TOP_HEIGHT_PX / 2, 'kyiv');
    kyiv.depth = Depths.OBJECTS;

    const goverla = this.scene_.add.sprite(counter.x + 166, Config.WORLD_WALL_TOP_HEIGHT_PX / 2, 'goverla');
    goverla.depth = Depths.OBJECTS;

    this.addNonResettableObstacleSprite_(piano);
    this.addNonResettableObstacleSprite_(flowers);
    this.addNonResettableObstacleSprite_(bookcase);
    this.addNonResettableObstacleSprite_(counterObstacle);
  }

  addNonResettableObstacleSprite_(sprite) {
    this.nonResettableObstacles_.push(sprite);
  }

  addObstacleSprite(sprite) {
    this.obstacleSprites_.push(sprite);
  }

  addNonPathBlockingObstacleSprite(sprite) {
    this.nonBlockingObstacleSprites_.push(sprite);
  }

  anyPathBlockingObstacleInRegion(centerX, centerY, width, height) {
    return this.anyObstacleInRegion_(
        this.obstacleSprites_.concat(this.nonResettableObstacles_),
        centerX,
        centerY,
        width,
        height);
  }

  anyObstacleInRegion(centerX, centerY, width, height) {
    return this.anyObstacleInRegion_(
        this.obstacleSprites_.concat(this.nonBlockingObstacleSprites_).concat(this.nonResettableObstacles_),
        centerX,
        centerY,
        width,
        height);
  }

  anyObstacleInRegion_(obstacles, centerX, centerY, width, height) {
    const region = new Phaser.Geom.Rectangle(centerX - width / 2, centerY - height / 2, width, height);
    for (let i = 0; i < obstacles.length; i++) {
      const obstacleRect = obstacles[i].getBounds();
      const intersection = Phaser.Geom.Rectangle.Intersection(region, obstacleRect);
      if (intersection.width || intersection.height) {
        return true;
      }
    }

    return false;
  }

  checkCollisions(sprite) {
    this.scene_.physics.collide(
        sprite,
        this.obstacleSprites_.concat(this.nonBlockingObstacleSprites_).concat(this.nonResettableObstacles_));
  }
}
