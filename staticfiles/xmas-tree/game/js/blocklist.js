class BlockList {
  constructor(scene, world, grid, directorState) {
    this.scene_ = scene;
    this.world_ = world;
    this.grid_ = grid;
    this.directorState_ = directorState;
    this.blocks_ = [];
    this.sprites_ = [];
    this.blockIndex_ = 0;
  }

  reset() {
    this.sprites_.forEach(s => s.destroy());
    this.blocks_ = [];
    this.sprites_ = [];
    this.blockIndex_ = 0;
  }

  addBlock_(centerX, centerY, spriteKey, spriteAnimationKey, hysteresis, canMoveOffGrid) {
    const blockState = new BlockState(this.scene_, this.world_, this.grid_, this.directorState_,
        centerX, centerY, spriteKey, spriteAnimationKey, hysteresis, canMoveOffGrid);
    this.blocks_.push(blockState);
    const sprite = blockState.getSprite();
    sprite.setData('blockIndex', this.blockIndex_++);
    this.sprites_.push(sprite);

    this.world_.addObstacleSprite(sprite);

    this.blockIndex_++;
    return sprite;
  }

  addBlockOffGrid(tileX, tileY, spriteKey, spriteAnimationKey) {
    const center = this.grid_.getTileCenterOffGrid(tileX, tileY);
    return this.addBlock_(center.x, center.y, spriteKey, spriteAnimationKey, Config.BLOCK_OFF_GRID_HYSTERESIS, true);
  }

  addBlockInGrid(tileX, tileY, spriteKey) {
    const center = this.grid_.getTileCenter(tileX, tileY);
    return this.addBlock_(center.x, center.y, spriteKey, null, Config.BLOCK_HYSTERESIS, false);
  }

  update(dashaSprite, cursors) {
    // Count the number of overlapping blocks and keep track of the overlapping block.
    let numOverlaps = 0;
    let collidingBlockIndex = -1;
    this.sprites_.forEach(blockSprite => {
      const intersection = Phaser.Geom.Rectangle.Intersection(dashaSprite.getBounds(), blockSprite.getBounds());
      if (intersection.width && intersection.height) {
        numOverlaps++;
        const blockIndex = blockSprite.getData('blockIndex');
        if (typeof blockIndex != "number") {
          console.error('No block index!');
          return;
        }
        collidingBlockIndex = blockIndex;
      }
    });

    // If there is a single overlapping block, mark it as touched. Otherwise, mark all other blocks as untouched.
    this.blocks_.forEach(blockState => {
      if (numOverlaps === 1  && blockState.getSprite().getData('blockIndex') === collidingBlockIndex) {
        blockState.touchFrom(cursors);
      } else {
        blockState.notTouching();
      }
    });
  }
}