class DirectorState {
  constructor(directorKeys) {
    this.directorKeys_ = directorKeys;
    this.isProductionRunning_ = false;
    this.isVictorious_ = false;
  }

  markVictorious() {
    this.isVictorious_ = true;
  }

  isVictorious() {
    return this.isVictorious_;
  }

  setIsProductionRunning(isProductionRunning) {
    this.isProductionRunning_ = isProductionRunning;
  }

  isProductionRunning() {
    return this.isProductionRunning_;
  }

  getRunnerTimeScale() {
    return this.directorKeys_.space.isDown ? Config.GRID_RUNNER_FAST_MULTIPLIER : 1;
  }
}