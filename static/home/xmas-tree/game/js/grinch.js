class Grinch {
  constructor(scene, grid, directorState, maxStamina) {
    this.scene_ = scene;
    this.grid_ = grid;

    this.runSprite_ = scene.physics.add.sprite(0, 0, 'grinchrun');
    this.runSprite_.displayWidth = Config.GRINCH_RUN_SPRITE_WIDTH * Config.GRINCH_RUN_SCALE;
    this.runSprite_.displayHeight = Config.GRINCH_RUN_SPRITE_HEIGHT * Config.GRINCH_RUN_SCALE;
    this.runSprite_.depth = Depths.GRINCH;
    this.runSprite_.setImmovable(true);
    this.runSprite_.visible = false;

    this.faintSprite_ = scene.add.sprite(0, 0, 'grinchfaint');
    this.faintSprite_.displayWidth = Config.GRINCH_FAINT_SPRITE_WIDTH * Config.GRINCH_FAINT_SCALE;
    this.faintSprite_.displayHeight = Config.GRINCH_FAINT_SPRITE_HEIGHT * Config.GRINCH_FAINT_SCALE;
    this.faintSprite_.depth = Depths.GRINCH;
    this.faintSprite_.visible = false;
    this.faintSprite_.setOrigin(10 / this.faintSprite_.displayWidth, (this.faintSprite_.displayHeight - 5) /
        this.faintSprite_.displayHeight);

    scene.anims.create({
      key: 'grinchRunRight',
      frames: scene.anims.generateFrameNumbers('grinchrun', {
        start: 0,
        end: 14
      }),
      frameRate: Config.GRINCH_ANIMATION_SPEED,
      repeat: -1
    });

    this.gridRunner_ = new GridRunner(scene, grid, directorState, this.runSprite_, 'grinchRunRight', Config.GRINCH_MOVE_DURATION);
  }

  getRunSprite() {
    return this.runSprite_;
  }

  reset(maxStamina) {
    this.gridRunner_.setMaxStamina(maxStamina);
    this.faintSprite_.angle = 0;
    this.hide();
  }

  hide() {
    this.gridRunner_.hide();
    this.faintSprite_.visible = false;
  }

  run(path) {
    this.faintSprite_.visible = false;
    return this.gridRunner_.run(path);
  }

  faint() {
    this.runSprite_.visible = false;
    this.faintSprite_.visible = true;

    const end = this.grid_.getEndTiles()[0];
    const center = this.grid_.getTileCenter(end.x, end.y);
    this.faintSprite_.x = center.x + (this.faintSprite_.originX - 0.5) * this.faintSprite_.displayWidth;
    this.faintSprite_.y = center.y + (this.faintSprite_.originY - 0.5) * this.faintSprite_.displayHeight;
    this.scene_.tweens.add({
      targets: this.faintSprite_,
      delay: Config.GRINCH_FAINT_DELAY,
      duration: Config.GRINCH_FAINT_DURATION,
      angle: -90,
      ease: 'Bounce.easeOut'
    });
  }

  update() {
    this.gridRunner_.update();
  }
}