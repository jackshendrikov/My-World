class GridRunner {
  /** Pass -1 to stamina to not render it. */
  constructor(scene, grid, directorState, sprite, runAnimation, moveDuration) {
    this.scene_ = scene;
    this.grid_ = grid;
    this.sprite_ = sprite;
    this.directorState_ = directorState;
    this.runAnimation_ = runAnimation;
    this.moveDuration_ = moveDuration;
    this.maxStamina_ = -1;

    this.staminaText_ = scene.add.text(0, 0, '');
    this.staminaText_.depth = Depths.STAMINA_TEXT;
    this.staminaText_.setColor('yellow');
    this.staminaText_.setFontSize(25);
    this.staminaText_.setStroke('black', 3);

    this.runState_ = null;

    this.hide();
  }

  setMaxStamina(maxStamina) {
    this.maxStamina_ = maxStamina;
  }

  hide() {
    // Don't clear the path markers here to give them time to finish animating after the production.
    this.staminaText_.visible = false;
    this.scene_.tweens.killTweensOf(this.sprite_);
    this.runState_ = null;
    this.sprite_.visible = false;
  }

  run(path) {
    if (this.runState_) {
      console.error('Already running!');
      return;
    }

    // Move the sprite to the start.
    const startCenter = this.grid_.getTileCenter(path[0].tile.x, path[0].tile.y);
    this.sprite_.x = startCenter.x - Config.GRID_TILE_SIZE_PX;
    this.sprite_.y = startCenter.y;
    this.sprite_.visible = true;
    this.sprite_.anims.play(this.runAnimation_);

    // Initialize the new state and make the first step.
    const newRunState = {
      path: path,
      nextIndex: -1,
      nextTile: null,
      nextCenter: null,
      stamina: this.maxStamina_,
      targetResolveFn: null,
      faintResolveFn: null,
      finishResolveFn: null
    };
    const targetPromise = new Promise(function(resolve, reject) {
      newRunState.targetResolveFn = resolve;
    });
    const faintPromise = new Promise(function(resolve, reject) {
      newRunState.faintResolveFn = resolve;
    });
    const finishPromise = new Promise(function(resolve, reject) {
      newRunState.finishResolveFn = resolve;
    });
    this.runState_ = newRunState;
    this.makeNextStep_();
    
    return {
      targetPromise: targetPromise,
      faintPromise: faintPromise,
      finishPromise: finishPromise
    };
  }

  update() {
    this.scene_.tweens.getTweensOf(this.sprite_)
        .forEach(t => t.setTimeScale(this.directorState_.getRunnerTimeScale()));

    if (!this.runState_) {
      return;
    }

    // We finished running!
    if (!this.runState_.nextCenter) {
      this.runState_.finishResolveFn();
      this.hide();
      return;
    }

    // Update the stamina text.
    if (this.runState_.stamina >= 0) {
      this.staminaText_.visible = true;
      this.staminaText_.x = this.sprite_.x - 5;
      this.staminaText_.y = this.sprite_.y - this.sprite_.displayHeight - 5;
      this.staminaText_.text = this.runState_.stamina;
    } else {
      this.staminaText_.visible = false;
    }

    if (this.runState_.stamina === 0) {
      // We fainted!
      this.runState_.faintResolveFn();
      return;
    }

    if (this.sprite_.x === this.runState_.nextCenter.x && this.sprite_.y === this.runState_.nextCenter.y) {
      // We reached the target.
      const targetTile = this.grid_.getTargetTile();
      if (this.runState_.nextTile
          && this.runState_.nextTile.x === targetTile.x
          && this.runState_.nextTile.y === targetTile.y) {
        this.runState_.targetResolveFn();
      }

      // We reached the next center, make the next step.
      this.addPathMarker_();
      this.runState_.stamina--;
      this.makeNextStep_();
    }
  }

  makeNextStep_() {
    if (!this.runState_ || this.runState_.nextIndex > this.runState_.path.length) {
      console.error('Unexpected call to makeNextStep_.');
      return;
    }

    // Update the next index and center in the state.
    this.runState_.nextIndex++;
    if (this.runState_.nextIndex > this.runState_.path.length) {
      // We're already done.
      this.runState_.nextCenter = null;
      return;
    }

    if (this.runState_.stamina === 0) {
      // We fainted.
      return;
    }

    let nextTile = null;
    let nextCenter = {};
    if (this.runState_.nextIndex === this.runState_.path.length) {
      // Run off the right side of the grid.
      nextCenter.x = this.sprite_.x + Config.GRID_TILE_SIZE_PX;
      nextCenter.y = this.sprite_.y;
    } else {
      nextTile = this.runState_.path[this.runState_.nextIndex].tile;
      nextCenter = this.grid_.getTileCenter(nextTile.x, nextTile.y);
    }
    this.runState_.nextTile = nextTile;
    this.runState_.nextCenter = nextCenter;

    // Add a tween to the next center.
    this.scene_.tweens.add({
      targets: this.sprite_,
      duration: this.moveDuration_,
      x: nextCenter.x,
      y: nextCenter.y
    });
    if (nextCenter.x > this.sprite_.x) {
      this.sprite_.flipX = false;
    } else if (nextCenter.x < this.sprite_.x) {
      this.sprite_.flipX = true;
    }
  }

  addPathMarker_() {
    if (!this.runState_ ||
        this.runState_.nextIndex >= this.runState_.path.length) {
      return;
    }

    const tile = this.runState_.path[this.runState_.nextIndex].tile;
    const center = this.grid_.getTileCenter(tile.x, tile.y);
    const pathMarker = this.scene_.add.sprite(center.x, center.y, 'pathmarker');
    pathMarker.alpha = Config.GRID_RUNNER_PATH_MARKER_ALPHA;
    pathMarker.depth = Depths.PATH_MARKER;

    const pathMarkerTween = this.scene_.tweens.add({
      targets: pathMarker,
      duration: Config.GRID_RUNNER_PATH_MARKER_FADE_DURATION,
      alpha: 0
    });
    pathMarkerTween.setCallback('onComplete', function() {
      pathMarker.destroy();
    }, []);
  }
}