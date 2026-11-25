import Phaser from "phaser";
import { assets } from "./assets";
import {
  createFruit,
  createTerrain,
  GAME_HEIGHT,
  GAME_WIDTH,
  GRAVITY,
  overlapsCircle,
  overlapsCircleBox,
  pointInHill,
  randomFruit,
  scoreAnimal,
} from "./game-logic";
import type { Animal, Fruit, Score, TerrainBox } from "./game-logic";
import "./style.css";

const imageKeys = {
  background: "background",
  banana: "banana",
  click: "click",
  dragon: "dragon",
  grape: "grape",
  grass: "grass",
  ground: "ground",
  hand: "hand",
  lose: "lose",
  meat: "meat",
  monkey: "monkey",
  score: "score",
  shootHill: "shootHill",
  slingshot: "slingshot",
  logo: "logo",
  win: "win",
  worm: "worm",
} as const;

const imageAssets = Object.entries(assets);

abstract class ForestScene extends Phaser.Scene {
  protected loadForestAssets(): void {
    for (const [key, path] of imageAssets) this.load.image(key, path);
  }

  protected addBackground(): void {
    this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, imageKeys.background)
      .setDisplaySize(GAME_WIDTH, GAME_HEIGHT);
  }

  protected addCenteredImage(key: string, x: number, bottomY: number): Phaser.GameObjects.Image {
    return this.add.image(x, GAME_HEIGHT - bottomY, key);
  }
}

class MenuScene extends ForestScene {
  constructor() {
    super("menu");
  }

  preload(): void {
    this.loadForestAssets();
  }

  create(): void {
    this.addBackground();
    this.add.image(GAME_WIDTH / 2, GAME_HEIGHT - 700, imageKeys.logo);
    this.add.image(GAME_WIDTH / 2, GAME_HEIGHT - 380, imageKeys.click);
    this.input.once("pointerdown", () => this.scene.start("game"));
  }
}

class GameScene extends ForestScene {
  private fruit!: Fruit;
  private fruitSprite!: Phaser.GameObjects.Image;
  private handSprite!: Phaser.GameObjects.Image;
  private animals: Animal[] = [];
  private animalSprites = new Map<Animal, Phaser.GameObjects.Image>();
  private boxes: TerrainBox[] = [];
  private score: Score = { score: 0, bonus: 0 };
  private scoreLabel!: Phaser.GameObjects.Text;
  private bonusLabel!: Phaser.GameObjects.Text;
  private rightRope!: Phaser.GameObjects.Line;
  private leftRope!: Phaser.GameObjects.Line;
  private pointerDown = false;
  private dragging = false;
  private aimPoint = { x: 0, y: 0 };
  private readonly slingPoint = { x: 327, y: 503 };

  constructor() {
    super("game");
  }

  create(): void {
    this.addBackground();
    this.fruit = createFruit(randomFruit());
    this.buildTerrain();
    this.addSlingshot();
    this.addHud();
    this.addProjectile();
    this.bindInput();
  }

  private buildTerrain(): void {
    const terrain = createTerrain();
    this.boxes = terrain.boxes;
    this.animals = terrain.animals;

    this.addCenteredImage(imageKeys.shootHill, 249, 141);
    for (const box of this.boxes) {
      this.addCenteredImage(box.kind, box.x, box.y);
    }
    for (const animal of this.animals) {
      const sprite = this.addCenteredImage(animal.kind, animal.x, animal.y);
      this.animalSprites.set(animal, sprite);
    }
  }

  private addSlingshot(): void {
    this.addCenteredImage(imageKeys.slingshot, 327, 400);
    this.rightRope = this.add.line(0, 0, 348, GAME_HEIGHT - 503, 0, 0, 0xd9b48a, 5)
      .setOrigin(0, 0).setVisible(false);
    this.leftRope = this.add.line(0, 0, 289, GAME_HEIGHT - 490, 0, 0, 0xd9b48a, 5)
      .setOrigin(0, 0).setVisible(false);
    this.handSprite = this.addCenteredImage(imageKeys.hand, 0, 0).setVisible(false);
  }

