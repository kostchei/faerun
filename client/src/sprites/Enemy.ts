/**
 * Path: client/src/sprites/Enemy.ts
 * Purpose: AI-controlled enemy with basic combat behavior
 * Logic:
 *   - Extends CombatEntity with enemy-specific AI
 *   - Implements patrol and chase behaviors
 *   - Handles attack patterns and aggro detection
 *   - Provides loot drops on defeat
 */

import * as PIXI from 'pixi.js';
import { CombatEntity, EntityStats } from './CombatEntity';

type AIState = 'patrol' | 'chase' | 'attack' | 'idle';

export class Enemy extends CombatEntity {
    private aiState: AIState = 'patrol';
    private target: CombatEntity | null = null;
    private patrolSpeed: number = 50;
    private chaseSpeed: number = 120;
    private attackRange: number = 60;
    private detectionRange: number = 250;
    private attackCooldown: number = 0;
    private attackCooldownMax: number = 1.5;

    // Patrol behavior
    private patrolDirection: number = 1; // 1 for right, -1 for left
    private patrolDistance: number = 150;
    private patrolOrigin: number;

    constructor(container: PIXI.Container, x: number, y: number, difficulty: number = 1) {
        const stats: EntityStats = {
            maxHealth: 50 * difficulty,
            attack: 10 * difficulty,
            defense: 2 * difficulty,
            speed: 50
        };

        super(container, stats, x, y);
        this.patrolOrigin = x;
        this.createEnemySprite();
    }

    /**
     * Create enemy sprite with visual representation
     */
    private createEnemySprite(): void {
        // Create a simple graphics-based enemy sprite (placeholder)
        const graphics = new PIXI.Graphics();

        // Draw a goblin-like enemy
        // Body
        graphics.rect(-12, -8, 24, 30);
        graphics.fill(0x228B22); // Forest green

        // Head
        graphics.circle(0, -20, 10);
        graphics.fill(0x32CD32); // Lime green

        // Eyes (menacing red)
        graphics.circle(-4, -22, 2);
        graphics.fill(0xFF0000);
        graphics.circle(4, -22, 2);
        graphics.fill(0xFF0000);

        // Weapon (crude club)
        graphics.rect(-15, 0, 3, 15);
        graphics.fill(0x8B4513); // Brown
        graphics.circle(-13.5, 15, 4);
        graphics.fill(0x696969); // Dark gray

        // Add graphics directly to sprite container
        this.sprite.addChild(graphics);
    }

    /**
     * Set the target for the enemy to chase/attack
     */
    public setTarget(target: CombatEntity): void {
        this.target = target;
    }

    /**
     * Patrol behavior: move back and forth
     */
    private patrol(): void {
        // Move in current patrol direction
        this.velocity.x = this.patrolSpeed * this.patrolDirection;
        this.velocity.y = 0;

        // Check if we've reached patrol boundary
        const distanceFromOrigin = this.sprite.x - this.patrolOrigin;
        if (Math.abs(distanceFromOrigin) > this.patrolDistance) {
            this.patrolDirection *= -1; // Reverse direction
        }
    }

    /**
     * Chase behavior: move toward target
     */
    private chase(): void {
        if (!this.target) {
            this.aiState = 'patrol';
            return;
        }

        const targetPos = this.target.getPosition();
        const myPos = this.getPosition();

        const dx = targetPos.x - myPos.x;
        const dy = targetPos.y - myPos.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.attackRange) {
            // Within attack range
            this.aiState = 'attack';
            this.velocity.x = 0;
            this.velocity.y = 0;
        } else {
            // Chase target
            this.velocity.x = (dx / distance) * this.chaseSpeed;
            this.velocity.y = (dy / distance) * this.chaseSpeed;
        }
    }

    /**
     * Attack behavior: attack the target
     */
    private attackTarget(): void {
        if (!this.target || this.attackCooldown > 0) {
            return;
        }

        const targetPos = this.target.getPosition();
        const myPos = this.getPosition();
        const distance = Math.sqrt(
            (targetPos.x - myPos.x) ** 2 + (targetPos.y - myPos.y) ** 2
        );

        if (distance > this.attackRange) {
            // Target moved out of range
            this.aiState = 'chase';
            return;
        }

        // Perform attack
        this.target.takeDamage(this.stats.attack);
        this.attackCooldown = this.attackCooldownMax;

        // Visual feedback
        this.sprite.tint = 0xFF4500; // Orange flash
        setTimeout(() => {
            this.sprite.tint = 0xFFFFFF;
        }, 100);
    }

    /**
     * Check if target is in detection range
     */
    private detectTarget(): boolean {
        if (!this.target || this.target.getIsDead()) {
            return false;
        }

        const targetPos = this.target.getPosition();
        const myPos = this.getPosition();
        const distance = Math.sqrt(
            (targetPos.x - myPos.x) ** 2 + (targetPos.y - myPos.y) ** 2
        );

        return distance < this.detectionRange;
    }

    /**
     * Update AI state machine
     */
    private updateAI(): void {
        switch (this.aiState) {
            case 'patrol':
                if (this.detectTarget()) {
                    this.aiState = 'chase';
                } else {
                    this.patrol();
                }
                break;

            case 'chase':
                if (!this.detectTarget()) {
                    this.aiState = 'patrol';
                } else {
                    this.chase();
                }
                break;

            case 'attack':
                if (!this.detectTarget()) {
                    this.aiState = 'patrol';
                } else {
                    this.attackTarget();
                }
                break;

            case 'idle':
                // Do nothing
                break;
        }
    }

    /**
     * Override update to include AI logic
     */
    public override update(deltaTime: number): void {
        super.update(deltaTime);

        if (this.attackCooldown > 0) {
            this.attackCooldown -= deltaTime;
        }

        this.updateAI();
    }

    /**
     * Handle damage taken with enemy-specific effects
     */
    protected onDamageTaken(amount: number): void {
        console.log(`Enemy took ${amount} damage! Health: ${this.currentHealth}/${this.stats.maxHealth}`);

        // Become aggressive when hit
        if (this.aiState === 'patrol') {
            this.aiState = 'chase';
        }
    }

    /**
     * Handle enemy death and loot drop
     */
    protected onDeath(): void {
        console.log('Enemy defeated!');

        // Could drop loot, award XP, etc.
        // For now, just fade out and remove after delay
        setTimeout(() => {
            this.destroy();
        }, 2000);
    }

    /**
     * Get current AI state (for debugging/UI)
     */
    public getAIState(): AIState {
        return this.aiState;
    }
}
