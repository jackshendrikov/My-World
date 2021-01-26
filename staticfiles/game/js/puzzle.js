class Puzzle {
  constructor(world, grid) {
    this.world_ = world;
    this.grid_ = grid;
  }

  /**
   * Returns an array of objects describing the shortest path through the grid.
   * Each element of the returned array contains two properties: tile and targetCount.
   * Tile i contains the x, y coordinates (in tiles) within the grid of the i^th step in the path.
   * Target count i specifies how many targets have been reached after the i^th step in the path.
   *
   * Returns null if there is no path through the grid.
   */

  solve() {
    const results = {};
    const frontier = [];

    // Mark obstacles as visited.
    for (let tileX = 0; tileX < Config.GRID_WIDTH_IN_TILES; tileX++) {
      for (let tileY = 0; tileY < Config.GRID_HEIGHT_IN_TILES; tileY++) {
        const center = this.grid_.getTileCenter(tileX, tileY);
        if (this.world_.anyPathBlockingObstacleInRegion(center.x, center.y,
            Config.GAME_COLLISION_DETECTION_SIZE,
            Config.GAME_COLLISION_DETECTION_SIZE)) {
          const tile = {x: tileX, y: tileY};
          results[this.tileKey_(tile, 0)] = {tile: tile, targetCount: 0, distance: 99999, parentResult: null};
          results[this.tileKey_(tile, 1)] = {tile: tile, targetCount: 1, distance: 99999, parentResult: null};
        }
      }
    }

    // Initially visit the end tiles.
    this.grid_.getEndTiles().forEach(tileEnd => {
      this.visit_(results, frontier, tileEnd, 1, null);
    });

    // Perform the breadth-first search for the start tiles.
    while (frontier.length) {
      const tileKey = frontier.splice(0, 1)[0];
      const result = results[tileKey];
      if (tileKey === this.tileKey_(this.grid_.getTargetTile(), 1)) {
        // If on the target with target count 1, visit the target again with count 0.
        this.visit_(results, frontier, result.tile, 0 /* targetCount */, result);
      }
      [[0, 1], [0, -1], [1, 0], [-1, 0]].forEach(d => {
        this.visit_(results, frontier, {x: result.tile.x + d[0], y: result.tile.y + d[1]}, result.targetCount, result);
      });
    }

    // Find the start tile with minimal distance.
    let bestTileStart = null;
    let bestDistance = 99999;
    this.grid_.getStartTiles().forEach(tileStart => {
      const tileKey = this.tileKey_(tileStart, 0);
      const result = results[tileKey];
      if (result && result.distance < bestDistance) {
        bestTileStart = tileStart;
        bestDistance = result.distance;
      }
    });

    // Return the best path if there is one.
    return bestTileStart ? this.constructPath_(results, bestTileStart) : null;
  }

  visit_(results, frontier, tile, targetCount, parentResult) {
    if (tile.x < 0 || tile.x >= Config.GRID_WIDTH_IN_TILES || tile.y < 0 || tile.y >= Config.GRID_HEIGHT_IN_TILES) {
      // Out of bounds.
      return;
    }

    const tileKey = this.tileKey_(tile, targetCount);
    if (results[tileKey]) {
      // Already visited.
      return;
    }

    results[tileKey] = {
      tile: tile,
      targetCount: targetCount,
      distance: parentResult ? parentResult.distance + 1 : 0,
      parentResult: parentResult
    };
    frontier.push(tileKey);
  }

  constructPath_(results, tile) {
    const tileKey = this.tileKey_(tile, 0);
    let currentResult = results[tileKey];
    if (!currentResult) {
      console.error('No result for tile key.');
      return null;
    }
    const path = [];
    while (currentResult != null) {
      if (!currentResult.parentResult || currentResult.targetCount === currentResult.parentResult.targetCount) {
        // Don't include the target twice in the path.
        path.push({
          tile: currentResult.tile,
          targetCount: currentResult.targetCount
        });
      }
      currentResult = currentResult.parentResult;
    }
    return path;
  }

  tileKey_(tile, targetCount) {
    return tile.x + ',' + tile.y + ',' + targetCount;
  }
}