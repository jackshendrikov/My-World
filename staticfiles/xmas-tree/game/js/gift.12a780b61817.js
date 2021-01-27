class Gift {
  constructor(scene, grid) {
    this.grid_ = grid;
    this.sprite_ = scene.add.sprite(0, 0, 'gift');
    this.sprite_.visible = false;
    this.spriteToFollow_ = null;
  }

  getSprite() {
    return this.sprite_;
  }

  hide() {
    this.spriteToFollow_ = null;
    this.sprite_.visible = false;
    this.sprite_.displayWidth = Config.GIFT_WIDTH_PX * Config.GIFT_SCALE;
    this.sprite_.displayHeight = Config.GIFT_HEIGHT_PX * Config.GIFT_SCALE;
    this.sprite_.depth = Depths.GIFT;
  }

  moveToTarget() {
    this.spriteToFollow_ = null;
    this.sprite_.visible = true;

    const target = this.grid_.getTargetTile();
    const center = this.grid_.getTileCenter(target.x, target.y);
    this.sprite_.x = center.x + Config.GRID_TILE_SIZE_PX / 2 - this.sprite_.displayWidth / 2;
    this.sprite_.y = center.y + Config.GRID_TILE_SIZE_PX / 2 - this.sprite_.displayHeight / 2;
  }

  moveToVictory() {
    this.spriteToFollow_ = null;
    this.sprite_.visible = true;

    const victory = this.grid_.getEndTiles()[0];
    const center = this.grid_.getTileCenter(victory.x, victory.y);
    this.sprite_.displayWidth = Config.GIFT_WIDTH_PX * Config.GIFT_VICTORY_SCALE;
    this.sprite_.displayHeight = Config.GIFT_HEIGHT_PX * Config.GIFT_VICTORY_SCALE;
    this.sprite_.x = center.x;
    this.sprite_.y = center.y + Config.GRID_TILE_SIZE_PX / 2 - this.sprite_.displayHeight / 2;
    this.sprite_.depth = Depths.GIFT_VICTORY;
  }

  follow(spriteToFollow) {
    this.spriteToFollow_ = spriteToFollow;
    this.sprite_.visible = true;
  }

  update() {
    if (this.spriteToFollow_) {
      this.sprite_.visible = true;
      this.sprite_.x = this.spriteToFollow_.x - Config.GRID_TILE_SIZE_PX / 2;
      this.sprite_.y = this.spriteToFollow_.y - Config.GRID_TILE_SIZE_PX / 2;
    }
  }
}