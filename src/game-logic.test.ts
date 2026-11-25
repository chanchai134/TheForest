import { describe, expect, it } from "vitest";
import { createFruit, createTerrain, overlapsCircle, overlapsCircleBox, scoreAnimal } from "./game-logic";

describe("game rules", () => {
  it("uses the original matching-food bonus rules", () => {
    expect(scoreAnimal({ score: 0, bonus: 0 }, "dragon", "meat")).toEqual({ score: 90, bonus: 10 });
    expect(scoreAnimal({ score: 50, bonus: 0 }, "monkey", "grape")).toEqual({ score: 100, bonus: 0 });
  });

  it("detects target and terrain collisions at their boundaries", () => {
    expect(overlapsCircle({ x: 0, y: 0 }, 10, { x: 20, y: 0 }, 10)).toBe(true);
    expect(overlapsCircleBox({ x: 45, y: 0 }, 10, { x: 0, y: 0 })).toBe(true);
    expect(overlapsCircleBox({ x: 46, y: 0 }, 10, { x: 0, y: 0 })).toBe(false);
  });

  it("initializes each projectile with its original catch and hit radii", () => {
    expect(createFruit("grape").caughtRadius).toBe(35);
    expect(createFruit("banana").ateRadius).toBe(30);
    expect(createFruit("meat").caughtRadius).toBe(45);
  });

  it("generates terrain and targets inside the original playfield", () => {
    const terrain = createTerrain(() => 0.5);
    expect(terrain.hills).toHaveLength(8);
    expect(terrain.animals.length).toBeGreaterThan(0);
    expect(terrain.animals.every((animal) => animal.x > 0 && animal.x < 1910)).toBe(true);
    expect(terrain.boxes.some((box) => box.kind === "ground")).toBe(true);
  });
});
