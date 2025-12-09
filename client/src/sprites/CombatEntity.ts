/**
 * Path: client/src/sprites/CombatEntity.ts
 * Purpose: Base class for all combat participants (players, enemies, NPCs)
 * Logic:
 *   - Manages entity state (position, health, stats, status effects)
 *   - Handles damage/healing calculations
 *   - Manages sprite rendering and animations
 *   - Provides common interface for all combat entities
 */

import * as PIXI from 'pixi.js';

export interface EntityStats {
    maxHealth: number;
    attack: number;
    defense: number;
    speed: number;
}

export interface StatusEffect {
    type: 'poison' | 'stun' | 'burn' | 'buff' | 'debuff';
    duration: number;
    value: number;
}

export abstract class CombatEntity {
    // Sprite and rendering
    protected sprite: PIXI.Sprite;
    protected healthBarBg: PIXI.Graphics;
    protected healthBarFill: PIXI.Graphics;

    // Entity state
    protected currentHealth: number;
    protected stats: EntityStats;
    protected statusEffects: StatusEffect[] = [];
    protected isDead: boolean = false;

    // Movement and position
    protected velocity: PIXI.Point = new PIXI.Point(0, 0);
    protected facingRight: boolean = true;

    constructor(
        protected container: PIXI.Container,
        stats: EntityStats,
        x: number,
        y: number
    ) {
        this.stats = stats;
        this.currentHealth = stats.maxHealth;

        // Create sprite placeholder (will be overridden by subclasses)
        this.sprite = new PIXI.Sprite();
        this.sprite.anchor.set(0.5);
        this.sprite.position.set(x, y);

        // Create health bar
        this.healthBarBg = new PIXI.Graphics();
        this.healthBarFill = new PIXI.Graphics();

        this.createHealthBar();
        this.addToContainer();
    }

    /**
     * Creates visual health bar above entity
     */
    protected createHealthBar(): void {
        const barWidth = 60;
        const barHeight = 6;
        const offsetY = -40;

        // Background (red)
        this.healthBarBg.rect(-barWidth / 2, offsetY, barWidth, barHeight);
        this.healthBarBg.fill(0x8B0000);

        // Fill (green)
        this.updateHealthBar();

        this.sprite.addChild(this.healthBarBg);
        this.sprite.addChild(this.healthBarFill);
    }

    /**
     * Updates health bar fill based on current health
     */
    protected updateHealthBar(): void {
        const barWidth = 60;
        const barHeight = 6;
        const offsetY = -40;
        const healthPercent = this.currentHealth / this.stats.maxHealth;

        this.healthBarFill.clear();
        this.healthBarFill.rect(-barWidth / 2, offsetY, barWidth * healthPercent, barHeight);
        this.healthBarFill.fill(0x00FF00);
    }

    /**
     * Adds entity sprites to the container
     */
    protected addToContainer(): void {
        this.container.addChild(this.sprite);
    }

    /**
     * Apply damage to this entity
     */
    public takeDamage(amount: number): void {
        if (this.isDead) return;

        const actualDamage = Math.max(1, amount - this.stats.defense);
        this.currentHealth -= actualDamage;

        if (this.currentHealth <= 0) {
            this.currentHealth = 0;
            this.die();
        }

        this.updateHealthBar();
        this.onDamageTaken(actualDamage);
    }

    /**
     * Heal this entity
     */
    public heal(amount: number): void {
        if (this.isDead) return;

        this.currentHealth = Math.min(this.stats.maxHealth, this.currentHealth + amount);
        this.updateHealthBar();
    }

    /**
     * Handle entity death
     */
    protected die(): void {
        this.isDead = true;
        this.sprite.alpha = 0.5; // Temporary death visual
        this.onDeath();
    }

    /**
     * Move entity by velocity vector
     */
    public move(deltaTime: number): void {
        if (this.isDead) return;

        this.sprite.x += this.velocity.x * deltaTime;
        this.sprite.y += this.velocity.y * deltaTime;

        // Update facing direction
        if (this.velocity.x < 0) {
            this.facingRight = false;
            this.sprite.scale.x = -1;
        } else if (this.velocity.x > 0) {
            this.facingRight = true;
            this.sprite.scale.x = 1;
        }
    }

    /**
     * Apply status effect to entity
     */
    public addStatusEffect(effect: StatusEffect): void {
        this.statusEffects.push(effect);
    }

    /**
     * Update status effects (called each frame)
     */
    protected updateStatusEffects(deltaTime: number): void {
        this.statusEffects = this.statusEffects.filter(effect => {
            effect.duration -= deltaTime;

            if (effect.type === 'poison' && effect.duration > 0) {
                this.takeDamage(effect.value * deltaTime);
            }

            return effect.duration > 0;
        });
    }

    /**
     * Main update loop (called each frame)
     */
    public update(deltaTime: number): void {
        if (this.isDead) return;

        this.updateStatusEffects(deltaTime);
        this.move(deltaTime);
    }

    /**
     * Get entity position
     */
    public getPosition(): PIXI.Point {
        return new PIXI.Point(this.sprite.x, this.sprite.y);
    }

    /**
     * Set entity position
     */
    public setPosition(x: number, y: number): void {
        this.sprite.x = x;
        this.sprite.y = y;
    }

    /**
     * Check if entity is dead
     */
    public getIsDead(): boolean {
        return this.isDead;
    }

    /**
     * Get current health
     */
    public getHealth(): number {
        return this.currentHealth;
    }

    /**
     * Get entity stats
     */
    public getStats(): EntityStats {
        return this.stats;
    }

    /**
     * Clean up resources
     */
    public destroy(): void {
        this.sprite.destroy();
    }

    // Abstract methods to be implemented by subclasses
    protected abstract onDamageTaken(amount: number): void;
    protected abstract onDeath(): void;
}
