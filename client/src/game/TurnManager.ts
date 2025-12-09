/**
 * Path: client/src/game/TurnManager.ts
 * Purpose: Manages turn-based combat flow and initiative order
 * Logic:
 *   - Rolls initiative at combat start
 *   - Tracks current turn and round number
 *   - Auto-advances turns after player action completes
 *   - Processes all enemy turns sequentially
 *   - Returns control to player
 */

import { CombatEntity } from '../sprites/CombatEntity';

export type TurnPhase = 'PLAYER_TURN' | 'ENEMY_TURNS' | 'COMBAT_END';

export interface TurnState {
    phase: TurnPhase;
    currentRound: number;
    playerHasMoved: boolean;
    playerHasActed: boolean;
    movementRemaining: number;
}

export class TurnManager {
    private initiativeOrder: CombatEntity[] = [];
    private currentRound: number = 1;
    private turnPhase: TurnPhase = 'PLAYER_TURN';
    private playerMoveSpeed: number = 200; // pixels per turn (30 feet)

    // Turn state
    private playerHasMoved: boolean = false;
    private playerHasActed: boolean = false;
    private movementRemaining: number = 0;

    // Callbacks for UI updates
    private onTurnChangeCallback?: (state: TurnState) => void;
    private onEnemyTurnCallback?: (enemy: CombatEntity) => void;

    constructor() {
        this.resetPlayerTurn();
    }

    /**
     * Roll initiative for all entities and determine turn order
     */
    public rollInitiative(player: CombatEntity, enemies: CombatEntity[]): void {
        const entities = [player, ...enemies];

        // Simple initiative: d20 + DEX modifier (assuming DEX is stats.speed/10)
        const rolls = entities.map(entity => ({
            entity,
            roll: this.d20() + Math.floor((entity.getStats?.()?.speed || 0) / 10)
        }));

        // Sort by initiative (highest first)
        rolls.sort((a, b) => b.roll - a.roll);

        this.initiativeOrder = rolls.map(r => r.entity);

        console.log('Initiative Order:', rolls.map(r =>
            `${r.entity.constructor.name}: ${r.roll}`
        ));

        // Check if player goes first
        if (this.initiativeOrder[0] === player) {
            this.startPlayerTurn();
        } else {
            // Enemies go first
            this.turnPhase = 'ENEMY_TURNS';
            this.processEnemyTurns(player, enemies);
        }
    }

    /**
     * Start player's turn
     */
    private startPlayerTurn(): void {
        this.turnPhase = 'PLAYER_TURN';
        this.resetPlayerTurn();
        this.notifyTurnChange();

        console.log(`=== ROUND ${this.currentRound}: PLAYER TURN ===`);
    }

    /**
     * Reset player turn state
     */
    private resetPlayerTurn(): void {
        this.playerHasMoved = false;
        this.playerHasActed = false;
        this.movementRemaining = this.playerMoveSpeed;
    }

    /**
     * Player uses movement
     */
    public useMovement(distance: number): boolean {
        if (this.turnPhase !== 'PLAYER_TURN') return false;
        if (this.playerHasActed) return false; // Can't move after acting

        if (distance <= this.movementRemaining) {
            this.movementRemaining -= distance;
            this.playerHasMoved = true;
            this.notifyTurnChange();
            return true;
        }

        return false;
    }

    /**
     * Player takes an action (automatically ends turn)
     */
    public playerAction(actionName: string): void {
        if (this.turnPhase !== 'PLAYER_TURN') return;
        if (this.playerHasActed) return;

        console.log(`Player uses: ${actionName}`);
        this.playerHasActed = true;
        this.notifyTurnChange();

        // Auto-advance to enemy turns after brief delay
        setTimeout(() => {
            this.endPlayerTurn();
        }, 500);
    }

    /**
     * End player turn and start enemy turns
     */
    private endPlayerTurn(): void {
        console.log('=== PLAYER TURN END ===');
        this.turnPhase = 'ENEMY_TURNS';
        this.notifyTurnChange();
    }

    /**
     * Process all enemy turns sequentially
     */
    public async processEnemyTurns(_player: CombatEntity, enemies: CombatEntity[]): Promise<void> {
        if (this.turnPhase !== 'ENEMY_TURNS') return;

        console.log('=== ENEMY TURNS START ===');

        for (const enemy of enemies) {
            if (enemy.getIsDead()) continue;

            // Notify UI that this enemy is acting
            if (this.onEnemyTurnCallback) {
                this.onEnemyTurnCallback(enemy);
            }

            // Enemy AI will handle movement and action
            // For now, just wait a bit for animation
            await this.wait(1000);

            console.log(`${enemy.constructor.name} completed turn`);
        }

        console.log('=== ENEMY TURNS END ===');

        // Start next round with player turn
        this.currentRound++;
        this.startPlayerTurn();
    }

    /**
     * Get current turn state (for UI)
     */
    public getTurnState(): TurnState {
        return {
            phase: this.turnPhase,
            currentRound: this.currentRound,
            playerHasMoved: this.playerHasMoved,
            playerHasActed: this.playerHasActed,
            movementRemaining: this.movementRemaining
        };
    }

    /**
     * Register callback for turn changes
     */
    public onTurnChange(callback: (state: TurnState) => void): void {
        this.onTurnChangeCallback = callback;
    }

    /**
     * Register callback for enemy turns
     */
    public onEnemyTurn(callback: (enemy: CombatEntity) => void): void {
        this.onEnemyTurnCallback = callback;
    }

    /**
     * Check if it's currently player's turn
     */
    public isPlayerTurn(): boolean {
        return this.turnPhase === 'PLAYER_TURN' && !this.playerHasActed;
    }

    /**
     * Notify UI of turn state change
     */
    private notifyTurnChange(): void {
        if (this.onTurnChangeCallback) {
            this.onTurnChangeCallback(this.getTurnState());
        }
    }

    /**
     * Roll d20
     */
    private d20(): number {
        return Math.floor(Math.random() * 20) + 1;
    }

    /**
     * Wait for specified milliseconds
     */
    private wait(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
