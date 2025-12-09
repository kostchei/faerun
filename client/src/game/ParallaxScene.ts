/**
 * Path: client/src/game/ParallaxScene.ts
 * Purpose: Manages 5-layer parallax scene with mouse-controlled camera
 * Logic:
 *   - Layer 0 (Foreground): Grass silhouettes at 1.5x scroll speed
 *   - Layer 1 (Stage): Character plane at 1.0x scroll speed (baseline)
 *   - Layer 2 (Midground): Trees at 0.5x scroll speed
 *   - Layer 3 (Background): Mountains at 0.2x scroll speed
 *   - Layer 4 (Skybox): Stars at 0.05x scroll speed
 *   - Tracks mouse X position to control camera pan
 *   - Smoothly interpolates camera movement for cinematic feel
 *   - Each layer offset = cameraX * layer.speedMultiplier
 */

import { Application, Container, Graphics, Rectangle } from 'pixi.js';

interface ParallaxLayer {
    container: Container;
    speedMultiplier: number;
}

export class ParallaxScene {
    private app: Application;
    private layers: ParallaxLayer[] = [];
    private cameraX: number = 0;
    private targetCameraX: number = 0;

    constructor(app: Application) {
        this.app = app;
    }

    async init(): Promise<void> {
        // Create parallax layers (back to front)
        this.createSkyboxLayer();      // Layer 4 - 0.05x speed
        this.createBackgroundLayer();  // Layer 3 - 0.2x speed
        this.createMidgroundLayer();   // Layer 2 - 0.5x speed
        this.createStageLayer();       // Layer 1 - 1.0x speed
        this.createForegroundLayer();  // Layer 0 - 1.5x speed

        // Mouse/touch controls camera
        this.setupInputHandlers();
    }

    private createSkyboxLayer(): void {
        const container = new Container();

        // Gradient sky using graphics
        const sky = new Graphics();
        sky.rect(0, 0, this.app.screen.width * 3, this.app.screen.height);
        sky.fill({ color: 0x0f0c29 }); // Deep purple
        container.addChild(sky);

        // Stars
        for (let i = 0; i < 100; i++) {
            const star = new Graphics();
            star.circle(0, 0, Math.random() * 2 + 0.5);
            star.fill({ color: 0xffffff, alpha: Math.random() * 0.8 + 0.2 });
            star.x = Math.random() * this.app.screen.width * 3;
            star.y = Math.random() * this.app.screen.height * 0.6;
            container.addChild(star);
        }

        this.app.stage.addChild(container);
        this.layers.push({ container, speedMultiplier: 0.05 });
    }

    private createBackgroundLayer(): void {
        const container = new Container();

        // Distant mountains
        const mountains = new Graphics();
        mountains.moveTo(0, this.app.screen.height);

        // Draw mountain silhouettes
        const peaks = [
            { x: 0, y: 0.7 }, { x: 150, y: 0.4 }, { x: 300, y: 0.6 },
            { x: 500, y: 0.3 }, { x: 700, y: 0.5 }, { x: 900, y: 0.35 },
            { x: 1100, y: 0.55 }, { x: 1300, y: 0.4 }, { x: 1500, y: 0.6 },
            { x: 1700, y: 0.45 }, { x: 1900, y: 0.5 }, { x: 2100, y: 0.7 }
        ];

        for (const peak of peaks) {
            mountains.lineTo(peak.x, this.app.screen.height * peak.y);
        }
        mountains.lineTo(2100, this.app.screen.height);
        mountains.closePath();
        mountains.fill({ color: 0x1a1a3e }); // Dark purple-blue

        container.addChild(mountains);
        this.app.stage.addChild(container);
        this.layers.push({ container, speedMultiplier: 0.2 });
    }

    private createMidgroundLayer(): void {
        const container = new Container();

        // Trees / structures silhouettes
        for (let i = 0; i < 20; i++) {
            const tree = new Graphics();
            const x = i * 150 + Math.random() * 50;
            const height = 100 + Math.random() * 150;
            const baseY = this.app.screen.height * 0.85;

            // Trunk
            tree.rect(x - 5, baseY - height * 0.3, 10, height * 0.3);
            tree.fill({ color: 0x2a2a4a });

            // Canopy (triangle for pine tree style)
            tree.moveTo(x, baseY - height);
            tree.lineTo(x - 40, baseY - height * 0.3);
            tree.lineTo(x + 40, baseY - height * 0.3);
            tree.closePath();
            tree.fill({ color: 0x1f3a3a }); // Dark teal

            container.addChild(tree);
        }

        this.app.stage.addChild(container);
        this.layers.push({ container, speedMultiplier: 0.5 });
    }

    private createStageLayer(): void {
        const container = new Container();

        // Ground platform
        const ground = new Graphics();
        ground.rect(0, this.app.screen.height * 0.85, this.app.screen.width * 3, this.app.screen.height * 0.15);
        ground.fill({ color: 0x3d3d5c });
        container.addChild(ground);

        // Demo characters removed - using actual combat entities instead

        this.app.stage.addChild(container);
        this.layers.push({ container, speedMultiplier: 1.0 });
    }

    private createForegroundLayer(): void {
        const container = new Container();

        // Foreground grass/foliage silhouettes
        for (let i = 0; i < 30; i++) {
            const grass = new Graphics();
            const x = i * 100 + Math.random() * 50 - 200;
            const baseY = this.app.screen.height;

            grass.moveTo(x, baseY);
            grass.lineTo(x + 10, baseY - 40 - Math.random() * 30);
            grass.lineTo(x + 20, baseY);
            grass.closePath();
            grass.fill({ color: 0x0a0a15, alpha: 0.8 });

            container.addChild(grass);
        }

        this.app.stage.addChild(container);
        this.layers.push({ container, speedMultiplier: 1.5 });
    }

    private setupInputHandlers(): void {
        // Track mouse position for camera
        this.app.stage.eventMode = 'static';
        this.app.stage.hitArea = this.app.screen;

        this.app.stage.on('pointermove', (e) => {
            const normalizedX = (e.global.x / this.app.screen.width) - 0.5;
            this.targetCameraX = normalizedX * 400; // Max 400px offset
        });
    }

    update(_deltaTime: number): void {
        // Smooth camera follow
        this.cameraX += (this.targetCameraX - this.cameraX) * 0.05;

        // Apply parallax offset to each layer
        for (const layer of this.layers) {
            layer.container.x = -this.cameraX * layer.speedMultiplier;
        }
    }

    onResize(width: number, height: number): void {
        this.app.stage.hitArea = new Rectangle(0, 0, width, height);
    }
}
