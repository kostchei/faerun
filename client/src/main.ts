/**
 * Path: client/src/main.ts
 * Purpose: Application entry point - initializes PixiJS and turn-based combat
 * Logic:
 *   - Creates PixiJS Application with WebGL renderer
 *   - Initializes ParallaxScene for background
 *   - Creates PlayerCharacter and Enemy entities
 *   - Sets up TurnManager for turn-based combat
 *   - Creates UI overlay for actions and turn state
 *   - Handles keyboard input for actions
 */

import { Application, Text, TextStyle, Graphics } from 'pixi.js';
import { ParallaxScene } from './game/ParallaxScene';
import { PlayerCharacter } from './sprites/PlayerCharacter';
import { Enemy } from './sprites/Enemy';
import { TurnManager } from './game/TurnManager';
import { AttackAction, DashAction, DodgeAction, PassAction } from './game/Action';

// Global state
let turnManager: TurnManager;
let player: PlayerCharacter;
let enemies: Enemy[] = [];

async function init() {
    const app = new Application();

    await app.init({
        width: window.innerWidth,
        height: window.innerHeight,
        backgroundColor: 0x1a1a2e,
        resolution: window.devicePixelRatio || 1,
        autoDensity: true,
    });

    document.body.appendChild(app.canvas);
    app.renderer.resize(window.innerWidth, window.innerHeight);

    const scene = new ParallaxScene(app);
    await scene.init();

    // Create player character
    player = new PlayerCharacter(
        app.stage,
        window.innerWidth * 0.3,
        window.innerHeight * 0.6
    );

    // Create enemies
    const numEnemies = 2;
    for (let i = 0; i < numEnemies; i++) {
        const enemy = new Enemy(
            app.stage,
            window.innerWidth * 0.6 + (i * 200),
            window.innerHeight * 0.6,
            1
        );
        enemy.setTarget(player);
        enemies.push(enemy);
    }

    // Create UI overlay
    createUI(app);

    // Initialize turn manager
    turnManager = new TurnManager();
    turnManager.onTurnChange((state) => {
        updateTurnUI(state);
    });

    // Start combat!
    console.log('=== COMBAT START ===');
    turnManager.rollInitiative(player, enemies);

    // Handle window resize
    window.addEventListener('resize', () => {
        app.renderer.resize(window.innerWidth, window.innerHeight);
        scene.onResize(window.innerWidth, window.innerHeight);
    });

    // Game loop - only updates visuals now
    app.ticker.add((ticker) => {
        scene.update(ticker.deltaTime);

        // Only visual updates, no movement during enemy turn
        if (turnManager.isPlayerTurn()) {
            // Could allow movement here later
        }
    });

    // Setup keyboard controls for actions
    setupKeyboardControls();
}

function createUI(app: Application): void {
    // Create semi-transparent overlay at top
    const overlay = new Graphics();
    overlay.rect(0, 0, app.screen.width, 100);
    overlay.fill({ color: 0x000000, alpha: 0.7 });
    app.stage.addChild(overlay);

    // Turn indicator
    const style = new TextStyle({
        fontFamily: 'Arial',
        fontSize: 20,
        fill: 0xffffff,
        fontWeight: 'bold'
    });

    const turnText = new Text({ text: 'Initializing...', style });
    turnText.x = 20;
    turnText.y = 20;
    (turnText as any).id = 'turnIndicator'; // Store ID for updates
    app.stage.addChild(turnText);

    // Action bar instructions
    const actionStyle = new TextStyle({
        fontFamily: 'Arial',
        fontSize: 16,
        fill: 0xcccccc
    });

    const actionText = new Text({
        text: '[1] Attack  [2] Dash  [3] Dodge  [0] Pass',
        style: actionStyle
    });
    actionText.x = 20;
    actionText.y = 55;
    app.stage.addChild(actionText);
}

function updateTurnUI(state: any): void {
    // Find and update turn indicator
    const turnIndicator = (window as any).app?.stage.children.find((c: any) => c.id === 'turnIndicator');
    if (turnIndicator) {
        if (state.phase === 'PLAYER_TURN') {
            turnIndicator.text = `Round ${state.currentRound} - YOUR TURN | Movement: ${Math.floor(state.movementRemaining)}px`;
            turnIndicator.style.fill = 0x00ff00;
        } else if (state.phase === 'ENEMY_TURNS') {
            turnIndicator.text = `Round ${state.currentRound} - ENEMY TURN`;
            turnIndicator.style.fill = 0xff0000;
        }
    }
}

function setupKeyboardControls(): void {
    const actions = {
        '1': new AttackAction(),
        '2': new DashAction(),
        '3': new DodgeAction(),
        '0': new PassAction()
    };

    window.addEventListener('keydown', (e) => {
        if (!turnManager.isPlayerTurn()) return;

        const action = actions[e.key as keyof typeof actions];
        if (!action) return;

        if (action.requiresTarget) {
            // For now, automatically target first alive enemy
            const target = enemies.find(e => !e.getIsDead());
            if (!target) {
                console.log('No valid targets!');
                return;
            }

            const result = action.execute(player, target);
            console.log(`${action.name}: ${result.message}`);

            // End player turn
            turnManager.playerAction(action.name);

            // After brief delay, process enemy turns
            setTimeout(async () => {
                await turnManager.processEnemyTurns(player, enemies);
            }, 800);
        } else {
            const result = action.execute(player);
            console.log(`${action.name}: ${result.message}`);

            turnManager.playerAction(action.name);

            setTimeout(async () => {
                await turnManager.processEnemyTurns(player, enemies);
            }, 800);
        }
    });
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
    init().catch(console.error);
});
