export const GAME_WIDTH = 1910;
export const GAME_HEIGHT = 900;
export const GRAVITY = 0.35;

export type FruitKind = "grape" | "banana" | "meat";
export type AnimalKind = "worm" | "monkey" | "dragon";
export type BoxKind = "grass" | "ground";

export interface Point {
  x: number;
  y: number;
}

export interface Fruit extends Point {
  kind: FruitKind;
  centerX: number;
  centerY: number;
  caughtRadius: number;
  ateRadius: number;
  centerOffsetX: number;
  centerOffsetY: number;
  velocityX: number;
  velocityY: number;
  velocityYPrevious: number;
  velocityYNext: number;
  startVelocityX: number;
  aiming: boolean;
  launched: boolean;
  specialAvailable: boolean;
  specialPressed: boolean;
  frozenVelocityY: number;
  frozenVelocityYNext: number;
}

export interface Animal extends Point {
  kind: AnimalKind;
  centerX: number;
  centerY: number;
  radius: number;
  centerOffsetX: number;
  centerOffsetY: number;
  collisionRadiusX?: number;
  collisionRadiusY?: number;
}

export interface TerrainBox extends Point {
  kind: BoxKind;
}

export interface Hill {
  x: number;
  height: number;
}

export interface Score {
  score: number;
  bonus: number;
}

const fruitSettings: Record<FruitKind, Pick<Fruit, "caughtRadius" | "ateRadius" | "centerOffsetX" | "centerOffsetY">> = {
  grape: { caughtRadius: 35, ateRadius: 25, centerOffsetX: 0, centerOffsetY: -10 },
  banana: { caughtRadius: 40, ateRadius: 30, centerOffsetX: -4, centerOffsetY: -9 },
  meat: { caughtRadius: 45, ateRadius: 35, centerOffsetX: -3, centerOffsetY: -7 },
};

const animalSettings: Record<AnimalKind, Pick<
  Animal,
  "radius" | "centerOffsetX" | "centerOffsetY" | "collisionRadiusX" | "collisionRadiusY"
>> = {
  worm: { radius: 30, centerOffsetX: -20, centerOffsetY: 0 },
  monkey: { radius: 40, centerOffsetX: -10, centerOffsetY: 20 },
  dragon: { radius: 60, centerOffsetX: 0, centerOffsetY: 0, collisionRadiusX: 125, collisionRadiusY: 95 },
};

export function createFruit(kind: FruitKind, x = 327, y = 503): Fruit {
  const settings = fruitSettings[kind];
  return {
    kind,
    x,
    y,
    centerX: x + settings.centerOffsetX,
    centerY: y + settings.centerOffsetY,
    ...settings,
    velocityX: 0,
    velocityY: 0,
    velocityYPrevious: 0,
    velocityYNext: 0,
    startVelocityX: 0,
    aiming: false,
    launched: false,
    specialAvailable: true,
    specialPressed: false,
    frozenVelocityY: 0,
    frozenVelocityYNext: 0,
  };
}

export function createAnimal(kind: AnimalKind, x: number, y: number): Animal {
  const settings = animalSettings[kind];
  return {
    kind,
    x,
    y,
    centerX: x + settings.centerOffsetX,
    centerY: y + settings.centerOffsetY,
    ...settings,
  };
}

export function randomFruit(random: () => number = Math.random): FruitKind {
  const kinds: FruitKind[] = ["grape", "banana", "meat"];
  return kinds[Math.min(kinds.length - 1, Math.floor(random() * kinds.length))];
}

export function createTerrain(random: () => number = Math.random): {
  hills: Hill[];
  boxes: TerrainBox[];
  animals: Animal[];
} {
  const groundXs: number[] = [];
  for (let x = 533; x + 35 < GAME_WIDTH; x += 71) groundXs.push(x);

  const randomXs = groundXs.slice(-17, -1);
  const hills: Hill[] = [];
  for (let i = 0; i + 1 < randomXs.length; i += 2) {
    hills.push({ x: randomXs[i], height: 1 + Math.floor(random() * 5) });
  }

  const randomXSet = new Set(randomXs);
  const boxes: TerrainBox[] = [];
  for (const x of groundXs) {
    if (!randomXSet.has(x)) boxes.push({ x, y: 106, kind: "grass" });
    boxes.push({ x, y: 36, kind: "ground" });
  }

  for (let i = 0; i < hills.length; i += 1) {
    const hill = hills[i];
    const topY = 106 + 71 * hill.height;
    for (const x of [hill.x, hill.x + 71]) {
      boxes.push({ x, y: topY, kind: "grass" });
      for (let level = hill.height - 1; level > 0; level -= 1) {
        boxes.push({ x, y: 107 + 71 * level, kind: "ground" });
      }
    }
  }

  const animals: Animal[] = [];
  for (let i = 0; i < hills.length;) {
    const hill = hills[i];
    const nextHill = hills[i + 1];
    const y = 107 + 71 * hill.height;
    if (nextHill && hill.height === nextHill.height && random() < 0.7) {
      animals.push(createAnimal("dragon", (hill.x + 71 + nextHill.x) / 2, y + 150));
      i += 2;
      continue;
    }
    const kind: AnimalKind = random() < 0.5 ? "worm" : "monkey";
    animals.push(createAnimal(kind, hill.x + 35.5, y + (kind === "worm" ? 90 : 100)));
    i += 1;
  }

  return { hills, boxes, animals };
}

export function overlapsCircle(
  first: Point,
  firstRadius: number,
  second: Point,
  secondRadius: number,
): boolean {
  return Math.hypot(first.x - second.x, first.y - second.y) <= firstRadius + secondRadius;
}

export function overlapsCircleEllipse(
  circle: Point,
  circleRadius: number,
  ellipse: Point,
  ellipseRadiusX: number,
  ellipseRadiusY: number,
): boolean {
  const radiusX = ellipseRadiusX + circleRadius;
  const radiusY = ellipseRadiusY + circleRadius;
  const dx = (circle.x - ellipse.x) / radiusX;
  const dy = (circle.y - ellipse.y) / radiusY;
  return dx * dx + dy * dy <= 1;
}

export function overlapsCircleBox(circle: Point, radius: number, box: Point, halfSize = 35): boolean {
  const closestX = Math.max(box.x - halfSize, Math.min(circle.x, box.x + halfSize));
  const closestY = Math.max(box.y - halfSize, Math.min(circle.y, box.y + halfSize));
  return Math.hypot(circle.x - closestX, circle.y - closestY) <= radius;
}

export function scoreAnimal(score: Score, animal: AnimalKind, fruit: FruitKind): Score {
  const bonusMatches: Record<AnimalKind, FruitKind> = {
    worm: "grape",
    monkey: "banana",
    dragon: "meat",
  };
  return {
    score: score.score + (animal === "dragon" ? 90 : 50),
    bonus: score.bonus + (bonusMatches[animal] === fruit ? 10 : 0),
  };
}

export function pointInHill(point: Point): boolean {
  const polygon: Point[] = [
    { x: 1, y: 0 },
    { x: 497, y: 0 },
    { x: 497, y: 141 },
    { x: 355, y: 141 },
    { x: 355, y: 283 },
    { x: 284, y: 283 },
    { x: 143, y: 141 },
    { x: 1, y: 141 },
  ];
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i, i += 1) {
    const a = polygon[i];
    const b = polygon[j];
    const intersects = (a.y > point.y) !== (b.y > point.y)
      && point.x < ((b.x - a.x) * (point.y - a.y)) / (b.y - a.y) + a.x;
    if (intersects) inside = !inside;
  }
  return inside;
}