  private addHud(): void {
    this.scoreLabel = this.add.text(1550, GAME_HEIGHT - 800, "Score : 0", {
      color: "#111111",
      fontFamily: "Arial, sans-serif",
      fontSize: "50px",
    });
    this.bonusLabel = this.add.text(1550, GAME_HEIGHT - 720, "Bonus : 0", {
      color: "#111111",
      fontFamily: "Arial, sans-serif",
      fontSize: "50px",
    });
    this.add.text(GAME_WIDTH / 2, GAME_HEIGHT - 60, "Some food have special skills. Hold the mouse button to use them.", {
      color: "#111111",
      fontFamily: "Arial, sans-serif",
      fontSize: "20px",
    }).setOrigin(0.5);
    this.add.text(GAME_WIDTH / 2, GAME_HEIGHT - 25, "Some animals like certain food and give a bonus.", {
      color: "#111111",
      fontFamily: "Arial, sans-serif",
      fontSize: "20px",
    }).setOrigin(0.5);
  }

  private addProjectile(): void {
    this.fruitSprite = this.addCenteredImage(this.fruit.kind, this.fruit.x, this.fruit.y);
  }

  private bindInput(): void {
    this.input.on("pointermove", (pointer: Phaser.Input.Pointer) => {
      this.aimPoint = { x: pointer.x, y: GAME_HEIGHT - pointer.y };
      if (this.dragging) this.updateAim();
    });
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      if (this.fruit.launched) {
        this.pointerDown = true;
        return;
      }
      const x = pointer.x;
      const y = GAME_HEIGHT - pointer.y;
      const dx = x - this.fruit.centerX;
      const dy = y - this.fruit.centerY;
      if (Math.hypot(dx, dy) <= this.fruit.caughtRadius) {
        this.pointerDown = true;
        this.dragging = true;
        this.fruit.aiming = true;
        this.aimPoint = { x, y };
        this.updateAim();
      }
    });
    this.input.on("pointerup", () => {
      this.pointerDown = false;
      if (this.dragging) {
        this.dragging = false;
        this.fruit.aiming = false;
        this.fruit.launched = true;
        this.fruit.velocityYNext = this.fruit.velocityYPrevious + GRAVITY;
      }
    });
  }

  private updateAim(): void {
    this.fruit.x = this.aimPoint.x;
    this.fruit.y = this.aimPoint.y;
    this.updateFruitCenter();
    const dx = this.slingPoint.x - this.aimPoint.x;
    const dy = this.slingPoint.y - this.aimPoint.y;
    const angle = Math.atan2(dy, dx);
    const velocity = Math.hypot(dx, dy) / 12;
    this.fruit.startVelocityX = velocity * Math.cos(angle);
    this.fruit.velocityX = this.fruit.startVelocityX;
    this.fruit.velocityYPrevious = velocity * Math.sin(angle);
    this.fruit.velocityYNext = this.fruit.velocityYPrevious - GRAVITY;
    this.fruitSprite.setPosition(this.fruit.x, GAME_HEIGHT - this.fruit.y);
  }

  update(_time: number, delta: number): void {
    this.updateRopes();
    this.updateHand();
    if (!this.fruit.launched) return;

    const frameScale = Math.min(delta, 50) / (1000 / 60);
    this.applySpecialSkill(frameScale);
    const displacementY = (this.fruit.velocityYNext ** 2 - this.fruit.velocityYPrevious ** 2)
      / (-2 * GRAVITY) * frameScale;
    this.fruit.velocityYPrevious += -GRAVITY * frameScale;
    this.fruit.velocityYNext += -GRAVITY * frameScale;
    this.fruit.x += this.fruit.velocityX * frameScale;
    this.fruit.y += displacementY;
    this.updateFruitCenter();
    this.fruitSprite.setPosition(this.fruit.x, GAME_HEIGHT - this.fruit.y);

    if (this.checkHits()) return;
    if (this.fruit.x > GAME_WIDTH || this.fruit.x < 0 || this.fruit.y < 0) {
      this.score.score -= 10;
      this.scoreLabel.setText(`Score : ${this.score.score}`);
      this.resetFruit();
    }
  }

  private applySpecialSkill(frameScale: number): void {
    if (!this.pointerDown || !this.fruit.specialAvailable) {
      if (this.fruit.kind === "banana" && this.fruit.specialPressed && !this.pointerDown) {
        this.fruit.velocityX = this.fruit.startVelocityX;
        this.fruit.velocityYPrevious = this.fruit.frozenVelocityY + GRAVITY;
        this.fruit.velocityYNext = this.fruit.frozenVelocityYNext + GRAVITY;
        this.fruit.specialAvailable = false;
        this.fruit.specialPressed = false;
      }
      return;
    }

    if (this.fruit.kind === "grape") {
      this.fruit.velocityX = 0;
      this.fruit.velocityYPrevious += -5 * GRAVITY;
      this.fruit.velocityYNext += -5 * GRAVITY;
    } else if (this.fruit.kind === "banana") {
      this.fruit.velocityX = this.fruit.startVelocityX + 20;
      this.fruit.y -= (this.fruit.velocityYNext ** 2 - this.fruit.velocityYPrevious ** 2)
        / (-2 * GRAVITY) * frameScale;
      if (!this.fruit.specialPressed) {
        this.fruit.frozenVelocityY = this.fruit.velocityYPrevious;
        this.fruit.frozenVelocityYNext = this.fruit.velocityYNext;
        this.fruit.specialPressed = true;
      }
    }
    this.updateFruitCenter();
  }

  private updateRopes(): void {
    const visible = this.fruit.aiming;
    this.rightRope.setVisible(visible);
    this.leftRope.setVisible(visible);
    if (!visible) return;
    this.rightRope.setTo(348, GAME_HEIGHT - 503, this.aimPoint.x, GAME_HEIGHT - this.aimPoint.y);
    this.leftRope.setTo(289, GAME_HEIGHT - 490, this.aimPoint.x, GAME_HEIGHT - this.aimPoint.y);
  }

  private updateHand(): void {
    this.handSprite.setVisible(this.fruit.aiming);
    if (!this.fruit.aiming) return;
    const angle = Math.atan2(this.aimPoint.y - this.slingPoint.y, this.aimPoint.x - this.slingPoint.x);
    this.handSprite.setPosition(this.aimPoint.x, GAME_HEIGHT - this.aimPoint.y);
    this.handSprite.setRotation(-angle);
  }

  private updateFruitCenter(): void {
    this.fruit.centerX = this.fruit.x + this.fruit.centerOffsetX;
    this.fruit.centerY = this.fruit.y + this.fruit.centerOffsetY;
  }

  private checkHits(): boolean {
    for (const animal of this.animals) {
      if (!overlapsCircle(
        { x: animal.centerX, y: animal.centerY },
        animal.radius,
        { x: this.fruit.centerX, y: this.fruit.centerY },
        this.fruit.ateRadius,
      )) continue;

      this.score = scoreAnimal(this.score, animal.kind, this.fruit.kind);
      this.animals = this.animals.filter((entry) => entry !== animal);
      this.animalSprites.get(animal)?.destroy();
      this.animalSprites.delete(animal);
      this.scoreLabel.setText(`Score : ${this.score.score}`);
      this.bonusLabel.setText(`Bonus : ${this.score.bonus}`);
      if (this.animals.length === 0) {
        this.scene.start("results", { score: this.score });
        return true;
      }
      this.resetFruit();
      return true;
    }

    const hitBox = this.boxes.some((box) =>
      overlapsCircleBox({ x: this.fruit.centerX, y: this.fruit.centerY }, this.fruit.caughtRadius, box),
    );
    const hillX = this.fruit.centerX - 1;
    const hillY = this.fruit.centerY;
    const hitHill = hillX >= 0 && hillX <= 497 && hillY >= 0 && hillY <= 283
      && pointInHill({ x: hillX, y: hillY });
    if (hitBox || hitHill) {
      this.score.score -= 10;
      this.scoreLabel.setText(`Score : ${this.score.score}`);
      this.resetFruit();
      return true;
    }

    return false;
  }

  private resetFruit(): void {
    this.fruit = createFruit(randomFruit());
    this.fruitSprite.destroy();
    this.addProjectile();
  }
}

class ResultsScene extends ForestScene {
  constructor() {
    super("results");
  }

  create(data: { score: Score }): void {
    this.addBackground();
    this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, imageKeys.score);
    const isWin = data.score.score + data.score.bonus > 0;
    this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 240, isWin ? imageKeys.win : imageKeys.lose);
    const labels = [
      ["Score", data.score.score],
      ["Bonus", data.score.bonus],
      ["Total Score", data.score.score + data.score.bonus],
    ] as const;
    labels.forEach(([label, value], index) => {
      const y = 365 + index * 120;
      this.add.text(630, y, label, { color: "#111111", fontSize: "50px", fontFamily: "Arial, sans-serif" });
      this.add.text(1200, y, String(value), { color: "#111111", fontSize: "50px", fontFamily: "Arial, sans-serif" });
    });
    this.input.once("pointerdown", () => this.scene.start("menu"));
  }
}

const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: "game",
  width: GAME_WIDTH,
  height: GAME_HEIGHT,
  backgroundColor: "#84c5df",
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  scene: [MenuScene, GameScene, ResultsScene],
});

window.addEventListener("pagehide", () => game.destroy(true));

export type { AnimalKind, FruitKind } from "./game-logic";
