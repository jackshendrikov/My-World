class Grid {
  constructor(scene, world) {
    this.scene_ = scene;
    this.world_ = world;
    
    this.startY_ = null;
    this.endY_ = null;
    this.targetTile_ = null;

    this.fireplace_ = null;
    this.treeObstacle_ = null;
    this.tree_ = null;
    this.glow_ = null;

    this.renderRug_();

    scene.anims.create({
      key: 'treeTwinkle',
      frames: this.scene_.anims.generateFrameNumbers('tree', { start: 0, end: 1 }),
      frameRate: Config.TREE_ANIMATION_SPEED,
      repeat: -1
    });
  }

  reset(startY, endY, targetTile) {
    this.startY_ = startY;
    this.endY_ = endY;
    this.targetTile_ = targetTile;

    if (this.fireplace_) this.fireplace_.destroy();
    if (this.treeObstacle_) this.treeObstacle_.destroy();
    if (this.tree_) this.tree_.destroy();
    if (this.glow_) this.glow_.destroy();

    const fireplaceCenter = this.getTileCenter(0, startY);
    const fireplaceWidth = Config.WORLD_FIREPLACE_WIDTH_PX * Config.WORLD_FIREPLACE_SCALE;
    const fireplaceHeight = Config.WORLD_FIREPLACE_HEIGHT_PX * Config.WORLD_FIREPLACE_SCALE;
    const fireplace = this.scene_.physics.add.sprite(Config.WORLD_WALL_SIDE_WIDTH_PX + fireplaceWidth / 2,
        fireplaceCenter.y + Config.GRID_TILE_SIZE_PX / 2 - fireplaceHeight / 2, 'fireplace');
    fireplace.displayWidth = fireplaceWidth;
    fireplace.displayHeight = fireplaceHeight;
    fireplace.depth = Depths.OBJECTS;
    fireplace.setImmovable(true);
    this.world_.addObstacleSprite(fireplace);

    const treeCenter = this.getTileCenter(targetTile.x, targetTile.y);
    const treeObstacle = this.scene_.physics.add.sprite(treeCenter.x, treeCenter.y, 'crate');
    treeObstacle.alpha = 0;
    treeObstacle.displayWidth = Config.GRID_TILE_SIZE_PX;
    treeObstacle.displayHeight = Config.GRID_TILE_SIZE_PX;
    treeObstacle.setImmovable(true);
    this.world_.addNonPathBlockingObstacleSprite(treeObstacle);

    const treeWidth = Config.TREE_SPRITE_WIDTH * Config.TREE_SCALE;
    const treeHeight = Config.TREE_SPRITE_HEIGHT * Config.TREE_SCALE;
    const tree = this.scene_.add.sprite(treeCenter.x, treeCenter.y + Config.GRID_TILE_SIZE_PX / 2 - treeHeight / 2, 'tree');
    tree.displayWidth = treeWidth;
    tree.displayHeight = treeHeight;
    tree.depth = Depths.OBJECTS_IN_FRONT;
    tree.anims.play('treeTwinkle');

    const endCenter = this.getTileCenter(0, endY);
    const glow = this.scene_.add.sprite(0, 0, 'glow');
    glow.x = Config.WORLD_WIDTH_PX - glow.displayWidth / 2;
    glow.y = endCenter.y;
    glow.depth = Depths.GLOW;

    const welcome = this.scene_.add.sprite(0, 0, 'welcome');
    welcome.x = Config.WORLD_WIDTH_PX - welcome.displayWidth / 2 - 10;
    welcome.y = endCenter.y;
    welcome.depth = Depths.OBJECTS;

    this.fireplace_ = fireplace;
    this.treeObstacle_ = treeObstacle;
    this.tree_ = tree;
    this.glow_ = glow;
  }

  renderRug_() {
    let tileY;
    let tileX;
// Render the corners.
    this.renderSprite_(0, 0, 'rugtopleft', Depths.RUG);
    this.renderSprite_(Config.GRID_WIDTH_IN_TILES - 1, 0, 'rugtopleft', Depths.RUG).flipX = -1;
    this.renderSprite_(0, Config.GRID_HEIGHT_IN_TILES - 1, 'rugtopleft', Depths.RUG).flipY = -1;
    const bottomRight = this.renderSprite_(Config.GRID_WIDTH_IN_TILES - 1, Config.GRID_HEIGHT_IN_TILES - 1, 'rugtopleft', Depths.RUG);
    bottomRight.flipX = -1;
    bottomRight.flipY = -1;

    // Render the sides.
    for (tileX = 1; tileX < Config.GRID_WIDTH_IN_TILES - 1; tileX++) {
      this.renderSprite_(tileX, 0, 'rugtop', Depths.RUG);
      this.renderSprite_(tileX, Config.GRID_HEIGHT_IN_TILES - 1, 'rugtop', Depths.RUG).flipY = -1;
    }
    for (tileY = 1; tileY < Config.GRID_HEIGHT_IN_TILES - 1; tileY++) {
      this.renderSprite_(0, tileY, 'rugleft', Depths.RUG);
      this.renderSprite_(Config.GRID_WIDTH_IN_TILES - 1, tileY, 'rugleft', Depths.RUG).flipX = -1;
    }

    // Render the middle.
    for (tileX = 1; tileX < Config.GRID_WIDTH_IN_TILES - 1; tileX++) {
      for (tileY = 1; tileY < Config.GRID_HEIGHT_IN_TILES - 1; tileY++) {
        this.renderSprite_(tileX, tileY, 'rugmiddle', Depths.RUG);
      }
    }
  }

  renderSprite_(tileX, tileY, key, depth) {
    const center = this.getTileCenter(tileX, tileY);
    const sprite = this.scene_.add.sprite(center.x, center.y, key);
    sprite.depth = depth;
    return sprite;
  }

  getStartTiles() {
    return [{x: 0, y: this.startY_}];
  }

  getEndTiles() {
    return [{x: Config.GRID_WIDTH_IN_TILES - 1, y: this.endY_}];
  }

  getTargetTile() {
    return this.targetTile_;
  }

  getTileCenter(tileX, tileY) {
    if (tileX < 0 || tileX >= Config.GRID_WIDTH_IN_TILES || tileY < 0 || tileY >= Config.GRID_HEIGHT_IN_TILES) {
      console.error('Invalid tileX, tileY: ' + tileX + ', ' + tileY);
      return null;
    }

    return this.getTileCenterOffGrid(tileX, tileY);
  }

  getTileCenterOffGrid(tileX, tileY) {
    return {
      x: Config.GRID_TOP_LEFT_X + Config.GRID_TILE_SIZE_PX * (tileX + 0.5),
      y: Config.GRID_TOP_LEFT_Y + Config.GRID_TILE_SIZE_PX * (tileY + 0.5)
    };
  }

  isInGrid(x, y) {
    return x >= Config.GRID_TOP_LEFT_X && x <= Config.GRID_TOP_LEFT_X + Config.GRID_TILE_SIZE_PX * Config.GRID_WIDTH_IN_TILES
        && y >= Config.GRID_TOP_LEFT_Y && y <= Config.GRID_TOP_LEFT_Y + Config.GRID_TILE_SIZE_PX * Config.GRID_HEIGHT_IN_TILES;
  }
}