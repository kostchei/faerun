/**
 * Path: client/src/sprites/PlayerCharacter.ts
 * Purpose: Player-controlled character with keyboard/touch input handling
 * Logic:
 *   - Extends CombatEntity with player-specific behavior
 *   - Handles keyboard input for movement and attacks
 *   - Manages player abilities and cooldowns
 *   - Provides visual feedback for player actions
 */

import * as PIXI from 'pixi.js';
import { CombatEntity, EntityStats } from './CombatEntity';

interface Ability {
    name: string;
    damage: number;
    cooldown: number;
    currentCooldown: number;
    range: number;
}

export class PlayerCharacter extends CombatEntity {
    private keys: Map<string, boolean> = new Map();
    private abilities: Ability[] = [];
    private moveSpeed: number = 200;
    private attackCooldown: number = 0;
    private attackCooldownMax: number = 0.5; // Attack every 0.5 seconds

    constructor(container: PIXI.Container, x: number, y: number) {
        const stats: EntityStats = {
            maxHealth: 100,
            attack: 15,
            defense: 5,
            speed: 200
        };

        super(container, stats, x, y);
        this.createPlayerSprite();
        this.setupInputHandlers();
        this.setupAbilities();
    }

    /**
     * Create player sprite with visual representation
     */
    private createPlayerSprite(): void {
        // Create a simple graphics-based sprite (placeholder until we have assets)
        const graphics = new PIXI.Graphics();

        // Draw a knight-like character
        // Body
        graphics.rect(-15, -10, 30, 40);
        graphics.fill(0x4169E1); // Royal blue

        // Head
        graphics.circle(0, -25, 12);
        graphics.fill(0xFFDBAC); // Skin tone

        // Helmet
        graphics.rect(-12, -35, 24, 10);
        graphics.fill(0xC0C0C0); // Silver

        // Sword (on right side)
        graphics.rect(15, -5, 3, 25);
        graphics.fill(0xFFD700); // Gold hilt
        graphics.rect(16, -15, 1, 10);
        graphics.fill(0xC0C0C0); // Silver blade

        // Add graphics directly to sprite container
        this.sprite.addChild(graphics);
    }

    /**
     * Setup keyboard input handlers
     */
    private setupInputHandlers(): void {
        window.addEventListener('keydown', (e) => {
            this.keys.set(e.key.toLowerCase(), true);

            // Handle attack on spacebar
            if (e.key === ' ') {
                e.preventDefault();
                this.attack();
            }
        });

        window.addEventListener('keyup', (e) => {
            this.keys.set(e.key.toLowerCase(), false);
        });
    }

    /**
     * Setup player abilities
     */
    private setupAbilities(): void {
        this.abilities = [
            {
                name: 'Quick Strike',
                damage: 20,
                cooldown: 1.0,
                currentCooldown: 0,
                range: 80
            },
            {
                name: 'Power Attack',
                damage: 40,
                cooldown: 3.0,
                currentCooldown: 0,
                range: 80
            }
        ];
    }

    /**
     * Handle player movement based on keyboard input
     */
    private handleMovement(): void {
        this.velocity.x = 0;
        this.velocity.y = 0;

        // Horizontal movement
        if (this.keys.get('a') || this.keys.get('arrowleft')) {
            this.velocity.x = -this.moveSpeed;
        }
        if (this.keys.get('d') || this.keys.get('arrowright')) {
            this.velocity.x = this.moveSpeed;
        }

        // Vertical movement
        if (this.keys.get('w') || this.keys.get('arrowup')) {
            this.velocity.y = -this.moveSpeed;
        }
        if (this.keys.get('s') || this.keys.get('arrowdown')) {
            this.velocity.y = this.moveSpeed;
        }

        // Normalize diagonal movement
        if (this.velocity.x !== 0 && this.velocity.y !== 0) {
            const length = Math.sqrt(this.velocity.x ** 2 + this.velocity.y ** 2);
            this.velocity.x = (this.velocity.x / length) * this.moveSpeed;
            this.velocity.y = (this.velocity.y / length) * this.moveSpeed;
        }
    }

    /**
     * Perform basic attack
     */
    private attack(): void {
        if (this.attackCooldown > 0 || this.isDead) return;

        console.log('Player attacks!');
        this.attackCooldown = this.attackCooldownMax;

        // Visual feedback: brief flash
        this.sprite.tint = 0xFFFFFF;
        setTimeout(() => {
            this.sprite.tint = 0xFFFFFF;
        }, 100);
    }

    /**
     * Use ability by index
     */
    public useAbility(index: number): boolean {
        if (index >= this.abilities.length || this.isDead) return false;

        const ability = this.abilities[index];
        if (ability.currentCooldown > 0) return false;

        console.log(`Player uses ${ability.name} for ${ability.damage} damage!`);
        ability.currentCooldown = ability.cooldown;

        // Visual feedback
        this.sprite.tint = 0xFF4500; // Orange flash
        setTimeout(() => {
            this.sprite.tint = 0xFFFFFF;
        }, 150);

        return true;
    }

    /**
     * Get ability cooldown percentage for UI
     */
    public getAbilityCooldown(index: number): number {
        if (index >= this.abilities.length) return 0;
        const ability = this.abilities[index];
        return ability.currentCooldown / ability.cooldown;
    }

    /**
     * Update cooldowns
     */
    private updateCooldowns(deltaTime: number): void {
        if (this.attackCooldown > 0) {
            this.attackCooldown -= deltaTime;
        }

        this.abilities.forEach(ability => {
            if (ability.currentCooldown > 0) {
                ability.currentCooldown -= deltaTime;
            }
        });
    }

    /**
     * Override update to include player-specific logic
     */
    public override update(deltaTime: number): void {
        super.update(deltaTime);

        this.handleMovement();
        this.updateCooldowns(deltaTime);
    }

    /**
     * Handle damage taken with player-specific effects
     */
    protected onDamageTaken(amount: number): void {
        console.log(`Player took ${amount} damage! Health: ${this.currentHealth}/${this.stats.maxHealth}`);

        // Screen shake or damage flash could go here
        this.sprite.tint = 0xFF0000; // Red flash
        setTimeout(() => {
            this.sprite.tint = 0xFFFFFF;
        }, 150);
    }

    /**
     * Handle player death
     */
    protected onDeath(): void {
        console.log('Player has died!');
        // Game over logic would go here
    }

    /**
     * Clean up event listeners
     */
    public override destroy(): void {
        // Remove event listeners
        window.removeEventListener('keydown', () => { });
        window.removeEventListener('keyup', () => { });
        super.destroy();
    }
}
