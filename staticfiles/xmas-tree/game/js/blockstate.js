class BlockState {
  constructor(scene, world, grid, directorState, centerX, centerY, spriteKey, spriteAnimationKey,
              hysteresis, canMoveOffGrid) {
    const sprite = scene.physics.add.sprite(0, 0, spriteKey);
    sprite.x = (centerX - Config.GRID_TILE_SIZE_PX / 2 + sprite.displayWidth / 2);
    sprite.y = (centerY - Config.GRID_TILE_SIZE_PX / 2 + sprite.displayHeight / 2);
    sprite.depth = Depths.BLOCKS;
    if (spriteAnimationKey) sprite.anims.play(spriteAnimationKey);
    sprite.setImmovable();
    sprite.setCollideWorldBounds(true);

    this.scene_ = scene;
    this.world_ = world;
    this.grid_ = grid;
    this.directorState_ = directorState;
    this.sprite_ = sprite;
    this.force_ = 0;
    this.forceDirection_ = null;
    this.hysteresis_ = hysteresis;
    this.canMoveOffGrid_ = canMoveOffGrid;
  }

  getIndex() {
    return this.index_;
  }

  getSprite() {
    return this.sprite_;
  }

  touchFrom(cursors) {
    const direction = this.directionFromCursors_(cursors);
    if (!direction) {
      // More than one key is being pressed, ignore touch.
      this.force_ = 0;
      return;
    }

    if (!this.forceDirection_ || this.forceDirection_.label !== direction.label) {
      // The user changed direction, ignore touch.
      this.force_ = 0;
      this.forceDirection_ = direction;
      return;
    }

    this.force_++;
    if (this.force_ >= this.hysteresis_) {
      this.moveAwayFrom_();
      this.force_ = 0;
    }
  }

  notTouching() {
    this.force_ = 0;
  }

  moveAwayFrom_() {
    if (!this.forceDirection_) {
      console.error('Unexpected state.');
      return;
    }

    const dx = this.forceDirection_.dx;
    const dy = this.forceDirection_.dy;
    if (dx * dy !== 0 || Math.abs(dx) + Math.abs(dy) !== 1) {
      console.error('Unexpected state.');
      return;
    }

    const newCenterX = this.sprite_.x + dx * Config.GRID_TILE_SIZE_PX;
    const newCenterY = this.sprite_.y + dy * Config.GRID_TILE_SIZE_PX;
    if (!this.shouldMoveTo_(newCenterX, newCenterY,
        Config.GRID_TILE_SIZE_PX - Config.BLOCK_MOVE_OBSTACLE_ALLOWANCE,
        Config.GRID_TILE_SIZE_PX - Config.BLOCK_MOVE_OBSTACLE_ALLOWANCE)) {
      // Abort the move.
      return;
    }

    const tween = {
      targets: this.sprite_,
      duration: Config.BLOCK_MOVE_DURATION
    };
    if (dx !== 0) tween.x = newCenterX;
    if (dy !== 0) tween.y = newCenterY;
    this.scene_.tweens.add(tween);
  }

  directionFromCursors_(cursors) {
    if (cursors.left.isDown && !cursors.up.isDown && !cursors.down.isDown) return {label: 'left', dx: -1, dy: 0};
    if (cursors.right.isDown && !cursors.up.isDown && !cursors.down.isDown) return {label: 'right', dx: 1, dy: 0};
    if (cursors.up.isDown && !cursors.left.isDown && !cursors.right.isDown) return {label: 'up', dx: 0, dy: -1};
    if (cursors.down.isDown && !cursors.left.isDown && !cursors.right.isDown) return {label: 'down', dx: 0, dy: 1};
    return null;
  }

  shouldMoveTo_(newCenterX, newCenterY, width, height) {
    // The production is running, don't move.
    if (this.directorState_.isProductionRunning()) {
      return false;
    }

    // The given location is outside of the grid, don't move.
    if (!this.canMoveOffGrid_ && !this.grid_.isInGrid(newCenterX, newCenterY)) {
      return false;
    }

    return !this.world_.anyObstacleInRegion(newCenterX, newCenterY, width, height);
  }
}