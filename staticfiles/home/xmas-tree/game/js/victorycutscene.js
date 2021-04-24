class VictoryCutscene {
  constructor(scene, dasha, gift, directorState, confettiSpriteKeys) {
    this.scene_ = scene;
    this.dasha_ = dasha;
    this.gift_ = gift;
    this.directorState_ = directorState;
    this.confettiSpriteKeys_ = confettiSpriteKeys;

    this.flashGraphics_ = scene.add.graphics();
    this.flashGraphics_.fillStyle(0xffffff);
    this.flashGraphics_.fillRect(-10000, -10000, 20000, 20000);
    this.flashGraphics_.depth = Depths.FLASH;
    this.flashGraphics_.visible = false;

    this.finalText_ = scene.add.text(53, 185, 'Yay! You did it! Merry Christmas!');
    this.finalText_.setColor('#ffffcc');
    this.finalText_.setFontSize(30);
    this.finalText_.setStroke('black', 5);
    this.finalText_.fontWeight = 'bold';
    this.finalText_.depth = Depths.FINAL_TEXT;
    this.finalText_.visible = false;

    this.playing_ = false;
  }

  update() {
    if (this.playing_ || !this.directorState_.isVictorious()) {
      return;
    }

    const dashaSprite = this.dasha_.getSprite();
    const giftSprite = this.gift_.getSprite();
    const distance = Math.abs(dashaSprite.x - giftSprite.x) + Math.abs(dashaSprite.y - giftSprite.y);
    if (distance < Config.VICTORY_GIFT_DASHA_PROXIMITY) {
      this.play_();
    }
  }

  play_() {
    this.playing_ = true;
    this.flashGraphics_.visible = true;
    const flashTween = this.scene_.tweens.add({
      targets: this.flashGraphics_,
      duration: Config.VICTORY_FLASH_DURATION,
      alpha: 0
    });
    flashTween.setCallback('onComplete', function() {
      this.flashGraphics_.destroy();
    }, [] /* params */, this);
    
    this.pulsateFinalText_();
    this.spawnRandomConfetti_();
  }

  pulsateFinalText_() {
    this.finalText_.visible = true;
    this.finalText_.alpha = 0.2;
    const alphaUpTween = this.scene_.tweens.add({
      targets: this.finalText_,
      duration: Config.VICTORY_TEXT_PULSATE_DURATION,
      alpha: 1
    });
    alphaUpTween.setCallback(
        'onComplete',
        () => {
          const alphaDownTween = this.scene_.tweens.add({
            targets: this.finalText_,
            duration: Config.VICTORY_TEXT_PULSATE_DURATION,
            alpha: 0.2
          });
          alphaDownTween.setCallback('onComplete', () => this.pulsateFinalText_(), [] /* params */);
        },
        [] /* params */)
  }

  spawnRandomConfetti_() {
    const x = Math.floor(Math.random() * Config.WORLD_WIDTH_PX);
    let endAngle = (Math.random() * 360 * 3) + 90;
    if (Math.random() < 0.5) endAngle *= -1;
    const keyIndex = Math.floor(Math.random() * this.confettiSpriteKeys_.length);
    const key = this.confettiSpriteKeys_[keyIndex];
    const confetti = this.scene_.add.sprite(x, -10, key);
    confetti.displayWidth *= Config.VICTORY_CONFETTI_SCALE;
    confetti.displayHeight *= Config.VICTORY_CONFETTI_SCALE;
    confetti.depth = Depths.CONFETTI;
    confetti.angle = 0;

    const yTween = this.scene_.tweens.add({
      targets: confetti,
      duration: Config.VICTORY_CONFETTI_DURATION,
      y: Config.WORLD_HEIGHT_PX + 10
    });
    const angleTween = this.scene_.tweens.add({
      targets: confetti,
      duration: Config.VICTORY_CONFETTI_DURATION,
      angle: endAngle
    });
    yTween.setCallback('onComplete', function() {
      confetti.destroy();
    }, [] /* params */);

    // Do it again!
    setTimeout(
        () => this.spawnRandomConfetti_(),
        Config.VICTORY_CONFETTI_FREQUENCY);
  }
}